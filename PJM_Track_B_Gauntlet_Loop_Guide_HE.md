# יישום Gauntlet Loop על פרויקט ה־DE-LU Capstone — Track B

גרסה קנונית: 3.2
תאריך: 4 באוגוסט 2026
מקור השיטה: Matt Shumer, [How to Run a Gauntlet Loop](https://somethingbig.ai/gauntlet-loop)
תחום המסמך: Track B בלבד — ה־Capstone ההנדסי של חיזוי מחירי Day-Ahead באזור DE-LU
מצב חוזה: חבילת v6.4 / map v6 / חוזי התפקיד והתבניות כוללים את הקשחת provenance/Git ואת פרוטוקול CP-2 label-blind four-catalog מ־4 באוגוסט; operational validation ממתין לריצה מאושרת. M1 טרם התחיל ו־CP-1 עדיין ממתין לבריף מה־Orchestrator

---

## תקציר מנהלים

המערך הנכון אינו Orchestrator חדש בתוך Track B ואינו מערכת YAML שמנסה לנהל מחדש את כל התוכנית.

ה־Orchestrator הקיים נשאר אחראי על שלושת המסלולים A/B/C ועל ההחלטה **מתי** לפתוח כל checkpoint. כאשר הוא פותח B-Claude block, אתה מעביר פעם אחת את ה־brief ל־Engineering Lead של Track B. מאותו רגע Track B עובד באופן עצמאי: ה־Lead מאמת את מצב ה־repository, בוחר בעצמו כיצד לפרק את העבודה, מפעיל Builders ו־Critics בעלי הקשר נפרד, מעביר ביניהם verdicts, מריץ תיקונים וחוזר על הלולאה. בסיום ה־checkpoint הוא מבצע ביקורת אינטגרציה, עוצר ומחזיר packet יחיד ל־Orchestrator באמצעותך.

הזרימה היא:

```text
Orchestrator
   │ מחליט מתי Track B נפתח ומנסח brief
   ▼
Yarden — העברה ידנית אחת
   ▼
Track B Engineering Lead
   ├─ בוחר decomposition
   ├─ Builder → artifact
   ├─ fresh Critic → verdict
   ├─ FAIL → Builder מתקן → Critic חדש
   ├─ PASS → הרכיב נסגר
   └─ Integration Critic בסוף ה-checkpoint
   ▼
Checkpoint Return Packet + עצירה מוחלטת
   ▼
Yarden — העברה ידנית אחת
   ▼
Orchestrator מחליט מה קורה עכשיו בין A/B/C
```

המסמך המקורי של הפרויקט כבר מכיל חלק גדול מרף האיכות: CP-1–CP-5, baselines, latency targets, invariant tests, strict-gate schema, coverage criteria ו־stranger test. לכן אין צורך להמציא framework חדש. צריך להוסיף את החלק שחסר: **מבקר עצמאי שבודק את התוצר הממשי, ולא את ההסבר של מי שבנה אותו, ולולאת תיקון שנמשכת כל עוד קיים פער משמעותי.**

היישום שאושר ונכתב ב־2 באוגוסט 2026:

1. `capstone_V6_4.md` כולל forward audit window, תיקון ניסוח ה־KFT, experiment lineage ו־CQR rank fixture.
2. `engineering-role.md` כולל חוזה Gauntlet אוטונומי בתוך checkpoint מאושר; `orchestrator-role.md` כולל את חוזה הצד השני.
3. לאפשר ל־Lead לבחור את הפירוק בזמן אמת; לא לקבע מראש 26 לולאות או שישה workstreams מחייבים. ה־Lead הוא Git writer יחיד; Builders מקבילים מבודדים ואינם מבצעים פעולת Git כותבת.
4. לקבוע **חמישה** component-level critic surfaces חובה כאשר הם רלוונטיים, ולבצע fresh Integration Critic בכל checkpoint.
5. להשתמש ב־`workbench.md` זמני וקצר בלבד, לא ב־state machine מקביל; הוא אינו עובר ל־Orchestrator ונמחק/מוקפא בסיום.
6. בסוף כל checkpoint להחזיר packet יחיד, לעצור, ולאפשר ל־Orchestrator לשאול את ירדן במפורש אם לפתוח את השלב הבא.
7. לשמור ראיות חיות תחת `.gauntlet/evidence/<checkpoint>/` המוחרג מ־Git; לכל Critic יש `<critic-run-id>/` ייחודי ובלתי משתנה שמכיל בדיוק manifest מכני ו־verdict מובנה.
8. לחייב שכל component PASS שעליו נשען PASS טרמינלי ייבדק מחדש מול אותו final SHA/tree בדיוק, ולשמר כל SHA מצוטט באמצעות ref מקומי שאינו מתפרסם.
9. ב־CP-2 לחייב **label-blind four-catalog review**: Critic מחשב ומקפיא metrics אנונימיים `A/B/C/D` בלי לבחור winner; reveal מותר רק אחרי schema-valid `PASS` מוקפא; Integration חדש מפעיל את §4.1 על הזהויות ומאמת את ה־winner המקובע.

---

# חלק א׳ — ביקורת בונה על המערך הנוכחי

## 1. תחום הבדיקה ומצב הפרויקט

נבדקו חומרי Track B והחלקים הרלוונטיים לניהולו:

- `capstone_V6_4.md` וה־amendment מ־v6.3;
- `engineering-role.md`;
- `README.md`;
- `docs/spike-feed-status.md`;
- `progress.md`, רק סעיפי Track B והחלטות scope רלוונטיות;
- `program-stage-sequence.md`, רק routing ו־checkpoint timing של Track B;
- `AGENTS.md` ו־`CLAUDE.md`;
- `pyproject.toml`, קוד ה־spike וה־git state.

ענפי הלמידה והשיווק לא נותחו כתוכניות בפני עצמן. הם רלוונטיים למסמך זה רק כדי לכבד את גבול הסמכות: ה־Orchestrator מנהל את שלושת המסלולים, ו־Track B אינו רשאי לקבוע לעצמו מתי הוא מתחיל checkpoint חדש.

מצב ה־repository שנמצא והמצב לאחר יישום מסמך זה:

- ה־spike branch כבר נמצא בהיסטוריה של `main`.
- M0 סגור; M1/CP-1 הוא ה־build milestone הבא כאשר ה־Orchestrator יפתח אותו.
- הקוד הקיים הוא code spike ולא M1 pipeline.
- קבצי Python עוברים compilation.
- כבר קיימים governance/protocol helper tests ב־`tests/test_gauntlet_protocol.py`, אך עדיין אין M1 product/invariant tests, CI workflow, ingestion pipeline מלא, DuckDB mart, modeling pipeline או deployed artifact—תואם לכך ש־M1 טרם התחיל.
- לפני התיקון `AGENTS.md` ו־`CLAUDE.md` שכפלו הקשר רחב מדי. כעת `AGENTS.md` הוא router קצר וקנוני ו־`CLAUDE.md` הוא pointer בלבד.
- חבילת התיעוד/ממשל של v6.4 נשמרת כחבילת Git אטומית וניתנת לשחזור; אין בה קוד מוצר של M1. האימות התפעולי הראשון נשאר בתוך CP-1 המאושר.

## 2. מה נעשה טוב במיוחד

### 2.1 המטרה, הקהל והגבולות ברורים

הפרויקט מגדיר תוצר חד: תחזית הסתברותית ל־DE-LU D+1 בשעת day-ahead gate, עם quantiles ו־intervals מכוילים. הוא גם יודע מה אינו בונה: אין trading layer, neural model race, multi-day forecast, scheduled retraining או MLOps תעשייתי מדומה.

זה בסיס טוב ל־Gauntlet משום שה־Lead יכול לבחור את הדרך בלי לשנות את היעד.

### 2.2 strict-gate design הוא נכס מרכזי

v6.4 נושא קדימה את החלטת v6.3: הוא אוסר delivery-day A69 וכל actual column ב־champion runtime, מגביל A75 ל־proper-training fit target ומפריד schema של champion מ־post-gate benchmark. ההחלטה נולדה מראיות spike ולא מנרטיב נוח.

זהו Gauntlet ברמת התוכנית: בדיקה חשפה פער, והתכנון השתנה כך שלא ניתן לעקוף אותו באמצעות disclosure בלבד.

### 2.3 ה־M0 spike הוא דוגמה טובה לגילוי unknown errors

ה־spike מצא בפועל:

- publication timing בעייתי ל־A69;
- PT15M היסטורי בפידים;
- partial hourly bins בגבולות query;
- archive ו־reconciliation behavior;
- מגבלת SFTP בסביבת sandbox.

לכן האבחנה הנכונה אינה שלפרויקט אין מנגנון לגילוי טעויות בלתי צפויות. המנגנון קיים ופעל. החולשה המדויקת יותר היא:

> עד היום הביקורת העצמאית פעלה בעיקר על התוכנית ועל spikes. החל מ־M1 צריך להפנות אותה אל artifacts אמיתיים: data, code, predictions, tests, plots והיישום הרץ.

### 2.4 ה־pre-registration של ארבעת הקטלוגים חזק

ארבעת הקטלוגים, retention rule, stability condition, coverage guardrail ו־tie breakers מוגדרים מראש. גם "אף proxy לא שרד" הוא outcome תקין. זה מצמצם p-hacking ומונע שימוש ב־SHAP כ־feature-selection theater.

### 2.5 ה־invariant tests מכוונים לכשלים מסוכנים

הם בודקים:

- quantile monotonicity;
- rolling leakage;
- UTC/DST lags;
- PT15M aggregation ו־complete bins;
- champion/benchmark schema ו־fit lineage.

אלה bars אמיתיים שה־Critic יכול להריץ. הם טובים יותר ממדדי test coverage קוסמטיים.

### 2.6 קיימת תרבות של תוצאות שליליות לגיטימיות

הפרויקט מוכן לדווח על proxy שלא שרד, coverage divergence, feature שאינו headline וחולשה של strict-gate model מול post-gate benchmark. זו התנהגות מדעית טובה ויש לשמור עליה.

## 3. הטעויות או החוסרים החשובים

### 3.1 selection/evaluation contamination ב־M2

אותם five folds משמשים לבחירת feature catalog ול־hyperparameter work, ולאחר מכן Fold 5 או pooled folds משמשים ל־DM gate. לכן ה־p-value הוא post-selection ואינו confirmatory נקי.

הפתרון המועדף הוא forward audit window:

- selection מתבצע על snapshot cutoff קפוא;
- כל data לאחר cutoff מוסגר ואינו נבדק במהלך catalog selection או tuning;
- champion, catalog ו־hyperparameters מוקפאים לפני פתיחת audit data;
- ה־DM על חמשת ה־folds הקיימים מסווג כ־descriptive post-selection evidence;
- confirmatory DM רץ פעם אחת על forward window כאשר קיים sample size שנקבע מראש.

יש לקבע מראש גם minimum duration או minimum number of delivery days. אם עד M3 אין מספיק observations, אין להכריח p-value חסר כוח להיות gate; ה־confirmatory result יכול להיסגר מאוחר יותר בהתאם ל־amendment המאושר.

### 3.2 ניסוח ה־KFT של A65/A01 חזק מהראיה

ה־spike ראה load forecast ב־15:35 D-1. זה תואם את חובת הפרסום הרגולטורית, אבל אינו מוכיח empirically שהנתון היה זמין לפני gate של 12:00.

ב־M1 יש לבצע captures בכמה delivery days בחלון שלפני gate, לדוגמה 10:30–11:45 לפי שעון השוק, ולשמור ledger. עד אז יש להבחין בטקסט בין:

- regulatory pre-gate availability;
- observed presence at 15:35.

### 3.3 דרישת "לפחות חמישה experiments" ניתנת למשחק

מספר runs אינו quality bar. יש להחליף אותו ב־lineage:

- hypothesis;
- parent run;
- change made;
- fixed budget;
- result;
- keep/reject decision.

### 3.4 לפני התיקון, ה־Builder יכול היה לסגור את עבודתו בעצמו

לפני התיקון, `engineering-role.md` אפשר ל־Lead לתכנן, לבצע, לנהל debugging ולדווח אילו CP items נסגרו. ניתן היה להפעיל review subagent, אך לא הייתה חובה שמבקר נפרד יאשר את ה־artifact. הפער נסגר כעת באמצעות Critic עצמאי ו־Integration Critic טרי כתנאי ל־PASS.

זהו הפער העיקרי מול המאמר: Builder ו־Critic צריכים להיות סוכנים נפרדים, וה־Critic צריך לקבל fresh context ולבדוק את התוצר הממשי.

### 3.5 CP checklists הם bars, אבל אינם loops

ה־CP מתארים את סוף השלב, אך לא קובעים כיצד failure חוזר ל־Builder, כיצד נשמר verdict או כיצד ממשיכים כל עוד reference/bar עדיין מנצח.

הפתרון אינו להוסיף עשרות checklists חדשים. הפתרון הוא לתת ל־Lead חוזה עבודה קצר של split → build → judge → repeat.

### 3.6 אין עדיין product acceptance harness

כלי ה־Gauntlet/provenance קיימים כעת, אך אין עדיין tests/CI/golden fixtures של מוצר M1. לכן בתחילת M1 יש להקים את ה־product harness שכבר נדרש על ידי v6.4. זו sequencing correction, לא scope חדש.

### 3.7 לפני התיקון, README תיאר בעיקר יעד עתידי

הפער נסגר: נוסף Current Status המבדיל בין:

- M0/spike שכבר קיימים;
- M1–M5 המתוכננים;
- commands שניתנים להרצה היום.

### 3.8 הקשר ה־root היה רחב וסותר את גבול Track B

לפני התיקון, bootstrap documents ברמת ה־root חשפו ל־Engineering Lead פרטי Orchestrator ושלושת המסלולים ואף שכפלו זה את זה. זה יצר שתי תקלות: סוכן הנדסי יכול היה לבחור לעצמו מה “השלב הבא”, ושינוי הוראה במקום אחד היה עלול לסטות מהעותק השני.

התיקון שבוצע הוא router יחיד ב־`AGENTS.md`: הוא מזהה אם ההקשר הוא Orchestrator, Engineering Lead, subagent מוגבל או תחזוקת role. `CLAUDE.md` מפנה אליו בלבד. Engineering Lead קורא בזמן ביצוע רק את ה־brief, `engineering-role.md` ותוכנית הקאפסטון המדויקת שה־brief מציין; הוא אינו קורא `progress.md`, את הסילבוס או מסלולי A/C.

### 3.9 הקשחת provenance ו־Git שנדרשה לאחר הביקורת

ביקורת חוזית נוספת חשפה שבעה פערים תפעוליים שלא שינו את הרף המדעי, אך כן יכלו להפוך ראיה תקינה לכאורה לבלתי ניתנת לאימות:

- helper הבידוד הוכיח checkout נקי אך לא היה מוגדר כיצרן של manifest מתמשך; כעת manifest מכני של create/verify ו־Critic verdict הם records נפרדים, ושניהם נדרשים;
- “stale verdict” לא היה כלל מכני בטוח; כעת אין reuse סלקטיבי: כל component PASS שעליו נשען terminal PASS חייב להצביע ל־final candidate SHA/tree המדויק, וכל commit חדש מבטל את כולם;
- SHA שהיה קיים רק על ענף disposable יכול היה להפוך ל־unreachable; כעת ה־Lead יוצר לכל review, לפני פתיחתו, ref מקומי בלתי ניתן לדריסה תחת `refs/gauntlet-evidence/<checkpoint>/<run-id>/<piece>` שמצביע ל־candidate `HEAD`, וה־verdict נקשר אליו; לפני terminal return כל ref מצוטט מאומת מחדש;
- לא הוגדר בית לראיות החיות; כעת הוא `.gauntlet/evidence/<checkpoint>/`, מחוץ לכל worktree של Builder/Critic ומחוץ ל־candidate Git tree, עם run directory ייחודי לכל Critic ו־`_support/<run-id>/` ייחודי לכל הקבצים שעליהם ה־verdict מצביע;
- מיקום פיזי לא הוכיח בעלות בלעדית על inode; כעת כל קובץ artifact/input/stdout/stderr/evidence ב־support root חייב גם `st_nlink == 1`, כך ש־hard link אינו יכול “לשאול” inode מ־run או נתיב אחר;
- הפניית bar בפרוזה לא הוכיחה שה־Critic שפט את הטקסט המקובע; כעת `plan.filename` הוא נתיב `.md` בטוח ויחסי לריפו, `plan.sha256` קושר את ה־blob המקובע ב־candidate, `plan.version` ו־`plan.bar_citation` מזהים אותו לאדם, ו־`plan.bar_excerpt` חייב להיות ציטוט מילולי שמוכח כמופיע באותו blob;
- Builders מקבילים יכלו להתחרות על branch/index משותף; כעת ה־Lead הוא Git writer יחיד, כל Builder עובד ב־worktree/snapshot מבודד וב־allowlist נפרד, וה־Lead משלב ומקבע serially.

הבחירה לא לשמור live verdicts תחת `docs/track-b/evidence/` מכוונת: verdict נוצר אחרי שקיבעו candidate. קיבוע verdict בתוך אותו candidate היה משנה את ה־SHA ומבטל את הביקורת שהוא אמור להוכיח.

## 4. מה לא צריך לפתוח מחדש

המלצות Gauntlet אינן הרשאה לבטל החלטות ratified:

- SFTP נשאר fallback בלבד, ורק אם ה־API נכשל בפועל.
- החלטת SMARD gas נשארת סגורה ללא ראיה חדשה.
- אין להוסיף WIS; mean pinball על תשעת quantiles יחד עם coverage ו־interval width כבר מספקים את המידע הדרוש.
- אין להחזיר neural challenger, trading layer, DVC, live ingestion או AWS לפני ההחלטה המתוזמנת.
- אין להוריד spectral EDA, marimo, static-first page או offline health report באמצעות מסמך זה. הקטנת bar של checkpoint דורשת תחילה amendment של הקאפסטון/criterion שאושר בידי owner, anchor מדויק חדש, ורק אז brief חלופי מה־Orchestrator; היא אינה נובעת אוטומטית מהמאמר.

## 5. העלות והגבול

המדריך הקודם הציע מערכת רחבה מדי: custom agents רבים, skill, YAML state machine, evidence hierarchy ו־Critic כמעט לכל רכיב. זו הייתה הצעה שאינה מתומחרת ועלולה להפוך לפרויקט שני.

הגרסה שאושרה מגבילה את התוספת לעתודת תכנון מפורשת:

| תוספת | הערכת מאמץ |
|---|---:|
| CP-1 — ingest, PIT evidence ושלושת משטחי הביקורת הראשונים | 6 שעות Gauntlet reserve |
| CP-2 — lineage ו־mandatory label-blind four-catalog review | 5 שעות |
| CP-3 — CQR fixture/real-fold calibration critic | 5 שעות |
| CP-4 — registry/artifact integration | 3 שעות |
| CP-5 — cross-surface/deployment integration | 3 שעות |

העתודה היא **22 שעות בדיוק**, בתוך הטווח שנבחן 18–24; מעטפת התוכנית עולה מכ־705 לכ־727 שעות. זו הערכת עומס לתכנון, לא סכום agent-hours. בעת פתיחת checkpoint ה־Orchestrator מחבר את העתודה להקצאת ה־milestone וכותב ב־brief תקרת active elapsed wall-clock כוללת שמכסה orientation, בנייה, ביקורת, תיקונים, אינטגרציה ו־Return Packet. שעון UTC יחיד רץ מתחילת ה־checkpoint עד terminal return; הקשרים מקבילים חופפים ואינם נסכמים. רק ה־Orchestrator רשאי להרחיב את התקרה.

## 5.1 מה בהתנגדות ה־Orchestrator היה נכון, ומה השתנה בהחלטה הסופית

ההתנגדות הייתה נכונה בחמישה נושאים מהותיים, וכולם נשמרו:

1. אין להקים Orchestrator שני או state machine מקביל בתוך Track B.
2. ה־Orchestrator אינו מנסח tasks ל־subagents; הוא מנסח outcome/checkpoint brief יחיד ל־Engineering Lead.
3. אין להחליף את ה־capstone checklist בגרסה שהמדריך ממציא מחדש.
4. Track B אינו קובע לעצמו מתי להתחיל ואינו מתקדם אוטומטית לאחר PASS.
5. הכנת החוזה אינה הרשאה להתחיל M1, לקרוא את תוכנית ה־companion מוקדם או לשנות את מסלולי A/C.

הנקודה שנשקלה מחדש היא **מועד כתיבת התיעוד**. כל עוד לא הייתה הרשאת owner, היה נכון להסתפק בהמלצה. לאחר שניתנה הרשאה מלאה, כתיבת v6.4 עכשיו עדיפה על השארת החלטות קריטיות כפתקים לעתיד—ובלבד שמצב הביצוע נשאר M1 not started. לכן “לעשות הכול עכשיו” פירושו כאן להשלים את חבילת הממשל, הראיות והתבניות; הוא אינו פירושו להריץ את הקאפסטון לפני ה־gate.

---

# חלק ב׳ — קריאה מדויקת של שיטת Gauntlet Loop

## 6. שבעת העקרונות שמחייבים את ההתאמה

### 6.1 להשתמש ב־agentic harness אמיתי

המערכת צריכה להיות מסוגלת לפתוח קבצים, לשנות code, להריץ tests, לבדוק artifacts ולהפעיל subagents. Codex או Claude Code מתאימים; chat רגיל שאינו יכול לבדוק את התוצר אינו מספיק.

### 6.2 לתת מטרה ורף, לא implementation plan חדש

ה־Orchestrator brief צריך לומר:

- איזה checkpoint נפתח;
- מה צריך להיות נכון בסופו;
- אילו constraints ו־CP criteria מחייבים;
- איזה reference או measurement הוא ה־bar;
- מהו קובץ ה־capstone המדויק והמאושר;
- מהי תקרת ה־active elapsed wall-clock המספרית הכוללת ל־checkpoint.

הוא אינו צריך לכתוב ל־Engineering Lead את פירוק ה־modules, סדר הקבצים או מספר הסוכנים.

`capstone_V6_4.md` מכיל החלטות מתודולוגיות ratified ולכן הן constraints אמיתיים, לא micromanagement. Templates עתידיים אינם מקודדים version: כל brief מעתיק את ה־anchor המדויק מ־`progress.md`. בתוך הגבולות האלה ה־Lead בוחר את הדרך.

### 6.3 להשתמש ברף קונקרטי

בפרויקט הזה bars יכולים להיות:

- invariant test;
- golden/adversarial fixture;
- latency target;
- ENTSO-E↔SMARD reconciliation;
- baseline predictions;
- frozen metric implementation;
- coverage/width requirements;
- running app;
- rendered static page;
- technical/non-technical stranger test;
- reference implementation לחישוב סטטיסטי קטן.

"נראה טוב", "production-ready" או "ה־Builder אומר שהבדיקות עברו" אינם bars.

### 6.4 ה־Lead בוחר את הפירוק

זו נקודה שבה המדריך הקודם סטה מהמאמר. הוא קיבע מראש M1-G1…M1-G6 ועשרות loops. המאמר אומר שה־Lead צריך לבחור את החלקים הקטנים ביותר שניתן לשפר ולשפוט בנפרד.

לכן ה־brief אינו מכתיב decomposition. התוכנית קובעת חמישה surfaces בסיכון גבוה שדורשים Critic עצמאי כאשר הם מופיעים:

- temporal normalization;
- champion/benchmark schema firewall;
- A75 climatology fit lineage;
- CP-2 label-blind four-catalog metric recomputation ו־freeze-before-reveal chain;
- ב־M3, חישוב CQR threshold על ה־fixture הידני והשוואה ל־persisted calibration predictions.

ה־Lead יכול להוסיף Critic נוסף אם הוא מגלה artifact חשוב בעל failure risk אמיתי, אך אינו מפעיל Critics באופן מכני על כל פונקציה.

### 6.5 Builder אינו מבקר את עצמו

לכל piece חשוב:

1. ה־Lead יוצר Builder worktree/snapshot מבודד ומגדיר allowlist של paths שאינו חופף ל־Builder מקביל.
2. Builder יוצר artifact אך אינו מבצע `git add`, `commit`, `merge`, `checkout`/`switch`, שינוי refs או ניהול worktrees.
3. ה־Lead בודק את התוצאה, מייבא רק את ה־paths המורשים, מאמת את ה־staged path set ומקבע serially על `gauntlet/<checkpoint>`.
4. fresh Critic מקבל goal, bar, relevant rules וה־artifact המקובע.
5. ה־Critic אינו מקבל את היסטוריית ההצדקות של ה־Builder.
6. הוא בודק בפועל code, data, predictions, tests, screenshot או running product.
7. אם העבודה מפסידה ל־bar, הוא מחזיר את הפער המשמעותי ביותר.
8. ה־Lead מעביר את הפער ל־Builder בלי שירדן ישמש שליח.

### 6.5.1 בידוד Critic וראיות הניתנות לביקורת

לפני כל component Critic ה־Lead מקבע את המועמד, מקצה `critic-run-id` ו־`piece` חדשים, מאתחל run root ויוצר `refs/gauntlet-evidence/<checkpoint>/<run-id>/<piece>` בלתי ניתן לדריסה ב־candidate `HEAD` המדויק. רק אז הוא יוצר checkout חדש, נקי ו־detached ב־SHA/tree המלאים מחוץ לכל עץ עבודה של Builder, באמצעות `scripts/gauntlet_critic_snapshot.sh` או מנגנון מחמיר שקול. ה־Critic אינו מקבל uncommitted diff, את שיחת ה־Builder או `workbench.md`.

כל component או Integration review מקבל `<critic-run-id>` ייחודי ובלתי משתנה. מפעילים עבורו:

```text
python3 scripts/gauntlet_protocol.py init-evidence --repo-root <abs> --checkpoint <id> --run-id <critic-run-id>
```

ה־run root שנוצר ב־`.gauntlet/evidence/<checkpoint>/<critic-run-id>/` מכיל בסיום בדיוק שני artifacts:

1. `integrity-manifest.json` שנוצר ומתעדכן מכנית בידי helper הבידוד. רשומת create מקפיאה SHA/tree/path/status/היעדר `workbench.md`; ה־hash שלה מוקפא לפני הביקורת. רשומת verify מקבלת את אותו hash ומסרבת אם create חסרה, שונתה או אינה תואמת, ואז מוכיחה שאותו מצב נשמר אחרי הבדיקה.
2. `critic-verdict.json` נפרד שה־Critic כותב רק לאחר verify ושחייב לעבור את ה־validator הסטנדרטי וה־fail-closed ב־`scripts/gauntlet_protocol.py validate-verdict`; `docs/track-b/schemas/critic-verdict.schema.json` הוא הייצוג הדקלרטיבי הקנוני של אותה סכימה. ה־record נקשר ל־piece/ref, ל־candidate SHA/tree, ל־schema ולכלי ה־candidate המקובעים, ול־manifest הסופי וה־hash שלו, אך ה־Critic אינו רשאי לכתוב או “לתקן” את ה־manifest.

כל verdict record מחייב:

- piece/ref, candidate SHA/tree מלאים, committed schema SHA-256 ו־artifact SHA-256;
- קשירת תוכנית מלאה: `plan.filename` הוא נתיב `.md` בטוח ויחסי לריפו, `plan.sha256` הוא SHA-256 המדויק של תוכן ה־blob המקובע ב־candidate SHA, `plan.version` ו־`plan.bar_citation` הם הזיהויים האנושיים, ו־`plan.bar_excerpt` הוא טקסט לא־ריק ומילולי שמוכח כמופיע באותו blob;
- SHA-256 של data/input מכריעים, או סיבת `N/A` מפורשת;
- פקודות שחזור ו־tolerance צפוי, כולל exit code ו־stdout/stderr paths+hashes;
- לפני ואחרי: אותו `HEAD` ואותו `HEAD^{tree}`, `git diff` ו־cached diff נקיים, `git status --porcelain=v1 --untracked-files=all --ignored=matching` ריק, ואין `workbench.md`;
- כל artifact/input/command stdout/stderr/evidence שמופיע כקובץ ב־verdict נשמר כקובץ רגיל ולא־סימלינקי תחת `_support/<run-id>/` המדויק שלו, עם SHA-256 ועם inode link count של אחד בדיוק (`st_nlink == 1`); verdict, הפער הגדול ביותר ומבחן הקבלה הבא. hard link, inode משותף, נתיב מ־run אחר, snapshot או temp נפסלים, ו־observation פרוזאי ללא hash אינו ראיית החלטה.

תחת initialization lock בלעדי אחד, `init-evidence` יוצר גם את run root וגם את `_support/<run-id>/` ומגלגל לאחור כשל יצירה חלקי רגיל. אף נתיב אינו רשאי להתקיים מראש, להיעשות בו שימוש חוזר או לעבור דרך symlink; אם מתגלה half-pair, הכלי נכשל סגור ואינו משלים או ממחזר אותו. זוהי יצירת זוג עם lock/rollback/fail-closed, לא primitive אטומי לשתי תיקיות. את שני ה־records כותבים ל־run root בלבד. כל artifact/input/cache/output/fixture/log/evidence שמוצהר ב־verdict נשמר תחת support root המדויק ומקיים `st_nlink == 1`; לנתונים restricted או גדולים מדי שומרים manifest בטוח של hashes/lineage במקום raw data. workbench snapshot ו־Return Packet יכולים להישמר ברמת checkpoint root כי אינם ראיית verdict. אין לנקות או לבצע reset לפני בדיקת ה־after-state. שינוי SHA/tree/ref, status שאינו ריק, pre-review-manifest hash mismatch, schema שאינו תקין, plan binding בלתי בטוח/לא תואם, `bar_excerpt` שאינו מופיע ב־blob, או evidence חיצוני/לא־מגובה hash/hard-linked פוסלים את ה־verdict ודורשים checkout, run ID, support root ו־ref חדשים.

לאחר שה־candidate מפסיק להשתנות, כל component PASS שדרוש ל־terminal PASS מורץ מול **אותו final SHA/tree בדיוק**. כל commit חדש—גם אם נראה שאינו נוגע ב־reviewed path—מבטל את כל ה־component PASS הקודמים ודורש להריץ מחדש את כולם. זה מחמיר יותר מ־`reviewed_paths[]`, אך אינו מסתמך על Critic שזכר למנות כל dependency עקיף. ל־Integration Critic נוצר checkout חדש נוסף באותו final SHA/tree.

`create-ref` מופעל לפני כל review ודורש שה־SHA יהיה ה־`HEAD` המדויק של `gauntlet/<checkpoint>`; לכן repair או candidate חדש מקבלים run ID/ref חדשים ולא מזיזים ref קיים. לפני כל terminal return ה־Lead מפעיל `verify-ref` מחדש לכל SHA שמצוטט ב־packet. ה־refs אינם נדחפים לעולם ורק ירדן רשאי להזיז או למחוק אותם. ענף `gauntlet/*` אינו “spent” לפני שכל ה־refs נבדקו.

### 6.5.2 CP-2 — label-blind four-catalog review מחייב

זהו לא Blind A/B גנרי. יש ארבעה קטלוגים סמנטיים קבועים—`strict_base`, `residual_arm`, `scarcity_arm`, `both_arms`—וה־Critic מקבל עותקים אנונימיים `A/B/C/D`. הוא מחשב metrics בלבד. הוא **אינו** מזהה את ה־base, אינו מפעיל eligibility/tie-break, אינו בוחר label ואינו מצהיר מי ה־winner. ההכרעה הזהותית מתרחשת רק אחרי freeze ו־reveal, ב־Integration חדש.

#### חוזה המדדים המדויק

- ה־primary loss הוא mean pinball משוקלל לפי מספר האובסרבציות על **כל השורות, כל חמשת ה־folds וכל תשעת ה־quantiles** `{.025,.05,.10,.25,.50,.75,.90,.95,.975}`; זה אינו mean לא־משוקלל של חמישה fold means.
- coverage גולמי של 80% הוא היחס של `q10 <= y <= q90`, כאשר שני הקצוות inclusive. משתמשים ב־q10/q90 שהוגשו כמו שהם. raw crossing מותר ב־M2 ואסור ל־blind protocol לתקן, לדחות או להפעיל isotonic/CQR; אלה שייכים ל־M3.
- improvement הוא `(L_base-L_arm)/L_base`. אם `L_base=0`, `strict_base` מנצח מייד. תנאי ה־coverage הוא חד־צדדי, `C_strict_base-C_arm <= 0.02`: ירידת coverage של בדיוק 2pp עוברת, וכל coverage גבוה משל ה־base עובר גם הוא. שוויון בדיוק ב־1% וב־2pp עובר; ב־stability נדרש `L_base,f-L_arm,f > 0` בלפחות 4/5 folds—אפס אינו חיובי.
- tie מוגדר כ־`(L_c-L_min)/L_min <= 0.001`; שוויון ב־0.1% עובר. אם `L_min=0`, רק loss ששווה בדיוק לאפס נכנס ל־tie set. מכריעים לפי פחות added features (`1,1,2`), אחר כך `|coverage_80-0.80|`, ולבסוף `residual_arm -> scarcity_arm -> both_arms`.
- כל source CSV זהותי הוא UTF-8/LF עם header מדויק `fold_id,row_id,y,q025,q05,q10,q25,q50,q75,q90,q95,q975` ומיון `(fold_id numeric, row_id UTF-8 byte order)`. הקובץ האנונימי `blind-public-input.csv` מוסיף רק `label` בתחילת ה־header ומסודר בדיוק לפי `(fold_id numeric, row_id UTF-8 byte order, label A->D)`. `row_id` הוא token אטום התואם בדיוק `^r[0-9]{6,}$`, ללא timestamp או זהות קטלוג; כל טבלת lookup של זמן/זהות נשארת במשטח ה־source/preparation הזהותי ומחוץ ל־Blind context. ערכים נקראים כ־`Decimal` עשרוני סופי; NaN/Inf, שורות חסרות/כפולות, decision מ־binary float או מערך שעוגל לתצוגה נפסלים. השוואות המכריעות מבוצעות ב־Decimal/integer cross-products לפני rounding. כל JSON בפרוטוקול, לרבות שני קובצי הזהות המקובעים, נשמר ב־UTF-8 בדיוק עם keys ממוינים, הזחה של שני רווחים, LF ו־newline יחיד בסוף; JSON תקין סמנטית אך לא קנוני ברמת הבתים נפסל. גם הטיפוסים קשיחים: שדה integer חייב להיקרא כ־JSON integer שאינו Boolean, שדה Boolean חייב להיות JSON Boolean, ו־`true`, `1` ו־`1.0` לעולם אינם שקולים.

ה־schema המכני הוא `docs/track-b/schemas/cp2-blind-four-catalog.schema.json`; מעברי המצב היחידים הם `blind-prepare`, `blind-recompute`, `blind-freeze`, `blind-reveal`, `blind-adjudicate` ב־`scripts/gauntlet_protocol.py`.

#### סדר הפעולות ובתי הראיות

1. **Final candidate תחילה.** לפני blind prep ה־candidate כבר מקובע ומכיל את `artifacts/cp2/blind/source-manifest.json`, שקושר את ארבעת ה־IDs לנתיבי/האשי predictions, ואת `artifacts/cp2/blind/selection-declaration.json`, שמצהיר winner אמיתי. שניהם committed ו־blob-hash-bound. ה־Blind Critic אינו מקבל או קורא אותם.
2. **Prepare.** מקצים blind-review ID ו־Blind component run/piece/ref/support בלבד—עדיין לא Integration. מפעילים `python3 scripts/gauntlet_protocol.py blind-prepare --repo-root <ABS_REPO> --candidate-sha <FULL_SHA> --blind-review-id <ID> --component-run-id <RUN>`. הכלי מגריל seed/nonce קריפטוגרפי של 256 ביט ו־permutation חדש. ה־preimage של ה־commitment, המיפוי, הזהויות והקובץ הזהותי שנוצר מכנית `preparation-invocation.json` נשמרים create-only ב־`.gauntlet/evidence/CP-2/_blind-custody/<blind-review-id>/`, כאשר התיקייה `0700` והקבצים `0600`. כל log של harness נשאר Lead-private ומחוץ ל־Blind allowlist. ה־Blind support מכיל רק `blind-public-input.csv` אנונימי ומשולב עם labels `A/B/C/D`, את `blind-public-manifest.json`, `blind-commitment.json` ו־`blind-preparation-receipt.json`—לא command evidence שעלול להדליף source paths/roles. ה־commitment קושר את ה־hash המדויק של `preparation-invocation.json`; לאחר יצירת רשומת ה־custody נוצר ה־receipt הציבורי, שקושר את ה־SHA-256 המדויק של הרשומה בלי לחשוף את תוכנה. ה־256-bit secret מונע brute force טריוויאלי של 24 ה־permutations.
3. **Blind recompute.** fresh Critic מפעיל `python3 scripts/gauntlet_protocol.py blind-recompute --support-root <ABS_BLIND_SUPPORT> --blind-review-id <ID>` רק על public support וקוד/סכמת metric שב־allowlist. `blind-metrics.json`, ה־stdout/stderr הבטוחים וה־verdict נקשרים לאותו component support/run. לפני קבלת verdict, הוולידטור סורק כל filename וכל raw byte stream ב־support—גם bytes שאינם UTF-8 תקין—וכן כל string בכל עומק ב־verdict, ופוסל זהות סמנטית או נתיב identity אסור. ה־Critic עוצר לאחר verify ו־validated PASS/FAIL ואינו מבקש mapping.
4. **Freeze לפני reveal.** רק אחרי schema-valid Blind `PASS` מספקים ל־`blind-freeze` מזהי Integration run/piece חדשים, אך **לא מאתחלים אותם ידנית**. הפקודה `python3 scripts/gauntlet_protocol.py blind-freeze --repo-root <ABS_REPO> --blind-review-id <ID> --component-verdict <ABS_CRITIC_VERDICT> --integration-run-id <RUN> --integration-piece <PIECE>` היא המקצה היחיד: היא מאמתת תחילה את ה־Blind PASS, מסרבת לכל run/support/ref שהוקצו מראש, ורק אז מאתחלת את ה־run/support ויוצרת ref באותו final SHA/tree. אובייקט `blind_component` ב־freeze חייב לשעתק בדיוק את run/piece/ref, נתיב/hash ה־verdict, נתיב/hash ה־integrity manifest וזמן הרשומה של ה־verdict המאומת; קובץ אחר בעל hash תקין אינו תחליף. לאחר מכן היא יוצרת `blind-freeze.json` ואת חמשת העותקים החד־קישוריים שבבעלות Integration: `frozen-blind-public-input.csv`, `frozen-blind-public-manifest.json`, `frozen-blind-commitment.json`, `frozen-blind-preparation-receipt.json` ו־`frozen-blind-metrics.json`. Blind FAIL נשמר אך אינו מקבל reveal ואינו יוצר Integration run; כשל לאחר תחילת freeze משאיר ניסיון חלקי שמור ומחייב IDs חדשים.
5. **Reveal.** מפעילים `python3 scripts/gauntlet_protocol.py blind-reveal --repo-root <ABS_REPO> --blind-review-id <ID> --integration-run-id <RUN>`. הכלי מסרב בלי freeze תקין, מאמת את הסדר `preparation invocation → public manifest → commitment → custody → receipt`, דורש ש־`custody_record_sha256` שב־receipt המוקפא יתאים בדיוק לרשומת המשמורת, ומשווה כל role/נתיב repository/hash של מקור במשמורת גם ל־source manifest המקובע וגם ל־mapping preimage המחויב. לאחר מכן הוא מאמת commitment, קורא אך אינו משנה custody, ומעתיק—**לא hard-link**—ל־Integration support את `blind-reveal.json`, `revealed-mapping.json`, ארבעת קובצי `revealed-source-<semantic-role>.csv`, `revealed-source-manifest.json`, `revealed-selection-declaration.json` ו־`revealed-preparation-record.json`. כל עותק hash-bound ו־`st_nlink == 1`.
6. **Integration adjudication.** fresh Integration Critic מפעיל `python3 scripts/gauntlet_protocol.py blind-adjudicate --integration-support-root <ABS_INTEGRATION_SUPPORT> --blind-review-id <ID>` רק על העותקים שב־Integration support ועל ה־metrics המוקפאים—לא על custody. הוא יוצר `blind-adjudication.json`, מאמת chronology/hashes, מפעיל את כלל §4.1 ודורש שה־winner המכני זהה ל־selection declaration המקובע. ה־adjudication/chain validation נקשר ל־Integration verdict. שני ה־run roots נשארים עם שני הקבצים הקנוניים בלבד.

ב־Blind component verdict, האובייקט `blind_review` חייב לקשור בדיוק את `blind_review_id`, `public_manifest {path, sha256}`, `commitment {path, sha256}`, `preparation_receipt {path, sha256}`, `metrics {path, sha256}`, `protocol_schema {repo_relative_path, sha256}`, `recompute_command` ואת הקבוע `identity_decision: NOT_PERFORMED`; רק component אחד שעליו נשענים רשאי לשאת אותו. כך שינוי מתואם של custody+receipt לאחר הביקורת מבטל את ה־verdict. ב־CP-2 Integration verdict, האובייקט `blind_adjudication` חייב לקשור `blind_review_id`, `freeze {path, sha256}`, `reveal {path, sha256}`, `adjudication {path, sha256}`, `selected_role` ו־`selection_declaration {repo_relative_path, sha256}`. `PASS` טרמינלי דורש גם `match: true` ברשומת ה־adjudication.

כל record הוא create-only ואסור reveal לפני freeze. כל שינוי ב־SHA/source/rule/canonicalization/selection, כל Blind FAIL, חשיפה מוקדמת, tamper, reuse או winner mismatch מבטלים את כל הניסיון. שומרים אותו ומתחילים מחדש עם blind ID, runs/refs, seed, permutation, custody, Critic, freeze, reveal ו־Integration חדשים. לעולם לא ממחזרים mapping שנחשף.

#### גבול האיום האמיתי

`0700/0600` מגנים מפני גישה של users אחרים; הם **לא** סודיות אדברסרית מפני process אחר שרץ תחת אותו Unix UID. ה־hashes מוכיחים state ו־chronology, לא non-observation. מותר לכתוב `ENFORCED_READ_ISOLATION` רק אם ה־harness אוכף read allowlist/sandbox המונעים מה־Blind Critic custody, source manifest/files זהותיים, selection declaration, reveal artifacts, `preparation-invocation.json` או log של harness וכל מעקף דרך Git/object store. detached checkout מלא עם unrestricted reads אינו מספיק כאשר ניתן להתאים artifacts. בלי enforcement כזה ה־Return Packet חייב לומר `COOPERATIVE_PROCEDURAL`; אסור לקרוא לזה cryptographically enforced blindness.

### 6.6 לא לקבוע מספר rounds שרירותי

אין "שלושה סבבים וזהו". הלולאה ממשיכה עד שאחד מאלה מתקיים:

- ה־artifact עובר את ה־bar;
- השיפור הבא קטן מכדי להצדיק את העלות;
- הושג plateau בשני ניסיונות מהותיים;
- checkpoint budget הגיע לתקרה;
- נדרשת החלטת owner או amendment;
- ה־Orchestrator או ירדן עוצרים את הריצה.

תקרת השעות מכסה את כל הריצה מ־orientation ועד Return Packet. רושמים `started_at_utc`, כל זוג `paused_at_utc`/`resumed_at_utc` עם סיבה וראיה, `terminal_at_utc`, ואת מספר השניות הגולמי. `consumed = terminal − start − pauses eligible`. Pause נחשב רק כאשר כל ה־Lead/Builder/Critic/Integration/tests/tools עצורים עקב תלות חיצונית שכבר אושרה או השעיית platform; credential, source או authority חדשים מחזירים `BLOCKED` ואינם pause פתוח. עבודה מקבילית אינה נסכמת. הגעה לתקרה לפי השניות הגולמיות לפני PASS מחזירה `BUDGET_EXHAUSTED`; היא אינה מתירה למחוק criterion. רק ה־Orchestrator רשאי להוציא brief חדש עם הרחבה מספרית. הקטנת bar אפשרית רק אחרי amendment שאושר בידי owner ויצר anchor חדש.

### 6.7 לצפות בלי להפריע, ואז לבצע smoothing pass

ה־Lead מתחזק `workbench.md` פשוט עם שעון/pauses, artifacts, tests, metrics ו־verdicts. הוא ignored ב־Git ואינו נכנס ל־candidate commit או ל־Critic checkout/context. זהו זיכרון עבודה פנימי בלבד: ה־Orchestrator אינו קורא אותו וירדן אינו מעביר ממנו מידע. ראיות חיות נשמרות תחת `.gauntlet/evidence/<checkpoint>/`, שאף הוא ignored ואינו חלק מה־candidate tree. אין לשמור שם secrets או raw restricted data **למעט** מיפוי/seed ה־CP-2 הזמניים והמקובעים ב־`_blind-custody/<blind-review-id>/` המוגן כמפורט לעיל; אף raw production/restricted dataset אינו נכנס לשם. בסיום snapshot של ה־workbench מוקפא ברמת checkpoint root—לעולם לא בתוך Critic run directory—רק אם הוא ייחודי, או נמחק.

בסוף גל משמעותי או checkpoint מופעל fresh Integration Critic. תפקידו לחבר וליישר את החלקים, לא לעצב מחדש את המערכת.

---

# חלק ג׳ — הארכיטקטורה הארגונית המתוקנת

## 7. חלוקת הסמכות

### ה־Orchestrator

אחראי על:

- שלושת המסלולים A/B/C;
- התזמון;
- פתיחת checkpoint;
- ניסוח B-Claude brief שמכיל repo אחד, checkpoint אחד, anchor מדויק ותקרת active-elapsed wall-clock מספרית אחת;
- ratification ו־scope;
- עדכון `progress.md`;
- בדיקת ה־Return Packet מול ה־criteria;
- לאחר PASS נתמך: סגירת checkpoint ושאלה מפורשת לירדן אם לאשר את השלב הבא. ה־Orchestrator אינו פותח אותו אוטומטית.

### Track B Engineering Lead

אחראי, רק לאחר שקיבל brief מאושר, על:

- אימות מצב ה־repository;
- תכנון בקול רם;
- בחירת decomposition;
- הפעלת Builders ו־Critics;
- יצירת worktrees/snapshots מבודדים ל־Builders והיותו Git writer יחיד שמשלב allowlisted paths ומקבע serially;
- routing אוטומטי של verdicts;
- debugging;
- evidence;
- integration review;
- return packet;
- עצירה בסוף ה־checkpoint.

### ירדן

אחראי על:

- העברת brief אחד מה־Orchestrator ל־Track B;
- העברת return packet אחד חזרה;
- credentials ופעולות owner-only;
- הכרעות שמסלימות authority חדשה.

ירדן אינו מעביר הודעות בין Builder ל־Critic.

## 8. היחס בין שני סוגי state

`progress.md` אצל ה־Orchestrator הוא state סמכותי: הוא קובע מה פתוח ומה נסגר בתוכנית.

`workbench.md` בתוך Track B הוא state תפעולי זמני בלבד. הוא אינו רשאי לפתוח checkpoint, לשנות את התוכנית או לשמש evidence כלפי מעלה. ה־evidence audit trail הנפרד נשמר תחת `.gauntlet/evidence/<checkpoint>/`; גם הוא אינו program state ואינו authority לפתוח checkpoint. בסיום אין active workbench: snapshot ייחודי נשמר ברמת checkpoint evidence root מחוץ לכל Critic run directory, או שהקובץ נמחק.

אין צורך ב־`GAUNTLET_STATE.yaml`, ב־Stage Controller נוסף או ב־owner-approval machine. ה־checkpoint architecture הקיימת כבר ממלאת את התפקיד הזה.

## 9. מחזור החיים של B-Claude block

### שלב 1 — Orchestrator פותח עבודה

ה־brief מציין:

- target repo;
- milestone/checkpoint;
- exact ratified plan anchor;
- project state שה־Orchestrator מצפה למצוא;
- goal;
- relevant constraints;
- citation לרשימת ה־CP/FCP המלאה + task-specific supporting extract;
- numeric active-elapsed wall-clock ceiling אחד שמכסה את כל ה־Gauntlet;
- owner-only actions;
- עצירה והחזרה בסוף ה־checkpoint.

### שלב 2 — ה־Lead מאמת מצב

הוא בודק branch, commit, working tree, tests ו־artifacts. תיאור ה־Orchestrator אינו נחשב ראיה.

### שלב 3 — ה־Lead בוחר decomposition

הוא מחליט:

- אילו pieces חשובים;
- מה ניתן להריץ במקביל;
- איזה bar חל על כל piece;
- היכן נדרש Builder נפרד;
- היכן נדרש Critic נפרד;
- איך לחלק פנימית את התקרה הכוללת בין workstreams. ה־Lead אינו מגדיל אותה.

לכל Builder מקביל מוקצים worktree/snapshot מבודד ו־path allowlist שאינו חופף לאחר. Builders אינם writers של Git. ה־Lead הוא היחיד שמשלב paths ומקבע candidate commits, אחד אחרי השני, על הענף המקומי `gauntlet/<checkpoint>`.

### שלב 4 — Gauntlet loops

ה־Lead מפעיל Builder, מקבל changed paths/evidence, מייבא רק את ה־allowlist ומקבע candidate commit בעצמו. לאחר מכן הוא יוצר clean detached Critic checkout לפי פרוטוקול הבידוד, מורה ל־helper לייצר manifest מכני ב־evidence root, מפעיל fresh read-only Critic שמפיק verdict record נפרד, מעביר את הפער חזרה וממשיך. ירדן אינו משתתף ב־routing.

### שלב 5 — progress visibility

ה־Lead מעדכן `workbench.md` פנימי עם `last_updated_at_utc`, שעון/pauses ונתיבי evidence. כל Critic מקבל run directory ייחודי תחת `.gauntlet/evidence/<checkpoint>/` עבור manifest+verdict בלבד, ו־`_support/<run-id>/` ייחודי עבור כל artifact/input/log/evidence שה־verdict קושר. ירדן אינו נדרש לקרוא את ה־workbench או לשאול "מה קורה?" במהלך הריצה.

### שלב 6 — integration/smoothing

כאשר ה־candidate מפסיק להשתנות, ה־Lead מקפיא final SHA/tree. הוא מבטל ומריץ מחדש את כל component PASS records שנוצרו לפני אותו SHA; רק verdicts שנקשרים בדיוק ל־final SHA/tree יכולים לתמוך ב־PASS. לאחר מכן נוצר clean detached checkout חדש באותו SHA/tree, ו־fresh Integration Critic מריץ את ה־artifact מקצה לקצה ובודק consistency ואת מערכת הראיות המלאה.

### שלב 7 — עצירה והחזרה

לפני ההחזרה ה־Lead מאמת מחדש את `refs/gauntlet-evidence/...` שנוצרו לפני ה־reviews לכל SHA שמצוטט ב־packet. Track B אינו מתחיל את ה־checkpoint הבא ואינו מבצע planning מפורט שלו. הוא מחזיר packet ל־Orchestrator ועוצר.

---

# חלק ד׳ — השינויים המינימליים ב־Track B

## 10. השינוי שבוצע ב־`engineering-role.md`

הסעיף כבר יושם, ולא נשאר כ־snippet להעתקה. החוזה המחייב דורש:

- brief תקף עם repo/checkpoint/anchor יחידים ותקרת active-elapsed wall-clock מספרית אחת;
- אימות מצב אמיתי ותכנון בקול רם;
- Builders ו־fresh Critics בהקשרים נפרדים;
- Lead יחיד כ־Git writer, Builder worktrees מבודדים ושילוב serially;
- חמישה surfaces חובה כאשר הם רלוונטיים;
- evidence root מוחרג, manifest מכני ו־verdict מובנה נפרדים, refs מקומיים לשימור SHAs;
- התאמה מדויקת של כל component PASS ל־final SHA/tree והרצה מחדש של כולם אחרי כל שינוי;
- `PASS`, `BLOCKED`, `PLATEAU` או `BUDGET_EXHAUSTED` בלבד;
- fresh Integration `PASS` כתנאי סגירה;
- Return Packet מלא ועצירה לפני עבודה כלשהי על השלב הבא.

המקור לביצוע הוא `engineering-role.md`; התבניות הקנוניות נמצאות ב־`docs/track-b/gauntlet-templates.md`. אין לתחזק כאן עותק נוסף שעלול לסטות.

## 11. תבנית B-Claude brief מה־Orchestrator

ה־brief צריך להיות קצר יחסית, בהתאם למאמר:

```text
Target repository: [repo אחד, מדויק]
Authorized checkpoint: [M#/CP-#]
Ratified plan anchor: [exact filename/version copied from progress.md]
Complete checkpoint checklist: [exact CP/FCP checklist citation; every item controls]
Supporting sections: [task-specific plan citations]
Total checkpoint active-elapsed ceiling: [מספר שעות כולל]

Goal:
[המצב שצריך להתקיים בסוף ה-block]

Complete checkpoint quality bar:
[every item in the named CP/FCP checklist; a convenience extract cannot narrow it]

Ratified constraints:
[רק constraints רלוונטיים; הפניה לסעיפי capstone]

CP-2 mandatory label-blind outcome (include only for CP-2):
- exact metric authority: capstone §4.1
- exact custody/freeze/reveal authority: capstone §12
- committed identity artifacts required at
  artifacts/cp2/blind/source-manifest.json and
  artifacts/cp2/blind/selection-declaration.json
- Blind Critic recomputes/freezes anonymous A/B/C/D metrics only and chooses no winner
- reveal only after schema-valid Blind PASS freeze; fresh Integration adjudicates
- schema/commands: docs/track-b/schemas/cp2-blind-four-catalog.schema.json;
  blind-prepare, blind-recompute, blind-freeze, blind-reveal, blind-adjudicate
- threat label required: ENFORCED_READ_ISOLATION or COOPERATIVE_PROCEDURAL

Orchestrator-reported expected project state:
[תמצית; Engineering Lead חייב לאמת]

Owner-only actions already authorized:
[none / פעולה מדויקת]

Run this checkpoint as a Gauntlet Loop. Choose the implementation and
decomposition yourself. Use Builders and separate fresh-context Critics for
important pieces, inspect real artifacts, and keep improving the largest gap
until the bar is met or a true blocker/resource limit is reached.

Maintain a temporary ignored internal workbench.md. Review only committed
candidates from clean detached Critic checkouts under engineering-role.md. Keep
live evidence in the ignored .gauntlet evidence root. Create each non-moving
candidate evidence ref before its review. At checkpoint completion run a fresh
isolated integration review, reverify every cited ref, stop all Track B work,
and return one packet. Do not begin the next milestone.
```

ה־Orchestrator אינו מכתיב modules, exact decomposition או fixed rounds.

## 12. `workbench.md` פשוט

```markdown
# Active Track B Workbench — [M#/CP-#]

## Goal and bar
- Goal: ...
- Exact plan anchor: [from brief]
- Authoritative criteria: §...
- Active-elapsed ceiling: ...
- Checkpoint evidence root: `.gauntlet/evidence/<checkpoint>/`
- started_at_utc / last_updated_at_utc: ...
- consumed active elapsed: ... raw seconds / ... decimal hours

## Eligible pauses
| paused_at_utc | resumed_at_utc | seconds | reason/evidence | all contexts stopped? |
|---|---|---:|---|---|

## Current pieces
| Piece chosen by Lead | Disjoint owned paths | Isolated Builder path | Lead commit SHA | Critic verdict record | Biggest gap |
|---|---|---|---|---|---|
| ... | ... | ... | ... | PASS/FAIL + path/hash | ... |

## Latest visible outputs
- tests: ...
- metrics: ...
- screenshots/plots: ...

## Open blocker or owner decision
- none / exact question

## CP-2 label-blind chain (when active)
- blindness strength / enforcement or candid limitation: ...
- committed `artifacts/cp2/blind/source-manifest.json` + `artifacts/cp2/blind/selection-declaration.json` blob hashes: ...
- blind-review ID / Blind component run-piece-ref-support: ...
- private custody path only (never contents): ...
- `blind-public-input.csv` / `blind-public-manifest.json` / `blind-commitment.json` / `blind-metrics.json` / verdict: ...
- Integration allocated only after schema-valid Blind PASS: ...
- freeze/reveal/adjudication paths, hashes and UTC times: ...
- latest invalidation/reset reason: ...

## Integration and terminal blocker
- final candidate SHA/tree / commands / tool integrity manifest / schema-valid fresh verdict
- local evidence refs for every cited SHA
- none / exact blocker

## Critic run inventory
| Run ID / piece | Component/Integration | Candidate ref/SHA | Run root / owned `_support` root | Manifest path/hash | Committed schema hash | Verdict path/hash/result |
|---|---|---|---|---|---|---|
```

הקובץ ignored ב־Git, אינו audit log מלא ואינו מועבר ל־Orchestrator. Critics אינם מקבלים אותו והוא אינו קיים ב־checkout שלהם. לאחר Return Packet אין להשאיר אותו active: שומרים snapshot ששמו שונה ברמת checkpoint evidence root ומחוץ לכל immutable Critic run directory רק אם יש בו מידע ייחודי, אחרת מוחקים.

## 13. Builder brief

```text
You are the Builder for [piece chosen by the Engineering Lead].

Goal: [observable result]
Bar: [test/reference/measurement]
Ratified constraints: [relevant sections]
File ownership: [paths]
Lead-created isolated writable detached worktree/snapshot: [path]
Required artifact and evidence: [files/commands/results]

Build only the allowlisted paths. Do not stage, commit, merge, switch branches,
update refs, create/remove worktrees, or share a writable Git index. Return the
changed-path list, artifact/input hashes, and exact reproduction commands to the
Lead. The Lead alone imports allowed paths and commits serially. Do not grade
your own work, write the critic verdict, close a CP item, or expand scope.
```

## 14. Critic brief

```text
You are a fresh independent, read-only Critic.

Goal: [piece goal]
Piece ID: [mandatory ref-safe ID]
Pre-created candidate evidence ref: [refs/gauntlet-evidence/<checkpoint>/<run-id>/<piece>]
Full candidate commit SHA: [sha]
Full candidate tree: [tree]
Artifact path/SHA-256: [path/hash]
plan.filename (safe repo-relative committed .md path): [path]
plan.sha256 (exact SHA-256 of that blob's bytes at candidate SHA): [hash]
plan.version (human-readable version): [version]
plan.bar_citation (exact human citation): [citation]
plan.bar_excerpt (non-empty verbatim text present in that same blob): [excerpt]
Decision-bearing input/data SHA-256: [hashes or N/A reason]
Exact commands and expected tolerance: [commands/bar]
Command stdout/stderr destinations: [absolute paths outside immutable run root]
Unique immutable Critic run ID: [mandatory ref-safe ID; never reused]
Critic ID: [ref-safe harness context ID when suitable; otherwise assigned]
Critic run root: [absolute <repo>/.gauntlet/evidence/<checkpoint>/<critic-run-id>/]
Critic-owned support root: [absolute <repo>/.gauntlet/evidence/<checkpoint>/_support/<critic-run-id>/]
Tool-generated integrity manifest path: [absolute <run-root>/integrity-manifest.json]
Pre-review integrity-manifest SHA-256: [create output]
Separate Critic verdict record path: [absolute <run-root>/critic-verdict.json]
Canonical schema: [docs/track-b/schemas/critic-verdict.schema.json]
Committed schema SHA-256: [hash at candidate SHA]

The Lead initializes the unique run root and creates/verifies the immutable
candidate ref at exact checkpoint HEAD before launch. Create the snapshot with
gauntlet_critic_snapshot.sh create <sha> <snapshot> <manifest> <critic-run-id>.
Work only in the clean detached checkout; do not inspect any
Builder workspace, uncommitted files, or workbench.md. Inspect/recompute the real artifact. Route
caches/output/fixtures/logs and every declared artifact/input/evidence path to
_support/<critic-run-id>/ under the checkpoint root,
outside both the checkout and immutable run root. Every such file must be a
regular non-symlink file with its declared SHA-256 and st_nlink == 1; a
hard-linked or borrowed inode invalidates the evidence.
Do not author or repair the helper-owned integrity manifest. Without cleaning or
resetting, run verify with the pre-review manifest hash; it must reject a missing,
mutated, or mismatched create record. Only then write a separate PASS/FAIL verdict
bound to piece/ref/SHA/tree/schema, all five plan.* fields, input/commands and the final manifest hash, and validate it
with gauntlet_protocol.py validate-verdict. The run root ends with exactly these
two records. Include command exit codes and stdout/stderr paths/hashes, hashed
evidence paths under the exact owned support root with SHA-256 and st_nlink == 1,
UTC record time after verify, largest
gap, and next acceptance test. Any dirty/changed checkout/ref, unsafe or mismatched
plan binding, bar_excerpt absent from the committed blob, unhashed/hard-linked
evidence, or invalid record invalidates the review.
```

הפקודות הקנוניות הן:

```text
python3 scripts/gauntlet_protocol.py init-evidence --repo-root <abs> --checkpoint <id> --run-id <critic-run-id>
python3 scripts/gauntlet_protocol.py create-ref --repo-root <abs> --checkpoint <id> --run-id <critic-run-id> --piece <piece> --candidate-sha <full-current-head-sha>
python3 scripts/gauntlet_protocol.py verify-ref --repo-root <abs> --checkpoint <id> --run-id <critic-run-id> --piece <piece> --candidate-sha <full-current-head-sha>
scripts/gauntlet_critic_snapshot.sh create <full-sha> <outside-snapshot-path> <absolute-manifest-path> <critic-run-id>
scripts/gauntlet_critic_snapshot.sh verify <full-sha> <outside-snapshot-path> <absolute-manifest-path> <pre-review-manifest-sha256>
python3 scripts/gauntlet_protocol.py validate-verdict --verdict <absolute-verdict-path>
```

### 14.1 CP-2 Blind Metric Critic — בריף ייעודי

ה־Lead משתמש בבריף הזה רק אחרי שה־final candidate מכיל את `artifacts/cp2/blind/source-manifest.json` ו־`artifacts/cp2/blind/selection-declaration.json`, ואחרי `blind-prepare`. הוא מקצה רק Blind run/ref/support; Integration עדיין לא נוצר.

```text
You are the CP-2 Blind Metric Critic for a mandatory label-blind four-catalog
review. You recompute identity-free metrics only; you never choose a winner.

Blind review ID: [id]
Blind component run/piece/ref: [ids/ref]
Full final candidate SHA/tree: [sha/tree]
Blind run root / owned support root: [paths]
Integrity manifest / verdict destinations: [paths]
General verdict schema path/blob hash: [path/hash]
CP-2 blind schema path/blob hash:
  docs/track-b/schemas/cp2-blind-four-catalog.schema.json / [hash]
Canonical tool path/blob hash: scripts/gauntlet_protocol.py / [hash]
plan.filename / plan.version / plan.sha256: [identity]
plan.bar_citation / verbatim plan.bar_excerpt: [piece bar]
Anonymous interleaved CSV path/hash: [<ABS_BLIND_SUPPORT>/blind-public-input.csv]
Identity-free public manifest / commitment / safe receipt paths+hashes:
  [blind-public-manifest.json / blind-commitment.json / blind-preparation-receipt.json]
Read-isolation class: ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL
Enforced allowlist/deny mechanism or candid limitation: [details]

Read only the anonymous support, exact §4.1 metric text, schemas and allowlisted
metric code. Do not read custody, identity source files/manifest, selection
declaration, reveal artifacts, preparation-invocation record or harness logs,
Builder material, or any
Git/object-store path that retrieves them.

Run:
python3 scripts/gauntlet_protocol.py blind-recompute --support-root <ABS_BLIND_SUPPORT> --blind-review-id <ID>
Enforce exact header label,fold_id,row_id,y,q025,q05,q10,q25,q50,q75,q90,q95,q975,
UTF-8/LF, sort (fold_id numeric, row_id UTF-8 byte order, label A-D), opaque
row_id matching ^r[0-9]{6,}$, matched rows/folds, nine raw quantiles, finite
Decimal inputs and exact comparisons. row_id contains no timestamp/catalog identity;
do not receive or consult any timestamp/identity lookup in the Blind context.
Compute observation-weighted pinball and inclusive
submitted q10<=y<=q90 coverage. Raw crossing is allowed; do not repair, reject,
calibrate or isotonize it.

Write metrics only by A/B/C/D. Validate arithmetic and completeness. Never infer
base identity, apply eligibility/tie-breaks, select a label, or assert a winner.
Complete post-review verify, write the verdict with blind_review binding, validate
it, then stop without requesting or receiving reveal.
```

### 14.2 Freeze ו־Reveal handoffs מכניים

```text
FREEZE HANDOFF
Blind review ID: [id]
Final SHA/tree: [sha/tree]
Schema-valid Blind PASS verdict + manifest + run/piece/ref: [paths/hashes]
blind-public-input.csv / public manifest / commitment / metrics: [paths/hashes]

Supply fresh Integration run/piece IDs but do not initialize them. Revalidate the
Blind PASS through blind-freeze; that command alone initializes run/support, creates
the ref at the same SHA/tree, and refuses any preallocated identity.
Canonical command:
python3 scripts/gauntlet_protocol.py blind-freeze --repo-root <ABS_REPO> --blind-review-id <ID> --component-verdict <ABS_CRITIC_VERDICT> --integration-run-id <RUN> --integration-piece <PIECE>
On FAIL/mismatch/tamper/preexisting output: no reveal; preserve any allocated or
partial attempt and restart with wholly new IDs/seed/permutation/custody.

REVEAL HANDOFF
Blind review ID: [id]
Integration run/piece/ref/support: [values]
Freeze path/hash/time: [record]
Private custody-record path/SHA-256 + receipt-bound SHA-256/modes: [record; do not print secret contents]

Run blind-reveal only after freeze verification. Read but never modify custody.
Canonical command:
python3 scripts/gauntlet_protocol.py blind-reveal --repo-root <ABS_REPO> --blind-review-id <ID> --integration-run-id <RUN>
Verify the commitment. Copy—never hard-link—the mapping, four identity-bearing
canonical source CSVs, source manifest, selection declaration and safe post-reveal
preparation record into Integration support. Record create-only paths/hashes/times.
Never write reveal artifacts into Blind support or return them to the Blind Critic.
```

כל record create-only. כל SHA/source/rule/selection change, FAIL, exposure, tamper, reuse או winner mismatch דורשים שרשרת חדשה מלאה; mapping שנחשף אינו ממוחזר.

## 15. Integration Critic brief

```text
You are a fresh read-only Integration Critic for [M#/CP-#]. Work from a new clean
detached checkout at the full final candidate SHA under the same before/after
integrity protocol.

Full final candidate commit SHA: [sha]
Full final candidate tree: [tree]
Final candidate artifact path/SHA-256: [path/hash]
plan.filename (safe repo-relative committed .md path): [path]
plan.sha256 (exact SHA-256 of that blob's bytes at final candidate SHA): [hash]
plan.version (human-readable version): [version]
plan.bar_citation (complete checkpoint citation): [citation]
plan.bar_excerpt (non-empty verbatim text present in that same blob): [excerpt]
Decision-bearing input/data SHA-256: [hashes or N/A reason]
Exact reproduction commands: [commands]
Expected output/tolerances: [bar]
Data snapshot/cutoff/hash: [date/hash]
Unique immutable Integration Critic run ID/root: [id/path]
Component integrity-manifest paths/hashes: [records]
Component schema-valid verdict paths/hashes: [records]

CP-2 revealed-chain inputs (mandatory only for CP-2):
- blind review ID / blindness strength + enforcement or limitation
- cp2-blind schema + tool blob hashes
- committed artifacts/cp2/blind/source-manifest.json blob hash
- committed artifacts/cp2/blind/selection-declaration.json blob hash + winner
- Blind run/piece/ref/manifest/verdict PASS
- anonymous `blind-public-input.csv` / public-manifest / commitment / metrics hashes
- freeze and reveal paths/hashes/times
- Integration-owned copied mapping, four real source CSVs, source manifest,
  selection declaration and safe prepare record
- adjudication/chain-validation destination

Ignore Builder narratives. Reproduce the complete named checklist and verify
that every component PASS used for terminal PASS binds this exact final SHA/tree,
the same plan identity (plan.filename, plan.version, and plan.sha256), and current
input hashes. Each component and Integration verdict keeps its own piece-appropriate
plan.bar_citation and plan.bar_excerpt; the excerpt, not the human citation
string, is independently proven verbatim against that same committed blob.
Those two fields need not equal the Integration pair.
Any candidate change invalidates all earlier component
PASS verdicts; all required Critics rerun, without selective path-based reuse.
Verify contracts, invariants, metrics, documentation, and absence of later work.

At CP-2 run:
python3 scripts/gauntlet_protocol.py blind-adjudicate --integration-support-root <ABS_INTEGRATION_SUPPORT> --blind-review-id <ID>
Use only Integration-owned copies and frozen anonymous
metrics, never custody. Verify 256-bit commitment, create-only chronology, PASS
freeze before reveal, exact SHA/source/rule/selection bindings and no map reuse.
Apply §4.1 to strict_base/residual_arm/scarcity_arm/both_arms: observation-weighted
nine-quantile Decimal pinball, inclusive submitted raw q10<=y<=q90 coverage,
exact eligibility thresholds and deterministic tie-break. Do not repair raw
crossing. Require adjudicated winner == committed selection declaration and bind
the adjudication record in the Integration verdict's blind_adjudication field.

Verify each revealed identity-bearing source CSV has exact header
fold_id,row_id,y,q025,q05,q10,q25,q50,q75,q90,q95,q975, canonical sort
(fold_id numeric, row_id UTF-8 byte order), and the same opaque ^r[0-9]{6,}$
row universe as the anonymous input. Timestamp/identity lookup is post-reveal
Integration evidence, never Blind input.

Do not redesign. Return PASS only if the complete bar and provenance contract
pass. Write a separate schema-valid Integration verdict tied to its tool-generated
manifest; otherwise identify the highest-impact integration gap and rerun condition.
```

## 16. Checkpoint Return Packet

```markdown
# Track B Checkpoint Return — [M# / CP-#]

Status: PASS | BLOCKED | PLATEAU | BUDGET_EXHAUSTED
Target repository: ...
Ratified plan anchor: [exact anchor from brief]
Checkpoint evidence root: ...
Final candidate commit/tree/branch: <sha/tree/branch>
Working-tree state: ...
Data snapshot/cutoff: <hash/date>
Checkpoint active-elapsed ceiling: ...
started_at_utc / terminal_at_utc: ...
Eligible pause ledger: ...
Consumed active elapsed: <raw seconds / decimal hours>
Integration verdict and evidence: PASS | FAIL | NOT_RUN — <path/result or exact reason>
Integration integrity manifest (tool-generated): <path/SHA-256>
Integration Critic verdict record (schema-valid): <path/SHA-256>

## Critic run inventory
| Run ID / piece | Component/Integration | Candidate ref/SHA | Run root / owned `_support` root | Manifest path/hash | Committed schema hash | Verdict path/hash/result |
|---|---|---|---|---|---|---|

## CP-2 label-blind four-catalog chain (mandatory only for CP-2)
Blindness strength: ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL
Enforcement mechanism or candid same-UID limitation: ...
Committed source manifest path/blob hash: artifacts/cp2/blind/source-manifest.json / ...
Committed selection path/blob hash/winner: artifacts/cp2/blind/selection-declaration.json / ...
Blind schema + tool blob hashes: ...

| Attempt/blind ID | Final SHA/tree | Blind run/piece/ref/support | Custody-record path/SHA-256 + receipt-bound SHA/modes | `blind-public-input.csv` / manifest / commitment / receipt hashes | Metrics + Blind verdict | Integration run/piece/ref/support | Freeze path/hash/time | Reveal + copied-source paths/hashes/time | Adjudication path/hash/winner | Result/reset reason |
|---|---|---|---|---|---|---|---|---|---|---|---|

Chronology: prepare < metrics < Blind verify/PASS < Integration init/ref < freeze < reveal < adjudication < Integration verify/PASS
Blind Critic did not choose or assert any winner: PASS | FAIL
Revealed mapping was never reused: PASS | FAIL

## Preserved candidate refs
| Local evidence ref | Exact commit SHA | Purpose | Verified reachable? |
|---|---|---|---|

## Complete named CP/FCP checklist
| Criterion citation | PASS/OPEN | Direct evidence/reproduction |
|---|---|---|

## Independent criticism performed
| Piece/surface | Critic/run ID | Candidate SHA/tree | Artifact/input hashes | Plan filename/blob hash/version/citation + verbatim excerpt | Commands/tolerances | Integrity manifest path/hash | Schema-valid verdict path/hash/result | Gap/disposition |
|---|---|---|---|---|---|---|---|---|

## Engineering decisions and tradeoffs
- מה הוחלט ולמה
- אילו חלופות נדחו
- איזה פער משמעותי מצא ה-Gauntlet וכיצד תוקן

## Reproduction
- commands
- artifacts
- metrics

## Open risks or owner actions
- ...

## Defense questions
1. ...
2. ...
3. ...

Track B has stopped. No later-checkpoint work has begun.
```

`PASS` חוקי רק כאשר הטבלה מכסה כל item ברשימת ה־CP/FCP המלאה, לכל review חובה יש manifest מכני ו־verdict record תקין ונפרד, וכל component PASS שעליו נשענים מצביע לאותו checkpoint, לאותה זהות תוכנית—`plan.filename`, `plan.version` ו־`plan.sha256`—ול־final SHA/tree המדויק. לכל component ול־Integration נשמרים `plan.bar_citation` ו־`plan.bar_excerpt` שמתאימים ל־piece שלו; ה־excerpt, ולא מחרוזת ה־citation האנושית, מוכח עצמאית כמופיע מילולית באותו blob. אין דרישה שצמד ה־citation/excerpt של component יהיה זהה לצמד הכלל־צ'קפוינטי של Integration. כל commit חדש מבטל את כל ה־PASSים הקודמים ודורש rerun מלא עם run ID/ref חדשים. נדרש גם fresh Integration `PASS` באותו final SHA/tree, ו־ref מקומי שנוצר לפני review ואומת מחדש לכל SHA מצוטט. שדה/record/ref חסר, schema לא תקין, plan identity לא תואמת, citation שאינו מתאים ל־piece או excerpt שאינו מופיע ב־blob, evidence לא־מגובה hash או עם `st_nlink != 1`, checkout מלוכלך או SHA/tree שהשתנו פוסלים verdict. במצב non-PASS מותר `NOT_RUN` רק עם הסיבה הטרמינלית המדויקת—`BLOCKED`, `PLATEAU` או `BUDGET_EXHAUSTED`—שמנעה את האינטגרציה.

ב־CP-2 נדרש בנוסף chain טרמינלי אחד ומלא של **label-blind four-catalog review**: Blind Critic שחישב והקפיא metrics אנונימיים בלי winner; Integration שאותחל רק אחרי אותו PASS; freeze שקדם ל־reveal; עותקי source זהותיים שהועתקו ל־Integration support; adjudication שמצא את אותו winner כמו ה־declaration המקובע; ו־Integration PASS שקשור ל־chain. כל attempts/resets/paths/hashes/timestamps ו־blindness strength מופיעים ב־packet. מיפוי שנחשף לא ממוחזר; `ENFORCED_READ_ISOLATION` ללא sandbox אמיתי הוא טענה שגויה.

---

# חלק ה׳ — bars והתאמה לפי milestones

הסעיפים הבאים אינם decomposition מחייב. הם מזכירים ל־Lead ול־Critic אילו artifacts ו־bars קיימים בכל checkpoint. ה־Lead בוחר את ה־pieces בזמן הריצה.

## 17. M1 / CP-1 — Data Layer

### bars מרכזיים

- feed coverage ו־provenance;
- ENTSO-E↔SMARD reconciliation;
- UTC/DST correctness;
- exactly-four-quarter-hours aggregation;
- no partial bins;
- runtime schema firewall;
- proper-training-only A75 lineage;
- closed-left features;
- DuckDB mart consistency;
- CC BY attribution;
- spectral artifacts לפי התוכנית.

### ביקורות component-level חובה

- temporal normalization;
- champion/benchmark schema firewall;
- A75 climatology fit lineage.

### חמשת independent acceptance oracles המחייבים

ה־Critic מייצר את הקלטים מחוץ ל־candidate checkout לפי המפרט הקפוא, מחשב expected output בעצמו ורושם fixture hash ופקודות. tests שכתב ה־Builder אינם מספיקים:

1. **M1-O1 — misaligned chunk stitch:** שני chunks סמוכים שנחתכים ב־00:15 יוצרים לאחר stitching ערך 00:00 יחיד מממוצע ארבעה quarters ידועים; fragment של שלושה quarters לעולם אינו ממוצע.
2. **M1-O2 — missing quarter:** שעה שחסר בה quarter אינה מפיקה hourly value ומחזירה incomplete/recovery מפורש.
3. **M1-O3 — fall-back DST:** ב־2025-10-26 `Europe/Berlin` שני ערכי 02:00 עם offsets שונים נשמרים כ־UTC instants שונים, היום מכיל 25 שעות, ו־UTC instant כפול אמיתי נדחה.
4. **M1-O4 — poisoned A75:** שינוי A75 רק ב־calibration/eval אינו משנה coefficients או predictions; fit manifest מכיל proper-training בלבד. poison בתוך proper training חייב לשנות את ה־fit כביקורת חיובית.
5. **M1-O5 — poisoned schema:** input champion תקין עובר; הזרקת A69, נגזרת A69 או actual column נכשלת לפני prediction. benchmark מוסיף רק שדות A69 המאושרים ועדיין דוחה actuals.

החבילה משרתת את שלושת משטחי M1 הראשונים ואינה מחליפה את חמשת property tests של §9.4.

### תוספת M1

- A65/A01 capture ledger על **לפחות שלושה delivery days לא־רצופים**, ב־10:30 וב־11:45 `Europe/Berlin`, כולל pulled-at, delivery date, request identity, response hash, row count/completeness ו־error state;
- `selection_cutoff`, snapshot hash ו־audit-quarantine manifest מוקפאים אחרי ה־capture;
- README Current Status.

## 18. M2 / CP-2 — Baselines ו־Model Selection

### bars מרכזיים

- baseline conventions נכונים על hand-calculated days;
- אותו data, rows, folds, seeds ו־budget בכל ארבעת הקטלוגים `strict_base`, `residual_arm`, `scarcity_arm`, `both_arms`;
- ה־final candidate מכיל `artifacts/cp2/blind/source-manifest.json` ו־`artifacts/cp2/blind/selection-declaration.json`, שניהם committed ו־hash-bound;
- metrics מחושבים מחדש מ־frozen predictions לפי החוזה המדויק: observation-weighted pooled mean על rows/folds/9 quantiles, coverage inclusive `q10<=y<=q90`, ו־Decimal/canonical CSV;
- raw crossing מותר ונשאר כמו שהוגש; אין CQR/isotonic ב־M2;
- retention rule מיושם בדיוק: `(base-arm)/base`, base loss אפס מחזיר base, תנאי coverage חד־צדדי `C_base-C_arm <= 0.02`, שוויון ב־1%/2pp עובר, וחיובי ממש ב־4/5 folds;
- tie ב־0.1% כולל את מקרה `L_min=0`, ומוכרע לפי fewer features → calibration error → `residual_arm -> scarcity_arm -> both_arms`;
- CI green;
- experiment hypothesis lineage;
- five-fold DM מסווג descriptive post-selection;
- forward audit quarantined עד model freeze;
- α, comparator, daily probabilistic loss, Newey–West rule, `δ*`, `LRV_ref`, `N80`, `N_required=max(90,N80)`, מינימום 12 שבועות וכלל no-reuse מוקפאים לפני unseal.

### ביקורת component-level חובה

- **label-blind four-catalog review מחייב** עם labels אנונימיים `A/B/C/D`, public manifest, 256-bit-seeded commitment ו־private create-only custody;
- Blind Critic מחשב ומקפיא metrics זהות־חופשיים מקבצי predictions, ולא מסתמך על summary של training code;
- הוא לעולם אינו בוחר winner. רק אחרי schema-valid PASS מוקפא מותר reveal;
- fresh Integration קורא רק עותקים שב־Integration support, מפעיל את כלל §4.1 ומאמת שה־winner זהה ל־declaration;
- Return Packet מציג את כל attempts, paths, hashes, chronology, reset reasons ו־`ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL`.

ה־protocol המלא מוגדר ב־§6.5.2; סכמה ומעברים מכניים ב־`docs/track-b/schemas/cp2-blind-four-catalog.schema.json` ו־`scripts/gauntlet_protocol.py`.

## 19. M3 / CP-3 — Calibration ו־Diagnostics

### bars מרכזיים

- proper-training/calibration/eval separation;
- CQR thresholds נכונים;
- כלל rank מדויק: `k=ceil((n+1)(1-alpha))` ב־one-based notation ו־`scores[k-1]` ב־Python, ללא interpolated quantile או clipping שקט;
- three-stage coverage;
- zero final crossings;
- coverage, pinball ו־interval width מוצגים יחד;
- SHAP מסביר champion קפוא ואינו מבצע feature selection;
- post-gate benchmark שונה רק ב־A69 ונגזרותיו;
- regime/negative-price diagnostics כוללים n_obs ו־uncertainty.

### ביקורת component-level חובה ב־M3

- Critic טרי מחשב ביד את fixture `n=20`, scores `−11…8`, עבור α=.05/.10/.20/.50, כולל negative `Q`, median שלא השתנה ומיפוי one-based/zero-based;
- אותו Critic מחשב מחדש לפחות fold אמיתי אחד מתוך persisted calibration predictions;
- forward-audit verdict מוצג כ־`PENDING_UNDERPOWERED`, `CONFIRMED` או `NOT_CONFIRMED`; “sealed” ו־“eligible” הם מצבי lifecycle, לא verdicts נוספים. underpowered לעולם אינו forced verdict.

ה־Integration Critic של M3 חייב לבדוק את prediction artifacts ואת reliability outputs בפועל, גם אם לא הופעל component critic נפרד לכל plot.

## 20. M4 / CP-4 — Local Artifact

### bars מרכזיים

- cold-start מקומי;
- registry-first/bundle-fallback;
- retained-feature controls בלבד;
- lookup ללא live compute;
- OOD flags;
- CLI smoke test;
- offline health artifact לפי scope הקיים.

כאן ה־Critic בודק running app ו־rendered output, לא README claim.

## 21. M5 / CP-5 — Deployment ו־Stranger Test

### bars מרכזיים

- static page <3s cold cache ו־zero runtime calls;
- Space cold/warm load;
- bundle fallback;
- technical ו־non-technical stranger tests;
- reproducibility from tagged commit;
- metrics, limitations ו־training cutoff עקביים בכל surfaces;
- static page, Space, README ו־MLflow אינם סותרים זה את זה.

ה־stranger test הוא Gauntlet חיצוני טבעי: המשתמשים בודקים את התוצר הממשי בלי לשמוע קודם את הסבר ה־Builder.

---

# חלק ו׳ — amendment מתודולוגי שאושר ויושם

## 22. שלושת התיקונים שננעלו ב־v6.4

### AMD-1 — Forward confirmatory audit

- חמשת ה־folds הקיימים נשארים selection + stress diagnosis.
- DM עליהם מתויג post-selection descriptive.
- snapshot cutoff ננעל לפני M2 selection.
- data עתידי מוסגר ואינו נצפה עד freeze.
- champion/catalog/hyperparameters מוקפאים.
- minimum sample/period ו־DM rule נקבעים לפני פתיחת audit.
- confirmatory result רץ פעם אחת; אם sample אינו מספיק ב־M3, הוא אינו מזויף כ־gate.

### AMD-2 — Point-in-time load evidence

- captures לפני gate בכמה delivery days;
- שמירת pulled-at, delivery date, row completeness ו־hash;
- תיקון הטקסט כך שיבדיל בין regulatory proof ל־observed proof.

### AMD-3 — Experiment lineage

- מחיקת `≥5 experiments` כ־checkbox;
- לכל run: hypothesis, delta, fixed budget, result, keep/reject;
- אין דרישה למספר מלאכותי.

## 23. מה בוצע עכשיו ומה עדיין לא נפתח

בעל הפרויקט אישר לבצע את חבילת התיעוד במלואה, ולכן אין עוד “אישור עתידי” ל־AMD-1/2/3:

- `capstone_V6_4.md` ו־`capstone_V6_3-to-V6_4-amendments.md` נכתבו;
- `engineering-role.md` ו־`orchestrator-role.md` עודכנו משני צדי הגבול;
- map v6, `progress.md`, הסילבוס, README, NotebookLM pointer, spike note ו־AWS future cascade יושרו;
- `AGENTS.md`/`CLAUDE.md` תוקנו ו־`docs/track-b/gauntlet-templates.md` נוצר;
- DEC-AWS אכן זז ל־v6.5 / map v7 אם יאושר בעתיד.

זהו שינוי state תיעודי/ממשלי, אך **לא** שינוי במצב הביצוע ההנדסי: M0 עדיין סגור, M1 עדיין לא התחיל ו־CP-1 עדיין ממתין. החוזה Git-durable, אך operational validation עדיין ממתין לריצת CP-1 המאושרת הראשונה. אין להפעיל את מסלול B מוקדם רק משום שהחוזה מוכן.

## 23.1 מה במפורש לא עושים עכשיו

- לא משנים code של M1;
- לא יוצרים `workbench.md` פעיל;
- לא מפעילים Builders או Critics;
- לא משנים את ה־checkpoint state;
- לא פותחים מחדש SFTP, gas, spectral, marimo או AWS;
- לא נותנים למסמך Gauntlet לדחוק את G0 או עבודה פעילה במסלולים האחרים.

המסמך הוא design מוכן ל־Track B כאשר יגיע תורו, לא אות להתחיל אותו כעת.

---

# חלק ז׳ — הפעלה בפועל

## 24. מה ירדן עושה

בשיחת ה־Orchestrator, פקודת המפעיל יכולה להיות משפט אחד: **“בצע את הקאפסטון.”** ה־Orchestrator קורא את `progress.md`, מזהה את ה־checkpoint הבא שמותר לתזמן, ובונה עבורו brief מלא. המשפט אינו מאשר את כל M1–M5 ברצף ואינו עוקף gate שעדיין לא נפתח; אם Track B עדיין אינו בתור, ה־Orchestrator מסביר זאת ומתזמן את המסלול הנכון.

1. ה־Orchestrator מחליט ש־Track B הגיע ל־checkpoint הבא.
2. הוא מפיק B-Claude brief לפי התבנית הקצרה.
3. ירדן מעביר אותו פעם אחת ל־Engineering Lead ב־repo הנכון.
4. Track B עובד אוטונומית; ירדן אינו צריך לקרוא או להעביר את `workbench.md` ואינו מעביר הודעות בין agents.
5. אם נדרש credential או authority חדשה, ה־Lead מחזיר terminal `BLOCKED` packet עם פעולה אחת מדויקת; אין שאלה ישירה באמצע הלולאה.
6. בסיום Track B מחזיר Checkpoint Return Packet ועוצר.
7. ירדן מעביר אותו ל־Orchestrator.
8. ה־Orchestrator בודק את ה־packet. אם PASS נתמך, הוא מעדכן `progress.md` ואומר לירדן: **“CP-# הסתיים. לאשר מעבר לשלב הבא?”** רק תשובת go/no-go פותחת brief חדש; ייתכן שבינתיים הוא יתזמן A או C.

## 25. מתי Track B רשאי לעצור לפני PASS

- credential או owner-only action;
- שינוי ratified methodology;
- destructive/public action חדשה;
- תקרת ה־active elapsed wall-clock לפי raw seconds נוצלה (`BUDGET_EXHAUSTED`);
- שני ניסיונות מהותיים ללא שיפור;
- reference/bar אינו ניתן לבדיקה;
- contradiction בין plan למציאות.

בכל המקרים האלה Track B אינו מתחיל את השלב הבא. הוא מחזיר `BLOCKED`, `PLATEAU` או `BUDGET_EXHAUSTED` עם evidence והשאלה/החלטה המדויקת הדרושה. Partial progress אינו PASS.

## 26. כיצד נשמרת הלמידה של ירדן

אוטונומיה אינה צריכה להסתיר את reasoning. לכן:

- ה־Lead מתכנן בקול רם בתחילת ה־block, כפי שכבר דורש `engineering-role.md`;
- `workbench.md` מציג את התוצר והפערים, לא logs חסרי ערך;
- ה־Return Packet כולל decisions, rejected alternatives והכשל המשמעותי ביותר;
- מצורפות שלוש עד חמש defense questions שירדן צריך לדעת לענות עליהן לפני שה־Orchestrator מתייחס ל־checkpoint כבסיס מוכן לראיון.

כך ירדן אינו שליח בין סוכנים, אך גם אינו מקבל codebase שאינו מבין.

## 27. Dry run בתחילת ה־M1/CP-1 המאושר

אין לפתוח dry run עצמאי לפני שה־Orchestrator אישר M1/CP-1. לאחר שה־brief התקף נפתח, ה־Lead משתמש ב־artifact קטן מה־spike כחלק הראשון בתוך אותה תקרה, לפני bulk ingestion:

1. ה־Lead בוחר piece קטן ומקפיא עבורו oracle עצמאי מתוך M1-O1…M1-O5.
2. ה־Lead יוצר Builder worktree/snapshot מבודד; Builder משפר רק allowlisted paths ומחזיר changed paths/evidence בלי פעולת Git כותבת. הוא אינו כותב את expected output של ה־oracle.
3. ה־Lead מייבא ומקבע serially, מקצה `critic-run-id` ו־piece ייחודיים, מאתחל את ה־run root, יוצר ומאמת evidence ref ב־candidate `HEAD`, יוצר clean detached checkout, וה־helper מפיק create record ו־pre-review manifest hash.
4. fresh read-only Critic בודק artifact ממשי; helper verify מקבל את ה־hash ומשלים את ה־manifest, ורק לאחר הצלחה ה־Critic מפיק ומאמת schema-valid verdict record נפרד. ה־run root מכיל בסוף בדיוק שני records.
5. FAIL, אם קיים, חוזר אוטומטית ל־Builder.
6. `workbench.md` מפנה ל־verdict; records עצמם נשמרים ב־run root הייחודי תחת `.gauntlet/evidence/<checkpoint>/`.
7. לאחר final SHA/tree מריצים מחדש כל PASS קודם, ו־Integration Critic קטן מאמת מ־checkout חדש ונקי באותו SHA/tree.
8. כל evidence ref שנוצר לפני review מאומת מחדש, ונבדק שמבנה ה־Return Packet הסופי יכול לקלוט את כל הראיות.

הניסיון עובר אם ירדן לא נדרש להעביר אף הודעה פנימית, Builders לא התחרו על Git state, Critic טרי החזיר manifest מכני ו־verdict מובנה תקינים, ה־SHA נשמר ב־ref מקומי, וה־Lead ממשיך את CP-1 בלי לפתוח milestone נוסף. אין Return Packet ניסיוני נפרד באמצע; packet יחיד מוחזר רק במצב terminal של CP-1.

---

## מסקנה

היישום הנכון של המאמר בפרויקט אינו להוסיף מערכת ניהול גדולה. הוא לשנות את אופן הביצוע של Track B בתוך ה־checkpoint architecture שכבר קיימת.

ה־Orchestrator ממשיך להחליט **מתי** Track B עובד ומהו ה־checkpoint המאושר. ה־Engineering Lead מחליט **איך** להשיג את המטרה, מפרק אותה בעצמו, מבודד Builders אך נשאר Git writer יחיד, מפעיל Critics נפרדים, ומשווה artifacts ל־bars אמיתיים עד שהפער נסגר. `workbench.md` מאפשר לצפות בלי להפריע; evidence root, records מובנים ו־refs מקומיים מאפשרים לאמת את התוצאה גם לאחר שהריצה הסתיימה. Integration Critic מחבר את החלקים באותו final SHA/tree. בסוף מוחזר packet והמסלול עוצר.

במילים הקצרות של השיטה:

> מטרה שאפתנית, רף קונקרטי, Lead שבוחר את הפירוק, Builder שאינו שופט את עצמו, Critic טרי שבודק את הדבר האמיתי, ולולאה שנמשכת כל עוד נותר פער משמעותי.

---

## מקורות

- Matt Shumer, [How to Run a Gauntlet Loop](https://somethingbig.ai/gauntlet-loop)
- [הפרומפט המקורי של Claude of Duty](https://github.com/mshumer/Claude-of-Duty/blob/main/prompt.md)
- OpenAI, [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- OpenAI, [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- מסמכי Track B המקומיים המפורטים בסעיף 1
