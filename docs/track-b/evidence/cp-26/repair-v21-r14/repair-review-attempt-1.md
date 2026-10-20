# ביקורת מוכנות לתיקון CP-26 — v21-r14

**פסק דין: REPAIR_INCOMPLETE.** מרבית חוזי התיקון אומתו, אך ההגנה מפני שימוש חוזר ב־PID אינה מתקיימת במסלול גילוי וסיום קבוצת התהליכים. 81 הבדיקות הקיימות עברו; בדיקת קבלה נוספת, ללא אות אמיתי לתהליך, שחזרה אימוץ של תהליך זר ושליחת אות מדומה לקבוצתו. זו ביקורת תיקון בלבד, ולא ביקורת Integration של CP-26. CP-26 נשאר INCOMPLETE.

## זהות, סמכות וגבולות

- מועמד שנבדק: `c1e46c41bd83e7e91082fd4f9c626aed1de72a03`.
- checkout מנותק ונקי: `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/repair-review-c1e46`.
- עוגן: `capstone_v21.md`, **v21-r14 candidate**, §§24.7–24.9.
- SHA-256 של העוגן: `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`.
- commit העוגן: `332baeb861cec5a58516c58a29a1a3afe1eec909`.
- בסיס הקוד הנחת: `647d6eb81b2cf6e0cfaf4152f659d689ff973578`.
- brief מחייב: `docs/track-b/evidence/cp-26/issued-repair-brief-v21-r14.md`, SHA-256 `5b6a0cdfad870da6b59a03ff29576ff6ec98891e941d56986516e6f3f743ff84`.
- r14 ממתין לסקירה ולאשרור של הבעלים. הרשאה ליצור את הבתים אינה אשרור שלהם.
- נקראו AGENTS.md, engineering-role.md, העוגן/brief הנקובים, קוד/בדיקות CP-26 והראיות הנדרשות. לא נקראו progress.md, orchestrator-role.md, syllabus או חומרי Track A/C; לא נעשה שימוש ברשת, credentials, חיפוש אמיתי, pilot, replay ניסויי, ציוני CP-26 או זרועות CP-28.
- גילוי נאות פרוצדורלי: קריאת `collaboration.list_agents` לבדיקת מקום להאצלת ביקורת לקריאה בלבד הציגה אגב כך סיכומי סיום של סוכנים קודמים. לא נפתחו checkout או היסטוריית Builder, והסיכומים לא שימשו ראיה או בסיס לממצא. הביקורת התומכת לחשבונאות הופעלה בהקשר חדש, על קובצי המועמד בלבד.
- הבידוד פרוצדורלי ושיתופי, לא mount אכוף לקריאה בלבד. לא שונתה שורת קוד/מסמך במועמד ולא בוצעה פעולת Git משנה. ההורה בלבד מייבא את הביקורת ומנהל את ה־checkout.
- בתחילת הסקירה ולפני כתיבת מסמך זה: `git status --porcelain=v1` יצא 0 ללא פלט; `git rev-parse HEAD` יצא 0 והחזיר את מלוא SHA המועמד לעיל.

## רף הקבלה שנבדק

הטקסט הבא הועתק מ־**Acceptance:** ב־brief המחויב במועמד; נבדק שהוא מופיע בו בדיוק, כולל שבירות השורה:

> **Acceptance:** monitored synthetic/support tests cover all14 dates×three routes, effective
> distinctness/eight members, D−2 warmth/recovery, central failure refusal, B0/CQR differences,
> partial scoring/full DST days, once-only release/historical scale/causality, restart equivalence,
> search-boundary continuity, learning/H separation, route isolation, unchanged emitted fallback,
> and death/hard kill/PID reuse/orphan/unreconciled reserve accounting. Old-settings parity fits
> alone are permitted for current gate evidence, never serving CP-26.

גם **Stop/return:** נבדק מול העוגן: עצירה לפני real searches, timing pilot, experimental-calendar replay וציוני CP-26; אין מימוש/הרצת CP-28; מוכנות לתיקון אינה השלמת CP-26; pilot עתידי חייב לתמחר 42 חיפושים ואת כל ההוצאה ההיסטורית/המדווחת/הרזרבות מול 388 שעות; אין טענת Integration PASS ואין שינוי ל־integration.md.

## הפער המשמעותי ביותר והבדיקה הבאה

**[P1] בעלות על קבוצת תהליכים אינה נקשרת לזהות המקורית.** ב־`src/cp26/supervisor.py:112`, `worker_members()` מתחיל ב־`group_members(pgid)` ומכניס כל תהליך בעל PGID מספרי זה למפת הבעלות, לפני בדיקת PID/create_time של הילד המקורי. ב־`terminate_group()` בשורות 244–265 האות נשלח באמצעות `os.killpg(pgid, ...)` ללא קישור כזה. אם PID/PGID המקורי שימש מחדש לסשן זר אחרי שהקבוצה המקורית נעלמה, התהליך הזר מאומץ כעובד ונעשה יעד לסיום. בדיקת PID-reuse הקיימת מכסה `identity_status()` ו־`reconcile_running()` בלבד, ואינה מכסה מסלול זה.

השחזור המדומה החזיר `unrelated_replacement_adopted=true`, `mocked_group_signals=[[10001,15]]`, `acceptance_satisfied=false`; `real_signals_sent=0`. לכן רף PID reuse לא הושלם, גם כשהבדיקות הקיימות עוברות.

**בדיקת הקבלה הבאה:** כאשר זהות הילד המקורי היא PID 10001/create_time 1 והגילוי מחזיר תהליך זר עם אותו PID/PGID ו־create_time 2, יש לסרב באופן fail-closed בלי לאמץ או לסמן את התהליך הזר, בלי לשלוח אליו killpg/os.kill ובלי להפיק ראיית סיום בטוחה. יש לכסות גם שהילד המקורי הסתיים אך descendant מקורי מזוהה עדיין חי. התיקון דורש מועמד חדש וביקורת חדשה; מסמך זה אינו מאשר את המימוש הבא מראש.

## מיפוי ששת חוזי התיקון

| חוזה | תוצאה וראיה |
|---|---|
| 1. Jan15+182k, קוביות 28 יום, עד 11 החדשות הכשירות, mask/week נחת ו־250/14 בכל פיצול | אומת. search.py משתמש ב־G.window, באותו pool שבועות ו־20% holdout; extrema הם N פחות m השבועות הכבדים ו־m הקלים. כל 42 שורות הראיה חושבו מחדש; B=[1,7,11×12], קובייה ראשונה 2019-12-18..2020-01-14, minima 251/46. |
| 2. sampler128, מרחב/halving/rank/ties, seeds נפרדים, ארבע תצורות אפקטיביות×שניים, strict8 | אומת בקוד ובבדיקות synthetic. sampler/size/rank/halving הם cp24.sampler; מזהה trial אינו identity אפקטיבי, no-load מסיר flags; duplicates אינם גוררים דגימות נוספות. seed domains נפרדים וקבועים. batch כושל אינו יכול לדרג על כל הקוביות; search כושל אינו מאריך ensemble ישן; daily D2 דורש שמונה fits ומסרב לתת־קבוצה. |
| 3. native central/H readiness/scored source/error eligibility; warming/recovery ב־D−2 | אומת. PolicyState שומר native central וסקאלה לפני release; רק מחסור בהיסטוריית H מתיר intake בעת fallback. central/member/solver/identity/scale/numeric H failure אינם נכנסים. fallback שהונפק נשאר ברשומה ואינו מוחלף בדיעבד. |
| 4. B0 raw וללא A1 scale/self fallback; v1-R nine heads/CQR/embargoes | אומת בקוד ובבדיקות. RawResidualState שומר שגיאות גולמיות; B0 נשאר missing בזמן מדידה בלי quantiles תקפים. v1-R מעביר 9 heads דרך CQR ו־isotonic ואז בורר 7; חלונות D−62/D−1 נשמרים, ואין issued-error H במקום CQR. |
| 5. scoring/full own error/full3-member learning נפרדים; state/cache רציף ומבודד | אומת. partial issuance אינו day מלא, DST23/24/25 נשמר; partial scoring subset יכול להיות נפרד מהנפקה native מלאה. pending/consumed/scales/errors ושקילות restart מאומתים לאורך warm-up/measurement/search/failure. release מאוחר אינו נראה בתצוגה היסטורית מוקדמת. route/policy caches נפרדים. |
| 6. CP-28 prospective, H28 מול learning364/728, protocol unchanged | אומת לתיקון בלבד. learning מקבל שלושה members native מלאים גם כאשר v5 פלט fallback רק בשל H, ואינו מקבל member מועתק/partial. startup תלוי support בפועל. protocol v21-r14 משמר שבע זרועות, gates/Holm/selection/shared fits/start weights; לא מומשו זרועות. |

## מיפוי כל פריטי Acceptance והמשאבים

| פריט | תוצאה |
|---|---|
| all14 dates×three routes | אומת: 42 שורות חושבו מחדש והבדיקות לכל המסלולים עברו. |
| effective distinctness/eight members | אומת: ID/load flags, duplicates, disjoint seeds, strict8, failed member/search/stale ensemble/caches. |
| D−2 warmth/recovery | אומת: לא נדרש truth עבור D או D−1; error מקורי נכנס פעם אחת אחרי D−2 גם בתאריך fallback בשל H. |
| central failure refusal | אומת: גם failure ב־solver/member/identity/scale/numeric H אינו intake. |
| B0/CQR differences | אומת: raw-error buffer מול 9-head/CQR adapter, בלי self fallback. |
| partial scoring/full DST days | אומת: אין שעה מומצאת; complete(day,index) מול day_hours; DST23/25 ורשומות רגילות24. |
| once-only release/historical scale/causality | אומת: שינוי truth לאחר consumption אינו משנה buffer; סקאלה מקורית נשמרת גם לאחר restart; restored central/scale/error provenance נבדקים. |
| restart equivalence | אומת: serialized state זהה לריצה רציפה במספר גבולות. |
| search-boundary continuity | אומת: אין reset ב־ReplayState, כולל D2 failure/recovery. |
| learning/H separation | אומת: latest728/min364/728 מול H28; אין learning מתוך fallback member או מפתחות חלקיים. |
| route isolation | אומת: history של nominal אינו ממלא noload/gfs6; fallback nominal B0 הוא מקור שהוגדר במפורש, ללא borrowing של errors. |
| unchanged emitted fallback | אומת: ההנפקה המדודה המקורית נשמרת לאחר release/recovery. |
| death/hard kill | אומת בבדיקות אמיתיות מבודדות: independent supervisor, SIGKILL של outer ושל supervisor, no receipt אינו מרשה compute. |
| PID reuse | **לא הושלם**: מסלול PGID adoption/killpg שתואר לעיל. |
| orphan accounting | אומת למקרים שנבדקו: descendant מקורי/registered detached worker; uncertain/no receipt מסרב ואינו מחייב idle-gap כנמדד. PGID reuse מגביל את טענת הבעלות הכוללת. |
| unreconciled reserve accounting | אומת: reserve לא מפויס חוסם compute; reconciliation חד־פעמי; ההיסטוריה והשונות בין measured/reported/reserved נשמרות. |
| old-settings parity/current custody | אומת ללא fit נוסף: require_pass() קיבל בדיוק96 checks; current code/input fingerprint וה־historical Git/manifests custody התאימו. CP24 ensembles הם fixtures בלבד. |
| resource caps/projection | אומת לחשבונאות ול־declared allocations: 485h, repair10h, 4 workers, BLAS1, CPU, RSS12GB; projected_cost דורש בדיוק42 searches + הוצאות נוספות והיסטוריה, מול388h. מקביליות detached היא cooperative ומחייבת register_worker; אין ראיה לעודף workers בפועל. ה־registration אינו אוכף בעצמו מספר compute identities, ולכן כל parallel bootstrap עתידי צריך חוזה/אימות slots במסגרת ההמשך. |

## זהות הראיות וה observations

- parity פעיל: `reports/rebaseline/parity.json`; gate ישן בלבד, 96 checks. require_pass אימת שלמות, exact float64 bits/keys, קוד/inputs נוכחיים ו־custody היסטורי.
- support: `reports/rebaseline/repair-v21-r14/search-support.json`, SHA-256 **586525380e8552cce416fe44bb25525413fc936dc281a51160884e1a1d1e7ba8**; ה־Markdown המצורף מצטט SHA זה.
- signed global digest: **6317b167848707fe29a6d32ef834b7ab7cc34926001244ae019d94b65600c2f2**; גם כל extended row digest וגם underlying support_freeze digest אומתו.
- H.identities אימת27 pins ו־H.landed_code אימת146 modules. אין שינוי ב־landed code.
- כל42 support rows התאימו ל־batch_support המחושב מחדש; 31,575 trial/batch fits הם full-success support bound לתמחור עתידי, לא fits שבוצעו.
- החשבונאות המגובה: 547.5647564170067s היסטוריים, כולל6.125s כבר בפנים; 90.127s נוסף פעם אחת כ־reported;15.01s נשאר lower-bound metadata בלבד;2826s נשאר reserve מורשה, ולא measured.
- audit window1791907417..1791908415 נמצא בין parity end1791905827.8090382 לבין receipt1791908653.442842; hash/ראיית החלון וה־reserve התאימו. ביקורת חשבונאות נפרדת לקריאה בלבד אימתה45 hashes של run files ותשע bindings של request/completion.
- snapshot המוניטור לאחר השחזור האחרון: measured1626.9317353788647s, reported96.252s, reserved2826s; total4549.183735378865s =1.2636621487163515h. repair used1085.4919789618584s; יתרה34914.50802103814s; אין unreconciled reserves.
- כל תוספת בדיקה, גם טעות בסקריפט הביקורת וגם acceptance שלילי, נשארת בחשבונאות. אין איפוס או הפחתת reserve.

## פקודות מדויקות, exit codes ופלט שנצפה

כל פקודות ה־compute בוצעו מן ה־checkout המנותק לעיל, עם interpreter הנעול, דרך המוניטור הראשי המצטבר. ההפעלות יצרו logs/request/progress/clock receipts ב־`/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/`; pytest השתמש ב־basetemp חדש בתוך הפרויקט. קריאות cat/sed/rg/wc ופקודות Git read-only יצאו0. לא הורצו parity fits נוספים.

| job | exit | observations |
|---|---:|---|
| repair-r14-critic-tests | 0 |81 passed in34.87s; monitor wall36.62892920896411s ×2 workers; peakRSS1778368512 bytes. |
| repair-r14-critic-identities | 1 |Assertion line25: בטעות הושווה digest של extended report row לזה של underlying support. זו שגיאת בדיקת המבקר, לא defect במועמד. require_pass96/pins/code/global digest/reportSHA כבר עברו לפני assertion. |
| repair-r14-critic-identities-corrected | 0 |27pins,146modules,96paritychecks,42rows recomputed; B ו־251/46 התאימו; wall22.64554683404276s. |
| repair-r14-critic-pgid-reuse | 1 |mock group-members sequence נגמר מוקדם (StopIteration); תוקן בסקריפט המבקר בלבד. wall1.9519169589621015s. |
| repair-r14-critic-pgid-reuse-confirmed | 1 |הקבלה השלילית שחזרה adoption של replacement ו־SIGTERM מדומה ל־PGID; real_signals_sent=0; wall1.9352504170383327s. |

### repair-r14-critic-tests

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-critic-tests --workers 2 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest tests/test_cp26_harness.py tests/test_cp26_parity.py tests/test_cp26_search.py tests/test_cp26_state.py tests/test_cp26_replay.py tests/test_cp26_monitor.py tests/test_cp26_repair_contract.py -q --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/repair-critic-tests
```

### repair-r14-critic-identities

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-critic-identities --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -c 'from pathlib import Path
import hashlib, json
from cp26 import harness as H, parity as P, search as S
from cp24 import design as G
root = Path.cwd()
pins = H.identities(root)
landed = H.landed_code(root)
parity = P.require_pass(root)
assert len(parity["checks"]) == 96
support_path = root / "reports/rebaseline/repair-v21-r14/search-support.json"
support = json.loads(support_path.read_text())
assert support["content_sha256"] == S.digest(support)
assert support["inputs_sha256"] == pins
assert all(H.sha(root / name) == value for name, value in support["code_sha256"].items())
report_sha = hashlib.sha256(support_path.read_bytes()).hexdigest()
assert report_sha in support_path.with_suffix(".md").read_text()
assert len(support["searches"]) == 42
data = H.load(root, H.NEW, before=S.search_day(13))
seen = set()
for route in S.ROUTES:
    dd = G.build(data, H.weather_design(root, H.GFS6 if route == "gfs6" else H.NEW))
    for k in range(14):
        row = next(r for r in support["searches"] if r["route"] == route and r["k"] == k)
        computed = S.batch_support(dd, k)
        assert all(row[name] == value for name, value in computed.items())
        assert row["support_freeze_sha256"] == computed["content_sha256"]
        assert (route, k) not in seen
        seen.add((route, k))
        if k == 0:
            b = row["batches"][0]
            assert (b["first"], b["last"], b["minimum_possible_train_days"], b["minimum_possible_hold_days"]) == ("2019-12-18", "2020-01-14", 251, 46)
assert all(v == [1, 7] + [11] * 12 for v in support["B_by_route"].values())
assert support["search_count_for_future_pilot_cost"] == 42
assert sum(support["search_fit_counts_at_full_success"].values()) == 31575
print(json.dumps({"pins": len(pins), "landed_modules": len(landed), "parity_checks": len(parity["checks"]), "parity_require_pass": True, "support_rows_recomputed": len(seen), "report_sha256": report_sha, "signed_digest": support["content_sha256"], "B": [1, 7] + [11] * 12, "first_minima": [251, 46], "model_fits": 0, "experiment_scores": 0}, sort_keys=True))
'
```

### repair-r14-critic-identities-corrected

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-critic-identities-corrected --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -c 'from pathlib import Path
import hashlib, json
from cp26 import harness as H, parity as P, search as S
from cp24 import design as G
root = Path.cwd()
pins = H.identities(root)
landed = H.landed_code(root)
parity = P.require_pass(root)
assert len(parity["checks"]) == 96
support_path = root / "reports/rebaseline/repair-v21-r14/search-support.json"
support = json.loads(support_path.read_text())
assert support["content_sha256"] == S.digest(support)
assert support["inputs_sha256"] == pins
assert all(H.sha(root / name) == value for name, value in support["code_sha256"].items())
report_sha = hashlib.sha256(support_path.read_bytes()).hexdigest()
assert report_sha in support_path.with_suffix(".md").read_text()
assert len(support["searches"]) == 42
data = H.load(root, H.NEW, before=S.search_day(13))
seen = set()
for route in S.ROUTES:
    dd = G.build(data, H.weather_design(root, H.GFS6 if route == "gfs6" else H.NEW))
    for k in range(14):
        row = next(r for r in support["searches"] if r["route"] == route and r["k"] == k)
        computed = S.batch_support(dd, k)
        assert all(row[name] == value for name, value in computed.items() if name != "content_sha256")
        assert row["content_sha256"] == S.digest(row)
        assert row["support_freeze_sha256"] == computed["content_sha256"]
        assert (route, k) not in seen
        seen.add((route, k))
        if k == 0:
            b = row["batches"][0]
            assert (b["first"], b["last"], b["minimum_possible_train_days"], b["minimum_possible_hold_days"]) == ("2019-12-18", "2020-01-14", 251, 46)
assert all(v == [1, 7] + [11] * 12 for v in support["B_by_route"].values())
assert support["search_count_for_future_pilot_cost"] == 42
assert sum(support["search_fit_counts_at_full_success"].values()) == 31575
print(json.dumps({"pins": len(pins), "landed_modules": len(landed), "parity_checks": len(parity["checks"]), "parity_require_pass": True, "support_rows_recomputed": len(seen), "report_sha256": report_sha, "signed_digest": support["content_sha256"], "B": [1, 7] + [11] * 12, "first_minima": [251, 46], "model_fits": 0, "experiment_scores": 0}, sort_keys=True))
'
```

### repair-r14-critic-pgid-reuse

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-critic-pgid-reuse --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -c 'import json, signal
from unittest.mock import patch
from cp26 import supervisor as S
old = {"pid": 10001, "create_time": 1.0}
replacement = {"pid": 10001, "create_time": 2.0}
known = {}
with patch.object(S, "group_members", return_value=[replacement]), patch.object(S, "identity_status", side_effect=lambda item: "reused" if item == old else "same"):
    observed = S.worker_members(10001, old, known)
signals = []
with patch.object(S, "group_members", side_effect=[[replacement], [], []]), patch.object(S.os, "killpg", side_effect=lambda pgid, sig: signals.append([pgid, int(sig)])):
    S.terminate_group(10001)
unsafe = replacement in observed and bool(signals)
print(json.dumps({"old_identity": old, "replacement_identity": replacement, "unrelated_replacement_adopted": replacement in observed, "mocked_group_signals": signals, "real_signals_sent": 0, "acceptance_satisfied": not unsafe}, sort_keys=True))
raise SystemExit(1 if unsafe else 0)
'
```

### repair-r14-critic-pgid-reuse-confirmed

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-critic-pgid-reuse-confirmed --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -c 'import json, signal
from unittest.mock import patch
from cp26 import supervisor as S
old = {"pid": 10001, "create_time": 1.0}
replacement = {"pid": 10001, "create_time": 2.0}
known = {}
with patch.object(S, "group_members", return_value=[replacement]), patch.object(S, "identity_status", side_effect=lambda item: "reused" if item == old else "same"):
    observed = S.worker_members(10001, old, known)
signals = []
groups = iter([[replacement]])
with patch.object(S, "group_members", side_effect=lambda _: next(groups, [])), patch.object(S.os, "killpg", side_effect=lambda pgid, sig: signals.append([pgid, int(sig)])):
    S.terminate_group(10001)
unsafe = replacement in observed and bool(signals)
print(json.dumps({"old_identity": old, "replacement_identity": replacement, "unrelated_replacement_adopted": replacement in observed, "mocked_group_signals": signals, "real_signals_sent": 0, "acceptance_satisfied": not unsafe}, sort_keys=True))
raise SystemExit(1 if unsafe else 0)
'
```


## מגבלות והחזרה

זהו תיקון תשתית עם synthetic/support evidence ו־gate parity קיים. לא הוכחה הצלחה מספרית של ארבע תצורות אמיתיות/שמונה fits יומיים, עלות החיפושים, CQR על כל התאריכים או תוצאה מדעית. קוביית החיפוש הראשונה היא קוביית חורף יחידה; גיל/span של buffers נשמר ומדווח בקוד.

ה־README המחויב אומר במפורש שה־end-to-end experiment CLI, orchestration/checkpoint-resume scheduling ו־score/inference assembly עדיין צריכים השלמה ואימות במסגרת continuation. פריטים אלה מחוץ לרף התיקון הנוכחי; גם לאחר תיקון ה־PGID אין בכך השלמת CP-26. נדרשים אשרור exact r14, continuation brief, תמחור42 searches כולל כל history/reserves מול388h, ניסוי/תוצרים וביקורת Integration נפרדת.

לא נוצרו branch/tag/worktree על ידי מבקר זה; ה־checkout נשאר לטיפול ההורה. חומרי הביקורת המקומיים הנשמרים הם מסמך זה, ה־monitor receipts/logs ו־pytest basetemp. לא נמצאה חשיפת credential או exposure של outcome חדש. **Interview trigger:** כיצד מנענו בלבול בין זהות תהליך ובעלות על קבוצתו בעת PID reuse; טרם הושלם התיקון ולכן אין לתאר הגנה זו כמוכחת.

**Post-return reads:** none. פסק הדין הסופי למועמד הזה הוא **REPAIR_INCOMPLETE**.

