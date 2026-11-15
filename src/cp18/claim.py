"""One issuance per delivery day across the runner and the local fallback: the claim.

**The rule.** The day's issued record on the product repository's `main` is the claim.
- **Fetch before issuing.** Before each day, the pipeline fetches `main` and checks out exactly that commit (detached,
  on a clean tree), then reloads and verifies the store. A day already decided there is never issued again.
- **Push after issuing.** The day's records are committed on top of that commit, with the secret guard, the leak scan
  and the publication guard running as git hooks (`core.hooksPath` must resolve to the repository's `.githooks`, or
  nothing is committed), and pushed as a fast-forward of `main`. Nothing is ever force-pushed.
- **A moved `main` that touches none of this commit's own files: the records are re-applied** (the Orchestrator's
  O47, CP-18d). If `main` moved while the day was being issued or recorded, the push is refused as a non-fast-forward.
  The claim fetches the new `main` and reads every file each moved commit touched (`base..theirs`). When none of them
  is one of this commit's own files, and all of its own files are under `live/`, it commits the same files with the
  same content on top of the new `main` (through the same hooks) and pushes again, a fast-forward: nothing another
  writer made is overwritten, nothing is force-pushed, and no path outside `live/` is written. On the first runner
  day a documentation commit pushed during the records step made the claim discard that run's records; this keeps
  them. It retries at most `REAPPLY_ATTEMPTS` times.
- **The loser of a push race discards its own issuance.** When a moved commit touched any of this commit's own files
  (another host's issuance or records: the store's ledger, the same archive day, the same as-of day's records), the
  claim checks out the new `main` (its own commit, which no ref names, is dropped), and the pipeline stops the run:
  the other host's record is the day's issuance, and nothing is replaced, rescored or relabelled. A push refused for
  any other reason (a guard, the network) is not a lost race: the run fails closed and publishes nothing.

The git commands run in the pipeline's own checkout: a fresh one on the runner, a dedicated clone on the Owner's Mac.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess

IDENTITY = {'GIT_AUTHOR_NAME': 'delu-daily', 'GIT_AUTHOR_EMAIL': 'delu-daily@users.noreply.github.com',
            'GIT_COMMITTER_NAME': 'delu-daily', 'GIT_COMMITTER_EMAIL': 'delu-daily@users.noreply.github.com'}


LIVE = 'live/'
REAPPLY_ATTEMPTS = 3


class ClaimError(RuntimeError):
    """The checkout cannot be synchronized or published safely; the run publishes nothing."""


class Claim:
    def __init__(self, repo, remote: str = 'origin', branch: str = 'main', env: dict | None = None):
        self.repo, self.remote, self.branch = Path(repo), remote, branch
        self.env = {**os.environ, **IDENTITY, 'GIT_TERMINAL_PROMPT': '0', 'GIT_PAGER': 'cat', 'GIT_EDITOR': 'true',
                    **(env or {})}

    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        done = subprocess.run(['git', '-C', str(self.repo), *args], capture_output=True, text=True, env=self.env)
        if check and done.returncode != 0:
            raise ClaimError(f'git {args[0]} failed (exit {done.returncode}): {done.stderr.strip()[-600:]}')
        return done

    def remote_ref(self) -> str:
        return f'refs/remotes/{self.remote}/{self.branch}'

    def head(self) -> str:
        return self.git('rev-parse', 'HEAD').stdout.strip()

    def hooks_active(self) -> bool:
        """`core.hooksPath` resolves to this checkout's `.githooks` (relative or absolute)."""
        value = self.git('config', '--get', 'core.hooksPath', check=False).stdout.strip()
        if not value:
            return False
        path = Path(value) if Path(value).is_absolute() else self.repo / value
        return path.resolve() == (self.repo / '.githooks').resolve()

    def fetch(self) -> str:
        self.git('fetch', '--quiet', '--no-tags', self.remote,
                 f'+refs/heads/{self.branch}:{self.remote_ref()}')
        return self.git('rev-parse', self.remote_ref()).stdout.strip()

    def sync(self) -> str:
        """Fetch `main` and check out exactly that commit, detached, on a clean tree."""
        if self.git('status', '--porcelain', '--untracked-files=all').stdout.strip():
            raise ClaimError('the pipeline checkout has uncommitted changes; it never issues over them')
        tip = self.fetch()
        self.git('checkout', '--quiet', '--detach', tip)
        return tip

    def moved(self) -> bool:
        """Whether `main` on the remote has moved past this checkout's base since the last sync."""
        before = self.git('rev-parse', self.remote_ref()).stdout.strip()
        return self.fetch() != before

    def changed(self, a: str, b: str) -> list[str]:
        """The files one commit range changes (renames as a deletion and an addition)."""
        out = self.git('diff', '--name-only', '--no-renames', a, b).stdout.split('\n')
        return sorted(x for x in out if x)

    def touched(self, base: str, theirs: str) -> tuple[list[str], list[str]]:
        """Every file any commit in `base..theirs` touched (not only the net difference), and those commits."""
        commits = [c for c in self.git('rev-list', '--reverse', f'{base}..{theirs}').stdout.split() if c]
        names = self.git('log', '--format=', '--name-only', '--no-renames', f'{base}..{theirs}').stdout.split('\n')
        return sorted({x for x in names if x}), commits

    def _reapply(self, mine: str, base: str, theirs: str, message: str) -> str:
        """`mine`'s own files, with its content, committed on `theirs` through the hooks; checked file by file."""
        own = self.changed(base, mine)
        self.git('checkout', '--quiet', '--detach', theirs)
        present = [p for p in own if self.git('cat-file', '-e', f'{mine}:{p}', check=False).returncode == 0]
        gone = [p for p in own if p not in present]
        if present:
            self.git('checkout', mine, '--', *present)
        for path in gone:
            self.git('rm', '--quiet', '--ignore-unmatch', '--', path)
        done = self.git('commit', '--quiet', '-m', message, check=False)
        if done.returncode != 0:
            self.git('reset', '--quiet', '--hard', theirs)
            raise ClaimError(f'the re-applied commit was refused (a guard?): {done.stderr.strip()[-600:]}')
        new = self.head()
        if self.changed(theirs, new) != own:
            raise ClaimError('the re-applied commit does not change exactly its own files')
        for path in present:
            if self.git('rev-parse', f'{new}:{path}').stdout != self.git('rev-parse', f'{mine}:{path}').stdout:
                raise ClaimError(f'{path}: the re-applied content differs from the original commit')
        return new

    def publish(self, paths: list[str], message: str, *, before_push=None) -> dict:
        """Commit `paths` on the synchronized commit and fast-forward `main`. Returns {'pushed': sha} (with
        'reapplied' when `main` had moved by commits touching none of this commit's files, O47) or, when another
        writer's commit touched one of them, {'lost': True, 'theirs': sha, 'overlap': [...]} after discarding this
        commit. `before_push` (rehearsals only) runs once before the first push."""
        if not self.hooks_active():
            raise ClaimError('core.hooksPath does not point at the checkout\'s .githooks: nothing is committed '
                             'without the secret guard and the leak scan')
        base = self.git('rev-parse', self.remote_ref()).stdout.strip()
        if self.head() != base:
            raise ClaimError('the checkout is not on the synchronized main; nothing is committed')
        self.git('add', '--', *paths)
        if not self.git('diff', '--cached', '--name-only').stdout.strip():
            return {'pushed': None, 'nothing': True}
        done = self.git('commit', '--quiet', '-m', message, check=False)
        if done.returncode != 0:
            self.git('reset', '--quiet')                  # unstage only; the files stay for the run's own record
            raise ClaimError(f'the commit was refused (a guard?): {done.stderr.strip()[-600:]}')
        mine, first = self.head(), self.head()
        own = self.changed(base, mine)
        reapplied = []
        if before_push is not None:
            before_push()
        for attempt in range(REAPPLY_ATTEMPTS + 1):
            pushed = self.git('push', '--quiet', '--porcelain', self.remote, f'HEAD:refs/heads/{self.branch}', check=False)
            if pushed.returncode == 0:
                self.fetch()
                return {'pushed': mine, **({'reapplied': reapplied, 'original': first} if reapplied else {})}
            theirs = self.fetch()
            ancestor = self.git('merge-base', '--is-ancestor', base, theirs, check=False).returncode == 0
            if theirs == base or not ancestor:
                self.git('checkout', '--quiet', '--detach', base)
                raise ClaimError(f'the push was refused and main did not move (a guard or the network): '
                                 f'{pushed.stderr.strip()[-600:]}')
            touched, commits = self.touched(base, theirs)
            overlap = sorted(set(touched) & set(own))
            outside = [p for p in own if not p.startswith(LIVE)]
            if overlap or outside or attempt == REAPPLY_ATTEMPTS:
                self.git('checkout', '--quiet', '--detach', theirs)     # this commit, named by no ref, is dropped
                why = ('the moved main touched this commit\'s own files' if overlap else
                       'this commit writes outside live/, so it is never re-applied' if outside else
                       f'main kept moving ({REAPPLY_ATTEMPTS} re-applications)')
                return {'lost': True, 'theirs': theirs, 'discarded': mine, 'overlap': overlap, 'outside': outside,
                        'why': why, **({'reapplied': reapplied} if reapplied else {})}
            new = self._reapply(mine, base, theirs, message)
            reapplied.append({'over': theirs, 'moved_by': commits, 'touched': touched, 'original': mine,
                              'reapplied': new})
            base, mine = theirs, new
        raise AssertionError('unreachable')  # pragma: no cover
