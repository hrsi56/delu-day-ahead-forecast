"""CP-22: the Owner's explicit calendar exception for the window ending Sunday 2026-10-04 00:00 IDT.

On Saturday 2026-10-03 at 20:33 IDT the Owner wrote: "שבת יצאה. יש לך אישור מפורש ממני לעקוף את
הכלל הזה ולעבוד עכשיו. אם הוא תוקע אותך בצורה שמונעת ממך לעבוד, יש לך אישור מפורש ומלא למחוק אותו"
("Shabbat is over. You have my explicit permission to bypass this rule and work now. If it blocks
you from working, you have explicit and full permission to delete it.")

The rule is not deleted: neither the ratified anchor nor the frozen driver changes. This launcher
runs the frozen `scripts/cp22_revision.py` unchanged, with exactly one difference -- inside the
current window (before 2026-10-04 00:00 Asia/Jerusalem) its `calendar_stop` reports "outside the
window" -- so every other accounting rule and cap (machine time, workers, RSS, disk, fits,
policy-days, the active-hour stop, completion markers) stays exactly as frozen. Every use is
recorded in the ledger. From 2026-10-04 00:00 the frozen calendar applies again unchanged.

    python scripts/cp22_owner_calendar_exception.py monitor --name <job> ... -- <job command>
"""
from __future__ import annotations

from datetime import datetime
import importlib.util
from pathlib import Path
import sys
import time
from zoneinfo import ZoneInfo

JERUSALEM = ZoneInfo('Asia/Jerusalem')
GRANTED = datetime(2026, 10, 3, 20, 33, tzinfo=JERUSALEM).timestamp()
EXPIRES = datetime(2026, 10, 4, 0, 0, tzinfo=JERUSALEM).timestamp()
WORDS = ('שבת יצאה. יש לך אישור מפורש ממני לעקוף את הכלל הזה ולעבוד עכשיו. אם הוא תוקע אותך בצורה שמונעת '
         'ממך לעבוד, יש לך אישור מפורש ומלא למחוק אותו')


def main() -> int:
    spec = importlib.util.spec_from_file_location('cp22_revision', Path(__file__).with_name('cp22_revision.py'))
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    frozen = driver.calendar_stop

    def calendar_stop(now: float | None = None):
        moment = time.time() if now is None else now
        if GRANTED <= moment < EXPIRES:
            return False, EXPIRES + 5 * 86400 - moment  # the next Friday 00:00 after this window
        return frozen(now)

    now = time.time()
    if not GRANTED <= now < EXPIRES:
        raise SystemExit('the Owner exception covers only 2026-10-03 20:33 to 2026-10-04 00:00 IDT; use scripts/cp22_revision.py')
    driver.calendar_stop = calendar_stop
    if len(sys.argv) > 1 and sys.argv[1] == 'monitor':
        name = sys.argv[sys.argv.index('--name') + 1] if '--name' in sys.argv else '?'
        driver.Budget(driver.ledger_path()).event('owner_calendar_exception_used', job=name, granted_epoch=GRANTED,
                                                  expires_epoch=EXPIRES, owner_words=WORDS)
    sys.argv[0] = str(Path(__file__).with_name('cp22_revision.py'))
    return driver.main()


if __name__ == '__main__':
    raise SystemExit(main())
