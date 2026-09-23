"""Assemble programme 4.1 admission evidence from local caches (no network access).

Usage:  python assemble.py

Reads .local/weather-admission/{cache,logs,sources} and reports/weather-admission/decoded,
writes inventories, coverage, availability, decoded summaries, usage, verdicts and hashes
under reports/weather-admission/.  Deterministic given the same caches.
"""

from __future__ import annotations

import collections
import csv
import datetime as dt
import hashlib
import html
import json
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = HERE.parent
ROOT = REPORT.parents[1]
LOCAL = ROOT / ".local" / "weather-admission"
CACHE = LOCAL / "cache"
SOURCES = LOCAL / "sources"
LOGS = LOCAL / "logs"
MANIFEST = json.loads((REPORT / "sample-manifest.json").read_text())
LEADS = [21, 24, 27, 30, 33, 36, 39, 42, 45, 48]
LEAD_KEYS = [f"f{x:03d}" for x in LEADS]
GFS_FIELDS = ["u10", "v10", "u_hub", "v_hub", "radiation"]
FIELDS = GFS_FIELDS
FOLDS = MANIFEST["required_windows"]["folds"]
BOUNDARY_EXCLUDED_DELIVERY = "2019-01-01"


def d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def days(a: dt.date, b: dt.date):
    while a <= b:
        yield a
        a += dt.timedelta(days=1)


def fold_runs(fold: str) -> list[dt.date]:
    a, b = FOLDS[fold]["runs_00z"]
    return list(days(d(a), d(b)))


def fold_phase(fold: str, run: dt.date) -> str:
    delivery = run + dt.timedelta(days=1)
    ev = FOLDS[fold]["evaluation"]
    if d(ev[0]) <= delivery <= d(ev[1]):
        return "evaluation"
    if delivery >= d(FOLDS[fold]["first_warmup_delivery"]):
        return "warmup"
    return "history"


def gfs_version(run: dt.date) -> str:
    if run <= dt.date(2019, 6, 12):
        return "v14"
    if run <= dt.date(2021, 3, 22):
        return "v15.1"
    return "v16"


def jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    keys = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def text_of(b: bytes) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", b.decode("utf8", "replace"), flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


# ---------------------------------------------------------------- GFS inventory
def gfs_inventory() -> tuple[list[dict], dict]:
    ncar = {r["key"]: r for r in jsonl(CACHE / "gfs_inventory" / "ncar_days.jsonl")}
    aws = {r["key"]: r for r in jsonl(CACHE / "gfs_inventory" / "aws_days.jsonl")}
    idx = {r["key"]: r for r in jsonl(CACHE / "gfs_inventory" / "aws_idx.jsonl")}
    tail = {r["key"]: r for r in jsonl(CACHE / "gfs_inventory" / "ncar_tail.jsonl")}
    runs = sorted({r for f in FOLDS for r in fold_runs(f)})
    # per-version, per-lead NCAR size medians for truncation screening
    med = collections.defaultdict(list)
    for r in runs:
        rec = ncar.get(r.strftime("%Y%m%d"))
        if rec:
            for k, v in rec["files"].items():
                med[(gfs_version(r), k)].append(v["mbytes"])
    medians = {k: statistics.median(v) for k, v in med.items()}
    rows = []
    for r in runs:
        ymd = r.strftime("%Y%m%d")
        n, a = ncar.get(ymd), aws.get(ymd)
        ncar_leads = sorted(n["files"]) if n else []
        ncar_complete = n is not None and all(k in n["files"] for k in LEAD_KEYS)
        ncar_small = [k for k in ncar_leads if n["files"][k]["mbytes"] < 0.9 * medians[(gfs_version(r), k)]] if n else []
        aws_applicable = r >= dt.date(2021, 1, 1)
        aws_complete = bool(a) and all(k in a["files"] and k in a["idx"] for k in LEAD_KEYS)
        idx_fields = {f: 0 for f in GFS_FIELDS}
        idx_checked = 0
        for k in LEAD_KEYS:
            rec = idx.get(f"{ymd}_{k}")
            if rec:
                idx_checked += 1
                for f, key in (("u10", "u10"), ("v10", "v10"), ("u_hub", "u_hub"), ("v_hub", "v_hub"), ("radiation", "ssrd")):
                    if rec["records"].get(key):
                        idx_fields[f] += 1
        aws_fields_ok = aws_complete and idx_checked == 10 and all(v == 10 for v in idx_fields.values())
        size_equal = None
        if n and a and aws_complete:
            # NCAR catalog "Mbytes" are decimal MB truncated (not rounded) to 0.1 MB
            size_equal = all(k in n["files"] and -1e-6 <= a["files"][k] / 1e6 - n["files"][k]["mbytes"] < 0.1 + 1e-6 for k in LEAD_KEYS)
        tails = [tail.get(f"{ymd}_{k}") for k in LEAD_KEYS]
        ncar_intact = all(t and t["ends_7777"] for t in tails)
        if aws_fields_ok:
            endpoint, field_basis = "AWS", "idx_verified"
        elif ncar_complete and not ncar_small and ncar_intact:
            endpoint, field_basis = "NCAR", "file_intact_7777_version_layout"
        else:
            endpoint, field_basis = "NONE", "missing"
        rows.append({
            "run_00z": r.isoformat(), "delivery_day": (r + dt.timedelta(days=1)).isoformat(), "gfs_version": gfs_version(r),
            "ncar_catalog_status": n["status"] if n else "not_inventoried", "ncar_leads_present": len(ncar_leads), "ncar_complete": ncar_complete,
            "ncar_size_flags": ";".join(ncar_small),
            "ncar_files_end_7777": sum(1 for t in tails if t and t["ends_7777"]) if any(tails) else "",
            "ncar_first_modified": min((v["modified"] for v in n["files"].values()), default="") if n else "",
            "aws_applicable": aws_applicable, "aws_complete": aws_complete if aws_applicable else "",
            "aws_idx_leads_checked": idx_checked if aws_applicable else "", "aws_idx_all_fields": aws_fields_ok if aws_applicable else "",
            "ncar_aws_sizes_equal": "" if size_equal is None else size_equal,
            "chosen_endpoint": endpoint, "field_basis": field_basis,
            "folds": ";".join(f for f in FOLDS if r in set(fold_runs(f))),
        })
    stats = {"ncar_days_inventoried": len(ncar), "aws_days_inventoried": len(aws), "aws_idx_checked": len(idx), "ncar_tail_checked": len(tail),
             "ncar_tail_not_7777": sorted(k for k, t in tail.items() if not t["ends_7777"]), "ncar_size_medians_mb": {f"{k[0]}:{k[1]}": v for k, v in sorted(medians.items())}}
    return rows, stats


# ---------------------------------------------------------------- ICON inventory
def icon_inventory() -> tuple[list[dict], dict]:
    tree = json.loads((CACHE / "icon_tree" / "all_files.json").read_text())
    present = {}
    for e in tree:
        p = e["path"].split("/")
        hh = int(p[4].split(".")[0].split("_")[1])
        if hh == 0:
            present[dt.date(int(p[1]), int(p[2]), int(p[3]))] = (e["path"], e["size"])
    inv = {r["key"]: r for r in jsonl(CACHE / "icon_inventory.jsonl")}
    runs = sorted({r for f in FOLDS for r in fold_runs(f)})
    rows = []
    for r in runs:
        p = present.get(r)
        i = inv.get(r.isoformat())
        rows.append({
            "run_00z": r.isoformat(), "delivery_day": (r + dt.timedelta(days=1)).isoformat(),
            "archive_span": "inside" if dt.date(2020, 1, 1) <= r <= dt.date(2025, 8, 9) else "outside",
            "file_present": p is not None, "file_bytes": p[1] if p else "", "path": p[0] if p else "",
            "field_inventory": ("pass" if i.get("pass") else "fail") if i else ("not_inventoried" if p else ""),
            "n_step": i.get("n_step", "") if i else "", "missing_chunks": ";".join(i.get("missing_chunks", [])) if i else "",
            "inventory_error": i.get("error", "") if i else "",
            "folds": ";".join(f for f in FOLDS if r in set(fold_runs(f))),
        })
    irregular = sorted(e["path"] for e in tree if len(e["path"].split("/")[-1].split(".")[0]) != 11)
    return rows, {"tree_files": len(tree), "zero_utc_runs": len(present), "field_inventoried": len(inv), "irregular_names": irregular}


# ---------------------------------------------------------------- coverage and gaps
def coverage(gfs_rows, icon_rows):
    g = {r["run_00z"]: r for r in gfs_rows}
    ic = {r["run_00z"]: r for r in icon_rows}
    out, gaps = [], []
    for fold in FOLDS:
        runs = fold_runs(fold)
        for field in FIELDS:
            # GFS
            miss = [r for r in runs if g[r.isoformat()]["chosen_endpoint"] == "NONE"]
            ncar_basis = sum(1 for r in runs if g[r.isoformat()]["field_basis"] == "file_intact_7777_version_layout")
            out.append({"archive": "GFS", "fold": fold, "field": field, "required_runs": len(runs), "covered_runs": len(runs) - len(miss),
                        "missing_runs": len(miss), "missing_in_evaluation_or_warmup": sum(1 for r in miss if fold_phase(fold, r) != "history"),
                        "field_basis_idx_verified": len(runs) - len(miss) - ncar_basis, "field_basis_version_layout": ncar_basis,
                        "boundary_structural_missing": "delivery 2019-01-01 (pre-2019 run excluded)" if fold == "fold_1" else ""})
            for r in miss:
                gaps.append({"archive": "GFS", "fold": fold, "field": field, "run_00z": r.isoformat(), "phase": fold_phase(fold, r), "class": "ARCHIVE_ABSENCE_OR_INCOMPLETE", "detail": f"ncar_complete={g[r.isoformat()]['ncar_complete']} aws_complete={g[r.isoformat()]['aws_complete']} size_flags={g[r.isoformat()]['ncar_size_flags']}"})
            # ICON
            if field in ("u_hub", "v_hub"):
                out.append({"archive": "ICON", "fold": fold, "field": field, "required_runs": len(runs), "covered_runs": 0, "missing_runs": len(runs),
                            "missing_in_evaluation_or_warmup": sum(1 for r in runs if fold_phase(fold, r) != "history"),
                            "field_basis_idx_verified": "", "field_basis_version_layout": "", "boundary_structural_missing": "FIELD_UNSUPPORTED: archive has 10 m and isobaric winds only"})
                continue
            prefixes = {"u10": ("u_10m",), "v10": ("v_10m",), "radiation": ("aswdir_s", "aswdifd_s")}[field]

            def icon_ok(r, prefixes=prefixes):
                row = ic[r.isoformat()]
                if not row["file_present"] or row["field_inventory"] in ("", "not_inventoried"):
                    return False
                if row["field_inventory"] == "pass":
                    return True
                if row["inventory_error"]:
                    return False
                return not any(k.startswith(prefixes) for k in row["missing_chunks"].split(";") if k)

            miss_i = [r for r in runs if not icon_ok(r)]
            out.append({"archive": "ICON", "fold": fold, "field": field, "required_runs": len(runs), "covered_runs": len(runs) - len(miss_i), "missing_runs": len(miss_i),
                        "missing_in_evaluation_or_warmup": sum(1 for r in miss_i if fold_phase(fold, r) != "history"),
                        "field_basis_idx_verified": "", "field_basis_version_layout": "", "boundary_structural_missing": "delivery 2019-01-01 (pre-2019 run excluded)" if fold == "fold_1" else ""})
            for r in miss_i:
                row = ic[r.isoformat()]
                if row["archive_span"] == "outside":
                    cls = "ARCHIVE_ABSENCE (outside archive span 2020-01-01..2025-08-09)"
                elif not row["file_present"]:
                    cls = "ARCHIVE_ABSENCE (run file absent)"
                elif row["file_bytes"] and int(row["file_bytes"]) < 1_000_000:
                    cls = f"ARCHIVE_DEFECT (stub file {row['file_bytes']} bytes, not a readable zip)"
                else:
                    cls = f"FIELD_INCOMPLETE ({row['missing_chunks'] or row['inventory_error']})"
                gaps.append({"archive": "ICON", "fold": fold, "field": field, "run_00z": r.isoformat(), "phase": fold_phase(fold, r), "class": cls, "detail": ""})
    return out, gaps


# ---------------------------------------------------------------- availability sources
def availability():
    manifest = {r["name"]: r for r in jsonl(SOURCES / "manifest.jsonl")}
    gfs = []
    for name in sorted(manifest):
        if not name.startswith(("wayback_", "ncep_prdst")) or "ncep" not in name:
            continue
        t = text_of((SOURCES / name).read_bytes())
        i = t.find("00 UTC GFS")
        seg = t[i : i + 1200] if i >= 0 else ""
        m48 = re.search(r"48hr PRODUCTS (\d\d:\d\d:\d\d) (\d\d:\d\d:\d\d)", seg)
        fc = re.search(r"FORECAST (F\S+) (\d\d:\d\d:\d\d) (\d\d:\d\d:\d\d)", seg)
        cap = re.search(r"wayback_(\d{8})", name)
        gfs.append({"capture_utc_date": dt.datetime.strptime(cap.group(1), "%Y%m%d").date().isoformat() if cap else manifest[name]["retrieved_utc"][:10],
                    "source": name, "sha256": manifest[name]["sha256"], "url": manifest[name]["url"],
                    "gfs_00z_48h_products_avg_end_utc": m48.group(2) if m48 else "", "forecast_range": fc.group(1) if fc else "",
                    "forecast_avg_end_utc": fc.group(3) if fc else "", "basis": "NCEP production status, 30-day running average (page legend)"})
    icon = []
    for name in sorted(manifest):
        if "dwd_iconeu_00" not in name:
            continue
        raw = (SOURCES / name).read_text("utf8", "replace")
        var = name.split("_00_")[-1].replace(".html", "")
        steps = {}
        for fn, when in re.findall(r'href="([^"]+)">[^<]*</a>\s+(\d\d-\w{3}-\d{4} \d\d:\d\d(?::\d\d)?)', raw):
            m = re.search(r"_(\d{10})_(\d{3})_", fn)
            if m and 21 <= int(m.group(2)) <= 48:
                steps[int(m.group(2))] = (m.group(1), when)
        dirs = re.findall(r'href="([a-z_0-9.]+/)">[^<]*</a>\s+(\d\d-\w{3}-\d{4} \d\d:\d\d)', raw) if var == "root" else []
        times = sorted(dt.datetime.strptime(w, "%d-%b-%Y %H:%M:%S" if w.count(":") == 2 else "%d-%b-%Y %H:%M") for _, w in steps.values())
        cap = re.search(r"wayback_(\d{8})", name).group(1)
        icon.append({"capture_utc_date": dt.datetime.strptime(cap, "%Y%m%d").date().isoformat(), "variable_listing": var, "source": name, "sha256": manifest[name]["sha256"],
                     "run": sorted({v[0] for v in steps.values()}) and sorted({v[0] for v in steps.values()})[0] or "",
                     "steps_21_48_listed": len(steps), "first_publication": times[0].isoformat(sep=" ") if times else "", "last_publication": times[-1].isoformat(sep=" ") if times else "",
                     "root_directory_latest_mtime": max((w for _, w in dirs), default="", key=lambda w: dt.datetime.strptime(w, "%d-%b-%Y %H:%M")) if dirs else "",
                     "basis": "DWD opendata directory listing timestamps (server time; identical in CET and CEST captures)"})
    return gfs, icon, manifest


# ---------------------------------------------------------------- radiation precision checks (offline, cached raw bytes)
def gfs_ssrd_quantum(run: str, endpoint: str) -> float:
    import eccodes

    q = 0.0
    for lead in LEADS:
        p = CACHE / "gfs" / f"{run}_f{lead:03d}_ssrd_{endpoint}.grib2"
        g = eccodes.codes_new_from_message(p.read_bytes())
        q = max(q, 2.0 ** eccodes.codes_get(g, "binaryScaleFactor") / 10 ** eccodes.codes_get(g, "decimalScaleFactor"))
        eccodes.codes_release(g)
    return q


def icon_radiation_check(run: str) -> dict:
    import numpy as np
    from ocf_blosc2 import Blosc2

    codec = Blosc2(cname="zstd", clevel=9)
    j = json.loads((REPORT / "decoded" / f"icon_{run}.json").read_text())
    shape, chunks = j["fields"]["aswdir_s"]["zarray"]["shape"], j["fields"]["aswdir_s"]["zarray"]["chunks"]
    lat = 29.5 + 0.0625 * np.arange(shape[1])
    lon = -23.5 + 0.0625 * np.arange(shape[2])
    out, hourly_sum = {}, None
    for var in ("aswdir_s", "aswdifd_s"):
        full = {}
        for p in (CACHE / "icon").glob(f"{run}__{var}__*"):
            a, b, c = (int(x) for x in p.name.split("__")[-1].split("."))
            full[(a, b, c)] = np.frombuffer(codec.decode(p.read_bytes()), dtype="<f4").reshape(chunks)
        steps = sorted({k[0] for k in full}); las = sorted({k[1] for k in full}); los = sorted({k[2] for k in full})
        arr = np.concatenate([np.concatenate([np.concatenate([full[(s_, l_, o_)] for o_ in los], axis=2) for l_ in las], axis=1) for s_ in steps], axis=0).astype(np.float64)
        la = lat[las[0] * chunks[1] : las[0] * chunks[1] + arr.shape[1]]
        lo = lon[los[0] * chunks[2] : los[0] * chunks[2] + arr.shape[2]]
        box = arr[:, (la >= 47.0) & (la <= 55.25)][:, :, (lo >= 5.5) & (lo <= 15.5)]
        s0 = steps[0] * chunks[0]
        h = np.array([(k + 1) * box[k + 1 - s0] - k * box[k - s0] for k in range(22, 47)])
        out[var] = {"min": round(float(h.min()), 3), "share_below_minus5": float((h < -5).mean()), "box_mean_min": round(float(h.mean(axis=(1, 2)).min()), 4)}
        hourly_sum = h if hourly_sum is None else hourly_sum + h
    out["global_box_mean_min"] = round(float(hourly_sum.mean(axis=(1, 2)).min()), 4)
    out["pass"] = all(out[v]["box_mean_min"] >= -1 and out[v]["share_below_minus5"] <= 1e-4 for v in ("aswdir_s", "aswdifd_s"))
    return out


# ---------------------------------------------------------------- decoded evidence
def decoded_summary():
    rows = []
    for p in sorted((REPORT / "decoded").glob("*.json")):
        j = json.loads(p.read_text())
        if j.get("failure"):
            rows.append({"bundle": p.name, "status": "failure", "detail": j["failure"]})
            continue
        if p.name.startswith("gfs_"):
            leads = j["leads"]
            present = {f: sum(1 for L in leads.values() if f in L["fields"]) for f in ("u10", "v10", "ssrd", "u_hub", "v_hub")}
            units = sorted({f"{n}:{L['fields'][n]['meta']['units']}" for L in leads.values() for n in L["fields"]})
            steps = [L["fields"]["ssrd"]["meta"]["stepRange"] for L in leads.values() if "ssrd" in L["fields"]]
            valid_ok = all(
                dt.datetime.strptime(f"{F['meta']['validityDate']}{int(F['meta']['validityTime']):04d}", "%Y%m%d%H%M")
                == dt.datetime.strptime(f"{F['meta']['dataDate']}{int(F['meta']['dataTime']):04d}", "%Y%m%d%H%M") + dt.timedelta(hours=int(k[1:]))
                for k, L in leads.items() for F in L["fields"].values()
            )
            der = j["derived"]
            blocks = der.get("ssrd_3h_blocks", {})
            comp = j.get("comparisons", {}).get("ncar_vs_aws", {})
            q = gfs_ssrd_quantum(j["run_init_utc"][:10], j["endpoint"])
            bmin = min((b["min"] for b in blocks.values()), default=float("nan"))
            rows.append({
                "bundle": p.name, "status": "success", "archive": "GFS", "run": j["run_init_utc"], "endpoint": j["endpoint"], "delivery_day": j["hour_map"]["delivery_day"],
                "n_hours": j["hour_map"]["n_hours"], "hour_starts": f"{j['hour_map']['hour_start_leads'][0]}..{j['hour_map']['hour_start_leads'][-1]}",
                "leads_decoded": len(leads), "fields_all_leads": all(v == 10 for v in present.values()), "units": " ".join(units),
                "radiation_param": sorted({f"{L['fields']['ssrd']['meta']['discipline']}/{L['fields']['ssrd']['meta']['parameterCategory']}/{L['fields']['ssrd']['meta']['parameterNumber']}" for L in leads.values() if "ssrd" in L["fields"]}),
                "radiation_step_ranges": " ".join(steps), "valid_equals_init_plus_lead": valid_ok,
                "radiation_3h_blocks": len(blocks), "radiation_min_block": round(min((b["min"] for b in blocks.values()), default=float("nan")), 3),
                "radiation_max_block": round(max((b["max"] for b in blocks.values()), default=float("nan")), 1),
                "wind10_box_mean_range": f"{min(v['speed10_mean'] for v in der['wind'].values()):.2f}-{max(v['speed10_mean'] for v in der['wind'].values()):.2f}",
                "wind100_box_mean_range": f"{min(v.get('speed100_mean', 0) for v in der['wind'].values()):.2f}-{max(v.get('speed100_mean', 0) for v in der['wind'].values()):.2f}",
                "supports_within_decoded": der["all_supports_within_decoded_leads"],
                "grid": f"{leads['f024']['fields']['u10']['meta']['Ni']}x{leads['f024']['fields']['u10']['meta']['Nj']} d={leads['f024']['fields']['u10']['meta']['iDirectionIncrementInDegrees']}",
                "ncar_aws_sizes_equal": (all(c["size_equal"] for c in comp.values()) if comp else ""),
                "ncar_aws_messages_identical": (all(h["identical"] for c in comp.values() for h in c.get("message_hashes", {}).values()) if comp else ""),
                "messages_hashed": sum(len(L["fields"]) for L in leads.values()),
                "radiation_packing_quantum": q, "radiation_check": f"min 3h block {bmin:.3f} >= -3 x quantum ({-3 * q:g})",
                "radiation_pass": bmin >= -3 * q - 1e-9,
            })
        else:
            f = j["fields"]
            rad = j["derived"]["radiation"]
            rc = icon_radiation_check(j["run_init_utc"][:10])
            rows.append({
                "bundle": p.name, "status": "success", "archive": "ICON", "run": j["run_init_utc"], "endpoint": "ocf-hf@" + j["revision"][:7], "delivery_day": j["hour_map"]["delivery_day"],
                "n_hours": j["hour_map"]["n_hours"], "hour_starts": f"{j['hour_map']['hour_start_leads'][0]}..{j['hour_map']['hour_start_leads'][-1]}",
                "leads_decoded": f"steps 22-47 of {j['coords']['n_step']}", "fields_all_leads": j["coords"]["required_steps_present"] and all(x["n_nonfinite"] == 0 for x in f.values()),
                "units": " ".join(f"{k}:{v['attrs']['GRIB_units']}" for k, v in f.items()),
                "radiation_param": " ".join(f"{k}:{v['attrs']['GRIB_stepType']}" for k, v in f.items()),
                "radiation_step_ranges": "mean since start (0-h)", "valid_equals_init_plus_lead": j["coords"]["required_step_indices_contiguous"],
                "radiation_3h_blocks": "hourly", "radiation_min_block": round(min(rad["aswdir_s"]["min"], rad["aswdifd_s"]["min"]), 3),
                "radiation_max_block": round(max(rad["aswdir_s"]["max"], rad["aswdifd_s"]["max"]), 1),
                "wind10_box_mean_range": f"{j['derived']['speed10']['mean']:.2f} (mean over steps)", "wind100_box_mean_range": "UNSUPPORTED",
                "supports_within_decoded": j["derived"]["all_supports_within_decoded_steps"],
                "grid": f"{j['coords']['lon_first_last_n'][2]}x{j['coords']['lat_first_last_n'][2]} d=0.0625 lon {j['coords']['lon_first_last_n'][0]}..{j['coords']['lon_first_last_n'][1]}",
                "ncar_aws_sizes_equal": "", "ncar_aws_messages_identical": "", "messages_hashed": len(j["chunks_read"]),
                "radiation_packing_quantum": "float32 store; 16-bit-class spacing ~0.008 W m-2 in sampled chunks",
                "radiation_check": f"box-mean hourly min dir {rc['aswdir_s']['box_mean_min']} dif {rc['aswdifd_s']['box_mean_min']} global {rc['global_box_mean_min']}; point-hours < -5 W m-2: dir {rc['aswdir_s']['share_below_minus5']:.1e} dif {rc['aswdifd_s']['share_below_minus5']:.1e}",
                "radiation_pass": rc["pass"],
            })
    return rows


# ---------------------------------------------------------------- verdicts
def availability_status(gav, iav):
    """Bracketing dated producer-side evidence per archive x fold (rule frozen in sample-manifest)."""
    out = {}
    gpts = sorted((d(r["capture_utc_date"]), r["gfs_00z_48h_products_avg_end_utc"]) for r in gav if r["gfs_00z_48h_products_avg_end_utc"])
    ipts = sorted((d(r["capture_utc_date"]), (r["last_publication"] or r["root_directory_latest_mtime"])) for r in iav if (r["last_publication"] or r["root_directory_latest_mtime"]))
    for fold in FOLDS:
        a, b = (d(x) for x in FOLDS[fold]["runs_00z"])
        # GFS: 30-day running averages -> a capture up to 30 days after the start covers it
        before = [p for p in gpts if p[0] <= a + dt.timedelta(days=30)]
        after = [p for p in gpts if p[0] >= b]
        inside = [p for p in gpts if a <= p[0] <= b]
        latest = max((p[1] for p in before[-1:] + inside + after[:1]), default="")
        out[("GFS", fold)] = {
            "established": bool(before and after) and latest < "09:00:00",
            "evidence": f"before={before[-1][0] if before else None} inside={len(inside)} after={after[0][0] if after else None}; max 48h-products avg end {latest} UTC",
        }
        ib = [p for p in ipts if p[0] <= a]
        ia = [p for p in ipts if p[0] >= b]
        ii = [p for p in ipts if a <= p[0] <= b]
        span_ok = dt.date(2020, 1, 1) <= a and b <= dt.date(2025, 8, 9)
        lastpub = max((p[1][-8:] if len(p[1]) > 16 else p[1][-5:] for p in ib[-1:] + ii + ia[:1]), default="")
        out[("ICON", fold)] = {
            "established": bool(ib and ia) and span_ok,
            "evidence": f"before={ib[-1][0] if ib else None} inside={len(ii)} after={ia[0][0] if ia else None}; latest listed publication {lastpub} (server time); archive span covers window={span_ok}",
        }
    return out


def verdicts(cov, dec, avail):
    rows = []
    dec_ok = collections.defaultdict(list)
    for r in dec:
        if r.get("status") != "success":
            continue
        ok = all(r[k] in (True, "True") for k in ("fields_all_leads", "valid_equals_init_plus_lead", "supports_within_decoded", "radiation_pass"))
        run = d(r["run"][:10])
        key = gfs_version(run) if r["archive"] == "GFS" else ("early" if run < dt.date(2023, 3, 1) else "late")
        dec_ok[(r["archive"], key)].append(ok)
    for c in cov:
        arch, fold, field = c["archive"], c["fold"], c["field"]
        a, b = (d(x) for x in FOLDS[fold]["runs_00z"])
        if arch == "GFS":
            versions = sorted({gfs_version(x) for x in days(a, b)})
        else:
            versions = sorted({"early" if x < dt.date(2023, 3, 1) else "late" for x in days(max(a, dt.date(2020, 1, 1)), min(b, dt.date(2025, 8, 9)))}) if max(a, dt.date(2020, 1, 1)) <= min(b, dt.date(2025, 8, 9)) else []
        samples = all(dec_ok.get((arch, v)) and all(dec_ok[(arch, v)]) for v in versions) and bool(versions)
        reasons = []
        supported = not (arch == "ICON" and field in ("u_hub", "v_hub"))
        if not supported:
            reasons.append("FIELD_UNSUPPORTED")
        if supported and int(c["missing_runs"]) > 0:
            reasons.append(f"ARCHIVE_ABSENCE ({c['missing_runs']} of {c['required_runs']} runs; {c['missing_in_evaluation_or_warmup']} in warm-up/evaluation)")
        if supported and not samples:
            reasons.append("SAMPLES_INCOMPLETE")
        av = avail[(arch, fold)]
        if supported and not av["established"]:
            reasons.append("AVAILABILITY_UNPROVEN")
        rows.append({
            "archive": arch, "fold": fold, "field": field, "verdict": "ADMIT" if not reasons else "NOT_ADMITTED", "reasons": "; ".join(reasons),
            "access": "verified", "coverage": f"{c['covered_runs']}/{c['required_runs']}", "decoded_versions": ",".join(versions),
            "decoded_samples_pass": samples if supported else "", "availability": ("RECONSTRUCTED: " if av["established"] else "NOT ESTABLISHED: ") + av["evidence"],
        })
    return rows


# ---------------------------------------------------------------- usage
def usage():
    recs = jsonl(LOGS / "usage.jsonl")
    cat = collections.Counter()
    req = collections.Counter()
    for r in recs:
        p = r["purpose"]
        c = ("dependencies" if p.startswith("dependencies") else "sample retrieval (GFS)" if p.startswith("sample GFS") else "sample retrieval (ICON)" if p.startswith("sample ICON")
             else "inventory (GFS)" if p.startswith("inventory GFS") else "inventory (ICON)" if p.startswith(("inventory: OCF", "inventory ICON", "plan ICON"))
             else "cross-endpoint comparison" if p.startswith("compare GFS") else "sources and dated captures" if p.startswith(("source", "source-discovery"))
             else "debug/probe/discovery" if p.startswith(("debug", "probe", "discovery", "inventory-discovery", "structure")) else "access verification" if p.startswith("access") else "other")
        b = r["body_bytes"] + r["header_bytes"] + r["request_bytes"]
        cat[c] += b
        req[c] += 1
    attempts = jsonl(LOGS / "decode_attempts.jsonl")
    res = [l.split() for l in (LOGS / "resources.txt").read_text().splitlines()] if (LOGS / "resources.txt").exists() else []
    return {
        "requests": len(recs), "bytes": sum(cat.values()), "gib": round(sum(cat.values()) / 2**30, 4),
        "by_category": {k: {"requests": req[k], "mib": round(v / 2**20, 1)} for k, v in cat.most_common()},
        "errors": sum(1 for r in recs if r.get("error")), "http_status_counts": dict(collections.Counter(str(r["status"]) for r in recs)),
        "decode_attempts": {"total": len(attempts), "success": sum(1 for a in attempts if a["status"] == "success"), "failure": sum(1 for a in attempts if a["status"] != "success"),
                            "by_archive": dict(collections.Counter(f"{a['archive']}:{a['status']}" for a in attempts))},
        "resource_samples": len(res), "max_concurrent_processes": max((int(x[1]) for x in res), default=0),
        "max_summed_cpu_percent": max((float(x[2]) for x in res), default=0.0), "max_summed_rss_mib": round(max((int(x[3]) for x in res), default=0) / 1024, 1),
        "mean_summed_cpu_percent": round(statistics.mean(float(x[2]) for x in res), 1) if res else 0.0,
        "integrated_cpu_hours_sampled": round(sum(float(x[2]) / 100 * 20 for x in res) / 3600, 3),
        "max_cores_equivalent": round(max((float(x[2]) for x in res), default=0.0) / 100, 2),
        "sampled_span": [res[0][0], res[-1][0]] if res else [],
    }, attempts


def main() -> None:
    gfs_rows, gstats = gfs_inventory()
    icon_rows, istats = icon_inventory()
    cov, gaps = coverage(gfs_rows, icon_rows)
    gav, iav, srcman = availability()
    dec = decoded_summary()
    use, attempts = usage()
    avail = availability_status(gav, iav)
    ver = verdicts(cov, dec, avail)
    write_csv(REPORT / "verdicts.csv", ver)
    write_csv(REPORT / "inventory" / "gfs_required_runs.csv", gfs_rows)
    write_csv(REPORT / "inventory" / "icon_required_runs.csv", icon_rows)
    write_csv(REPORT / "inventory" / "coverage_by_archive_fold_field.csv", cov)
    write_csv(REPORT / "gaps.csv", gaps)
    write_csv(REPORT / "availability" / "gfs_ncep_production_status.csv", gav)
    write_csv(REPORT / "availability" / "icon_dwd_opendata_listings.csv", iav)
    write_csv(REPORT / "decoded" / "summary.csv", dec)
    write_csv(REPORT / "usage" / "decode_attempts.csv", [{k: a.get(k, "") for k in ("archive", "run", "endpoint", "status", "started_utc", "elapsed_s", "error", "manual_record")} for a in attempts])
    write_csv(REPORT / "sources" / "fingerprints.csv", [{k: r.get(k) for k in ("name", "url", "retrieved_utc", "status", "bytes", "sha256", "last_modified", "purpose")} for r in srcman.values()])
    (REPORT / "usage" / "transfer.json").write_text(json.dumps(use, indent=1))
    (REPORT / "inventory" / "inventory_stats.json").write_text(json.dumps({"gfs": gstats, "icon": istats}, indent=1))
    # hashes of every cached raw sample object
    lines = []
    for p in sorted((CACHE / "gfs").glob("*")) + sorted((CACHE / "icon").glob("*")):
        lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  .local/weather-admission/cache/{p.parent.name}/{p.name}")
    (REPORT / "hashes" / "raw_sample_objects.sha256").parent.mkdir(parents=True, exist_ok=True)
    (REPORT / "hashes" / "raw_sample_objects.sha256").write_text("\n".join(lines) + "\n")
    print(json.dumps({"gfs_runs": len(gfs_rows), "icon_runs": len(icon_rows), "gaps": len(gaps), "decoded": len(dec), "usage_gib": use["gib"], "attempts": use["decode_attempts"]}, indent=1))


if __name__ == "__main__":
    main()
