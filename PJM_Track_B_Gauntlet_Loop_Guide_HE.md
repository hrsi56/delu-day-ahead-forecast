# יישום Gauntlet Loop על פרויקט ה־DE-LU Capstone — Track B

גרסה קנונית: 3.0
תאריך: 2 באוגוסט 2026
מקור השיטה: Matt Shumer, [How to Run a Gauntlet Loop](https://somethingbig.ai/gauntlet-loop)
תחום המסמך: Track B בלבד — ה־Capstone ההנדסי של חיזוי מחירי Day-Ahead באזור DE-LU
מצב חוזה: חבילת v6.4 / map v6 / חוזי התפקיד והתבניות הוטמעו כחבילת Git קנונית; operational validation ממתין לריצת CP-1 המאושרת הראשונה. M1 טרם התחיל ו־CP-1 עדיין ממתין לבריף מה־Orchestrator

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
3. לאפשר ל־Lead לבחור את הפירוק בזמן אמת; לא לקבע מראש 26 לולאות או שישה workstreams מחייבים.
4. לקבוע **חמישה** component-level critic surfaces חובה כאשר הם רלוונטיים, ולבצע fresh Integration Critic בכל checkpoint.
5. להשתמש ב־`workbench.md` זמני וקצר בלבד, לא ב־state machine מקביל; הוא אינו עובר ל־Orchestrator ונמחק/מוקפא בסיום.
6. בסוף כל checkpoint להחזיר packet יחיד, לעצור, ולאפשר ל־Orchestrator לשאול את ירדן במפורש אם לפתוח את השלב הבא.

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
- עדיין אין `tests/`, CI workflow, ingestion pipeline מלא, DuckDB mart, modeling pipeline או deployed artifact — תואם לכך ש־M1 טרם התחיל.
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

### 3.6 אין עדיין executable harness

אין כרגע tests/CI/golden fixtures, ולכן בתחילת M1 יש להקים את ה־harness שכבר נדרש על ידי v6.4. זו sequencing correction, לא scope חדש.

### 3.7 לפני התיקון, README תיאר בעיקר יעד עתידי

הפער נסגר: נוסף Current Status המבדיל בין:

- M0/spike שכבר קיימים;
- M1–M5 המתוכננים;
- commands שניתנים להרצה היום.

### 3.8 הקשר ה־root היה רחב וסותר את גבול Track B

לפני התיקון, bootstrap documents ברמת ה־root חשפו ל־Engineering Lead פרטי Orchestrator ושלושת המסלולים ואף שכפלו זה את זה. זה יצר שתי תקלות: סוכן הנדסי יכול היה לבחור לעצמו מה “השלב הבא”, ושינוי הוראה במקום אחד היה עלול לסטות מהעותק השני.

התיקון שבוצע הוא router יחיד ב־`AGENTS.md`: הוא מזהה אם ההקשר הוא Orchestrator, Engineering Lead, subagent מוגבל או תחזוקת role. `CLAUDE.md` מפנה אליו בלבד. Engineering Lead קורא בזמן ביצוע רק את ה־brief, `engineering-role.md` ותוכנית הקאפסטון המדויקת שה־brief מציין; הוא אינו קורא `progress.md`, את הסילבוס או מסלולי A/C.

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
| CP-2 — lineage ו־blind four-catalog recomputation | 5 שעות |
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
- four-catalog metric recomputation;
- ב־M3, חישוב CQR threshold על ה־fixture הידני והשוואה ל־persisted calibration predictions.

ה־Lead יכול להוסיף Critic נוסף אם הוא מגלה artifact חשוב בעל failure risk אמיתי, אך אינו מפעיל Critics באופן מכני על כל פונקציה.

### 6.5 Builder אינו מבקר את עצמו

לכל piece חשוב:

1. Builder יוצר artifact.
2. fresh Critic מקבל goal, bar, relevant rules וה־artifact.
3. ה־Critic אינו מקבל את היסטוריית ההצדקות של ה־Builder.
4. הוא בודק בפועל code, data, predictions, tests, screenshot או running product.
5. אם העבודה מפסידה ל־bar, הוא מחזיר את הפער המשמעותי ביותר.
6. ה־Lead מעביר את הפער ל־Builder בלי שירדן ישמש שליח.

### 6.5.1 בידוד Critic וראיות הניתנות לביקורת

לפני כל component Critic ה־Builder commits את המועמד. ה־Lead יוצר checkout חדש, נקי ו־detached ב־SHA המלא מחוץ לעץ העבודה של ה־Builder, באמצעות `scripts/gauntlet_critic_snapshot.sh` או מנגנון מחמיר שקול. ה־Critic אינו מקבל uncommitted diff, את שיחת ה־Builder או `workbench.md`.

כל verdict מחייב:

- candidate SHA מלא ו־artifact SHA-256;
- קובץ/גרסת התוכנית והפניית bar מדויקת;
- SHA-256 של data/input מכריעים, או סיבת `N/A` מפורשת;
- פקודות שחזור ו־tolerance צפוי;
- לפני ואחרי: אותו `HEAD` ואותו `HEAD^{tree}`, `git diff` ו־cached diff נקיים, `git status --porcelain=v1 --untracked-files=all --ignored=matching` ריק, ואין `workbench.md`;
- evidence שנבדק, verdict, הפער הגדול ביותר ומבחן הקבלה הבא.

את caches, outputs וראיות ה־Critic כותבים מחוץ ל־checkout. אין לנקות או לבצע reset לפני בדיקת ה־after-state. שינוי SHA/tree, status שאינו ריק או metadata חסר פוסלים את ה־verdict ודורשים checkout ו־Critic חדשים. ל־Integration Critic נוצר checkout חדש נוסף ב־SHA הסופי.

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

ה־Lead מתחזק `workbench.md` פשוט עם שעון/pauses, artifacts, tests, metrics ו־verdicts. הוא ignored ב־Git ואינו נכנס ל־candidate commit או ל־Critic checkout/context. זהו זיכרון עבודה פנימי בלבד: ה־Orchestrator אינו קורא אותו וירדן אינו מעביר ממנו מידע. בסיום snapshot ששמו שונה מוקפא ליד הראיות רק אם הוא ייחודי, או נמחק.

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

`workbench.md` בתוך Track B הוא state תפעולי זמני בלבד. הוא אינו רשאי לפתוח checkpoint, לשנות את התוכנית או לשמש evidence כלפי מעלה. בסיום אין active workbench: snapshot ייחודי נשמר עם ראיות ה־checkpoint, או שהקובץ נמחק.

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

### שלב 4 — Gauntlet loops

ה־Lead מפעיל Builder, מקבל candidate commit, יוצר clean detached Critic checkout לפי פרוטוקול הבידוד, מפעיל fresh read-only Critic, מעביר את הפער חזרה וממשיך. ירדן אינו משתתף ב־routing.

### שלב 5 — progress visibility

ה־Lead מעדכן `workbench.md` פנימי עם `last_updated_at_utc`, שעון/pauses ונתיבי evidence. ירדן אינו נדרש לקרוא אותו או לשאול "מה קורה?" במהלך הריצה.

### שלב 6 — integration/smoothing

כאשר כל pieces החשובים עברו, נוצר clean detached checkout חדש ב־SHA הסופי. fresh Integration Critic מריץ את ה־artifact מקצה לקצה, בודק consistency ומוודא שה־component verdicts עדיין חלים על paths ו־input hashes שלא השתנו.

### שלב 7 — עצירה והחזרה

Track B אינו מתחיל את ה־checkpoint הבא ואינו מבצע planning מפורט שלו. הוא מחזיר packet ל־Orchestrator ועוצר.

---

# חלק ד׳ — השינויים המינימליים ב־Track B

## 10. השינוי שבוצע ב־`engineering-role.md`

הסעיף כבר יושם, ולא נשאר כ־snippet להעתקה. החוזה המחייב דורש:

- brief תקף עם repo/checkpoint/anchor יחידים ותקרת active-elapsed wall-clock מספרית אחת;
- אימות מצב אמיתי ותכנון בקול רם;
- Builders ו־fresh Critics בהקשרים נפרדים;
- חמישה surfaces חובה כאשר הם רלוונטיים;
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

Orchestrator-reported expected project state:
[תמצית; Engineering Lead חייב לאמת]

Owner-only actions already authorized:
[none / פעולה מדויקת]

Run this checkpoint as a Gauntlet Loop. Choose the implementation and
decomposition yourself. Use Builders and separate fresh-context Critics for
important pieces, inspect real artifacts, and keep improving the largest gap
until the bar is met or a true blocker/resource limit is reached.

Maintain a temporary ignored internal workbench.md. Review only committed
candidates from clean detached Critic checkouts under engineering-role.md. At
checkpoint completion run a fresh isolated integration review, stop all Track B
work, and return one packet. Do not begin the next milestone.
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
- started_at_utc / last_updated_at_utc: ...
- consumed active elapsed: ... raw seconds / ... decimal hours

## Eligible pauses
| paused_at_utc | resumed_at_utc | seconds | reason/evidence | all contexts stopped? |
|---|---|---:|---|---|

## Current pieces
| Piece chosen by Lead | Artifact | Latest evidence | Critic verdict | Biggest gap |
|---|---|---|---|---|
| ... | ... | ... | PASS/FAIL | ... |

## Latest visible outputs
- tests: ...
- metrics: ...
- screenshots/plots: ...

## Open blocker or owner decision
- none / exact question

## Integration and terminal blocker
- final candidate SHA / commands / isolated Critic manifest / fresh verdict
- none / exact blocker
```

הקובץ ignored ב־Git, אינו audit log מלא ואינו מועבר ל־Orchestrator. Critics אינם מקבלים אותו והוא אינו קיים ב־checkout שלהם. לאחר Return Packet אין להשאיר אותו active: שומרים snapshot ששמו שונה לצד evidence רק אם יש בו מידע ייחודי, אחרת מוחקים.

## 13. Builder brief

```text
You are the Builder for [piece chosen by the Engineering Lead].

Goal: [observable result]
Bar: [test/reference/measurement]
Ratified constraints: [relevant sections]
File ownership: [paths]
Required artifact and evidence: [files/commands/results]

Build and commit the artifact. Return the full candidate SHA, artifact/input
hashes, and exact reproduction commands. Do not grade your own work, write the
critic verdict, close a CP item, or expand scope.
```

## 14. Critic brief

```text
You are a fresh independent, read-only Critic.

Goal: [piece goal]
Full candidate commit SHA: [sha]
Artifact path/SHA-256: [path/hash]
Exact plan filename/version and bar citation: [citation]
Decision-bearing input/data SHA-256: [hashes or N/A reason]
Exact commands and expected tolerance: [commands/bar]
Critic run/context ID: [if exposed]
Before-review integrity evidence: [snapshot helper output]

Work only in the clean detached checkout; do not inspect the Builder workspace,
uncommitted files, or workbench.md. Inspect/recompute the real artifact. Route
caches/output/evidence outside this checkout. Without cleaning/resetting, repeat
the integrity check after review. Return PASS or FAIL with bound SHA/bar/input/
command/integrity provenance, evidence inspected, the largest meaningful gap,
and the exact next acceptance test. Any dirty/changed checkout invalidates you.
```

## 15. Integration Critic brief

```text
You are a fresh read-only Integration Critic for [M#/CP-#]. Work from a new clean
detached checkout at the full final candidate SHA under the same before/after
integrity protocol.

Full final candidate commit SHA: [sha]
Final candidate artifact path/SHA-256: [path/hash]
Exact ratified plan filename/version: [filename/version]
Complete checkpoint bar citation/version: [citation]
Decision-bearing input/data SHA-256: [hashes or N/A reason]
Exact reproduction commands: [commands]
Expected output/tolerances: [bar]
Data snapshot/cutoff/hash: [date/hash]

Ignore Builder narratives. Reproduce the complete named checklist and verify
that component verdicts still bind to unchanged reviewed paths/input hashes;
rerun stale verdicts. Verify contracts, invariants, metrics, documentation, and
absence of later-checkpoint work.

Do not redesign. Return PASS only if the complete bar and provenance contract
pass. Return SHA/bar/input/command/integrity evidence; otherwise identify the
single highest-impact integration gap and exact rerun condition.
```

## 16. Checkpoint Return Packet

```markdown
# Track B Checkpoint Return — [M# / CP-#]

Status: PASS | BLOCKED | PLATEAU | BUDGET_EXHAUSTED
Target repository: ...
Ratified plan anchor: [exact anchor from brief]
Commit/branch: <sha/branch>
Working-tree state: ...
Data snapshot/cutoff: <hash/date>
Checkpoint active-elapsed ceiling: ...
started_at_utc / terminal_at_utc: ...
Eligible pause ledger: ...
Consumed active elapsed: <raw seconds / decimal hours>
Integration verdict and evidence: PASS | FAIL | NOT_RUN — <path/result or exact reason>
Integration Critic provenance manifest: <path/SHA-256>

## Complete named CP/FCP checklist
| Criterion citation | PASS/OPEN | Direct evidence/reproduction |
|---|---|---|

## Independent criticism performed
| Piece/surface | Critic/run ID | Candidate SHA/artifact hash | Bar citation/version | Input hashes | Commands | Before/after integrity | Verdict/evidence | Gap/disposition |
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

`PASS` חוקי רק כאשר הטבלה מכסה כל item ברשימת ה־CP/FCP המלאה, לכל verdict חובה יש provenance ובדיקת integrity מלאה, ואין verdict שהתיישן אחרי שינוי ה־candidate; נדרש גם fresh Integration `PASS`. שדה חסר, checkout מלוכלך או SHA/tree שהשתנו פוסלים verdict. במצב non-PASS מותר `NOT_RUN` רק עם הסיבה הטרמינלית המדויקת—`BLOCKED`, `PLATEAU` או `BUDGET_EXHAUSTED`—שמנעה את האינטגרציה.

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
- אותו data, folds, seeds ו־budget בכל ארבעת הקטלוגים;
- retention rule מיושם בדיוק;
- metrics מחושבים מחדש מ־frozen predictions;
- CI green;
- experiment hypothesis lineage;
- five-fold DM מסווג descriptive post-selection;
- forward audit quarantined עד model freeze;
- α, comparator, daily probabilistic loss, Newey–West rule, `δ*`, `LRV_ref`, `N80`, `N_required=max(90,N80)`, מינימום 12 שבועות וכלל no-reuse מוקפאים לפני unseal.

### ביקורת component-level חובה

- four-catalog metric recomputation, רצוי עם labels אנונימיים A/B/C/D עד ההכרעה.

ה־Critic מחשב את המדדים מקבצי predictions ולא מסתמך על summary של training code.

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
2. Builder משפר את היישום/בדיקות ומחזיר candidate commit; הוא אינו כותב את expected output של ה־oracle.
3. ה־Lead יוצר clean detached checkout ו־fresh read-only Critic בודק artifact ממשי לפי פרוטוקול הבידוד.
4. FAIL, אם קיים, חוזר אוטומטית ל־Builder.
5. `workbench.md` מתעד verdict.
6. Integration Critic קטן מאמת מ־checkout חדש ונקי.
7. נשמרת חבילת ראיות פנימית ונבדק שמבנה ה־Return Packet הסופי יוכל לקלוט אותה.

הניסיון עובר אם ירדן לא נדרש להעביר אף הודעה פנימית, Critic טרי החזיר SHA/bar/input/command/integrity evidence תקין, וה־Lead ממשיך את CP-1 בלי לפתוח milestone נוסף. אין Return Packet ניסיוני נפרד באמצע; packet יחיד מוחזר רק במצב terminal של CP-1.

---

## מסקנה

היישום הנכון של המאמר בפרויקט אינו להוסיף מערכת ניהול גדולה. הוא לשנות את אופן הביצוע של Track B בתוך ה־checkpoint architecture שכבר קיימת.

ה־Orchestrator ממשיך להחליט **מתי** Track B עובד ומהו ה־checkpoint המאושר. ה־Engineering Lead מחליט **איך** להשיג את המטרה, מפרק אותה בעצמו, מפעיל Builder ו־Critic נפרדים, משווה artifacts ל־bars אמיתיים וממשיך עד שהפער נסגר. `workbench.md` מאפשר לצפות בלי להפריע. Integration Critic מחבר את החלקים. בסוף מוחזר packet והמסלול עוצר.

במילים הקצרות של השיטה:

> מטרה שאפתנית, רף קונקרטי, Lead שבוחר את הפירוק, Builder שאינו שופט את עצמו, Critic טרי שבודק את הדבר האמיתי, ולולאה שנמשכת כל עוד נותר פער משמעותי.

---

## מקורות

- Matt Shumer, [How to Run a Gauntlet Loop](https://somethingbig.ai/gauntlet-loop)
- [הפרומפט המקורי של Claude of Duty](https://github.com/mshumer/Claude-of-Duty/blob/main/prompt.md)
- OpenAI, [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- OpenAI, [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- מסמכי Track B המקומיים המפורטים בסעיף 1
