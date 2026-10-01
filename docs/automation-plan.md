# Automation plan: scripts, skills and hooks

Role-maintenance analysis, 2026-10-01. Proposal only: nothing below is implemented. Claude Code
capabilities were checked against code.claude.com/docs (hooks, skills, permissions) on 2026-10-01.

**Lockdown, stated once.** Every hook, permission rule and skill lives under `.claude/**`, which
`AGENTS.md:23-24` locks as agent configuration. Items 2, 3, 9 and 10 therefore need one Owner
suspension naming `.claude/settings.json`, `.claude/skills/critic/` and `.claude/skills/handover/`.
Once created, those files are protected by the same lock. The scripts and the Makefile target
(items 1, 4–8) touch no locked file.

## Summary

| # | Item | Destination | Saving | Effort |
|---|---|---|---|---|
| 1 | Checkpoint identity, return and receipt verifier | Script | ~45 hand-written return lines and 8–10 receipt commands per checkpoint, for both Lead and Orchestrator; removes the most common causes of an invalid `PASS` | M |
| 2 | Integration Critic launcher `/critic` | Skill (`context: fork`) | One 60–100-line hand-written assignment per Critic run (often two per checkpoint); the Critic's isolation is enforced by the harness instead of by procedure | S, after 1 and 4 |
| 3 | Session start: enable the guard and report the git state | Hook (SessionStart) | One Owner instruction and 3–5 state commands in every session, for every role; closes a gap where the secret guard silently stops running | S |
| 4 | Plan checklist extractor and brief checker | Script | The checklist is copied by hand into 4 documents per checkpoint and byte-checked twice; brief validation is done by reading, twice | S |
| 5 | Post-deploy publication receipt | Script | Identity records for 5 surfaces are built by hand at each publication; the future daily pipeline can reuse the script | M |
| 6 | Checkpoint disposition and reclamation | Script | ~12 commands and a citation search per closed checkpoint | S–M |
| 7 | Pre-review check runner | Script + `make prerelease` | ~7 checks run and recorded one at a time per publication | S |
| 8 | `progress.md` omission diff | Script | A manual diff of an 81 KB file at each state update | S |
| 9 | End-of-task handover packet `/handover` | Skill | The format and 3 git commands recalled at the end of every non-checkpoint task | XS |
| 10 | Credential-store deny rules | Hook layer (`permissions.deny`) | Turns a rule that must be remembered in every session into a harness setting | XS |

Build order: 4 → 1 → 3 → 2 → 6, then 5, 7, 8, 9 and 10.

---

## 1. Checkpoint identity, return and receipt verifier

1. **Capability:** Records the repository topology when a checkpoint starts. At return, prints the
   *Identity* and *Repository state* blocks of the checkpoint return, ready to paste. In receipt
   mode, runs the Orchestrator's checks and prints PASS or FAIL for each one.
2. **Current location and control:** `engineering-role.md:36` (verify state), `:45-52` (two SHAs,
   verdict-only delta), `:107` (reachability before return); `docs/track-b/gauntlet-templates.md:134-145`
   and `:183-193`; `orchestrator-role.md:327-339`. An agent runs these by hand at the checkpoint's
   start, at its return and at receipt, working from memory and reasoning. CP-21 spent 45
   hand-written lines on these blocks (`docs/track-b/evidence/cp-21/checkpoint-return.md:16-60`).
   CP-16 kept ad-hoc `main-state.txt` and `handover-state.json`.
3. **Destination:** Script. It is pure git, needs no judgment, and the same inputs always give the
   same output.
4. **Implementation:** `scripts/gauntlet.py` (stdlib and git):
   - `start <cp>`: writes `.local/tmp/<cp>-start.json` with HEAD, `main`, the local
     `origin/main` (no fetch), `worktree list --porcelain`, `for-each-ref refs/heads refs/tags`,
     the stash list and the porcelain status.
   - `return <cp> <final_candidate_sha> [<evidence_tip>=HEAD]`: checks that
     `diff --name-only` stays inside `docs/track-b/evidence/<cp>/`. Runs `cat-file -e` and
     `merge-base --is-ancestor … gauntlet/<cp>` on every 40-hex SHA cited in that folder.
     Checks that the verdict exists, reads `PASS` and cites `final_candidate_sha`. Lists the
     branches, worktrees, tags and stashes created since `start`, and compares the issued brief's
     SHA-256 with the canonical copy. Prints the markdown blocks plus the evidence tip for the
     terminal message, since a file cannot contain its own commit SHA. Exits 1 if any check fails.
   - `receipt <cp> <final> <tip>`: runs only the commands listed at `orchestrator-role.md:330-334`
     and `gauntlet-templates.md:186-190`, and prints one row per check.
5. **Notes:** No locked file is edited. Receipt mode must stay inside the Orchestrator's command
   list, which `orchestrator-role.md:337` declares exhaustive: no source reads and no tests. Item 3
   can write the `start` snapshot automatically. Citing the script from the templates is optional
   and would need a suspension for `gauntlet-templates.md`.

## 2. Integration Critic launcher `/critic`

1. **Capability:** Launches the one fresh Integration Critic. The Critic gets the full assignment
   and protocol, works in a clean detached worktree, and does not see the Lead's conversation.
2. **Current location and control:** `engineering-role.md:41` and `:56-73`;
   `docs/track-b/gauntlet-templates.md:70-120`. The Lead writes each assignment by hand. For
   example, `docs/track-b/evidence/cp-20/integration-assignment.md` holds the worktree command,
   the plan's SHA-256, a ~30-line verbatim excerpt and the no-Git-write rules. The Lead also
   creates and removes the worktree. Isolation is "cooperative" (`engineering-role.md:73`). There
   are often several runs per checkpoint: CP-20 had `integration-attempt-1` and `integration-2`;
   CP-21 had `critic` and `critic-2`.
3. **Destination:** Skill with `context: fork`. According to the docs, a forked skill "doesn't see
   your conversation history" and receives the skill content as its prompt. That makes "Receive
   the artifact, never the Builder's story" (`engineering-role.md:67`) a property of the harness
   rather than a rule the Lead must follow. The deterministic steps stay in the scripts from items
   1 and 4.
4. **Implementation:**
   - **Before the review:** the Lead writes a short assignment containing only the judgment
     fields: plan path, section heading, reproduction commands and tolerance. The Lead then runs
     `gauntlet.py critic-open <cp> <sha> <assignment>`. This creates
     `.local/worktrees/<cp>/critic-<n>`, checks that it is clean and that `HEAD` equals the SHA,
     and records the details in `.local/tmp/critic-open.json`.
   - **`.claude/skills/critic/SKILL.md` frontmatter:** `context: fork`,
     `agent: general-purpose`, `disable-model-invocation: true` (the Lead decides when the
     candidate is final), and `allowed-tools: Bash(python3 scripts/gauntlet.py *)`.
   - **Skill body:** `` !`python3 scripts/gauntlet.py critic-brief` `` injects the assignment, the
     plan's SHA-256 and the verbatim excerpt (via item 4) before the subagent starts. Fixed text
     follows: the protocol from `engineering-role.md:56-73` and the verdict form from templates §2.
     The Critic writes `docs/track-b/evidence/<cp>/integration.md` and performs no Git write.
   - **After the review:** the Lead runs `gauntlet.py critic-close`, which checks that the
     worktree is still clean and `HEAD` is unchanged, removes the worktree and hashes the verdict.
     The Lead then commits the verdict as the sole Git writer (`engineering-role.md:39`).
5. **Notes:** Needs the `.claude/skills/critic/` suspension. `engineering-role.md` needs no change,
   because the skill implements its protocol. A failing `!` command aborts the skill, so a dirty
   worktree stops the review before it starts. The skill follows the current worktree practice
   (`.local/worktrees/…`, `AGENTS.md:65-72`), but `engineering-role.md:62` still says
   `<path-outside-repo>`. The Owner may want to align that line at a future suspension; it is not
   required. Depends on items 1 and 4.

## 3. Session start: enable the guard and report the git state

1. **Capability:** At every session start, resume, clear or compaction:
   (a) points `core.hooksPath` at the main checkout's `.githooks` when it is unset or points to a
   directory without `pre-commit`;
   (b) prints at most 10 lines of git state;
   (c) writes the ref snapshot that item 1 uses.
2. **Current location and control:** `AGENTS.md:103-107` assumes `core.hooksPath` is set, but
   nothing sets it in a fresh clone or cloud container. This session started with it unset, and
   the Owner had to give the `git config` instruction. Git also commits without running any hook
   when `core.hooksPath` points to a missing directory, for example after the worktree that set it
   is removed (tested 2026-10-01). In that case the secret guard silently stops running. The state
   check in `engineering-role.md:36` and the branch declaration in `AGENTS.md:183` are done by
   hand.
3. **Destination:** Hook: `SessionStart` with matcher `startup|resume|clear|compact`, command
   `python3 "$CLAUDE_PROJECT_DIR/scripts/session_start.py"`. Its stdout reaches the agent's context.
4. **Implementation:** The script:
   - finds the main checkout with `git rev-parse --path-format=absolute --git-common-dir`;
   - sets `core.hooksPath` only if it is unset or broken, and says so in one line;
   - prints the branch, short HEAD, `main` ahead/behind `origin/main` (no fetch), the number of
     dirty files, the worktrees, any `gauntlet/*` branches and the stash count;
   - writes `.local/tmp/session-<session_id>-refs.json`.
   It uses only the standard library, always exits 0, and reports its own errors as one line.
5. **Notes:** Needs the `.claude/settings.json` suspension. It must print only git state: never
   `progress.md`, role documents or anchors, because an Engineering Lead may not read
   `progress.md` before its verdict (`AGENTS.md:116`). It enables the guard and never bypasses it
   (`AGENTS.md:106`). SessionStart hooks also run in Claude Code on the web.

## 4. Plan checklist extractor and brief checker

1. **Capability:**
   - `bar <plan> "<heading>" [--at SHA]` prints a plan section verbatim, from its heading to the
     next heading of the same or higher level, together with the plan's SHA-256 at that commit.
   - `check <file> --plan <plan> --at <sha>` checks that every `>`-quoted excerpt in a brief,
     assignment or verdict appears byte for byte in the plan at that commit.
   - `brief <brief.md>` checks the brief. All ten required fields must be present
     (`engineering-role.md:19-30`), with no `[...]` placeholders left, one checkpoint and one
     numeric timebox. The plan file must exist and the cited section must resolve. It also prints
     the brief's SHA-256.
2. **Current location and control:** `orchestrator-role.md:204` (validation before dispatch) and
   `:220-222` (the Lead validates the brief again); `engineering-role.md:58`, `:69` and `:109`
   (an excerpt missing from the plan invalidates `PASS`); `docs/track-b/gauntlet-templates.md:81-84`,
   `:101-103` and `:150`. Each is done by reading and copying by hand. CP-16's Critic
   re-implemented the extraction in `docs/track-b/evidence/cp-16/critic-audit.py`.
3. **Destination:** Script. The work is text extraction and byte comparison.
4. **Implementation:** `scripts/bar.py` uses only the standard library and reads the plan with
   `git show <sha>:<plan>`. Headings must match exactly. Only the `> ` quote prefix is stripped
   before comparison. On failure it exits 1 and prints the first line that does not match.
5. **Notes:** No locked file is edited. It checks form only: the brief's content (what to build,
   the timebox) stays the Orchestrator's decision. Items 1 and 2 use it.

## 5. Post-deploy publication receipt

1. **Capability:** Collects the actual public identity of every surface:
   - `origin` `main` (`git ls-remote`);
   - the bytes Pages serves, hashed with SHA-256 and compared with
     `git show <landing>:docs/index.html`;
   - the Space's revision and a per-file check, reusing `scripts/deploy_space.py` check mode;
   - the MLflow mirror, via `scripts/verify_mlflow_mirror.py`;
   - the links, via `scripts/check_links.py`.

   It writes dated records under `reports/presentation/release-checks/` and prints the packet's §8
   table: intended identity, observed identity, UTC time, result and outstanding action.
2. **Current location and control:** `docs/track-b/publication-runbook.md:49-52` and `:54-96`;
   `docs/track-b/publication-packet-template.md:164-190`. These records are built by hand at each
   release. No script in `scripts/` produces `2026-09-29-postdeploy-pages-identity.json`,
   `-space-identity.json` or `-summary.json`.
3. **Destination:** Script. The work is anonymous HTTP requests and hashes. The standing
   daily-publication exception (`AGENTS.md:162-175`) requires automated validation that fails
   closed, and this script can serve it.
4. **Implementation:** The script takes `--landing <sha>`, `--bundle <dir>` and
   `--expect <sha256>`. Each surface is checked independently, keeping the first failure and every
   retry (`docs/track-b/publication-runbook.md:91`). It exits 1 on any mismatch. The browser checks
   stay in `scripts/check_reader_paths.py`, which runs in a separate Playwright environment; the
   receipt only cites their records.
5. **Notes:** Read-only and network-bound, with no credential. No locked file is edited. If the
   runbook cites the script, the reference must be written as `file::symbol`, because
   `tests/test_42_publication_runbook.py` resolves every such reference.

## 6. Checkpoint disposition and reclamation

1. **Capability:** Adds subcommands to `scripts/gauntlet.py`:
   - `inspect [branch]`: prints the INSPECT block. For an unknown branch it reports the tip, age,
     ahead/behind, `diff --stat`, any attached worktree, and live documents citing SHAs reachable
     only from that branch.
   - `discard <cp> <k>`: creates the DISCARD tag.
   - `citations <cp>`: lists the documents to repoint.
   - `reclaim <cp>`: deletes the branch and worktrees, with the two guards enforced.
   - `land-commands <cp>`: prints the LAND commands for the Owner and never runs them.
2. **Current location and control:** `AGENTS.md:184` and `:186-193`;
   `docs/track-b/gauntlet-templates.md:195-239`; `orchestrator-role.md:348-354`. This is done by
   hand for each closed checkpoint. CP-16 compiled `branch-citations.txt` by hand.
3. **Destination:** Script. `AGENTS.md:191` itself calls this ref hygiene "tedium, not judgement".
4. **Implementation:**
   - `reclaim` refuses unless `evidence/<cp>` or `archive/<cp>-attempt-*` resolves and
     `merge-base --is-ancestor <tip> <tag>` holds. It refuses any branch that is not
     `gauntlet/*`, removes only worktrees under `.local/worktrees/<cp>/`, then runs
     `git worktree prune`.
   - `citations` uses `git grep -n`.
   - `inspect` is read-only.
5. **Notes:** No locked file is edited. LAND remains authored by the Owner (`AGENTS.md:191`); the
   script only prints it. The script enforces the existing guards mechanically and adds no new
   ones.

## 7. Pre-review check runner

1. **Capability:** Runs the offline checks of `docs/track-b/publication-runbook.md` §9 in order
   and writes one dated record. The checks:
   - the CI steps parsed from `.github/workflows/tests.yml`, under Python 3.12;
   - `make verify` and `make lint-publication`;
   - rebuild determinism: `scripts/rebuild_presentation.py`, then an empty
     `git status --porcelain`;
   - `scripts/check_links.py`;
   - `scripts/publication_guard.py tree`, which is expected to fail before the `--final` build and
     is recorded that way.
2. **Current location and control:** `docs/track-b/publication-runbook.md:308-330`;
   `Makefile:118-131`. These are run by hand at each publication, and each result is recorded by
   hand.
3. **Destination:** Script plus a `make prerelease` target.
4. **Implementation:** `scripts/prerelease.py` holds a list of (name, argv, expected exit code). It
   continues past failures and records the argv, exit code, duration and the last 40 lines of
   output in `reports/presentation/release-checks/<date>-prerelease.json`. It exits 1 on any
   unexpected result. `tests.yml` is parsed with PyYAML, which is already in `uv.lock`
   transitively, or with a small line parser. The browser checks in §10 stay out.
5. **Notes:** No locked file is edited. The script replaces the manual run and its recording; it
   adds no check.

## 8. `progress.md` omission diff

1. **Capability:** Compares `progress.md` with the last delivered version (`HEAD`, or
   `--against <ref>`). It confirms that the seven required sections are present and in order. It
   lists every removed bullet by section, and lists removals from the sections that may never be
   dropped (open questions, notes, standing decisions) separately.
2. **Current location and control:** `orchestrator-role.md:372-394`. The Orchestrator does this by
   reasoning over the 1,140-line file at each update.
3. **Destination:** Script.
4. **Implementation:** `scripts/progress_diff.py` splits the file on `## ` headings and into
   bullet blocks by indentation, then prints the set difference grouped by section. It always
   exits 0, because deciding whether each removal was resolved or pruned stays the Orchestrator's
   judgment.
5. **Notes:** No locked file is edited (`progress.md` is program state, `AGENTS.md:45-47`). It
   reads `progress.md`, so only the Orchestrator uses it, and it must never be wired into a hook
   (`AGENTS.md:116`).

## 9. End-of-task handover packet `/handover`

1. **Capability:** Produces the handover packet that ends every non-checkpoint task.
2. **Current location and control:** `AGENTS.md:159`. The agent assembles it from memory at the end
   of each task.
3. **Destination:** Skill. Model invocation is left on, so the agent can load the skill when the
   task ends.
4. **Implementation:** `.claude/skills/handover/SKILL.md` with
   `allowed-tools: Bash(git status *) Bash(git diff *) Bash(git ls-files *)`. It injects
   `git status --porcelain=v1`, `git diff --stat`, `git diff` and
   `git ls-files --others --exclude-standard` with `!` blocks. The instructions: one line of
   reason per file, a proposed commit message, then stop and wait.
5. **Notes:** Needs the `.claude/skills/handover/` suspension. It adds no step; it replaces
   recalling the format and running the commands by hand.

## 10. Credential-store deny rules

1. **Capability:** Claude Code refuses to read the credential stores or dump the environment.
2. **Current location and control:** `AGENTS.md:87-93`. The rule exists only in the agent's memory.
3. **Destination:** Hook layer: `permissions.deny` in `.claude/settings.json`. No script is needed;
   Claude Code evaluates these rules before any tool runs.
4. **Implementation:** These rules:
   - `Read(~/.zshrc)`, `Read(~/.zshrc.*)`, `Read(~/.zsh_history)`, `Read(~/.zsh_sessions/**)`
   - `Read(~/.bash_history)`, `Read(~/.claude/shell-snapshots/**)`
   - `Bash(env)`, `Bash(printenv)`, `Bash(printenv *)`, `Bash(export -p)`, `Bash(set)`
   - `Bash(launchctl getenv *)`
5. **Notes:** Needs the `.claude/settings.json` suspension. According to the docs, Read deny rules
   cover Claude's file tools, recognised file commands such as `cat`, `head`, `tail` and `sed`, and
   redirections. They do not cover arbitrary subprocesses. So these rules back up
   `scripts/secret_guard.py` and do not replace it. The guard is unaffected: Git runs it outside
   Claude's tools.

---

## Considered and left as is

- **Lockdown edit guard** (PreToolUse on edits to locked paths): it would also block edits the
  Owner has authorized, so every suspension would need an Owner toggle. That adds a step.
- **`git push` or commit-to-`main` guard:** the Owner authorizes pushes per task, and the daily
  pipeline pushes to `main`. A deny or ask rule would add an approval to every authorized push.
  The pre-push hook already guards against secrets and placeholders.
- **Stop hook that runs the tests:** it adds a step to every turn. Tests are the Lead's call and
  CI's job.
- **Injecting `progress.md` or the role documents at session start:** a hook cannot know the
  session's role, so this would break the Lead's isolation (`AGENTS.md:116`).
- **Interview-answer capture:** `scripts/qa_append.py` already makes it deterministic.
- **Duplicate test runs in CI** (`.github/workflows/tests.yml:22-35`): they cost CI minutes, not
  agent or Owner work.
