# CP-22 defects, repairs and process events — disclosed, not hidden

Every job, including failed and stopped ones, is in the cumulative ledger
(`.local/artifacts/cp-22/ledger/budget.json`; summarised in `resources.json`) and charged against the §20.8
caps. No defect below touched a forecast, a selection, a score or a rule: the PN fits, the replay, the
predictions and both scoring passes ran once each, from the frozen protocol, without repair.

## Defects in diagnostic and control code (written after the pre-run freeze)

| Job (ledger index) | Defect | Effect | Repair |
|---|---|---|---|
| `investigation` (14) | The ladder-identity sum unpacked two-element pairs as three | The job failed before writing anything | Corrected the unpacking; rerun (15) |
| `investigation` (15) | The LEAR penalty-stability reader assumed every HG cache entry logs fits; the two origins without eligible hours (fold 3, 2022-07-20 and 07-21) log none | The job failed before writing anything | Origins without fits are skipped; rerun (16) completed |
| `controls` (17) | Two defects in `src/cp22/controls.py`, found by the Lead while the job ran: (a) the ladder's "PN's target and features are L-N's" checks compared arrays containing NaN (ineligible rows) without `equal_nan`, so they read False; (b) the real-data check that DL without weights or ACI reproduces R's committed H vectors replayed a DL-class state through the frozen `replay`, which keys its output on the policy's layer table and would have raised | The Lead stopped the job through its monitor after its first representative origin (recorded: `monitor_signal_15`); that origin's record, with (a) reading False, is preserved in `.local/artifacts/cp-22/logs/controls.log`. Its 82 control fits and 8 component-days stay charged | (a) compares with `equal_nan=True` against CP-21's own L-N design, with a positive control that L-P's target differs; (b) uses a local replay loop around the state. The state and population controls were exercised alone first (`controls-state-dryrun`, 18; all passed, charged as control policy-days), then the full job was rerun (19) |

## Process events

- **The calendar.** No job ran on Friday 2026-10-02 or Saturday 2026-10-03 before 20:33 IDT. On Saturday
  2026-10-03 at 20:33 IDT the Owner wrote: "שבת יצאה. יש לך אישור מפורש ממני לעקוף את הכלל הזה ולעבוד עכשיו.
  אם הוא תוקע אותך בצורה שמונעת ממך לעבוד, יש לך אישור מפורש ומלא למחוק אותו". The rule was not deleted: the
  ratified anchor and the frozen driver are unchanged. Jobs from 20:33 IDT until 2026-10-04 00:00 IDT were
  started through `scripts/cp22_owner_calendar_exception.py`, which runs the frozen monitor with only that
  window's calendar check lifted; every use is a ledger event (`owner_calendar_exception_used`).
- **Effort accounting.** The ledger counts active effort from the Lead's first command (2026-10-01 15:37:39
  IDT). The idle gaps were recorded on resumption as pauses with conservative boundaries (Thursday 16:10–21:01,
  Thursday 21:04 to Saturday 20:09 including the Friday/Shabbat window, Saturday 20:12–20:33), each with its reason.
- **A stash the Lead did not create.** On 2026-10-01 at 22:08 IDT, GitHub Desktop stashed the working tree on
  `gauntlet/cp-22` (`stash@{0}: !!GitHub_Desktop<gauntlet/cp-22>`), taking the two then-untracked, post-freeze
  modules `src/cp22/controls.py` and `src/cp22/daily.py`, and rewrote the tracked files with unchanged content.
  The Lead restored the two files from the stash (`git show stash@{0}:<path>`), verified that every frozen
  implementation file still hashes as the protocol records, and left the stash in place for the Owner.

## Results that are not defects

- `cp22-replacement` yielded no replacement (first unmet condition 4 for both R and M: fold 4 decisively
  worse). This is the rule's mechanical result, not a failure; the layer arms on W were therefore not run, and
  `cp22-dynamic-layer` and `cp22-fast-component` do not apply (§20.6).
