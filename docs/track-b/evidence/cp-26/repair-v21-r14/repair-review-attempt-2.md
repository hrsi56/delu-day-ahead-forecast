# CP-26 — ביקורת עצמאית תחומה של מוכנות תיקון r14, ניסיון 2

**Verdict: REPAIR_READY**, לתיקון התחום בלבד. **CP-26 נשאר INCOMPLETE**; זה אינו Integration PASS, אינו אישור r14 ואינו הרשאה לחידוש ניסוי.

**המועמד שנבדק:** `68d5db593e968c8dcff31c35ecccc355799ddd8e`.
**Snapshot:** `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/repair-review-68d5db5`, detached ונקי לפי Git בתחילת הביקורת ובסיומה; HEAD נשאר המועמד המדויק. לא נערכו קוד, בדיקות, מסמכים או פעולות כתיבת Git ב־snapshot. הסתייגות לגבי תוצר pytest מוסברת להלן.

**החוזה:** `issued-repair-brief-v21-r14.md`, המועמד `capstone_v21.md` §§24.7–24.9, גיליון r13→r14 והפרוטוקול החדש `cp28-frozen-protocol-v21-r14.md`. עוגן r14 נוצר ב־`332baeb861cec5a58516c58a29a1a3afe1eec909`; בסיס השוואת landed הוא `647d6eb81b2cf6e0cfaf4152f659d689ff973578`.

קטעים מילוליים מן הבר שנבדק:

> **Stop/return:** stop before real searches, timing pilot, experimental-calendar replay or CP-26
> scores; no CP-28 implementation/execution. Return REPAIR_READY only with repair evidence, or
> precise blockers/gaps; CP-26 remains INCOMPLETE.

> **Separate four statuses on every date:** native-central validity, interval readiness, source
> of the emitted/scored output, and eligibility of the issuance for a complete-day own error.

> **The ensemble:** four best distinct effective configurations, two seeds each, exactly eight
> members. Effective identity excludes trial id; in the no-load variant it also excludes removed
> load flags. Duplicates consume trials; no extra sampling compensates for them.

הקטעים מופיעים במסמכים המחויבים במועמד. ההכרעה מבוססת על המימוש והראיות ולא על סיפור Builder או verdict קודם.

## בדיקות ופקודות

כל חישוב בביקורת הופעל דרך המנטר המצטבר מן ה־snapshot, CPU ו־BLAS1; לכל היותר שני workers מוצהרים בבדיקות. לא בוצעו fit אמיתי, download, חיפוש אמיתי, pilot, replay על לוח הניסוי או score. בדיקות parity השתמשו ב־stubs ובווקטורי reference מחויבים; שער parity הקיים נבדק בלי לחזור על אימונו. שחזור התמיכה שבבדיקות הספיק; לא הורץ שוב סקריפט התמיכה המלא.

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-fresh-critic-tests --workers 2 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest tests/test_cp26_harness.py tests/test_cp26_parity.py tests/test_cp26_search.py tests/test_cp26_state.py tests/test_cp26_replay.py tests/test_cp26_monitor.py tests/test_cp26_repair_contract.py -q --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/repair-fresh-critic-tests
```

**תוצאה:** exit 0, `88 passed in 38.52s`. המנטר רשם `wall_seconds=40.33212904102402`, workers=2, `peak_rss_bytes=1578385408`, ללא abort. קבלה `cp26-completion-v2` של job `3d7ba9521adf43779b6ab407007336b9`, index26, מאשרת `workers_stopped=true`, `group_empty=true`, `ending_error=null`, `worker_ceiling_error=null`. Hash בקשת העבודה: `17cded49797cf90adfd5e25323825b43fdd68e3c24f433e8326063e24bb2f8c9`.

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-fresh-critic-metadata --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B /Users/djourno/Downloads/PJM/.local/tmp/cp-26/repair-fresh-critic-metadata.py
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-fresh-critic-metadata-bounded --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B /Users/djourno/Downloads/PJM/.local/tmp/cp-26/repair-fresh-critic-metadata.py
```

שתי הריצות exit0; הראשונה `2.372314499982167s`, השנייה `3.197191707964521s`. אחרי תיקון סינון הנתיבים בסקריפט הביקורת, הריצה האחרונה אימתה 27 pins, ‏146 קובצי Python של landed, ‏96 checks של parity הנוכחי וארבעה קבצים משומרים. קבלת הריצה האחרונה מאשרת סיום תקין; hash בקשתה `90fd3250c97476d7019784b2b823c6dee6d68dba1e45fe099ef63fcd47420768`.

סקריפט metadata נכתב רק ב־primary `.local/tmp/cp-26`; SHA-256 סופי `d157fe4f95c0954df8feafaa6f1fb8a38b432f1341ed8eadf0b65f72a958b41c`. הפלט `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/repair-v21-r14/fresh-critic-metadata.json`, SHA-256 `69ba25a6cb1c3b9dd73e79ad22ca7086aa1330708d640630ded95dcfd49901d0`.

פקודות אימות Git שנקראו: `git rev-parse HEAD`, `git status --porcelain=v1`, `git diff --stat`; HEAD כמוגדר, status ו־diff ריקים. סקריפט metadata אימת detached באמצעות `git symbolic-ref -q HEAD` (exit1 צפוי), השתמש ב־`git show` להשוואת blob היסטורי ובבדיקות `H.identities`, `H.landed_code`, `P.require_pass`. קריאת קוד וחוזים נעשתה עם cat/sed/rg; לא היה Git write. ניסיון cat של שם קבלה עם index25 נכשל exit1, לאחריו `rg --files` איתר את קבלת index26 הנכונה, והיא נבדקה.

## תוצאות לפי חוזה התיקון

| דרישה | ראיה ומסקנה |
|---|---|
| 14 תאריכי חיפוש × שלוש routes; Jan15+182k; tiles28; newest≤11 | `search.py`, landed `cp24.design.window` ו־`sampler.week_pool`, ובדיקה מחויבת פרמטרית על כל42 הצירופים. ה־support mask אינו מוחלף בכלל full-day. נשמרת הוצאת שבעת הימים האחרונים. |
| extrema של כל split; מינימום250/14; B=[1,7,11,…]; חלון ראשון251/46 | סכום m השבועות הכבדים/קלים קובע את המינימום, לפני seed או loss. בדיקות exhaustive synthetic ובדיקות frozen inputs עברו. JSON תמיכה מחויב וזהויות קוד/inputs שלו אומתו; רשימות shared וחתומות לפני fit. |
| sampler128, fixed space/halving/ranking/ties, זרעים נפרדים | קריאת `search.py` מול landed sampler/search; בדיקות reproducibility/domain separation עברו. 128 כולל כפילויות; אין resampling או replacement seeds. |
| ארבע תצורות אפקטיביות × שני seeds, strict8, no-load diversity | effective identity מסיר id ו־load flags שנמחקו. validation דורש ארבע זהויות אפקטיביות ושמונה חברים; כשל batch אינו מדורג על כל batches. בדיקות duplicate/failure/strict8 עברו. |
| search failure/no carry/אין serving של CP24 | service period קשור ל־k ול־route; חיפוש חסר/כושל משבית D2 עד הבא המתוזמן. CP24 מותר רק במסלול OLD parity עם k=None. fit/cache דורשים ensemble תקף; אין subset median או retry. |
| native central / H readiness / measured output / own-error eligibility | `PolicyState.issue` שומר ארבעה סטטוסים. shortage בלבד מאפשר intake של central מקורי עם scale תקף ו־full canonical day. פלט B0 נשאר copied/scored/counted ואינו משתנה אחרי release. בדיקות warm-up/recovery/immutable output עברו. |
| member/solver/identity/scale/numerical-H failures | failure מסומן; אין pending own-error במקרים אלה. numerical predict failure מופרד מ־history shortage. בדיקות חיוביות ושליליות עברו. |
| B0 raw/no A1/no self fallback; v1-R תשעה heads+CQR | `RawResidualState` משתמש בשגיאות raw ללא scale. B0 ללא quantiles נשאר missing במדידה ויכול לחמם central מקורי. v1-R שומר windows728, שני embargoes, תשעה heads, CQR ואחריו isotonic ושבע quantiles; אין H במקום CQR. בדיקת adapter עם stub estimators עברה. |
| partial scoring לעומת full DST day | scoring_index נפרד מ־index של issuance. ימים חלקיים נשארים measured על keys קפואים; אין invented hour. full23/24/25 יכולים להיכנס ל־own errors ול־learning. בדיקות partial/DST עברו. |
| pending/consume once/historical scale/no D או D−1 feedback | release מתיר רק≤D−2 ו־complete truth; original central/scale נשמרים. once-only ו־late-truth historical view נבדקו. שינוי outcomes מאוחרים לא שינה issuance. |
| persistence/route-policy isolation/search continuity | `ReplayState` כולל pending, consumed, buffers, records, learning ומזהה תוכן; FitCache קושר route/day/keys/instant/input/code/ensemble. restart שווה continuous; search/failure אינו מאפס state. tamper/cache identity ו־wrong-key controls עברו. |
| CP28 learning364/728 נפרד מ־H28 | LearningLedger דורש c_HG, ‏L משני חבריו ו־D2 native על full canonical keys. יכול לגדול בזמן H shortage ואף בהיעדר scale; זה אינו היתר H intake. historical scale/provenance שמורים. אין arm, solver או selection של CP28 במימוש התיקון. |
| שבע arms/gates/Holm/shared fits/start weights | בדיקות משוות את sections3/4/5/8/9 של הפרוטוקול הקודם והחדש byte-identically. שבע זרועות,364/728,shared fits,0.995/1.02,עשרים endpoints,Holm וכל הרגישויות/שערי Owner נשמרו. הסתייגות ניסוחית P3 להלן. |
| supervisor/death/resume/PID reuse/orphans/ceilings | בדיקה עצמאית של worker_members/root_owns_group/signal_identity/terminate_workers/ending_evidence/register_worker/reconcile_running; בדיקות real hard death, detached registration denial, orphan, PID reuse ו־uncertain endings עברו. פרטי הערכת התכנון להלן. |
| history/reserve/resource contract | historical547.5647564170067s כולל6.125 הקודמים, audit90.127 נוסף פעם אחת,2826 reserve נשאר reserve,15.01 רק lower bound. tests מונעים הקטנת charge/reuse of charge id ו־unbounded import; כל classifications נכללים בתקרות וב־42-search projection. |
| pins/base/preservation/current parity | 27 pins תקפים; landed Pythonfiles146 ללא שינוי מול647d6eb; anchors §§1–23 והמסמכים המקוריים נשמרו. P.require_pass אימת96 bitwise checks,code/inputs/reference custody נוכחיים,OLD בלבד ו־scores0; ללא fit חוזר. |

## בדיקה עצמאית של supervision

`worker_members` מגלה descendants דרך identity קשור; numeric PGID אינו מקנה בעלות אחרי מוות/reuse. `root_owns_group` דורש PID/create_time המקורי יחד עם session/group root, ובודק זהות שוב אחרי discovery. כשבעלות אינה תקפה, חבר בלתי מוכר בקבוצה גורם לחסימה; replacement אינו נוסף ל־known.

`signal_identity` בודק create_time ומאותת באמצעות psutil לתהליך הקשור; אין killpg. `terminate_workers` ממשיך לעצור identities מקוריים ידועים גם כשקיימת בעיית בעלות, בלי לאמץ או לאותת replacement, ואז מחזיר את בעיית הבעלות. `ending_evidence` אינו ממיר אותה ל־workers_stopped/group_empty חיוביים. טבלת closing נשמרת תחת lock וממזגת registrations לפני הקבלה.

`register_worker` סופר גם root coordinator, dedupes identities, כולל unknown/denied כסלוטים conservatively, בודק allocation מקומי ואת שתי תקרות global (declared ו־active). denied identity נשמר לפני exception כך שאינו נעלם מן ending evidence; tick מסיים עם registered_worker_ceiling. Detached/parallel workers חייבים להירשם לפני compute: זה פרוטוקול שיתופי, לא sandbox נגד תהליך שמפר אותו במכוון. בדיקות real denied-worker מוכיחות שלא הגיע ל־marker של computation.

מוות outer monitor משאיר supervisor עצמאי שמודד עד הסיום. מוות supervisor בלי קבלה, orphan חי, identity לא ידוע או receipt בלי הוכחת סיום חוסמים המשך. reconciliation משתמש במשך שבקבלה וב־prefix שכבר חויב, בדיוק פעם אחת, ואינו מחייב idle gap כזמן מדוד.

## זהויות מהותיות

| קובץ | SHA-256 |
|---|---|
| capstone_v21.md | `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5` |
| r13-to-r14 amendment | `554a3aa4bf81f3fc1cc2319e624295570f919ff1fd4a6d9e2c9f56f8dcf6b79a` |
| issued-repair-brief-v21-r14.md | `5b6a0cdfad870da6b59a03ff29576ff6ec98891e941d56986516e6f3f743ff84` |
| cp28-frozen-protocol-v21-r14.md | `2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8` |
| active-documents.json | `aa29af82181769afefdb0a4446057dd08f7ebafaac27a398aa2679397a3cadfe` |
| original issued-brief.md | `5e16a134a9dd798733b0393f4f8e2570d03bf251471503d9292966e67e05214b` |
| original cp28-frozen-protocol.md | `f2ebee6ec207047bb1db7a311d7fbf437627ad7c395f1e07c92417c7f5a623cc` |
| current parity.json | `50b3472f81e8520af7ba70f93509584d59d6fedf337716ae6333ae3909150cdc` |
| repair search-support.json | `586525380e8552cce416fe44bb25525413fc936dc281a51160884e1a1d1e7ba8` |

ה־parity gate נוצר ב־`563be855d918cb7ec3a2b53497414a863dc43431`; תוקפו למועמד הנוכחי הוכח בבדיקת code/input/custody, ולא הונח משוויון SHA של commit. ארבע זהויות preserved-r13 מאומתות ב־metadata: anchor `173799d8…`, driver `844f6dce…`, monitor tests `ef0f0fb8…`, parity `5c2229b2…` — hashes מלאים מצורפים בפלט.

## משאבים, עצמאות ומגבלות

בקבלת metadata האחרונה: measured1795.0931119619636s, reported96.252s, reserved2826s, total4717.345111961964s =1.3103736422116568h; repair-used1253.6533555449573s, יתרת repair34746.34664445504s. אלו ערכי ה־ledger המצטבר בזמן אותה קבלה, כולל פעילות אחרות המתועדת בו; אין reset או טענה שהם רק עלות הביקורת. ceilings485h/4workers/12GB וה־pilot stop388h נשארו. הרזרבה אינה זמן מדוד מדויק.

לא קראתי progress.md, orchestrator-role.md, syllabus או Track A/C; לא נבדקו צ'אטים אחרים, histories/terminal summaries או חבילות/סיפור Builder, ולא נקרא verdict קודם. עוזר תחום טרי ביצע קריאה סטטית של search/landed comparator והפרוטוקול באותו snapshot; הוא לא חישב או כתב. ההכרעה, בדיקת supervision/state והריצות הן שלי.

**שתי חריגות פרוצדורליות מדווחות:** פקודת pytest המדויקת שבבריף יצרה `.pytest_cache` Git-ignored ב־snapshot. זו אינה עריכת artifact מחויב, ו־engineering-role מתיר ignored byproduct בלי לפסול ניקיון; עם זאת זו חריגה מלשון 'No writes snapshot', ולכן איני טוען אפס תוצרי לוואי. בנוסף, בלולאת SHA של metadata הראשון, row בעל path מוחלט ב־initial-inventory גרם לחישוב hash בלבד של attachment המקורי מחוץ ל־snapshot; תוכנו לא הוצג ולא שימש להכרעה. סיננתי paths מוחלטים ו־.local והרצתי שוב metadata תחום על ארבעת הקבצים המשומרים בתוך snapshot. כל הפלטים/סקריפטי הביקורת האחרים נמצאים ב־primary .local. הבידוד שיתופי; אין טענה ל־read-only mount.

**P3 תיעודי, inherited:** במשפט section3 של הפרוטוקול, 'All learned arms use w0 until their minimum history exists' מכליל גם A4, בעוד טבלת A4, המשפט הבא והעוגן §24.8 אומרים A4←A3_deployed עד728. כשיש364–727 ימים אין חובה A4=w0. section3 נשמר byte-identically לפי חוזה התיקון; אין כאן שינוי שיטה או חסר מכני. לפני מימוש CP28 יש להחיל את הטבלה והעוגן המפורשים, ולהבהיר את משפט הסיכום רק במסגרת סמכות מתאימה, בלי לשנות arms/gates.

לא נותר חסר מכני משמעותי בחוזה התיקון שנבדק. **ה־end-to-end CLI לחיפוש/pilot/replay/score assembly עדיין אינו שלם**, והוא חסר מוצהר ומותר בשלב הזה; driver חושף verify-inputs/parity בלבד. טרם הוכחו ארבע תצורות מוצלחות בחיפוש אמיתי, eight-member daily fits על לוח הניסוי, affordability, startup מדוד, או תוצאות מדעיות. המנטר אינו מחליף authorization. נדרשים Owner ratification ו־continuation brief לפני כל אלה; CP26 נותר INCOMPLETE ולא נכתב integration.md.

טריגר interview: כיצד הוכחת extrema לכל holdout-week split, והפרדת central מקורי מפלט fallback מדוד, מאפשרות warm-up/recovery סיבתי בלי לשכתב את המדידה. לא נוצרה חשיפת credential, publication או remote write בביקורת.

נשמרו לבדיקה מקומית: review זה, metadata JSON וסקריפט, logs וקבלות המנטר, תיקיית basetemp ו־pytest cache המוצהר. לא נפתחו refs,branches,tags או worktrees; הביקורת אינה מסירה את ה־snapshot שה־Lead יצר. ה־Lead רשאי לייבא את verdict המקומי ולהשלים את ה־handover. עבודה נוספת נעצרת כאן.
