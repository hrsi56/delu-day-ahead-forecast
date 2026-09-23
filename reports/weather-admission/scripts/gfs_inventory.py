"""Inventory every required GFS 00 UTC run across NCAR d084001 and NOAA AWS.

Usage:  python gfs_inventory.py ncar|aws|idx

ncar : one THREDDS catalog per required day -> presence/size/modified time of f021..f048
aws  : S3 ListObjectsV2 per required day (2021+) -> presence/size of f021..f048 and .idx
idx  : suffix range read of every required AWS .idx -> field-level presence of the five
       target records (full idx fetched only if the suffix misses a record)
tail : last 4 bytes of every NCAR file used as the chosen endpoint (2019-2020 + 2021-02-02)
       -> exact size and GRIB end section '7777' (truncation check)
Results are cached as JSON lines in .local/weather-admission/cache/gfs_inventory/.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gfs_sample import LEADS, aws_url  # noqa: E402
from net import LOCAL, CapReached, fetch  # noqa: E402

OUT = LOCAL / "cache" / "gfs_inventory"
WINDOWS = [("2019-01-01", "2022-09-27"), ("2023-04-01", "2026-04-06")]  # union of fold run windows
PATTERNS = {
    "u10": ":UGRD:10 m above ground:",
    "v10": ":VGRD:10 m above ground:",
    "ssrd": ":DSWRF:surface:",
    "u_hub": ":UGRD:100 m above ground:",
    "v_hub": ":VGRD:100 m above ground:",
}
_lock = threading.Lock()


def required_runs() -> list[dt.date]:
    out = []
    for a, b in WINDOWS:
        d, e = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
        while d <= e:
            out.append(d)
            d += dt.timedelta(days=1)
    return out


def done_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {json.loads(l)["key"] for l in path.read_text().splitlines() if l.strip()}


def append(path: Path, rec: dict) -> None:
    with _lock, path.open("a") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


def ncar_day(run: dt.date) -> dict:
    ymd = run.strftime("%Y%m%d")
    url = f"https://tds.gdex.ucar.edu/thredds/catalog/files/g/d084001/{run.year}/{ymd}/catalog.xml"
    st, _, body = fetch(url, f"inventory GFS NCAR catalog {ymd}", max_body=3_000_000)
    rec = {"key": ymd, "status": st, "files": {}}
    if st == 200:
        t = body.decode("utf8", "replace")
        for m in re.finditer(r'<dataset name="gfs\.0p25\.(\d{10})\.f(\d{3})\.grib2".*?<dataSize units="Mbytes">([\d.]+)</dataSize>\s*<date type="modified">([^<]+)</date>', t, re.S):
            init, lead, mb, mod = m.groups()
            if init == ymd + "00" and int(lead) in LEADS:
                rec["files"][f"f{lead}"] = {"mbytes": float(mb), "modified": mod}
    return rec


def aws_day(run: dt.date) -> dict:
    ymd = run.strftime("%Y%m%d")
    sub = "atmos/" if run >= dt.date(2021, 3, 23) else ""
    rec = {"key": ymd, "files": {}, "idx": {}, "status": []}
    for pre in ("f02", "f03", "f04"):
        prefix = f"gfs.{ymd}/00/{sub}gfs.t00z.pgrb2.0p25.{pre}"
        st, _, body = fetch(f"https://noaa-gfs-bdp-pds.s3.amazonaws.com/?list-type=2&prefix={prefix}", f"inventory GFS AWS listing {ymd} {pre}", max_body=2_000_000)
        rec["status"].append(st)
        for key, size in re.findall(r"<Key>([^<]+)</Key>.*?<Size>(\d+)</Size>", body.decode("utf8", "replace"), re.S):
            m = re.search(r"\.f(\d{3})(\.idx)?$", key)
            if m and int(m.group(1)) in LEADS:
                (rec["idx"] if m.group(2) else rec["files"])[f"f{m.group(1)}"] = int(size)
    return rec


def idx_check(item: tuple[dt.date, int]) -> dict:
    run, lead = item
    url = aws_url(run, lead) + ".idx"
    key = f"{run.strftime('%Y%m%d')}_f{lead:03d}"
    st, hdr, body = fetch(url, f"inventory GFS AWS idx suffix {key}", suffix=14000)
    text = body.decode("utf8", "replace")
    full = False
    if not all(p in text for p in PATTERNS.values()) and st in (200, 206):
        st, hdr, body = fetch(url, f"inventory GFS AWS idx full {key}")
        text = body.decode("utf8", "replace")
        full = True
    found = {}
    for n, p in PATTERNS.items():
        lines = [l for l in text.splitlines() if p in l and (n != "ssrd" or "ave" in l)]
        found[n] = lines[0].split(":", 2)[2] if lines else None
    return {"key": key, "status": st, "full_fetch": full, "records": found}


def tail_check(item: tuple[dt.date, int]) -> dict:
    """NCAR integrity: exact size (Content-Range) and GRIB end section '7777' at end of file."""
    from gfs_sample import ncar_url

    run, lead = item
    key = f"{run.strftime('%Y%m%d')}_f{lead:03d}"
    # THREDDS rejects suffix ranges, so learn the exact size first, then read the last 4 bytes.
    st, hdr, _ = fetch(ncar_url(run, lead), f"inventory GFS NCAR size {key}", byte_range=(0, 0))
    size = int(hdr["Content-Range"].split("/")[1]) if st == 206 and "Content-Range" in hdr else None
    if size is None:
        return {"key": key, "status": st, "bytes": None, "ends_7777": False}
    st2, _, body = fetch(ncar_url(run, lead), f"inventory GFS NCAR tail {key}", byte_range=(size - 4, size - 1))
    return {"key": key, "status": st2, "bytes": size, "ends_7777": body == b"7777"}


def run_pool(fn, items, path: Path, workers: int) -> None:
    done = done_keys(path)
    todo = [i for i in items if (i.strftime("%Y%m%d") if isinstance(i, dt.date) else f"{i[0].strftime('%Y%m%d')}_f{i[1]:03d}") not in done]
    print(f"{path.name}: {len(done)} done, {len(todo)} to do", flush=True)

    def work(i):
        try:
            append(path, fn(i))
        except CapReached as exc:
            print("CAP", exc, flush=True)
            raise

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for n, _ in enumerate(ex.map(work, todo)):
            if n % 200 == 0:
                print(n, flush=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1]
    runs = required_runs()
    if mode == "ncar":
        run_pool(ncar_day, runs, OUT / "ncar_days.jsonl", workers=10)
    elif mode == "aws":
        run_pool(aws_day, [r for r in runs if r >= dt.date(2021, 1, 1)], OUT / "aws_days.jsonl", workers=8)
    elif mode == "tail":
        sel = [r for r in runs if r < dt.date(2021, 1, 1) or r == dt.date(2021, 2, 2)]
        run_pool(tail_check, [(r, lead) for r in sel for lead in LEADS], OUT / "ncar_tail.jsonl", workers=12)
    elif mode == "idx":
        items = [(r, lead) for r in runs if r >= dt.date(2021, 1, 1) for lead in LEADS]
        run_pool(idx_check, items, OUT / "aws_idx.jsonl", workers=12)


if __name__ == "__main__":
    main()
