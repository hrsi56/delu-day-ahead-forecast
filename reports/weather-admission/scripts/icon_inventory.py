"""Field-level inventory of every OCF ICON-EU 00 UTC run inside the fold windows.

Usage:  HF_TOKEN=... python icon_inventory.py

For each existing run file (from the pinned-revision tree listing) the zip central
directory and the ``u_10m/.zarray`` and ``aswdir_s/.zarray`` members are read.  A run
passes when u_10m, v_10m, aswdir_s and aswdifd_s each hold every chunk object that
intersects the Germany box for steps 22-47 and the step dimension reaches index 47
with the hourly layout.  One authenticated 1-byte request resolves the signed CDN URL;
the remaining range reads use that URL without the token.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from icon_sample import BASE, FIELDS, LAT_BOX, LON_BOX, STEPS, TREE  # noqa: E402
from net import LOCAL, fetch  # noqa: E402
from rangefile import RangeFile  # noqa: E402

OUT = LOCAL / "cache" / "icon_inventory.jsonl"
WINDOWS = [("2020-01-01", "2022-09-27"), ("2023-04-01", "2025-08-09")]
_lock = threading.Lock()


def runs_in_windows() -> list[tuple[str, str, int]]:
    out = []
    for e in json.loads(TREE.read_text()):
        parts = e["path"].split("/")
        y, m, d = int(parts[1]), int(parts[2]), int(parts[3])
        hh = int(parts[4].split(".")[0].split("_")[1])
        day = dt.date(y, m, d)
        if hh == 0 and any(dt.date.fromisoformat(a) <= day <= dt.date.fromisoformat(b) for a, b in WINDOWS):
            out.append((day.isoformat(), e["path"], e["size"]))
    return sorted(out)


def needed_keys(v: str, chunks: list[int]) -> list[str]:
    lat0, lon0, d = 29.5, -23.5, 0.0625
    la = (int((LAT_BOX[0] - lat0) / d), int(-(-(LAT_BOX[1] - lat0) // d)))
    lo = (int((LON_BOX[0] - lon0) / d), int(-(-(LON_BOX[1] - lon0) // d)))
    cs = range(STEPS[0] // chunks[0], STEPS[-1] // chunks[0] + 1)
    cl = range(la[0] // chunks[1], la[1] // chunks[1] + 1)
    co = range(lo[0] // chunks[2], lo[1] // chunks[2] + 1)
    return [f"{v}/{a}.{b}.{c}" for a in cs for b in cl for c in co]


def check(item: tuple[str, str, int]) -> dict:
    day, path, size = item
    rec = {"key": day, "path": path, "file_bytes": size}
    st, hdr, _ = fetch(BASE + path, f"inventory ICON {day}: resolve", auth_hf=True, byte_range=(0, 0))
    rec["resolve_status"] = st
    if st not in (200, 206):
        rec["error"] = f"resolve {st}"
        return rec
    rf = RangeFile(hdr["X-Final-Url"], size, f"inventory ICON {day}: central directory/.zarray", block=4096)
    zf = zipfile.ZipFile(rf)
    names = {i.filename: i.compress_size for i in zf.infolist()}
    rec["members"] = len(names)
    def meta(v: str):
        """Zarr v2 (.zarray) or v3 (zarr.json; one run, 2025-03-07, uses v3) -> (shape, chunks, key format)."""
        if f"{v}/.zarray" in names:
            m = json.loads(zf.read(f"{v}/.zarray"))
            return m["shape"], m["chunks"], "v2"
        if f"{v}/zarr.json" in names:
            m = json.loads(zf.read(f"{v}/zarr.json"))
            return m["shape"], m["chunk_grid"]["configuration"]["chunk_shape"], "v3"
        return None

    metas = {v: meta(v) for v in ("u_10m", "aswdir_s")}
    rec["zarr_format"] = sorted({m[2] for m in metas.values() if m})
    rec["variables_present"] = {v: f"{v}/.zarray" in names or f"{v}/zarr.json" in names for v in FIELDS}
    za, zr = metas["u_10m"], metas["aswdir_s"]
    rec["u10_shape_chunks"] = [za[0], za[1]] if za else None
    rec["aswdir_shape_chunks"] = [zr[0], zr[1]] if zr else None
    missing = []
    for v in FIELDS:
        m = za if v in ("u_10m", "v_10m") else zr
        if m is None or not rec["variables_present"][v]:
            missing.append(f"{v}/metadata")
            continue
        for k in needed_keys(v, m[1]):
            key = k if m[2] == "v2" else f"{v}/c/" + k.split("/", 1)[1].replace(".", "/")
            if key not in names:
                missing.append(key)
    rec["missing_chunks"] = missing
    # Hourly layout: 0-78 h hourly (79 steps) then 3-hourly; index 47 is 47 h whenever n_step >= 48.
    n_step = min(x[0][0] for x in (rec["u10_shape_chunks"], rec["aswdir_shape_chunks"]) if x) if (za or zr) else 0
    if size < 1_000_000:
        rec["defect"] = f"stub file of {size} bytes"
    rec["n_step"] = n_step
    rec["steps_22_47_indexable"] = n_step >= 48
    rec["pass"] = not missing and rec["steps_22_47_indexable"]
    return rec


def main() -> None:
    done = set()
    if OUT.exists():
        done = {json.loads(l)["key"] for l in OUT.read_text().splitlines() if l.strip()}
    todo = [r for r in runs_in_windows() if r[0] not in done]
    print(f"{len(done)} done, {len(todo)} to do", flush=True)

    def work(item):
        try:
            rec = check(item)
        except Exception as exc:  # noqa: BLE001 - recorded per run
            rec = {"key": item[0], "path": item[1], "error": f"{type(exc).__name__}: {exc}"[:300], "pass": False}
        with _lock, OUT.open("a") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")

    with ThreadPoolExecutor(max_workers=8) as ex:
        for n, _ in enumerate(ex.map(work, todo)):
            if n % 100 == 0:
                print(n, flush=True)


if __name__ == "__main__":
    main()
