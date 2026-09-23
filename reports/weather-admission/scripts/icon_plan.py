"""Plan ICON sample transfer: read zip central directory + consolidated metadata only."""
import datetime as dt, json, sys, zipfile
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from icon_sample import BASE, FIELDS, LAT_BOX, LON_BOX, STEPS, run_path  # noqa: E402
from net import summary  # noqa: E402
from rangefile import RangeFile  # noqa: E402

def plan(run):
    path, size = run_path(run)
    rf = RangeFile(BASE + path, size, f"plan ICON {run}: central directory + .zmetadata", auth_hf=True)
    zf = zipfile.ZipFile(rf)
    md = json.loads(zf.read(".zmetadata"))["metadata"]
    infos = {i.filename: i for i in zf.infolist()}
    res = {"run": str(run), "file_bytes": size, "members": len(infos)}
    tot = 0
    for v in FIELDS:
        za = md.get(f"{v}/.zarray")
        if za is None:
            res[v] = "ABSENT"; continue
        shape, ch = za["shape"], za["chunks"]
        lat0, dlat = 29.5, 0.0625
        lon0 = -23.5
        la = [int((LAT_BOX[0]-lat0)/dlat), int(np.ceil((LAT_BOX[1]-lat0)/dlat))]
        lo = [int((LON_BOX[0]-lon0)/dlat), int(np.ceil((LON_BOX[1]-lon0)/dlat))]
        cs = range(STEPS[0]//ch[0], STEPS[-1]//ch[0]+1)
        cl = range(la[0]//ch[1], la[1]//ch[1]+1)
        co = range(lo[0]//ch[2], lo[1]//ch[2]+1)
        keys = [f"{v}/{a}.{b}.{c}" for a in cs for b in cl for c in co]
        present = [k for k in keys if k in infos]
        b = sum(infos[k].compress_size for k in present)
        tot += b
        res[v] = {"shape": shape, "chunks": ch, "needed_chunks": len(keys), "present": len(present), "bytes": b}
    res["planned_bytes"] = tot
    res["u_levels"] = md.get("isobaricInhPa/.zarray", {}).get("shape")
    return res

if __name__ == "__main__":
    for r in sys.argv[1:]:
        print(json.dumps(plan(dt.date.fromisoformat(r))), flush=True)
    print(summary())
