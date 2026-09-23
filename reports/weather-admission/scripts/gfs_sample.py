"""Decode one GFS 0.25 deg 00 UTC run bundle for programme 4.1 admission evidence.

Usage:  python gfs_sample.py RUN_DATE [--endpoint aws|ncar] [--compare-ncar]

For AWS runs the .idx inventory gives exact byte ranges.  NCAR d084001 has no
.idx files, so target messages are located by a bounded jump: fetch a 1.3 MB
window near the expected byte fraction, resynchronise on a GRIB2 section-0
header, then hop forward header by header (320-byte reads) until the target
messages are identified from their section-4 product definitions.  Every target
message is fetched whole, checked for the terminal '7777', hashed and decoded
locally with ecCodes.  Nothing is decoded by the server.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import struct
import sys
import time
from pathlib import Path

import eccodes
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from net import LOCAL, fetch  # noqa: E402

REPORT = Path(__file__).resolve().parents[1]
DECODED = REPORT / "decoded"
CACHE = LOCAL / "cache" / "gfs"
ATTEMPTS = LOCAL / "logs" / "decode_attempts.jsonl"
LEADS = [21, 24, 27, 30, 33, 36, 39, 42, 45, 48]
TARGETS = [
    ("u10", (0, 2, 2, 103, 10.0)),
    ("v10", (0, 2, 3, 103, 10.0)),
    ("ssrd", (0, 4, 7, 1, None)),
    ("u_hub", (0, 2, 2, 103, 100.0)),
    ("v_hub", (0, 2, 3, 103, 100.0)),
]
GROUPS = [("u10", "v10"), ("ssrd",), ("u_hub", "v_hub")]
LAT_BOX = (47.0, 55.25)
LON_BOX = (5.5, 15.5)
SPOTS = {"berlin_52.5N_13.5E": (52.5, 13.5), "north_sea_coast_54.0N_8.0E": (54.0, 8.0), "munich_48.25N_11.5E": (48.25, 11.5)}


def aws_url(run: dt.date, lead: int) -> str:
    ymd = run.strftime("%Y%m%d")
    sub = "atmos/" if run >= dt.date(2021, 3, 23) else ""
    return f"https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{ymd}/00/{sub}gfs.t00z.pgrb2.0p25.f{lead:03d}"


def ncar_url(run: dt.date, lead: int) -> str:
    ymd = run.strftime("%Y%m%d")
    return f"https://tds.gdex.ucar.edu/thredds/fileServer/files/g/d084001/{run.year}/{ymd}/gfs.0p25.{ymd}00.f{lead:03d}.grib2"


def parse_header(buf: bytes) -> dict | None:
    """Parse GRIB2 sections 0,1,(2),3,4 from the start of a message."""
    if len(buf) < 16 or buf[:4] != b"GRIB" or buf[7] != 2:
        return None
    disc = buf[6]
    total = struct.unpack(">Q", buf[8:16])[0]
    p = 16
    info = {"discipline": disc, "length": total}
    while p + 5 <= len(buf):
        slen = struct.unpack(">I", buf[p : p + 4])[0]
        snum = buf[p + 4]
        if snum == 1:
            info["ref"] = "%04d-%02d-%02dT%02d" % (struct.unpack(">H", buf[p + 12 : p + 14])[0], buf[p + 14], buf[p + 15], buf[p + 16])
        elif snum == 4:
            if p + 34 > len(buf):
                return info
            info["template"] = struct.unpack(">H", buf[p + 7 : p + 9])[0]
            info["cat"], info["num"] = buf[p + 9], buf[p + 10]
            info["ftime"] = struct.unpack(">I", buf[p + 18 : p + 22])[0]
            info["surf"] = buf[p + 22]
            scale = struct.unpack(">b", buf[p + 23 : p + 24])[0]
            val = struct.unpack(">I", buf[p + 24 : p + 28])[0]
            info["level"] = val / (10**scale) if info["surf"] == 103 else None
            return info
        elif snum not in (2, 3):
            return info
        if slen < 5:
            return None
        p += slen
    return info


def ident(info: dict) -> str | None:
    """Map section-0/4 identity to a target.  DSWRF was NCEP-local 0/4/192 in every sampled run
    (v14, v15.1 and v16); WMO 0/4/7 is accepted defensively but was never observed."""
    d, c, n, sf, lv = (info.get(k) for k in ("discipline", "cat", "num", "surf", "level"))
    if (d, c, sf) == (0, 2, 103) and n in (2, 3) and lv in (10.0, 100.0):
        return ("u" if n == 2 else "v") + ("10" if lv == 10.0 else "_hub")
    if (d, c, sf) == (0, 4, 1) and n in (7, 192) and info.get("template") == 8:
        return "ssrd"
    return None


def locate_aws(run: dt.date, lead: int) -> tuple[dict, str, str]:
    url = aws_url(run, lead)
    status, _, body = fetch(url + ".idx", f"sample GFS {run} f{lead:03d}: AWS idx")
    if status != 200:
        raise RuntimeError(f"idx missing {status}")
    lines = body.decode().splitlines()
    starts = [int(l.split(":")[1]) for l in lines]
    want = {
        "u10": ":UGRD:10 m above ground:",
        "v10": ":VGRD:10 m above ground:",
        "ssrd": ":DSWRF:surface:",
        "u_hub": ":UGRD:100 m above ground:",
        "v_hub": ":VGRD:100 m above ground:",
    }
    found = {}
    for i, line in enumerate(lines):
        for name, pat in want.items():
            if pat in line and name not in found:
                if name == "ssrd" and "ave" not in line:
                    continue
                end = starts[i + 1] - 1 if i + 1 < len(starts) else None
                found[name] = {"offset": starts[i], "end": end, "idx_line": line}
    return found, url, hashlib.sha256(body).hexdigest()


# Byte fractions of the first message of each group, measured per model version:
# v14 on 2019-01-01 f021 (UGRD 10 m 145.5 MB, DSWRF 166.6 MB, UGRD 100 m ~185.2 MB of 215.8 MB),
# v15.1 on 2019-06-13 f021 (246.8 / 273.5 / 303.8 MB of 345.7 MB), v16 from the AWS idx of
# 2022-08-25 f024.  The run's own version is tried first; the others are fallbacks.
FRACS_BY_VERSION = {
    "v14": {"u10": 0.674, "ssrd": 0.772, "u_hub": 0.858},
    "v15": {"u10": 0.714, "ssrd": 0.791, "u_hub": 0.879},
    "v16": {"u10": 0.785, "ssrd": 0.862, "u_hub": 0.927},
}


def gfs_version(run: dt.date) -> str:
    if run <= dt.date(2019, 6, 12):
        return "v14"
    if run <= dt.date(2021, 3, 22):
        return "v15"
    return "v16"


def locate_ncar(run: dt.date, lead: int) -> tuple[dict, str, int, list]:
    url = ncar_url(run, lead)
    status, headers, head = fetch(url, f"sample GFS {run} f{lead:03d}: NCAR size/first header", byte_range=(0, 319))
    if status != 206:
        raise RuntimeError(f"ncar file status {status}")
    size = int(headers["Content-Range"].split("/")[1])
    trace = []
    found = {}
    for group in GROUPS:
        order = [gfs_version(run)] + [v for v in FRACS_BY_VERSION if v != gfs_version(run)]
        for attempt, frac in enumerate(FRACS_BY_VERSION[v][group[0]] for v in order):
            est = max(0, int(frac * size) - 4_000_000)
            st, _, win = fetch(url, f"sample GFS {run} f{lead:03d}: NCAR resync window", byte_range=(est, min(size - 1, est + 1_300_000)))
            off = None
            i = 0
            while True:
                j = win.find(b"GRIB", i)
                if j < 0:
                    break
                info = parse_header(win[j : j + 320])
                if info and info.get("length", 0) < 6_000_000 and "ref" in info and "cat" in info:
                    off = est + j
                    break
                i = j + 4
            hops = 0
            while off is not None and off < size and hops < 30 and not all(g in found for g in group):
                st, _, hb = fetch(url, f"sample GFS {run} f{lead:03d}: NCAR header hop", byte_range=(off, min(size - 1, off + 319)))
                info = parse_header(hb)
                if not info:
                    raise RuntimeError(f"broken GRIB chain at {off}")
                name = ident(info)
                if name in group and name not in found:
                    found[name] = {"offset": off, "end": off + info["length"] - 1, "header": info}
                off += info["length"]
                hops += 1
            trace.append({"group": list(group), "attempt": attempt, "frac": frac, "window_start": est, "hops": hops, "found": [g for g in group if g in found]})
            if all(g in found for g in group):
                break
    return found, url, size, trace


def decode_message(msg: bytes) -> tuple[dict, np.ndarray, np.ndarray, np.ndarray]:
    gid = eccodes.codes_new_from_message(msg)
    try:
        keys = [
            "shortName", "name", "units", "typeOfLevel", "level", "stepType", "stepRange", "startStep", "endStep",
            "stepUnits", "dataDate", "dataTime", "validityDate", "validityTime", "gridType", "Ni", "Nj",
            "latitudeOfFirstGridPointInDegrees", "longitudeOfFirstGridPointInDegrees",
            "latitudeOfLastGridPointInDegrees", "longitudeOfLastGridPointInDegrees",
            "iDirectionIncrementInDegrees", "jDirectionIncrementInDegrees", "jScansPositively",
            "discipline", "parameterCategory", "parameterNumber", "productDefinitionTemplateNumber",
            "packingType", "bitsPerValue", "numberOfMissing", "centre", "generatingProcessIdentifier",
            "typeOfGeneratingProcess", "significanceOfReferenceTime", "productionStatusOfProcessedData",
        ]
        meta = {}
        for k in keys:
            try:
                meta[k] = eccodes.codes_get(gid, k)
            except eccodes.KeyValueNotFoundError:
                meta[k] = None
        if meta["productDefinitionTemplateNumber"] == 8:
            for k in ["typeOfStatisticalProcessing", "lengthOfTimeRange", "indicatorOfUnitForTimeRange"]:
                meta[k] = eccodes.codes_get(gid, k)
        vals = eccodes.codes_get_values(gid)
        ni, nj = meta["Ni"], meta["Nj"]
        grid = vals.reshape(nj, ni)
        la0, dla = meta["latitudeOfFirstGridPointInDegrees"], meta["jDirectionIncrementInDegrees"]
        lo0, dlo = meta["longitudeOfFirstGridPointInDegrees"], meta["iDirectionIncrementInDegrees"]
        lats = la0 + (dla if meta["jScansPositively"] else -dla) * np.arange(nj)
        lons = lo0 + dlo * np.arange(ni)
    finally:
        eccodes.codes_release(gid)
    return meta, grid, lats, lons


def box_stats(grid, lats, lons) -> tuple[dict, np.ndarray]:
    lm = (lats >= LAT_BOX[0]) & (lats <= LAT_BOX[1])
    om = (lons >= LON_BOX[0]) & (lons <= LON_BOX[1])
    sub = grid[np.ix_(lm, om)]
    spots = {}
    for k, (la, lo) in SPOTS.items():
        spots[k] = float(grid[int(np.argmin(np.abs(lats - la))), int(np.argmin(np.abs(lons - lo)))])
    return {
        "n": int(sub.size), "n_nonfinite": int((~np.isfinite(sub)).sum()), "mean": float(np.nanmean(sub)),
        "min": float(np.nanmin(sub)), "max": float(np.nanmax(sub)), "spots": spots,
        "box_rows": int(lm.sum()), "box_cols": int(om.sum()),
    }, sub


def berlin_hour_map(run: dt.date) -> dict:
    """Hour starts of delivery day D = run + 1 (Europe/Berlin) as leads from run 00 UTC."""
    from zoneinfo import ZoneInfo

    tz = ZoneInfo("Europe/Berlin")
    d = run + dt.timedelta(days=1)
    start = dt.datetime(d.year, d.month, d.day, tzinfo=tz)
    end = dt.datetime((d + dt.timedelta(days=1)).year, (d + dt.timedelta(days=1)).month, (d + dt.timedelta(days=1)).day, tzinfo=tz)
    init = dt.datetime(run.year, run.month, run.day, tzinfo=dt.timezone.utc)
    hours = []
    t = start.astimezone(dt.timezone.utc)
    while t < end.astimezone(dt.timezone.utc):
        hours.append(int((t - init).total_seconds() // 3600))
        t += dt.timedelta(hours=1)
    return {"delivery_day": d.isoformat(), "n_hours": len(hours), "hour_start_leads": hours}


def log_attempt(rec: dict) -> None:
    ATTEMPTS.parent.mkdir(parents=True, exist_ok=True)
    with ATTEMPTS.open("a") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--endpoint", choices=["aws", "ncar"], default="aws")
    ap.add_argument("--compare-ncar", action="store_true")
    args = ap.parse_args()
    run = dt.date.fromisoformat(args.run)
    t0 = time.time()
    attempt = {"archive": "GFS", "run": args.run, "endpoint": args.endpoint, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    CACHE.mkdir(parents=True, exist_ok=True)
    DECODED.mkdir(parents=True, exist_ok=True)
    out = {"archive": "GFS 0.25 deg pgrb2", "run_init_utc": f"{args.run}T00:00Z", "endpoint": args.endpoint, "hour_map": berlin_hour_map(run), "leads": {}, "comparisons": {}}
    try:
        fields_box = {}
        for lead in LEADS:
            if args.endpoint == "aws":
                found, url, idx_hash = locate_aws(run, lead)
                src = {"url": url, "idx_sha256": idx_hash}
            else:
                found, url, size, trace = locate_ncar(run, lead)
                src = {"url": url, "file_bytes": size, "locate_trace": trace}
            lead_rec = {"source": src, "fields": {}}
            # fetch contiguous groups in one request
            names = [n for n, _ in TARGETS if n in found]
            missing = [n for n, _ in TARGETS if n not in found]
            spans = []
            for n in sorted(names, key=lambda n: found[n]["offset"]):
                o, e = found[n]["offset"], found[n]["end"]
                if spans and spans[-1][1] + 1 == o:
                    spans[-1][1] = e
                    spans[-1][2].append(n)
                else:
                    spans.append([o, e, [n]])
            for o, e, group in spans:
                st, _, blob = fetch(url, f"sample GFS {run} f{lead:03d}: target messages {'+'.join(group)}", byte_range=(o, e))
                if st not in (200, 206) or len(blob) != e - o + 1:
                    raise RuntimeError(f"range fetch failed {st} {len(blob)}")
                p = 0
                for n in group:
                    ln = found[n]["end"] - found[n]["offset"] + 1
                    msg = blob[p : p + ln]
                    p += ln
                    if msg[-4:] != b"7777":
                        raise RuntimeError(f"{n} message not terminated")
                    h = hashlib.sha256(msg).hexdigest()
                    (CACHE / f"{args.run}_f{lead:03d}_{n}_{args.endpoint}.grib2").write_bytes(msg)
                    meta, grid, lats, lons = decode_message(msg)
                    stats, sub = box_stats(grid, lats, lons)
                    fields_box[(lead, n)] = sub
                    lead_rec["fields"][n] = {
                        "byte_range": [found[n]["offset"], found[n]["end"]], "sha256": h, "bytes": ln,
                        "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "idx_line": found[n].get("idx_line"), "meta": meta, "box": stats,
                    }
            lead_rec["missing_fields"] = missing
            out["leads"][f"f{lead:03d}"] = lead_rec
            print(args.run, f"f{lead:03d}", "ok", names, "missing", missing, flush=True)
        # derived checks
        der = {"wind": {}, "ssrd_3h_blocks": {}}
        for lead in LEADS:
            if (lead, "u10") in fields_box and (lead, "v10") in fields_box:
                s10 = np.hypot(fields_box[(lead, "u10")], fields_box[(lead, "v10")])
                rec = {"speed10_mean": float(s10.mean()), "speed10_max": float(s10.max())}
                if (lead, "u_hub") in fields_box:
                    s100 = np.hypot(fields_box[(lead, "u_hub")], fields_box[(lead, "v_hub")])
                    rec.update({"speed100_mean": float(s100.mean()), "speed100_max": float(s100.max()), "share_points_100_ge_10": float((s100 >= s10).mean())})
                der["wind"][f"f{lead:03d}"] = rec
        for lead in LEADS:
            key = f"f{lead:03d}"
            f = out["leads"][key]["fields"].get("ssrd")
            if not f:
                continue
            a0, a1 = f["meta"]["startStep"], f["meta"]["endStep"]
            if a1 - a0 == 3:
                block = fields_box[(lead, "ssrd")]
                how = f"direct {a0}-{a1} h average"
            elif a1 - a0 == 6 and (lead - 3, "ssrd") in fields_box:
                prev = out["leads"][f"f{lead - 3:03d}"]["fields"]["ssrd"]["meta"]
                if (prev["startStep"], prev["endStep"]) != (a0, a1 - 3):
                    raise RuntimeError("unexpected averaging chain")
                block = 2.0 * fields_box[(lead, "ssrd")] - fields_box[(lead - 3, "ssrd")]
                how = f"2*A({a0}-{a1}) - A({a0}-{a1 - 3})"
            else:
                continue
            der["ssrd_3h_blocks"][f"{lead - 3}-{lead}"] = {"method": how, "mean": float(block.mean()), "min": float(block.min()), "max": float(block.max()), "n_below_minus1": int((block < -1).sum())}
        hm = out["hour_map"]["hour_start_leads"]
        der["hour_support"] = {
            str(h): {"wind_endpoints": [3 * (h // 3), 3 * (h // 3) + 3] if h % 3 else [h], "ssrd_block": f"{3 * (h // 3)}-{3 * (h // 3) + 3}"}
            for h in hm
        }
        der["all_supports_within_decoded_leads"] = all(
            all(e in LEADS for e in v["wind_endpoints"]) and int(v["ssrd_block"].split("-")[1]) in LEADS for v in der["hour_support"].values()
        )
        out["derived"] = der
        if args.compare_ncar and args.endpoint == "aws":
            comp = {}
            for lead in LEADS:
                aws_bytes = None
                st, hdr, _ = fetch(aws_url(run, lead), f"compare GFS {run} f{lead:03d}: AWS size", byte_range=(0, 0))
                aws_size = int(hdr["Content-Range"].split("/")[1]) if st == 206 else None
                st2, hdr2, _ = fetch(ncar_url(run, lead), f"compare GFS {run} f{lead:03d}: NCAR size", byte_range=(0, 0))
                ncar_size = int(hdr2["Content-Range"].split("/")[1]) if st2 == 206 else None
                rec = {"aws_bytes": aws_size, "ncar_bytes": ncar_size, "size_equal": aws_size == ncar_size and aws_size is not None}
                if lead in (24, 48) and rec["size_equal"]:
                    hashes = {}
                    for n, f in out["leads"][f"f{lead:03d}"]["fields"].items():
                        o, e = f["byte_range"]
                        st3, _, nb = fetch(ncar_url(run, lead), f"compare GFS {run} f{lead:03d}: NCAR bytes {n}", byte_range=(o, e))
                        hashes[n] = {"aws_sha256": f["sha256"], "ncar_sha256": hashlib.sha256(nb).hexdigest()}
                        hashes[n]["identical"] = hashes[n]["aws_sha256"] == hashes[n]["ncar_sha256"]
                    rec["message_hashes"] = hashes
                comp[f"f{lead:03d}"] = rec
            out["comparisons"]["ncar_vs_aws"] = comp
        attempt.update({"status": "success", "elapsed_s": round(time.time() - t0, 1)})
    except Exception as exc:  # noqa: BLE001 - recorded as failed attempt
        attempt.update({"status": "failure", "error": f"{type(exc).__name__}: {exc}", "elapsed_s": round(time.time() - t0, 1)})
        out["failure"] = attempt["error"]
    log_attempt(attempt)
    (DECODED / f"gfs_{args.run}.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=str))
    print(json.dumps(attempt))


if __name__ == "__main__":
    main()
