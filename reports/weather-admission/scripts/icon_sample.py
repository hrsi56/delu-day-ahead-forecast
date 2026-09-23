"""Decode one OCF ICON-EU 00 UTC run bundle for programme 4.1 admission evidence.

Usage:  HF_TOKEN=... python icon_sample.py RUN_DATE

The archive stores one zipped Zarr v2 store per run (Blosc2/zstd chunks).  The
zip central directory, consolidated metadata, coordinate arrays and only the
chunk objects intersecting the Germany box and steps 22-47 are read through
metered HTTP range requests at the pinned dataset revision.  Chunk bytes are
hashed before decoding.  Hub-height wind is not retrieved: the archive carries
10 m and isobaric winds only.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import time
import zipfile
from collections.abc import Mapping
from pathlib import Path

import numcodecs
import numpy as np
import zarr
from ocf_blosc2 import Blosc2

sys.path.insert(0, str(Path(__file__).parent))
from gfs_sample import berlin_hour_map, log_attempt  # noqa: E402
from net import LOCAL  # noqa: E402
from rangefile import RangeFile  # noqa: E402

numcodecs.register_codec(Blosc2)
REV = "d3dea71c0edcb04e08e396ab4bf55afd1fdcfcf5"
BASE = f"https://huggingface.co/datasets/openclimatefix/dwd-icon-eu/resolve/{REV}/"
REPORT = Path(__file__).resolve().parents[1]
DECODED = REPORT / "decoded"
CACHE = LOCAL / "cache" / "icon"
TREE = LOCAL / "cache" / "icon_tree" / "all_files.json"
STEPS = list(range(22, 48))
FIELDS = ["u_10m", "v_10m", "aswdir_s", "aswdifd_s"]
LAT_BOX = (47.0, 55.25)
LON_BOX = (5.5, 15.5)
SPOTS = {"berlin_52.5N_13.5E": (52.5, 13.5), "north_sea_coast_54.0N_8.0E": (54.0, 8.0), "munich_48.25N_11.5E": (48.25, 11.5)}


def run_path(run: dt.date) -> tuple[str, int]:
    for e in json.loads(TREE.read_text()):
        parts = e["path"].split("/")
        y, m, d = int(parts[1]), int(parts[2]), int(parts[3])
        hh = parts[4].split(".")[0].split("_")[1]
        if (y, m, d) == (run.year, run.month, run.day) and int(hh) == 0:
            return e["path"], e["size"]
    raise FileNotFoundError(f"no 00 UTC file for {run}")


class ZipStore(Mapping):
    """Read-only zarr store over a remote zip; records hashes of every member read."""

    def __init__(self, zf: zipfile.ZipFile, tag: str):
        self.zf, self.tag, self.names = zf, tag, set(zf.namelist())
        self.reads: dict[str, dict] = {}

    def __getitem__(self, key):
        if key not in self.names:
            raise KeyError(key)
        data = self.zf.read(key)
        info = self.zf.getinfo(key)
        rec = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "zip_offset": info.header_offset, "compress_type": info.compress_type}
        self.reads[key] = rec
        if "/" in key and not key.split("/")[-1].startswith("."):
            safe = key.replace("/", "__")
            (CACHE / f"{self.tag}__{safe}").write_bytes(data)
        return data

    def __contains__(self, key):
        # Mapping's default __contains__ calls __getitem__, which would download the chunk twice.
        return key in self.names

    def __iter__(self):
        return iter(self.names)

    def __len__(self):
        return len(self.names)


def main() -> None:
    run = dt.date.fromisoformat(sys.argv[1])
    t0 = time.time()
    attempt = {"archive": "ICON", "run": sys.argv[1], "endpoint": "ocf-hf", "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    CACHE.mkdir(parents=True, exist_ok=True)
    DECODED.mkdir(parents=True, exist_ok=True)
    out = {"archive": "OCF ICON-EU (Hugging Face)", "revision": REV, "run_init_utc": f"{sys.argv[1]}T00:00Z", "hour_map": berlin_hour_map(run)}
    try:
        path, size = run_path(run)
        url = BASE + path
        out["source"] = {"url": url, "path": path, "file_bytes": size}
        rf = RangeFile(url, size, f"sample ICON {run}: zip/zarr members", auth_hf=True)
        zf = zipfile.ZipFile(rf)
        store = ZipStore(zf, sys.argv[1])
        members = zf.infolist()
        out["zip"] = {"members": len(members), "variables": sorted({m.filename.split("/")[0] for m in members if "/" in m.filename})}
        g = zarr.open_consolidated(zarr.storage.KVStore(store), mode="r")
        attrs_root = dict(g.attrs)
        out["root_attrs"] = {k: attrs_root.get(k) for k in ("GRIB_centre", "GRIB_edition", "history", "institution", "Conventions")}
        step = np.asarray(g["step"][:])
        tval = np.asarray(g["time"][...])
        lat = np.asarray(g["latitude"][:])
        lon = np.asarray(g["longitude"][:])
        step_attrs = dict(g["step"].attrs)
        out["coords"] = {
            "step_units_attr": step_attrs.get("units"), "step_dtype": str(step.dtype), "n_step": int(step.size),
            "step_values_first_last": [int(step[0]), int(step[-1])], "time_raw": str(tval), "time_attrs": dict(g["time"].attrs),
            "lat_first_last_n": [float(lat[0]), float(lat[-1]), int(lat.size)], "lon_first_last_n": [float(lon[0]), float(lon[-1]), int(lon.size)],
        }
        # step values are hours per attrs; locate required steps
        step_h = step.astype(np.int64)
        if step_attrs.get("units") not in ("hours", None):
            raise RuntimeError(f"unexpected step units {step_attrs.get('units')}")
        idx = [int(np.where(step_h == s)[0][0]) if (step_h == s).any() else None for s in STEPS]
        out["coords"]["required_steps_present"] = all(i is not None for i in idx)
        out["coords"]["required_step_indices_contiguous"] = idx == list(range(idx[0], idx[0] + len(idx))) if idx[0] is not None else False
        lon_deg = np.where(lon > 180, lon - 360, lon)
        lm = np.where((lat >= LAT_BOX[0]) & (lat <= LAT_BOX[1]))[0]
        om = np.where((lon_deg >= LON_BOX[0]) & (lon_deg <= LON_BOX[1]))[0]
        s0, s1 = idx[0], idx[-1] + 1
        fields = {}
        out["fields"] = {}
        for v in FIELDS:
            arr = g[v]
            vattrs = dict(arr.attrs)
            sub = np.asarray(arr[s0:s1, lm[0] : lm[-1] + 1, om[0] : om[-1] + 1], dtype=np.float64)
            fields[v] = sub
            spots = {}
            for k, (la, lo) in SPOTS.items():
                i = int(np.argmin(np.abs(lat[lm] - la)))
                j = int(np.argmin(np.abs(lon_deg[om] - lo)))
                spots[k] = [round(float(x), 3) for x in sub[:, i, j]]
            per_step = {int(step_h[s0 + k]): {"mean": float(np.nanmean(sub[k])), "min": float(np.nanmin(sub[k])), "max": float(np.nanmax(sub[k]))} for k in range(sub.shape[0])}
            out["fields"][v] = {
                "zarray": {"shape": list(arr.shape), "chunks": list(arr.chunks), "dtype": str(arr.dtype), "compressor": arr.compressor.get_config() if arr.compressor else None, "fill_value": str(arr.fill_value)},
                "attrs": {k: vattrs.get(k) for k in ("GRIB_name", "GRIB_shortName", "GRIB_units", "units", "GRIB_stepType", "GRIB_typeOfLevel", "GRIB_dataType", "GRIB_gridType", "GRIB_iDirectionIncrementInDegrees", "GRIB_jDirectionIncrementInDegrees", "GRIB_latitudeOfFirstGridPointInDegrees", "GRIB_longitudeOfFirstGridPointInDegrees", "GRIB_Nx", "GRIB_Ny", "long_name", "standard_name")},
                "box_shape": list(sub.shape), "n_nonfinite": int((~np.isfinite(sub)).sum()), "per_step": per_step, "spots": spots,
            }
        chunk_reads = {k: r for k, r in store.reads.items() if k.split("/")[0] in FIELDS and not k.split("/")[-1].startswith(".")}
        out["chunks_read"] = chunk_reads
        out["chunk_bytes_total"] = int(sum(r["bytes"] for r in chunk_reads.values()))
        # derived checks
        der = {}
        s10 = np.hypot(fields["u_10m"], fields["v_10m"])
        der["speed10"] = {"mean": float(s10.mean()), "max": float(s10.max())}
        hours = np.array(STEPS, dtype=np.float64)[:, None, None]
        rad = {}
        for v in ("aswdir_s", "aswdifd_s"):
            a = fields[v]
            hourly = hours[1:] * a[1:] - hours[:-1] * a[:-1]  # mean over [h, h+1) for h = 22..46
            fields[v + "_hourly"] = hourly
            rad[v] = {"min": float(hourly.min()), "n_below_minus5": int((hourly < -5).sum()), "max": float(hourly.max())}
        glob = fields["aswdir_s_hourly"] + fields["aswdifd_s_hourly"]
        rad["global_hourly_box_mean_by_hour_start"] = {str(h): round(float(glob[k].mean()), 2) for k, h in enumerate(range(22, 47))}
        rad["method"] = "mean since forecast start A(h); hourly mean over [h,h+1) = (h+1)A(h+1) - hA(h); global = direct + diffuse"
        der["radiation"] = rad
        der["hour_support"] = {str(h): {"wind_endpoint": h, "radiation_endpoints": [h, h + 1]} for h in out["hour_map"]["hour_start_leads"]}
        der["all_supports_within_decoded_steps"] = all(h in STEPS and h + 1 in STEPS for h in out["hour_map"]["hour_start_leads"])
        der["hub_wind"] = "UNSUPPORTED in archive (10 m and isobaric u/v only); not retrieved"
        out["derived"] = der
        attempt.update({"status": "success", "elapsed_s": round(time.time() - t0, 1), "chunk_bytes": out["chunk_bytes_total"]})
    except Exception as exc:  # noqa: BLE001
        attempt.update({"status": "failure", "error": f"{type(exc).__name__}: {exc}", "elapsed_s": round(time.time() - t0, 1)})
        out["failure"] = attempt["error"]
    log_attempt(attempt)
    (DECODED / f"icon_{sys.argv[1]}.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=str))
    print(json.dumps(attempt))


if __name__ == "__main__":
    main()
