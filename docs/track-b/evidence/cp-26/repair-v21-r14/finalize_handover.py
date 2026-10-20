"""Account terminal evidence-only IO and close this repair's local budget scope.

This is administrative packaging, not a model/test/search job. All prior jobs must
have terminal evidence first. Its own IO body is timed and journaled explicitly.
No Git mutation, publication, experiment restart or Orchestrator-state write occurs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / 'src'))
from cp26.budget import Budget, require_compute_ready, resource_summary


def main():
    began = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('--lead', type=Path, required=True)
    parser.add_argument('--candidate', required=True)
    args = parser.parse_args()
    lead = args.lead.resolve()
    primary = Path('/Users/djourno/Downloads/PJM')
    if lead != primary / '.local/worktrees/cp-26/lead':
        raise RuntimeError('terminal package is bounded to the authorized Lead')
    evidence = lead / 'docs/track-b/evidence/cp-26/repair-v21-r14'
    local = primary / '.local/artifacts/cp-26'
    budget = Budget(local / 'ledger/budget.json')
    state = budget.read()
    require_compute_ready(state)
    if any(job['running'] for job in state['jobs']):
        raise RuntimeError('terminal package refuses unfinished worker accounting')
    if any(job.get('completion_schema') == 'cp26-completion-v2' and not job.get('workers_stopped') for job in state['jobs']):
        raise RuntimeError('terminal package refuses uncertain worker ending')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=lead, text=True).strip() != args.candidate:
        raise RuntimeError('reviewed candidate moved before evidence-only return')
    if subprocess.check_output(['git', 'status', '--porcelain=v1'], cwd=primary):
        raise RuntimeError('primary checkout changed; report mismatch')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=primary, text=True).strip() != '647d6eb81b2cf6e0cfaf4152f659d689ff973578':
        raise RuntimeError('main identity changed; report mismatch')
    if subprocess.check_output(['git', 'branch', '--show-current'], cwd=lead, text=True).strip() != 'gauntlet/cp-26':
        raise RuntimeError('Lead branch changed; report mismatch')
    review = evidence / 'repair-review-attempt-2.md'
    text = review.read_text()
    if args.candidate not in text or 'REPAIR_READY' not in text:
        raise RuntimeError('terminal package lacks the exact fresh repair-ready verdict')
    budget.record_charge('repair-r14-terminal-copy-and-import-failure-batch-v1', 1.0, 'reported',
        {'classification': 'tool-reported administrative batch elapsed; rounded, not isolated model runtime',
         'source': 'functions.exec tool result: Script completed; Wall time 1.0 seconds',
         'actions': ['copy review, metadata and two reproduction scripts', 'remove clean created review snapshot',
                     'first finalizer exited 1 at ModuleNotFoundError before any writes/charge'],
         'all_commands_terminal': True, 'no_model_fits': True})
    rows = []
    for job in state['jobs']:
        if not job['name'].startswith('repair-r14-'):
            continue
        dest = evidence / 'runs' / job['name']
        dest.mkdir(parents=True, exist_ok=True)
        sources = [Path(job['log']), local / 'jobs' / (job['name'] + '.json')]
        sources += [Path(job[key]) for key in ('request', 'progress_clock', 'completion_clock') if job.get(key)]
        hashes = {}
        for source in sources:
            if not source.resolve().is_relative_to(local.resolve()):
                raise RuntimeError('receipt outside project custody')
            if source.exists():
                target = dest / source.name
                shutil.copy2(source, target)
                hashes[str(target.relative_to(lead))] = hashlib.sha256(target.read_bytes()).hexdigest()
        rows.append({'name': job['name'], 'workers': job['workers'], 'wall_seconds': job['wall_seconds'],
                     'machine_seconds': job['wall_seconds'] * job['workers'], 'exit_code': job['exit_code'],
                     'abort_reason': job['abort_reason'], 'files_sha256': hashes})
    index = json.loads((evidence / 'run-receipts.json').read_text())
    index['completed_runs'] = rows
    index['rule'] = 'all ended repair jobs preserved, including failed checks; terminal administrative IO is a separate measured charge in terminal-ledger.json'
    (evidence / 'run-receipts.json').write_text(json.dumps(index, indent=2) + '\n')
    builder_inventory = json.loads((local / 'repair-v21-r14/builders/inventory.json').read_text())
    created = []
    for item in builder_inventory['worktrees']:
        if Path(item['path']).exists():
            raise RuntimeError('created Builder worktree still exists')
        created.append({**item, 'terminal_state': 'allowed paths imported; recovery packet retained; created worktree removed'})
    for name, seed in [('repair-review-c1e46', 'c1e46c41bd83e7e91082fd4f9c626aed1de72a03'),
                       ('repair-review-68d5db5', args.candidate)]:
        path = primary / '.local/worktrees/cp-26' / name
        if path.exists():
            raise RuntimeError('created review snapshot still exists')
        created.append({'path': str(path), 'seed_sha': seed, 'purpose': 'clean detached bounded repair review',
                        'terminal_state': 'review preserved; created snapshot removed; no source/Git change'})
    removed_tmp = []
    for name in ['repair-core-tests', 'repair-monitor-tests', 'repair-final-tests', 'repair-stable-tests',
                 'repair-pgid-fix-tests', 'repair-critic-tests', 'repair-fresh-critic-tests']:
        path = primary / '.local/tmp/cp-26' / name
        if path.exists():
            shutil.rmtree(path)
            removed_tmp.append(str(path))
    lifecycle = {'schema': 'cp26-repair-local-lifecycle-v1', 'created_worktrees': created,
        'created_branches': [], 'created_tags': [], 'removed_refs': [],
        'retained_branch': {'name': 'gauntlet/cp-26', 'owner': 'existing CP-26 Owner/Lead',
            'purpose': 'repair candidate and reviewable evidence chain', 'repair_candidate_sha': args.candidate,
            'ahead_behind_main_at_candidate': '7 ahead, 0 behind',
            'disposition': 'leave open for Owner/main agent review; no LAND/discard/ref reclamation authorized'},
        'retained_worktrees': [str(primary), str(lead)], 'removed_disposable_test_directories': removed_tmp,
        'retained_recovery': ['.local/artifacts/cp-26/repair-v21-r14/initial/',
            '.local/artifacts/cp-26/repair-v21-r14/builders/', '.local/artifacts/cp-26/ledger/',
            '.local/artifacts/cp-26/jobs/', '.local/artifacts/cp-26/logs/', '.local/artifacts/cp-26/clocks/',
            '.local/tmp/cp-26/repair-*-message.txt and packaging/reproduction scripts'],
        'rule': 'only worktrees and disposable test directories created for this repair were removed; main and Lead remain'}
    (evidence / 'local-lifecycle.json').write_text(json.dumps(lifecycle, ensure_ascii=False, indent=2) + '\n')
    # Create all terminal names before the exhaustive per-file inventory.
    for name in ['terminal-resources.json', 'terminal-ledger.json', 'repair-return.md', 'files-changed.json']:
        (evidence / name).touch(exist_ok=True)
    reasons = runpy.run_path(str(evidence / 'build_handover.py'))['reason']
    changed = set(subprocess.check_output(['git', 'diff', '--name-only', '5cc3cc083c4340fd8d792eeaf6551a007987a877', 'HEAD'], cwd=lead, text=True).splitlines())
    changed.update(subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=lead, text=True).splitlines())
    changed.update(subprocess.check_output(['git', 'diff', '--name-only'], cwd=lead, text=True).splitlines())
    (evidence / 'files-changed.json').write_text(json.dumps({'schema': 'cp26-repair-file-reasons-v1',
        'initial_head': '5cc3cc083c4340fd8d792eeaf6551a007987a877',
        'landed_code_base': '647d6eb81b2cf6e0cfaf4152f659d689ff973578', 'repair_candidate_sha': args.candidate,
        'files': [{'path': name, 'reason': reasons(name)} for name in sorted(changed)]}, ensure_ascii=False, indent=2) + '\n')
    seconds = time.monotonic() - began
    budget.record_charge('repair-r14-terminal-bookkeeping-v1', seconds, 'measured',
        {'classification': 'measured administrative evidence IO body', 'command': [os.sys.executable, '-B', str(Path(__file__).resolve()), '--lead', str(lead), '--candidate', args.candidate],
         'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'no_model_fits': True})
    with budget.transaction() as state:
        state['rule'] = 'total = measured + reported + authorized reserves; supervised worker wall seconds x allocated workers, plus separately timed maintenance bodies; idle restart gaps excluded'
        state['repair_scope']['active'] = False
        state['repair_scope']['terminal_candidate_sha'] = args.candidate
        state['events'].append({'event': 'repair-v21-r14-terminal-evidence-ready', 'epoch': time.time(),
                                'candidate_sha': args.candidate, 'cp26_status': 'INCOMPLETE', 'experiment_resume_authorized': False})
    state = budget.read()
    resources = {**resource_summary(state), 'remaining_to_pilot_stop_hours': 388 - resource_summary(state)['machine_hours'],
                 'peaks': state['peaks'], 'counts': state['counts'], 'jobs_running': [],
                 'reserve_explanation': '2826 seconds authorized conservative failed-audit reserve; not measured, not reduced; 15.01 lower bound not charged twice',
                 'terminal_bookkeeping_body_seconds': seconds}
    (evidence / 'terminal-ledger.json').write_text(json.dumps(state, indent=2) + '\n')
    (evidence / 'terminal-resources.json').write_text(json.dumps(resources, ensure_ascii=False, indent=2) + '\n')
    report = f'''# החזרת תיקון CP-26 — v21-r14

מצב התיקון: **REPAIR_READY**. מצב CP-26: **INCOMPLETE**. גרסת r14 מועמדת לבדיקת הבעלים ולאשרור; הניסוי אינו מתחדש אוטומטית. אין Integration PASS של CP-26.

`repair_candidate_sha`: `{args.candidate}`. הביקורת הטרייה ב־`repair-review-attempt-2.md` קשורה ל־SHA הזה. ה־commit האחרון מוסיף ראיות בלבד; ה־SHA הסופי יימסר בהודעת ההחזרה ובחבילת Git המקומית, בלי מזהה עצמי מעגלי.

## זהויות וקבלה

עוגן r14: `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`, commit עוגן `332baeb861cec5a58516c58a29a1a3afe1eec909`. גיליון התיקון: `554a3aa4bf81f3fc1cc2319e624295570f919ff1fd4a6d9e2c9f56f8dcf6b79a`.

בריף התיקון: `5b6a0cdfad870da6b59a03ff29576ff6ec98891e941d56986516e6f3f743ff84`; פרוטוקול CP-28 החדש: `2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8`; manifest: `aa29af82181769afefdb0a4446057dd08f7ebafaac27a398aa2679397a3cadfe`. מקור r13 והבריפים המקוריים נשמרו, עם hashes וסיבות supersession ב־`active-documents.json`.

88 בדיקות ממוקדות עברו אצל ה־Lead; הביקורת העצמאית הטרייה הריצה שוב 88 בהצלחה. 96 בדיקות parity עדכניות בהגדרות הישנות עברו. לא בוצעו אימוני CP-26 חדשים, חיפוש אמיתי, פיילוט, replay של לוח הניסוי, ציוני ניסוי או זרועות CP-28.

תמיכת 14 המועדים × שלושה מסלולים שוחזרה: `B=[1,7,11,…,11]`; בחלון הראשון מינימום `251/46`. האלגוריתם נשען על המסכה וכלל השבועות שנחתו, ולא על המספרים המצופים. `S_13=2026-07-08`, `S_14=2027-01-06` הם מועדי פרוטוקול; לא נקראו נתונים עתידיים.

ה־checklist המלא, הפקודות והגבולות נמצאים ב־`README.md`; כל argv, תוצאה, משך וקבלה נשמרו ב־`runs/` ו־`run-receipts.json`, לרבות בדיקות שנכשלו. הביקורת הראשונה מצאה כשל בבעלות על PGID והוחזרה כ־REPAIR_INCOMPLETE. הכשל תוקן ונבדק במועמד החדש; ניסיון הביקורת והסטייה הפרוצדורלית שבו נשמרו ולא משמשים כאישור הסופי.

## חשבון משאבים

זמן נמדד: {resources['measured_seconds']:.12f} שניות; זמן מדווח: {resources['reported_seconds']:.3f}; רזרבה מאושרת: {resources['reserved_seconds']:.0f}. סך הכול: {resources['total_seconds']:.12f} שניות, {resources['machine_hours']:.9f} שעות מכונה. כל בדיקת תקציב כוללת את שלוש הקטגוריות.

בתיקון החדש נוצלו {resources['repair_seconds_used']:.12f} שניות; נותרו {resources['repair_seconds_remaining'] / 3600:.9f} מתוך 10 השעות שהוקצו. היתרה המצטברת לתקרת 485: {resources['headroom_hours']:.9f} שעות. המרווח לקו עצירת פיילוט 388: {resources['remaining_to_pilot_stop_hours']:.9f} שעות. מסגרת התיקון סומנה כסגורה ביומן; ההיסטוריה לא אופסה.

547.5647564170067 השניות ההתחלתיות כללו כבר 6.125 שניות מוקדמות. נוספו פעם אחת 90.127 שניות מדווחות; הסכום ההיסטורי המדווח הוא 96.252. נוספה שנייה אחת כמשך כולל מעוגל שדיווח הכלי על מקבץ IO סופי, הסרת snapshot והפעלת אורז שנכשלה בייבוא לפני כתיבה; היא אינה זמן מודל שנמדד. נתיב הייבוא תוקן. 2826 השניות הן רזרבה שמרנית לכשל הביקורת, לא מדידה. 15.01 הן גבול תחתון ולא חיוב נוסף. `audit-time-bound.json` מאמת שהפעולה תחומה בין סיום parity לקבלת הביקורת. רזרבה זו לא הוקטנה. היומן השלם והפסגות ב־`terminal-ledger.json` ו־`terminal-resources.json`; אין workers תלויים. CPU בלבד, BLAS 1, אפס הורדות ואפס כתיבות מרחוק.

## Git, קבצים ומחזור חיים

הבסיס שנחת נשאר `647d6eb81b2cf6e0cfaf4152f659d689ff973578`; main נקי. הענף הקיים `gauntlet/cp-26` וה־Lead נשארים לביקורת הבעלים/הסוכן הראשי. לא נוצרו ענפים או tags ולא נמחקו refs. כל חמשת worktrees המבודדים שנוצרו לתיקון הוסרו לאחר יבוא/שימור ראיות; לא הוסר worktree קיים. הפירוט, seeds, חבילות התאוששות ו־scratch שהוסר ב־`local-lifecycle.json`.

`files-changed.json` מונה כל קובץ ששונה עם סיבה. diff מלא של התיקון למועמד, diff מקור ממוקד ושני diff stats נמצאים ב־`reports/rebaseline/repair-v21-r14/`. diff סופי מלא ומצב Git אחרי commit הראיות יישמרו גם ב־`.local/artifacts/cp-26/repair-v21-r14/final-git/`; כל בתיהם ניתנים לשחזור מה־SHAs המקומיים השמורים. אין staging או commit ב־main. ה־hooks נשארו פעילים וכל commit מקומי נעשה עם `git commit -F`.

## מה נותר לפני הניסוי

נדרשים בדיקת הבעלים ואשרור הבתים המדויקים של r14, ובריף המשך המחייב את זהויות העוגן/המקור/הפרוטוקולים, בסיס הקוד שנחת, מסכות CP-25, הגבול 2026-09-06, זמן ההנפקה, ציונים והסקה ללא שינוי. יש לתמחר את כל 42 החיפושים ואת יתרת העבודה, לרבות היסטוריה ורזרבות, מול 388 שעות לפני ריצה מלאה.

פרימיטיבי החיפוש, ההתאמות, ההנפקות, replay, המטמונים והמצב הרציף נבנו ונבדקו; חיבור CLI של הניסוי כולו, תזמון/חידוש מלא של משימות והפקת קובצי ציונים/הסקה עדיין דורשים השלמה ואימות בבריף ההמשך. חיפושים אמיתיים, פיילוט 14 origins, replay מלא, scoring, bootstrap, diagnostics, חבילת הדיווח והביקורת הרשמית של CP-26 טרם בוצעו. פרוטוקול CP-28 הוקפא כמועמד; הזרועות לא מומשו ולא הורצו.

הביקורת מתעדת גם אי־דיוק P3 היסטורי בניסוח startup של CP-28: הטבלה והמשפט הספציפי קובעים A4←A3 עד 728, לצד משפט כללי על w0. כללי המשקולות והקטעים ההיסטוריים נשמרו; יש להבהיר בבריף ההמשך את הקדימות של הכלל הספציפי. תמיכה ו־parity אינם מבטיחים התכנסות, עלות, הצלחה מדעית או ארבע תצורות תקינות.

## גילוי ותיעוד

לא נצפה ערך credential ולא הייתה חשיפה חדשה. טריגרים לתיעוד ראיון בידי ה־Orchestrator בלבד: כשירות לכל פיצול שבועות; התאוששות מרכזית מקורית בלי שינוי רטרואקטיבי של גיבוי; הפרדת כשירות ציון/H/ledger; זמן מדוד/מדווח/רזרבה; ותיקון הסיכון שבזיהוי תהליך לפי PID/PGID ממוחזר.

Post-return reads: none. לא נקראו progress.md, orchestrator-role.md, syllabus או חומרי Track A/C; לא השתנה מצב תוכנית או integration.md. ההשעיה התחומה מסתיימת בהחזרה הסופית. אין חידוש אוטומטי של הניסוי.
'''
    (evidence / 'repair-return.md').write_text(report)
    print(json.dumps({'status': 'REPAIR_READY', 'cp26': 'INCOMPLETE', 'candidate': args.candidate,
                      'files_explained': len(changed), 'completed_jobs_preserved': len(rows), 'resources': resources}, ensure_ascii=False))


if __name__ == '__main__':
    main()
