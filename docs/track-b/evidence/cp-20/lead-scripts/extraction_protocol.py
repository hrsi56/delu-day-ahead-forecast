import hashlib, json, subprocess, sys
from pathlib import Path
from cp20.budget import atomic, CAPS
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
files = ['capstone_v21.md','docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md','docs/track-b/cp-20-direct-weather-brief.md',
         'docs/track-b/weather-content-intake-2026-09-23.md','reports/weather-admission/hashes/report_files.sha256',
         'reports/weather-admission/dossier.md','reports/weather-admission/inventory/gfs_required_runs.csv',
         'reports/weather-admission/availability/gfs_ncep_production_status.csv',
         'reports/weather-admission/scripts/requirements.freeze.txt','reports/v2-causal/input-manifest.json',
         'reports/weather-ablation/run-manifest.json']
code = ['src/cp20/budget.py','src/cp20/net.py','src/cp20/gfs.py','src/cp20/extract.py','src/cp20/plan.py','scripts/cp20_weather.py']
issued = {'capstone_v21.md':'150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167',
          'docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md':'3e0bdf6a343d5336f406f0eeb726b1b65c0f767ec8d9418a7d8118902e1ace55',
          'docs/track-b/cp-20-direct-weather-brief.md':'28a4e195fa7f66ff3270d5d54e477478e90aa42124bceb1ee529f95f5761883e'}
for k,v in issued.items(): assert sha(k)==v, k
wx = subprocess.check_output(['/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/wx-venv/bin/python','-c',
  'import importlib.metadata as m, json; print(json.dumps(sorted((d.metadata["Name"].lower(), d.version) for d in m.distributions())))'])
p = {'schema':'cp20-extraction-protocol-v1','stage':'pre-extraction freeze (before any GFS target message request)',
     'issued_identities_verified': issued, 'input_sha256': {f: sha(f) for f in files},
     'implementation_sha256': {f: sha(f) for f in code},
     'admission_bundle': 'reports/weather-admission (53 files) verified against hashes/report_files.sha256; reused as already committed on the base, not repackaged',
     'product': 'GFS 0.25 deg operational pgrb2, D-1 00 UTC runs only; fields u10/v10 (10 m), u100/v100 (100 m above ground), surface DSWRF average; leads f021..f048 every 3 h',
     'endpoints': {'aws':'https://noaa-gfs-bdp-pds.s3.amazonaws.com (idx byte ranges)','ncar':'https://tds.gdex.ucar.edu/thredds/fileServer d084001 (adaptive header jump)'},
     'endpoint_rule': 'admission-inventoried endpoint first; eight added runs AWS first; per failed (run, lead) object at most one same-product alternate-endpoint attempt (or one transient retry where no alternate exists)',
     'message_attempts': {'per_message_cap': 3, 'production_max': 2, 'reserved_for_independent_review': 1,
                          'counting': 'all five messages of a (run, lead) are charged when that lead is attempted, before any request'},
     'no_whole_file_downloads': True, 'bounded_requests': 'every request has a byte range or body bound; transfer reserved before sending',
     'validation': 'GRIB2 framing + length + 7777 + sha256; ecCodes 2.49 local decode; exact identity/units/level/step/averaging bounds/init/validity/grid/centre/process/status per message; version evidence (AWS atmos/ path, DSWRF packing precision); Contradiction stops the task with evidence',
     'retained_box': 'rows 139..172 x cols 22..62 of the 1440x721 grid: 47.00..55.25 N, 5.50..15.50 E inclusive, float64 as decoded',
     'retain_raw_runs': json.loads(Path('reports/weather-ablation/run-manifest.json').read_text())['retain_raw'],
     'representative_subset_first': json.loads(Path('reports/weather-ablation/run-manifest.json').read_text())['subset'],
     'stop_lines': {'extraction_transfer_gib': 150, 'reserve_after_extraction': 'controls, review, reconstruction'},
     'caps': CAPS, 'extraction_environment': json.loads(wx), 'conversion': 'frozen separately before any fit (section 15.2 items 2-4, section 15.3); extraction stores native decoded values only'}
atomic(Path('reports/weather-ablation/extraction-protocol.json'), p)
print('ok', len(p['input_sha256']))
