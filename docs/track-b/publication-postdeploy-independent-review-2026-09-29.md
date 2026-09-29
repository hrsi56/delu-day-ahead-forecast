# ביקורת עצמאית לאחר פרסום PRES-1 — 2026-09-29

**הכרעה: FAIL מול התקן הקיים.** המספרים המרכזיים, זהות הגרסאות, הדמו המבצע חישוב ומראת MLflow אומתו בהצלחה. ארבע הפרות נשארות: פקדים ללא שם נגיש בדמו; בקשת favicon נכשלת באתר הציבורי; נתוני האתחול המדודים מוסתרים במקום להופיע ליד פעולת הדמו; ומניין 448 ימי ההערכה חסר בחלק הגלוי של ההשוואה. אלו פערי פרסום ונגישות, לא ראיה לחישוב מחקרי שגוי. אין בדוח הוראה להסיר פרסום או הרשאה לפרסם תיקון.

**המלצה לתקן: להכין הצעת v2 ממוקדת לאישור הבעלים**, בשני נושאים שהוכחו גם בקריאה חדשה: שיוך שני אחוזי הכותרת למדדים, ויישוב הפער בין מגבלת הפיקסלים לבין מספר מסכי הקריאה עם כותרת דביקה. עד אישורו, v1 נשאר התקן המחייב. אף הצעת v2 אינה עילה ל־FAIL הנוכחי.

## 1. סמכות, נקודת פתיחה וסדר הבדיקה

התפקיד הוא בודק עצמאי לאחר פרסום, לפי הוראת הבעלים במשימה זו. לא Builder, לא Engineering Lead ולא Orchestrator. עבדתי ישירות ב־`/Users/djourno/Downloads/PJM`, בלי branch או worktree חדשים. בתחילת הבדיקה:

```text
branch: main
HEAD: 01e394d475202bb44a226f2ac5403aa084dc5b4c
git status --porcelain=v1: empty
```

לא בוצעו stage, commit, merge, push, העלאה או פריסה. לא שונו מימוש, תקן, מסמך ממשל או ראיה היסטורית. הדוח הזה נוצר בשם שלא היה קיים. חומרי העזר נוצרו ב־`.local/artifacts/postdeploy-independent-2026-09-29/` וב־`.local/tmp/postdeploy-independent-2026-09-29/`.

הקריאות לשירותים היו אנונימיות: GET ו־POST של חיפוש MLflow בלבד; אין כתיבה לשירות. לא נקראו, הודפסו או שונו ערכי סודות. לא הורצו אימון, איסוף נתוני מחקר, scoring חדש או bootstrap חדש. הפעלת הדמו היא החישוב המקומי שהמוצר הציבורי מציע בדפדפן.

ראיות הזהות נאספו החל מ־2026-09-28 22:24 UTC, כלומר **2026-09-29 01:24 בישראל**. אין סתירה בין תאריך הכותרת לתאריך UTC. הממצאים הראשונים הוקפאו בחומר העזר `initial-findings.md` **לפני** קריאת הביקורות הקודמות ויומן ההמלצות; ההשוואה אליהם נעשתה לאחר גיבושם. סוכן הקורא החדש נוצר ללא ירושת שיחה, וקיבל רק צילומי מסך ושאלות.

## 2. התקן וזהות התוצרים הציבוריים

### 2.1 המסמכים המחייבים

| מסמך | גרסה/זהות ותחולה |
|---|---|
| [AGENTS.md](../../AGENTS.md) | הרשות המוגבלת של הביקורת הנוכחית; נעילת ממשל, שמירת ראיות וסודות |
| [Publication Standard v1](publication-standard-v1.md) | אושר ב־2026-09-28; SHA-256 `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`, זהה לעותק המאושר |
| [תוכנית הצגה, revision 3](presentation-and-tracking-plan-2026-09-24.md) | כפופה לתיקונים המפורשים ב־v1 §15; יתר הדרישות בתוקף לפי §§14,16. SHA-256 שנבדק בביקורת זו: `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c` |
| [בריף ההתאמה](evidence/pres-1/pres-1-conformance-brief-2026-09-28.md) | SHA-256 שנבדק: `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502` |
| [החלטות הבעלים](evidence/pres-1/owner-decisions.md) | אשרור התקן, האצלת אישור חזותי, החלפת Safari/iPhone/VoiceOver אמיתיים בבדיקות התקן; יישוב דרישת zero-diff עבור artifacts הנושאים זהות |

נבדקו גם [runbook](publication-runbook.md), [תבנית packet](publication-packet-template.md), ובהמשך [יומן המלצות](publication-advisory-log.md) ו[רשומת הנחיתה](pres-1-landing-2026-09-29.md). הוראות הביצוע ההיסטוריות בבריף אינן הרשאה למשימה זו ליצור worktree, להעלות או לפרסם.

הכללים הממתינים לטריגר ב־§16 אינם שערים לפרסום הזה: צבע/סימון v4, compaction ב־v5 או בחריגת גודל, bootstrap של יחס מ־CP-21, ניסוי final-candidate, Live, תזמון ועדכון יומי. לא החמרתי את הבדיקה באמצעותם.

### 2.2 זהות שנמדדה בשירות, ולא הונחה מהקובץ המקומי

| משטח | בדיקה עצמאית ותוצאה |
|---|---|
| [GitHub / main](https://github.com/hrsi56/delu-day-ahead-forecast) | API ציבורי מחזיר `01e394d475202bb44a226f2ac5403aa084dc5b4c`, זהה ל־HEAD המקומי. deployment `6721690650`, סביבת `github-pages`, באותו SHA ובמצב `success` |
| [Pages](https://hrsi56.github.io/delu-day-ahead-forecast/) | HTTP 200; **1,560,646 bytes**; SHA-256 `d1227c0f64c6a478f6f076e713e2bed2755edf51d0b8f19522c9b978d42fab3d`. גוף התשובה זהה ל־raw GitHub `main/docs/index.html` ולקובץ המקומי |
| README המוגש ב־GitHub | גוף raw ציבורי: **39,420 bytes**, SHA-256 `675d9b5b380ca1d491480bd01b21be511548a18d34d7ff18e861be98a5f6b005`; זהה למקומי. נפתח גם ממשק GitHub המצויר |
| [HF Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast) | API ציבורי: commit **`59d941825755bf73eabb7ff20e31124fee305755`**, runtime `RUNNING`. כרטיס ציבורי: SHA-256 `6c89e63e7439f69992f43715edf25a5d15f65cadff060d0870ec837d3540680f`, זהה ל־`space-wasm/README.md` |
| [האפליקציה הישירה](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/) | redirect אל `/index.html`, HTTP 200; **82,919 bytes**, SHA-256 `c0621a646a8b413b24f02c9d6bc87b244ff2be457ce3be49fa303128fb3310fc` |
| מקור index ב־HF | **82,818 bytes**, SHA-256 `1d701cbeb146ee5c77b45d3c9d705656671444b5062fe3adca3ba7ae1341fa95`. ההבדל המדויק מול המוגש הוא הזרקת סקריפט מטא־נתונים ציבורי של HF ב־head; לא החלפת אפליקציה |
| [MLflow](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow/#/experiments/1) | `delu-generations`, experiment ID `1`; **23 ריצות, 560 היסטוריות מדדים, 6,928 נקודות, 55 artifacts** תואמים ליצוא המחויב. גם שמות, parents, parameters, tags ותיאור source of truth נבדקו |

רשומת הנחיתה מבדילה נכון בין squash `265661da4d8ae2565003c8ab6e8525f9ffec45d3`, המועמד שנבדק `a0302dd6c5ff6714709b4f3a3b742f71a4b596a7`, evidence tip `0df6dda203ea31ab35b34e7ad69d2a2e3e871ebf`, ו־HEAD הציבורי הנוכחי. אין ל־MLflow SHA פריסה יחיד: זהותו כאן היא תכולת היצוא ומיפוי run IDs, ולא ה־SHA של Pages.

Bundle SHA-256 המתועד בנחיתה וב־`reports/cp3b/space_wasm_bundle.json` הוא `b046c69b899bb9d5a2b2f9aeb3e5b3eebfdda820a419137ef5cdf8b8ac8f7c3d` — 805 קבצים. **לא בוצע כאן אימות מחדש של כל 805 הקבצים**; האימות העצמאי כיסה index, card, claims, קבצים שנצרכו באתחולים הציבוריים וחישוב זהות המודל בדמו. אין להציג את hash החבילה ההיסטורי כ־hash שחושב מחדש מהשירות בביקורת זו.

ראיות: [identity.json](../../.local/artifacts/postdeploy-independent-2026-09-29/identity.json), [deployment status](../../.local/artifacts/postdeploy-independent-2026-09-29/deploy-status.json), [MLflow mirror](../../.local/artifacts/postdeploy-independent-2026-09-29/mlflow-mirror.json).

## 3. אימות מדעי, מספרי וחוצה משטחים

### 3.1 מה חושב מחדש

קריאה עצמאית של CSV/JSON, ללא שימוש בפונקציות rederive לצורך בדיקת התא, אימתה **9,025 רשומות מקור ו־32 Git blob hashes**, ללא אי־התאמה. חישוב נפרד ב־Decimal חזר על נרמול חמש התקופות במשקל שווה, מרחקי הכותרת, יחס ההפרשים ורווחי הסמך, טווחי MAE וספירת החלופות. בדיקות המימוש וה־negative controls נוספו לכך, ולא החליפו זאת.

| טענה | מקור ותוצאה עצמאית | הכרעה |
|---|---|---|
| v3: ‏14% / 17% מתחת ל־daily LEAR | `weather-ablation/metrics.csv`: ‏−13.9934247% / −16.7095223%; עיגול תקין | PASS |
| v2: ‏2% / 4% מתחת ל־daily LEAR | אותם score rows: ‏−2.0885597% / −3.5933291% | PASS |
| v3 מול v2: ‏−12% [−16%,−9%] | הפרש score חלקי score של v2: ‏−12.158809%; interval ‏[−15.618709%,−8.854735%] | PASS |
| v3 מול v2: ‏−14% [−17%,−11%] | ‏−13.605068%; interval ‏[−16.944416%,−10.639067%] | PASS |
| מרווחי ציונים, v3−v2 | ‏−0.07831150099532369 ו־−0.08381129930970188; שני רווחי הסמך מתחת לאפס | PASS |
| MAE של v3 | רגיל 5.2539–15.6403; crisis ‏48.0354 → **5.3–15.6; 48.0 EUR/MWh** | PASS |
| MAE של naive | רגיל 8.6331–30.5034; crisis ‏86.9489 → **8.6–30.5; 86.9** | PASS |
| משבר 2022 אינו ניצחון נקודתי נפרד מובהק | `uncertainty.csv`, fold 3: ‏−3.1782 [−6.0898,+0.036877] EUR/MWh; הקצה החיובי מוצג ‏+0.037 | PASS |
| v2 מול pooled control | קצה MAE חיובי `3.857628092332211e-06`, מוצג ‏+0.0000039, מלא בטבלה; אין joint preference ואין טענת equivalence | PASS |
| אוכלוסיית ההשוואה | כל שבע השורות: **10,747 שעות / 448 ימים**, עד 2026-04-07; ללא ערבוב holdout של v1 | PASS מספרי; חסר במסלול הגלוי, F04 |
| חלופות שנבדקו מול אותו כלל | A1–A5 + V2-H + V2-P + HG = **8**; H0 הוא V2-H; רק HG עומד בשני היעדים | PASS |
| מניין לפי מועד החלטה | חמש זרועות המחקר מקבלות N=5, שתי זרועות v2 מקבלות N=7, v3 מקבל N=8. בדיקות שינוי סדר/השחתת מניין עוברות | PASS |

השבע בגרף וה־8 בכותרת **אינם אותו מניין**: הגרף מציג השוואה משותפת הכוללת references; ה־8 מונה זהויות שנבחנו מול אותו כלל, עד ההחלטה. ניסויי calibration קודמים אינם אוטומטית חלופות באותו כלל. זה נכון מחקרית, אך ההבחנה אינה מספיק ברורה לקורא — המלצה A02.

ראיות: [חישוב עצמאי](../../.local/artifacts/postdeploy-independent-2026-09-29/numbers-independent.json), [כל רשומות המקור](../../.local/artifacts/postdeploy-independent-2026-09-29/all-records.json), `src/delu_forecast/derived.py`, `registry.py`, `research.py`, claim maps תחת `docs/track-b/research-content/`.

### 3.2 משמעות, מגבלות וגרסאות

- v3 הוא v2 בתוספת רוח ב־10/100 מטר וקרינה, כולל missing indicators. אין טענה שהניסוי בודד תרומת כל רכיב. השיפור הוא evidence לאחר selection; אין הסקה אוטומטית למידע חדש או qualification מוצרי.
- v2 הוא blend של שני מודלי LEAR עם intervals לפי שעה. אין הוכחה שהרכיב השעתי לבדו גורם לשיפור; הבקרה ומרווח הסמך שמסתיים מעט מעל אפס נשמרים.
- v1 הוא המודל המשוחרר בדמו; הנתון 1.052 בהשוואה אינו סותר “28.58% worse”: הראשון הוא יחס שגיאות במשקל שווה לתקופות מול median של naive לאחר שכבת residual משותפת; השני pooling של ימים מול naive המקורי. ה־holdout הוא חלון ואומדן אחרים. ההסבר קיים, אך מאחורי disclosure.
- ל־v1 נשמרו הכישלון ההתפתחותי, p=0.948, statistic +1.6228, coverage ‏0.194 בשיא אוגוסט 2022 ומנגנון הכשל, crossing counts, ארבעת ה־cutoffs, ‏152 ימי staleness, ו־“confirmatory-style, not power-qualified”. הארכיון נותר השכבה ההיסטורית; אין להחיל עליו רטרואקטיבית את precision החדש.
- ה־holdout MAE ‏25.9 מול 27.8 ו־pinball ‏6.7 מול 13.9 מופיעים בנפרד. ה־p-value מתואר כניסוי על daily pinball, לא כראיה על MAE. על מסלול הקריאה החדש הוא `p < 10⁻⁶`.
- Planned אינו scored, אינו מקבל מספר דור, ואינו מוצג כיכולת זמינה. GFS attribution ומגבלות המקורות נמצאים במשטחים המתאימים. בקרת cutoff בקוד אינה מוצגת כאימות היסטורי של כל vintage.
- שמות וסטטוסים בין האתר, README, כרטיס HF ויצוא MLflow תואמים. הפרסום הגיע ל־final עם שישה routes וללא `data-unpublished`.

### 3.3 הבדיקה המקומית שנכשלה — אינה כשל שירות

הריצה הממוקדת של tests 29,30,35–42 נתנה **349 passed, 1 failed**. הכישלון הוא `test_the_browser_claim_file_is_current_when_present`: `app/public/claims.json` המקומי הוא cache ישן בשבעה שדות טקסט. לא בניתי אותו מחדש ולא שיניתי אותו.

הורדתי בנפרד את `public/claims.json` הציבורי של HF: שבעת השדות הציבוריים תואמים את המחולל הנוכחי. ההבדל היחיד מול הפקה מקומית חדשה הוא `champion_dir_bytes`, מדידת חבילת build; אין כאן פער בטענות המחקריות או בתיקוני הטקסט. לכן **אין להסיק מה־pytest המקומי שהדמו הציבורי ישן**. `verify_release.py` ו־publication guard עברו. לא בוצע full suite חדש בשתי גרסאות Python או rebuild, בהתאם לגבולות בדיקת קריאה בלבד; אין כאן PASS גורף ל־CI מחדש.

[פלט בדיקות](../../.local/artifacts/postdeploy-independent-2026-09-29/targeted-tests.log), [השוואת claims ציבורית/מקומית](../../.local/artifacts/postdeploy-independent-2026-09-29/claims-parity.json).

## 4. דפדפנים, גרפים, נגישות, קישורים ודמו

### 4.1 הדוח הציבורי

הבדיקה רצה על כתובת HTTPS של Pages. עטיפת כלי הבדיקה בתוך `.local/` שינתה **רק בזיכרון** את המרת `Path(...).as_uri()` כך שתקבל URL; `scripts/check_reader_paths.py` לא נערך. כך נמנע שימוש שגוי ב־`file://` כראיה לשירות.

| מנוע / רוחב | תוצאה |
|---|---|
| Google Chrome 153.0.8010.54: ‏1440×900, ‏768×1024, ‏390×844, ‏360×780, ‏320×640 | ללא overflow; גרפים ללא חיתוך/התנגשויות טקסט; בקשת favicon חוזרת ב־404 בכל חמש הריצות |
| Playwright WebKit 26.6: אותם חמישה גדלים | ללא overflow, שגיאות console או failed requests |
| iPhone 15 מדומה ב־WebKit | נבדק בנוסף לחמשת הרוחבים; ללא overflow או כשל בקשות |
| עצי נגישות של הדוח, שני מנועים × desktop/phone | charts נקובים בשם; disclosure expanded state; אין control ללא שם |
| מקלדת | 61 תחנות בשני המנועים, סדר מסמך, focus גלוי; Enter פותח disclosure; anchor אל replay פותח ארכיון |
| Touch בדוח | 100 targets ברוחב 390; אפס מתחת ל־44px לפי המדידה |
| Contrast בדוח | בכל מנוע: 2,382/2,376 פריטי טקסט ו־550/528 פריטים לא־טקסטואליים ב־1440/390; אפס מתחת לסף הרלוונטי |
| 200% / reflow | נבדקו CSS viewports שקולים ל־1440/1280 ב־200%, ו־320px, עם disclosures סגורים ופתוחים; אפס overflow. לא בוצע שימוש בתפריט zoom של דפדפן פיזי |

בכל אחד מ־11 ה־views נמדדו ארבעה charts כאשר הפרטים סגורים ועשרה כאשר פתוחים. טקסט מינימלי בגרפים המחקריים: 12.38px במחשב, 14.58px ב־390, ‏13.26px ב־360, ‏12.21px ב־320. בדיקת צילום משלימה כללה גם preview, replay, פקדי replay ופתיחה/סגירה של תמונות הארכיון. בדקתי חזותית את משפחות הגרפים: overview, השוואות v2, הפרש v3, per-fold, משבר, שעות היום, coverage/width, preview ו־replay. אין טענה שעברתי ידנית על כל פיקסל בכל צילום.

הסקאלות מציינות יחידות וכיוון; ההפרשים אינם מוצגים כציונים; CI מובחן מ־prediction interval; אפס וקצוות אינם מוסתרים; scales לפי fold מסומנים ככאלה. תיקון endpoints ‏7.5/4.5 נשמר. שמות, צורות וקווים מחזיקים משמעות גם ללא צבע; המספרים אינם תלויי hover. צילום הגרפים המבודדים הזיז את ה־header ל־static **לצורך crop בלבד**; צילומי הקורא החדש ומדידות placement השאירו את ה־header כפי שהמוצר מגיש אותו.

**מיקומים עם כל הפרטים סגורים, pixels מגבול המסמך:**

| פריט | Chrome | WebKit | סף v1 | תוצאה |
|---|---:|---:|---:|---|
| סוף headline, ‏1440×900 | 774.6 | 775.3 | 900 | PASS |
| סוף headline, ‏390×844 | 604.6 | 604.7 | 844 | PASS |
| סוף משפט ההשוואה, desktop | 1765.6 | 1767.0 | 1800 | PASS |
| סוף משפט ההשוואה, phone | 2488.5 | 2490.1 | 2532 | PASS |

הבדיקה האוטומטית הכוללת לדוח חזרה `passed:false` בגלל ה־404 של Chrome. אין להסתירו תחת התוצאות החזותיות התקינות.

[מדידות מלאות](../../.local/artifacts/postdeploy-independent-2026-09-29/public-release.json), [ראיית רשת Chrome](../../.local/artifacts/postdeploy-independent-2026-09-29/network-chrome.json), [מדידות כל הגרפים](../../.local/artifacts/postdeploy-independent-2026-09-29/charts.json).

### 4.2 הדמו הציבורי

| מנוע / גודל | Cold start לתחזית | 80→95 ותרחיש עומס | שגיאות ordinary load |
|---|---:|---|---|
| Chrome ‏1440×900 | 21.7 שניות | שניהם משנים view | 0 |
| Chrome ‏390×844 | 20.8 שניות | שניהם משנים view | 0 |
| WebKit ‏1440×900 | 21.8 שניות | שניהם משנים view | 0 |
| WebKit ‏390×844 | 21.3 שניות | שניהם משנים view | 0 |

כל ריצה בהקשר חדש ללא cookies/cache. הדמו מציג 54 ימים, 11,628 ערכי quantile ו־maximum deviation ‏0.0 מול fixture המודל הקפוא. זה אימות זהות חישוב על fixture, לא הערכה מחקרית חדשה ולא עדות לחיזוי עתידי.

Loading/failure/retry נבדקו על **ה־URL הציבורי** בשני המנועים, באמצעות חסימת נכסים/הזרקת מצב כשל/שעון בדיקה בצד הלקוח בלבד: חסימת asset מציגה failure, retry חוזר ל־ready; runtime failure מציג failure; runtime תלוי נשאר loading בדקה הראשונה ועובר ל־failure לאחר deadline. הכשלים המוזרקים אינם תקלות של השירות. אזהרות `Task was destroyed` בסגירת route שהושאר תלוי הן של harness ההזרקה, ולא console error של המוצר.

בדיקת נגישות נוספת לדמו מצאה slider וכפתור תפריט ללא שם נגיש — F01. PASS של נגישות הדוח אינו חל על הדמו. בדיקות touch/contrast המלאות של הדוח גם אינן ראיה שכל widget של marimo עומד בהן; אין בדוח טענת WCAG conformance לכל מעטפת צד שלישי.

[Cold starts](../../.local/artifacts/postdeploy-independent-2026-09-29/demo.json), [מצבי כשל ו־retry](../../.local/artifacts/postdeploy-independent-2026-09-29/demo-states.json), [פקדים ושמות נגישים](../../.local/artifacts/postdeploy-independent-2026-09-29/demo-accessibility.json), [עץ Chrome native](../../.local/artifacts/postdeploy-independent-2026-09-29/demo-full-ax-chrome.json), [WebKit native menu/chart](../../.local/artifacts/postdeploy-independent-2026-09-29/demo-native-webkit.json).

### 4.3 קישורים ו־MLflow

- 35 כתובות HTTP מפורשות מהתוכן הציבורי עברו; 20 קישורים יחסיים נוספים ב־README/card נבדקו. 19 עברו ישירות; הנתיב העברי של מסמך השאלות דרש percent-encoding לפני קריאת HTTP (הניסיון המתוקן החזיר HTTP 200 ומתועד בנפרד). כשל UnicodeEncodeError בניסיון הראשון הוא מגבלת harness, לא תשובת שירות. אין internal fragment של Pages המפנה ל־ID חסר. ספירות אלה הן קבוצות בדיקה, לא דרישת מספר קישורים קבועה.
- ששת מסלולי MLflow עברו REST, ולאחר מכן **12 בדיקות route×engine** בהקשרים אנונימיים. שמות הריצות, run IDs וה־experiment הנכונים הופיעו, ללא login redirect.
- מעבר להופעת שמות, בוצעו **10 בדיקות נפרדות של גרף שהשלים טעינה** בחמש ההשוואות ובשני המנועים. בכל אחת נוצר plot של Plotly, ללא HTTP error. צילום מוקדם עם skeleton נשמר; הוא אינו משמש ראיית הצלחה לגרף.
- ה־overview הציבורי נפתח כברירת מחדל ב־parallel coordinates עם `fold_mean_width95_eur`, `anchor_version`, `history_window`, `interval_method`, לרבות “unknown”. הוא מציג את הריצות הנכונות, אך אינו מביא את הקורא ישר לשני ציוני ההישג; A04.
- ה־HTML, README ו־MLflow אינם סותרים את מצב “v3 research / v1 released”. labels של ראיות audit מציינים type ו־freeze date; דיווחים ישנים עם “pending” נגישים כראיות קפואות, ולא כסטטוס נוכחי.

[קישורים מפורשים](../../.local/artifacts/postdeploy-independent-2026-09-29/public-links.json), [קישורים יחסיים ועוגנים](../../.local/artifacts/postdeploy-independent-2026-09-29/relative-links.json), [תיקון URL encoding](../../.local/artifacts/postdeploy-independent-2026-09-29/relative-links-encoding-retry.json), [routes בדפדפנים](../../.local/artifacts/postdeploy-independent-2026-09-29/mlflow-browser.json), [גרפים טעונים](../../.local/artifacts/postdeploy-independent-2026-09-29/mlflow-settled.json).

## 5. בדיקת קורא חדש — סוכן עצמאי

סוכן `/root/fresh_reader`, עם `fork_turns=none`, לא קרא מסמכים, קוד, metadata או ביקורות. הותרו רק רשימת קובצי הצילום ושימוש ב־view_image. הוא קרא screenshots בסדר: desktop Chrome ‏1440×900, ולאחריו phone WebKit ‏390×844, כל disclosures סגורים. אותו קורא ראה את desktop לפני phone; לכן קריאת הטלפון אינה replicate עיוור בלתי־תלוי נוסף. הוא עדיין הסוכן הנפרד וחסר ההיסטוריה ש־§11 דורש.

| שאלה קבועה | תשובת הקורא והמסך המספק אותה | השוואה לתקן/ראיות |
|---|---|---|
| 1. What is the headline result, with its numbers? | v3 השיג 14% ו־17% מתחת ל־daily LEAR, עבר שני יעדי 10%, הראשון מבין 8. מסך 1 בשני הגדלים. לא ידע איזה אחוז שייך לאיזה score | התשובה המספרית נכונה; אי־השיוך מובנה בנוסח §3.4, V2-01 |
| 2. Against what? | daily LEAR בכותרת; naive הוא normalizer; v2 הוא comparator לשינוי הדור. הגדרה מלאה של daily LEAR במסך desktop 2 / phone 1 | תואם; אינו מערבב normalizer עם comparator |
| 3. How sure are we, and on what class of evidence? | Development/post-selection, לא מבחן על מידע חדש. change מול v2: ‏−12% [−16%,−9%] נקודתי ו־−14% [−17%,−11%] interval. המשפט השלם מופיע desktop 3 / phone 4; caveat של משבר וייחוס weather בהמשך | תוכן נכון; קריאה רציפה מאוחרת מסיסמת “2/3 מסכים”, למרות PASS למגבלות pixels המפורשות. A01/V2-02, לא FAIL רטרואקטיבי |
| 4. What does the demo run, and why not the best model? | v1 LightGBM המשוחרר, historical replay; החלפה רק במודל סופי אחרי one-shot test ו־live run. desktop 1 / phone 2 | תואם registry/release rule |
| 5. What was tried and dropped? | Calibration experiment ו־model comparison study; recalibration לא הספיק, אף מדיניות במחקר לא עמדה ביעדים, והוא הוביל ל־blend. desktop 2 / phone 3; variants מדויקים מוסתרים | שני הענפים וההחלטות הובנו נכון. לא נטען שהקורא ידע לזהות את כל שמונת policies |
| 6. What would you ask the candidate? | כיצד selection על 8 policies יטופל במבחן הסופי; איזה weather input גורם לשיפור; משקל ראיות המשבר; כיצד אומתה זמינות מקורות היסטוריים; מה המועמד ביצע ובדק בעצמו לעומת AI | advisory בלבד; שאלות טובות לריאיון, לא הפרות ולא טענות שהפרויקט כבר ענה עליהן |

**הכרעת cold-reader לפי v1:** תשובות 1–5 תואמות ברמת התוכן; ה־headline במקומו והגבולות המספריים המפורשים עוברים. אין בסיס הוגן להחליף עכשיו את 1800/2532 בסף חדש ולפסול לפיו. עם זאת, אין לרשום שהקורא ראה את *מלוא* ההשוואה במסכי 2/3: הוא לא. זו סתירה תפעולית בין שפת התקן למימוש המדידה, והיא ההצדקה המצומצמת ל־V2-02.

## 6. א — הפרות התקן הקיים

### F01 — P1: לדמו יש controls ללא שם נגיש

**סעיף:** v1 §10, “no control is unnamed”; תחולת התקן על ה־Space והדמו בפתיחה; plan §7.12.

**תצפית וראיה:** בדמו הציבורי ברוחב 390, עץ Chrome native מחזיר `role=slider, name=""` ו־`role=button, name=""`. למחוון העומס יש טקסט חזותי בסמוך אך אין accessible name. כפתור שלוש הנקודות נושא SVG עם `aria-hidden`, ללא aria-label. ב־WebKit, snapshots של הפקדים מאשרים `- slider` ו־`- button` ללא שם; קריאה נוספת ב־WebKit inspector native מאשרת את כפתור התפריט ללא שם. בדיקת ה־native ב־WebKit אינה חוצה shadow roots ולכן אינה ראיה native למחוון עצמו. ה־radio buttons, לעומתם, נקובים כ־50%,80%,95%. ראה `demo-accessibility.json`, `demo-full-ax-chrome.json` וצילומי `demo-controls-*`.

**השפעה:** מי שמנווט באמצעות מידע נגיש אינו מקבל את מטרת הפעולה המרכזית שמשנה את תחזית התרחיש. זה כשל שימושיות, גם כשהמודל עולה ומחשב נכון. הכפתור גם קטן — כ־30.8×25.2px לעומת היעד של כ־44px; אין להסיק מגודל knob לבדו את מלוא hit area של slider.

**תיקון:** במחולל הדמו/מעטפת widgets, לחבר את label של תרחיש העומס אל slider באמצעות מנגנון naming נתמך; לתת לתפריט שם שימושי. להגדיל hit area של התפריט ולבדוק את שאר targets של הדמו, כולל shadow DOM. אין צורך בשינוי החישוב או התקן.

**קבלה:** שתי הרצות cold ציבוריות, Chrome/WebKit, מציגות שם ומשמעות למחוון ולתפריט במידע הנגיש של המנוע; radio names נשמרים; keyboard מפעיל אותם עם focus גלוי; target מתאים; שתי פעולות הדמו ממשיכות לשנות תחזית והזהות נשארת bitwise identical. בדיקה של הדוח בלבד אינה סוגרת את הממצא.

### F02 — P2: האתר הציבורי יוצר בקשת favicon שחוזרת 404

**סעיף:** v1 §10 “No failed requests”; §14 ושימור plan §6 invariant 1 — zero runtime network calls מעבר למסמך.

**תצפית וראיה:** Chrome מבקש `https://hrsi56.github.io/favicon.ico`; console מציג HTTP 404, וה־Resource Timing מציג את הכתובת. הכשל חזר בכל חמשת רוחבי Chrome ובריצה עצמאית נוספת. אין failed event של Playwright משום ש־HTTP 404 הוא response, לא transport failure; זה אינו מבטל את התצפית. WebKit לא ביקש אותו. `network-chrome.json` מתעד את כתובת console המדויקת.

**השפעה:** הפרה קטנה אך ממשית של חוזה offline/no-additional-requests ושל שער הבקשות. הכלי המקומי שסופר references חיצוניים החמיץ בקשת דפדפן אוטומטית. התוכן והתחזיות אינם נפגעים.

**תיקון:** להגדיר favicon inline באמצעות `data:` במחולל העמוד, ולכלול בדיקת public origin בהליך release. אין לתקן באמצעות התעלמות משגיאת console או whitelist ל־404.

**קבלה:** fresh context בשני המנועים, אותם widths: לאחר טעינה ושהייה אין resources נוספים לא־מורשים, אין favicon 404 ואין console error. מדידת bytes וה־offline test ממשיכים לעבור.

### F03 — P2: זמן האתחול והפרטים על המדידה מוסתרים

**סעיף:** plan §7.11, הדרישה שנותרה בתוקף: לצד demo action נמצאים download size, זמן מדוד עם מכשיר/דפדפן/תאריך ותאריך אימות אחרון. v1 §15 לא ביטל סעיף זה.

**תצפית וראיה:** לצד הכפתור כתוב רק “First visit downloads about 57 MB; startup time varies”. `20.4 seconds in Chrome 153 on a Mac, measured 2026-09-24` נמצא **בתוך** disclosure הסגור “What the demo does and startup details”. תאריך last verified נפרד אינו גלוי ליד הפעולה. ראיות: desktop screen 1 וההבדל בין `reading-path.txt` ל־`full-text.txt`.

**השפעה:** הקורא אינו מקבל את אומדן זמן ההמתנה לפני יציאה לדמו, למרות שזו היתה דרישת ההצגה המאושרת. זו אינה תלונה על מהירות נוכחית: הריצות כאן אכן נמשכו כ־21 שניות.

**תיקון:** להציג לצד הפעולה משפט קצר ומבוסס release record עם זמן, סביבה ותאריך; לשמור את ההסבר הטכני הארוך ב־disclosure. אין להעתיק את זמני ביקורת זו כערובה לכל מכשיר.

**קבלה:** כשהפרטים סגורים, שני המנועים ב־1440/390 מראים את כל הנתונים ליד הפעולה, והטקסט תואם רשומת מדידה. אחרי תוספת הטקסט יש למדוד מחדש את §1 — המרווח לפסקת ההשוואה דק.

### F04 — P2: 448 ימים אינם נכללים ב־fairness note הגלוי

**סעיף:** plan §7.9: החלק הגלוי ליד overview כולל “10,747 hours over 448 days; equal-fold scoring; development status”. דרישה זו לא תוקנה ב־v1 §15.

**תצפית וראיה:** `comparison.sub` מציג שבע מדיניות, 10,747 שעות, חמש תקופות ומשקל שווה, אך **אינו מציג 448 ימים**. החיפוש במסלול הקריאה הסגור אינו מוצא 448; המספר מופיע בהסבר מוסתר על ציוני v1. קוד המקור: `src/delu_forecast/research_claims.py`, block `comparison.sub`; CSV ציבורי/מחויב מאשר 448 לכל שורה.

**השפעה:** יחידת הדגימה הרלוונטית לאי־ודאות היומית חסרה בתמצית ההשוואה, אף שהמספר הכולל של שעות מוצג. הנתון אינו שגוי; מיקומו אינו תואם את הדרישה.

**תיקון:** להוסיף binding למניין הימים לצד מניין השעות, בלי hard-code.

**קבלה:** ב־overview הסגור מופיע “10,747 hours over 448 days” או נוסח שקול, נגזר מאותו record; אין ערבוב בין represented days ל־calendar span; בדיקות binding ו־§1 נשארות תקינות.

## 7. ב — המלצות לשיפור המוצר שאינן הפרות

| ID / עדיפות | תצפית והשפעה על Lead DS / מנהל פיתוח | פעולה ישימה ובדיקת תועלת |
|---|---|---|
| A01 / גבוהה | המדידה עוברת, אך המשפט המלא מגיע ב־desktop screen 3 וב־phone screen 4. ההיררכיה נותנת ל־title, release rule ו־lineage יותר מקום מאשר לתוצאה עם אי־ודאות | לצמצם whitespace/פתיחה בלי להקטין טקסט או להסתיר caveat; לשמור על הסדר המאושר. קורא חדש יראה את ההשוואה המלאה מוקדם יותר. שינוי נוסחת הסף מחייב V2-02 |
| A02 / גבוהה | 7 שורות בגרף מול 8 חלופות, והיעדר שיוך 14/17 למדדים, מקשים על קליטה מהירה | להסביר את ההבדל בין comparison set ל־tested policies במשפט אחד; לצרף שמות החלופות ב־detail. תיקון הכותרת עצמה רק לאחר אישור V2-01 |
| A03 / בינונית | README ארוך מאוד; limitations ורקע v1 חוזרים בפסקאות ובבולטים, וכוללים קודי פרוטוקול. שם ה־About הציבורי כולל “v6.8”, שאינו דור המודל | לצמצם את המסלול הטקסטואלי שמחוץ ל־generated top ולהפנות לעומק. לשמר statements מחייבים וארכיון. Owner יכול לעדכן About לתיאור מוצר שאינו נראה כמספר דור; אין המלצה לנקות root בניגוד ל־§8 |
| A04 / בינונית | “Compare … in MLflow” מוביל למסך עמוס בקודי פרמטרים וב־width של fold, לא לשני scores שמניעים את הסיפור | אם השירות תומך בקישור אמיתי לתצוגת scores/intervals, לבדוק ולפרסם אותו; אחרת לתייג הקישור כטבלת ריצות ולהוסיף הנחיה קצרה. אין להבטיח URL state שהשירות אינו משמר |
| A05 / בינונית | הפער בין 1.052, ‏28.58% ו־holdout win ניתן להסבר אך דורש disclosure. גם “same blend” מול הבדל point score בבקרה מעורר שאלה | משפט הסבר קצר בהקשר: aggregation/reference שונים; median מושפע משכבת interval. אין לשנות את המספרים כדי ליישב חזותית |
| A06 / בינונית | הדמו עשיר בפרוזת מגבלות, בעוד הראיה החזקה — חישוב fixture חי, deviation ‏0.0 — נראית אחרי הגרף. “ceteris-paribus”, A65, CQR ו־isotonic נשארים ז׳רגון | להסביר את בקרת העומס בעברית־מחשבתית אך בטקסט אנגלי פשוט: “Change load only; other inputs stay fixed”. לשמור caveat מהותי ולהעביר מנגנונים לעומק. לבחון אם identity summary קומפקטי ליד הגרף עוזר |
| A07 / בינונית | אותה מגבלת development חוזרת במספר שכבות. חלק מהחזרה נכפה ב־badge, headline definitions ו־chapter grammar | לערוך חזרות שאינן מוסיפות מידע, בלי להסיר qualification ליד תוצאה. לא לסווג כל חזרה כהפרת §1 כשהתקן עצמו מחייב חזרה במיקום אחר |
| A08 / נמוכה | stack line ארוך אך מבוסס; הצהרת contribution מסבירה אחריות יותר מאשר דוגמה קונקרטית להחלטה אישית | להשאיר stack בעומק. להכין תשובה לריאיון על החלטה אחת, כישלון אחד ובדיקת leakage אחת. נוסח contribution ושם הבעלים אינם סמכות עריכה של הבודק |

העמוד מצליח להראות מוצר, שיפור, comparator, uncertainty, כישלון v1 ותוכנית המשך. הבעיה העיקרית אינה מחסור בראיות אלא הגעה איטית לתמצית והעברת יותר מדי עבודת פענוח לקורא. אין המלצה להחליף את גרפי ההפרשים באינפוגרפיקה דקורטיבית או למחוק כישלונות.

## 8. ג — הצעות ממוקדות לתקן v2, לא קריטריוני פסילה עכשיו

### V2-01 — לשייך את מספרי הכותרת למדדים

**הבעיה המוכחת:** הקורא החדש בשני layouts לא ידע במסך הראשון איזה מדד מקבל 14% ואיזה 17%. אותה תופעה תועדה אצל שני קוראים קודמים, A-PRES1-9.

**מדוע v1 אינו מספיק:** §3.4 קובע ממש את המשפט העמום. המחולל מקיים אותו; שינוי עצמאי בנוסח יהיה דווקא סטייה מהטקסט המחייב.

**נוסח מוצע לאישור הבעלים, החלפת הסוגריים בלבד:**

> (v3: 14% on the point-error score and 17% on the interval score; the first of 8 policies tested to meet them).

לכל דור: כאשר headline נושא כמה quantities, כל quantity יצמיד את שם המדד. יתר sentence/badge, formula, rule, N ו־evidence class נשארים כפי שנקבעו.

**בדיקה:** קורא חדש רואה רק את המסך הראשון ומחזיר שיוך נכון של שני המספרים; parity זהה ב־README; חישוב זהה ו־§1 placements עוברים.

**עלות תחזוקה:** נמוכה — template אחד, fixture/claim-map ועדכון checks של headline; מדידת layout בכל שינוי headline כבר נדרשת. אין metadata חדש או metric חדש.

### V2-02 — להגדיר “שני/שלושה מסכים” לפי תוכן שניתן לראות עם header

**הבעיה המוכחת:** screenshot step הוא height פחות header. ב־desktop ה־header הוא 56px, ולכן שני הצילומים מגיעים עד y=1744, אך סוף finding הוא 1765.6–1767. בטלפון שלושה צילומים מגיעים עד y=2420, אך סוף finding הוא 2488.5–2490.1. הבדיקה מכריזה PASS כי משווה ל־1800/2532; הקורא זקוק לצילום נוסף. גם הרשומה הקודמת הודתה ב־desktop 2–3 / phone 4 וסימנה “within placement”.

**מדוע v1 אינו מספיק:** הוא מצמיד תיאור במסכים למספרי document pixels בלי להגדיר כיצד header והצילום הרציף משתתפים במדידה. שניהם אינם אותה בדיקה.

**נוסח מוצע:**

> For the orientation finding, use the same closed-disclosure, header-preserving scroll sequence as the cold-reader packet. With viewport height H and measured sticky-header occlusion h, the complete finding must be visible by screen N: its bottom must be at or above H + (N−1)×(H−h), and none of its lines may be hidden by fixed content. N is 2 on desktop and 3 on phone. Record both the document coordinates and the screen containing the last line.

**בדיקה:** screenshot packet וה־placement assertion משתמשים באותה פונקציית offsets; negative control עם finding שחוצה בשורה אחת את המסך האחרון חייב להיכשל. אין צורך למדוד זמן קריאה סובייקטיבי.

**עלות תחזוקה:** נמוכה–בינונית — שינוי פונקציית המדידה וה־acceptance, שני controls וחידוש cold read כשמשתנה layout. אין device חדש. נדרשת בדיקה בעת שינוי header; פעולה זו ממילא משפיעה על focus/anchors.

**לא מוצע כלל חדש עבור** favicon, שם נגיש, פרטי startup או מניין ימים: v1 כבר מספיק. שם נגיש במרימו וסריקת בקשות public origin הם תיקון מוצר/כלי בדיקה. אין להוסיף תקן מחמיר יותר לכל שכבת GitHub/HF שאינה בשליטת הפרויקט בלי צורך מוכח ותחולה מוגדרת.

## 9. מטריצת עמידה בסעיפים

PASS כאן מתייחס להיקף שנבדק, לא לאישור כל פעולה היסטורית מחדש. HIST = בדיקת מסמך/ראיה היסטורית, שאינה תצפית שירות חדשה. N/A = טריגר עתידי שלא הופעל.

| סעיף v1 | מצב | ראיה / חריג |
|---|---|---|
| §1 Audience, headline/orientation/journey | PASS עם advisory | headline, definition, release rule, byline ומגבלות pixels תקינים; cold-reader pacing A01 |
| §2 Evidence classes | PASS | development מול v1 holdout נפרדים; replay לא live |
| §3.1–3.4 Scores/comparator/derived/headline | PASS | חישוב עצמאי, N=8, exact headline ו־README parity; V2-01 אינו הפרה |
| §3.5 Branches/population | PASS | rejected branches אינם דור; population נשמר |
| §3.6 One-shot/live headline | N/A | אין final-candidate או live חדש; v1 מוגן בנוסחו |
| §4 Numbers/words/lint | PASS בהיקף reading path | rounding, positive endpoint, p floor, bindings, negative controls; archive/deep אינם נאכפים כאילו הם reading path |
| §5 Registry/status/comparability | PASS | alias H0=V2-H, slots/status tokens, population; MLflow תואם |
| §6 Architecture/grammar/scale | PASS | order, chapter evidence אחרי decision, branches, size 1.561MB; v5 trigger לא חל |
| §7 Evidence tiers | PASS | labels type/frozen date, target classification, 55 artifact hashes; no misleading current-status link נמצא |
| §8 Surfaces/parity/limitations | PASS תוכן | public bytes וכרטיס; MLflow source of truth; נגישות הדמו נבחנת ב־§10 |
| §9 Completeness | PASS | final build, routes6, guard, no placeholder |
| §10 Devices/accessibility/requests | **FAIL** | F01 בדמו; F02 ב־Pages; יתר בדיקות הדוח כמפורט §4 |
| §11 Gates/cold reader/independent check | **FAIL לשער release הנוכחי** | §10 אינו נקי; cold reader תוכני תקין עם פער תפעולי מתועד; pytest cache local failure אינו מוסתר |
| §12 Packet/runbook/order/postdeploy | PASS מסמכי / HIST לתהליך | runbook+packet וקשר symbols נבדקו; נחיתה/העלאה לפי הרשומה; אין ביצוע פרסום בביקורת זו |
| §13 Governance | PASS | hash מאושר, דוח חדש בלבד, אין שינוי core או יומן |
| §14 Carryover | **FAIL חלקי** | plan §7.9 ו־§7.11 לא בוטלו: F03/F04; invariant1: F02 |
| §15 Amendments | PASS | החלת התיקונים; לא נפסל מחמת Safari אמיתי, precision ישן או locate-only gate |
| §16 Applicability / §17 decisions | PASS | deferred triggers הופרדו; החלטות בעלים לא פורשו כהיתר לביקורת לפרסם |

### 9.1 כל invariants 1–26 של התוכנית, כפי שתוקנו

| # | מצב | בסיס |
|---|---|---|
| 1 | **FAIL** | favicon ציבורי, F02 |
| 2 | PASS תוכן ציבורי | מקור claims יחיד; cache מקומי ישן מתועד בנפרד |
| 3 | PASS | outputs generated; לא נערכו בביקורת |
| 4 | PASS | honesty statements וארכיון v1 נשמרו |
| 5 | PASS לפי scope המתוקן | מגבלות לכל מודל במשטח המציג אותו |
| 6 | PASS | קישורי tracking משתמשים ב־`.mlflow` |
| 7 | PASS בבדיקה סטטית | מחסום `live_` קיים; לא נכתב/נבדק deployment Live חדש |
| 8 | PASS | attribution/licensing, כולל GFS במשטחים המתאימים |
| 9 | PASS לפי §4 | positive endpoint ו־W1–W21; אין significance/equivalence claim בלתי־מותר |
| 10 | PASS | גבול 2026-04-07 למחקר; replay ההיסטורי של v1 הוא החריג המאושר |
| 11 | PASS | labels development, NOT_DEMONSTRATED בעומק, אי־equivalence, economics descriptive |
| 12 | PASS | תוכן מוצר באנגלית; דוח הביקורת בעברית לבעלים |
| 13 | HIST / unchanged in this review | dependencies לא נערכו; בדיקת זהות היסטורית בפסק הדין הסופי |
| 14 | PASS | לא נמצא retired governance tooling במסלול המוצר |
| 15 | PASS | metric/unit/aggregation/comparator/class; צירים יחידה אחת |
| 16 | PASS | no placeholder/final guard |
| 17 | PASS | 9,025 מקור, derived arithmetic, binding tests |
| 18 | PASS | ownership markers ו־generated README |
| 19 | PASS | REST+12 route checks+10 settled plots חדשים |
| 20 | HIST | הוראה מפורשת ואישור delegated מתועדים בנחיתה; אין אישור חדש בביקורת |
| 21 | PASS | לא נצרך research budget |
| 22 | PASS לגרפי הדוח | צורות/קווים/labels וערכים גלויים; לא תלוי צבע או hover |
| 23 | PASS | variants נפרדים וגדלי טקסט מדודים |
| 24 | PASS ראיית output/test | ארכיון נשמר; לא שוכתב כאן |
| 25 | PASS | public failure/loading/retry, בשני מנועים, בהזרקה מקומית |
| 26 | PASS | planned unscored/unversioned |

### 9.2 קבלת W1–W16 של הבריף

| פריטים | מצב בביקורת זו |
|---|---|
| W1 | PASS hashes והחלטות |
| W2 | PASS registry/alias/surface; test41 מאמת historical identity-only export diff לפי החלטת הבעלים |
| W3 | PASS חישוב עצמאי ומניין date-based |
| W4 | PASS exact headline וגבולות v1 המספריים |
| W5 | PASS architecture/grammar/archive/size |
| W6–W7 | PASS lint/display/status tests; אין שינוי template בביקורת |
| W8–W9 | PASS evidence labels, README/card, public parity |
| W10 | PASS final/guard/routes |
| W11 | PASS mirror, 12 routes ו־10 settled charts ציבוריים |
| W12 | PASS cold starts/assets שנצרכו; bundle hash מלא נשען על הרשומה ולא הוכח מחדש ל־805 קבצים |
| W13–W15 | PASS stack, contract tests, runbook/packet/advisory log קיימים ונבדקו |
| W16 | HIST | proposals ב־return ובפסק הדין הסופי; לא מתירים שינוי template או v4 כאן |

עמידה ברוב W אינה מבטלת הפרות של סעיפים שנשארו בתוקף.

## 10. השוואה לביקורות הקודמות — לאחר הממצאים העצמאיים

| ראיה קודמת | ממצא אז | מצב שנצפה עכשיו |
|---|---|---|
| independent-check-1 | מספרי מחקר מוקלדים במחולל, חסר direction ב־C5, בדיקת non-text חסרה | הראיות וה־bindings עוברים; C5 אומר lower is better; non-text נמדד ועובר |
| independent-check-2 | קצוות axis ‏7.5/4.5 הוצגו 8/4 | תוקן ונראה בצילומי הגרפים הציבוריים |
| checks 1–2 / F11 | Safari/iPhone/VoiceOver אמיתיים חסרים | אינו open blocker: דרישה זו תוקנה במפורש ב־v1 §10 ובהחלטת הבעלים |
| independent-check-3 | N תלוי CSV order; evidence לפני decision | תוקן: N=5/7/8, negative controls; evidence אחרי החלטה. אין הישנות |
| independent-check-4/5 | PASS על checks מקומיים, source/static zero-fetch, §10 | אינם מוכיחים שאין בקשת favicon ציבורית. F02 הוא פער כיסוי של origin אמיתי. בדיקות נגישות הדוח אינן מוכיחות naming של widgets בדמו — F01 |
| final editorial audit F03/F07 | כפילות ועומס בדמו/README | חלו שיפורים, אך החיכוך חוזר: A03/A06/A07. אין להפוך משאלת קיצור כללית לסף חדש |
| advisory A-PRES1-4 | finding קרוב לגבול pixel | ההישנות נמדדה בדיוק. נוסף אימות קורא חדש שמראה screen3/4; V2-02 |
| A-PRES1-9 | 14/17 ללא שיוך מדד | חזר אצל קורא עצמאי חדש; V2-01 מוצדק |
| A-PRES1-10/11/13 | 7 מול8, ציוני v1 נראים סותרים, pooled control משנה point score | עדיין קיימים וניתנים להסבר; A02/A05. לא numeric error |
| A-PRES1-7/8/12/15 | קודים ב־MLflow, “champion”, שמות וטרמינולוגיה | עדיין חיכוך בעומק; אינו אסור שם לפי §1/§4. ה־overview של MLflow מוסיף עומס בפרמטרים שאינם מסבירים הישג |
| A-PRES1-17 | “no additional runtime requests” סומן כאמת על הדוח | הדפדפן הציבורי חושף חריג favicon. ההערה הקודמת אינה סוגרת F02 |
| pres-1-landing F8 | 429 transient בדמו וב־MLflow, retries הצליחו | ארבע cold starts ו־12 routes בביקורת הנוכחית הצליחו; אין ראיה כאן לתקלה מתמשכת. ההיסטוריה נשארת ולא נמחקה |

לא נמצא רישום שסוגר במפורש את דרישת **448 ימים גלויים** או **פרטי זמן startup ליד הפעולה** באמצעות תיקון מאושר לתקן/תוכנית. PASS קודם אינו תיקון לדרישה שלא בוטלה. יומן ההמלצות לא שונה; ההמלצות החדשות נכתבות כאן בלבד בהתאם לסמכות הביקורת.

## 11. צילומי מסך מייצגים וחומרי עזר

אלה צילומים חדשים של שירותים ציבוריים. לא תצלומים שהופקו מקובץ מקומי.

**Pages, פתיחה במחשב — headline, released/research, פרטי startup סגורים:**

![Public Pages desktop opening](/Users/djourno/Downloads/PJM/.local/artifacts/postdeploy-independent-2026-09-29/screens/cold-reader/chrome-1440x900/screen-01.png)

**Pages, מסך הטלפון השלישי — רק תחילת משפט ההשוואה נכנסת בתחתית:**

![Public Pages phone screen 3](/Users/djourno/Downloads/PJM/.local/artifacts/postdeploy-independent-2026-09-29/screens/cold-reader/webkit-390x844/screen-03.png)

**דמו ציבורי פעיל — controls, תחזית והפרדת replay:**

![Public demo ready](/Users/djourno/Downloads/PJM/.local/artifacts/postdeploy-independent-2026-09-29/chrome-demo-ready.png)

**MLflow ציבורי לאחר טעינת הגרף — זהויות נכונות, תצוגת ברירת מחדל עמוסה:**

![Public MLflow settled overview](/Users/djourno/Downloads/PJM/.local/artifacts/postdeploy-independent-2026-09-29/mlflow-settled/compare-overview-chrome.png)

צילומים נוספים: [README top הציבורי](../../.local/artifacts/postdeploy-independent-2026-09-29/github-at-a-glance.png), [דמו בטלפון](../../.local/artifacts/postdeploy-independent-2026-09-29/webkit-demo-chart.png), [כרטיס HF](../../.local/artifacts/postdeploy-independent-2026-09-29/hf-card.png), [משבר עם CI שחוצה אפס](../../.local/artifacts/postdeploy-independent-2026-09-29/charts/1440/open/v3-c2b.png), [endpoints מתוקנים בנייד](../../.local/artifacts/postdeploy-independent-2026-09-29/charts/390/open/v3-c3.png).

הצילומים וה־JSON נמצאים ב־`.local/` המתעלם מ־Git; דוח זה כולל את הממצאים, המדידות, הזהויות והתוצאות המהותיות כדי שלא יהיו רק בקובץ זמני. יש לשמור את תיקיית העזר לצד הדוח לצורך ביקורת חזותית. אין כאן שינוי לראיות PRES-1 ההיסטוריות.

## 12. מגבלות הבדיקה ופעולות המשך

- לא נעשה שימוש ב־Safari אמיתי, iPhone אמיתי או screen reader; זו מגבלה מפורשת, **לא הפרה** לפי התקן שאושר. WebKit הוא Playwright; iPhone הוא emulation.
- אין אימות זמינות מתמשכת: אלו קריאות בזמן נתון. בדיקות MLflow הן anonymous read-only; לא הופעלו training, registry mutation או upload.
- הבדיקה המלאה של report §10 אינה audit מלא לכל chrome של GitHub/HF/MLflow או לכל shadow-root control ב־marimo. ה־unnamed controls בדמו מאומתים, אך אין טענת WCAG certification לשירות כולו.
- ה־200% נבדק בפריסת CSS שקולה, לא בתפריט native zoom. לא אומתה כל חבילת HF בקובץ־לקובץ מחדש. בדיקות historical ordering/authority אינן יכולות לשחזר פעולת בעלים בעבר; הן מבוססות על ראיות מתועדות שנבדקו.
- שאילתת כלי web החזירה תוצאת GitHub מיושנת וטעויות גישה לחלק מהכתובות. היא לא שימשה להכרעת המוצר: ה־HTTP והדפדפנים המקומיים הגיעו לשירותים ואומתו עצמאית. אין לייחס לשירות מגבלת crawler.
- פלט test ראשוני השתמש בשם קובץ בדיקה שגוי ותוקן; scripts עצמאיים תוקנו בזמן בניית harness. אלה טעויות כלי הביקורת, לא כשלי המוצר. התוצאות הסופיות המפורטות לעיל אינן מסתירות את כישלון cache המקומי שנשאר.

**סדר תיקון ישים:**

1. לתקן F01 במקור הדמו ואת F02 במחולל Pages; להוסיף checks שמגיעים לשירות הציבורי ולפקדי shadow DOM הרלוונטיים.
2. להשיב את דרישות התוכנית שנותרו בתוקף: startup details ליד action (F03), ו־448 ימים ב־fairness note (F04). להשתמש ב־records/bindings הקיימים.
3. ליצור מועמד חדש לפי סמכות שיינתן למבצע התיקון; לבנות את המשטחים הנגזרים, לבדוק parity/identity ומיקומים. **אין לערוך פלט שנוצר ביד ואין לשכתב ראיות היסטוריות.**
4. לאחר פרסום מורשה בלבד: לחזור על fresh public cold starts, controls/names, network, widths, links/MLflow ו־byte identity; להפיק דוח recheck חדש. כל FAIL כאן צריך תצפית קבלה מפורשת.
5. במקביל, להכין לבעלים הצעת v2 של V2-01/V2-02 בלבד. אם נדחית, לתקן את ארבע ההפרות לפי v1 ולהשאיר את המלצות המוצר כהמלצות. אין תלות הכרחית בין תיקון הפרות קיימות לאישור v2.

**מסירה:** דוח זה נשאר untracked לעיון הבעלים. לא נפתחו branches/worktrees/tags. הצעת הודעת commit לבעלים, אם יבחר לשמור אותו: `Document independent post-deployment PRES-1 review and public evidence`. אין לבצע commit מכוח הדוח.


בדיקת מסירה אחרונה:

```text
git branch --show-current: main
git rev-parse HEAD: 01e394d475202bb44a226f2ac5403aa084dc5b4c
git status --porcelain=v1:
?? docs/track-b/publication-postdeploy-independent-review-2026-09-29.md

git diff --stat: empty (the new report is untracked)
git diff --cached: empty
```

הקובץ היחיד שנוסף מחוץ ל־`.local/` הוא דוח זה, לצורך הביקורת המבוקשת. [ה־diff המלא לעיון](../../.local/artifacts/postdeploy-independent-2026-09-29/review-full.diff) מציג את תוכנו כקובץ חדש, בלי staging. חומרי העזר שנשמרו הם כ־40 MB של תמונות, תשובות ציבוריות, מדידות וסקריפטים לשחזור; לא נפתחו משאבי Git. אין למחוק אותם לפני עיון בצילומים.
