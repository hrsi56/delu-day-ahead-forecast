# Automation plan: scripts, skills and hooks

| # | Item | Destination | Saving | Effort |
|---|---|---|---|---|
| 1 | Checkpoint identity and return verifier (receipt mode only under a suspension) | Script | ~45 hand-written return lines and the elapsed-hours figure per checkpoint, for the Lead. The Orchestrator's 8–10 receipt commands only if `receipt` is authorized | M–L |
| 2 | Integration Critic launcher `/critic` | Skill (`context: fork`) | The fixed part of each Critic assignment (worktree, SHA-256, ~35-line excerpt, protocol, no-Git-write rules) is generated; the Lead still writes reproduction and tolerance. Lead steps 8 → 5, no Owner step. The harness isolates the Critic's starting context | S, after 1 and 4 |
| 3 | Session start: enable the guard and report the git state | Hook (SessionStart) | One Owner instruction per fresh clone, and the Lead's state check per checkpoint; a broken `core.hooksPath` no longer fails silently | S |
| 4 | Plan checklist extractor, brief checker and launch envelope | Script | The bar excerpt is quoted in the assignment and verdict, mapped in the return, and byte-checked by hand; brief validation is done by reading, twice; the fixed launch envelope is re-assembled for every brief | S |
| 5 | Post-deploy publication receipt | Script | Identity records for 5 surfaces are built by hand at each publication; the future daily pipeline can reuse the script | M |
| 6 | Checkpoint disposition and reclamation | Script | ~12 commands and a citation search per closed checkpoint | S–M |
| 7 | Pre-review check runner | Script + `make prerelease` | ~7 checks run and recorded one at a time per publication | S |
| 8 | `progress.md` omission diff | Script | Groups the removals from an 81 KB file by section at each state update (`git diff -U0` already lists them) | S |
| 9 | End-of-task handover packet `/handover` | Skill | The format, 3 git commands and the `.local/` account recalled at the end of every non-checkpoint task | XS |
| 10 | Credential-store deny rules | Hook layer (`permissions.deny`) | Puts the common direct reads and environment dumps of a remembered rule into a harness setting; the rule itself stays | XS |
| 11 | Credential-subscript check | Script | A rule every agent must remember when writing code becomes a listed result | XS |

Build order: 4 → 1 → 3 → 2 → 6, then 5, 11, 7, 9, 10 and 8. Item 8 is the weakest candidate.

Role-maintenance analysis, 2026-10-01. Proposal only: nothing below is implemented. Claude Code
capabilities were checked against code.claude.com/docs (hooks, skills, permissions, sub-agents) on
2026-10-01. Revised the same day to apply the review of `39f05e0` (verdict PASS WITH
CORRECTIONS); see § *Revision record*.

## Lockdown and discovery, stated once

**Locked files.** `AGENTS.md:23-24` locks `.claude/**` "and any file that configures how agents
run in this repository". The catch-all covers more than `.claude/`. The SessionStart script
decides what every session's context receives, and the output of the Critic-brief renderer *is*
the Critic's prompt. Both therefore live under `.claude/`, next to the configuration that calls
them. Items 2, 3, 9 and 10 need one Owner suspension naming:

- `.claude/settings.json` (items 3 and 10);
- `.claude/hooks/` (item 3's `session_start.py`);
- `.claude/skills/critic/` (item 2's `SKILL.md` and `brief.py`);
- `.claude/skills/handover/` (item 9).

Once created, those files are protected by the same lock. The scripts in `scripts/` (items 1, 4–8
and 11) configure no agent and touch no locked file.

**Receipt.** `orchestrator-role.md:327-339` lists the Orchestrator's receipt commands, and `:337`
says "That list is exhaustive". `python3 scripts/gauntlet.py receipt` is not on it. Item 1
therefore builds `receipt` only if the suspension also names `orchestrator-role.md` L327-339.
Otherwise `receipt` is dropped.

**Discovery.** An agent learns how to run a checkpoint only from `engineering-role.md` or
`gauntlet-templates.md` (both locked), or from `.claude/`. Lead use of items 1, 4 and 6 therefore
needs one line in `engineering-role.md` § *Checkpoint execution*, under the same suspension, or one
fixed pointer line printed by item 3. The Orchestrator-only scripts (items 4's `envelope` and 8)
need the same: one line in `orchestrator-role.md` under the suspension, or the same pointer line.

---

## 1. Checkpoint identity and return verifier

1. **Capability:** Records the repository topology when a checkpoint starts. At return, checks the
   evidence and prints the *Identity* and *Repository state* blocks of the checkpoint return and
   the elapsed hours, ready to paste. Receipt mode exists only under the suspension named in
   § *Lockdown and discovery*.
2. **Current location and control:** `engineering-role.md:36` (verify state), `:45-52` (two SHAs,
   verdict-only delta), `:87` (elapsed hours to the nearest half hour), `:107` (reachability
   before return); `docs/track-b/gauntlet-templates.md:134-145` and `:183-193`;
   `orchestrator-role.md:327-339`. An agent runs these by hand at the checkpoint's start, at its
   return and at receipt, working from memory and reasoning. CP-21 spent 45 hand-written lines on
   these blocks (`docs/track-b/evidence/cp-21/checkpoint-return.md:16-60`). CP-16 kept ad-hoc
   `main-state.txt` and `handover-state.json`.
3. **Destination:** Script. It is pure git, needs no judgment, and the same inputs always give the
   same output.
4. **Implementation:** `scripts/gauntlet.py` (stdlib and git):
   - `start <cp>`: reads the latest `.local/tmp/session-<id>-refs.json` written by item 3 (the
     hook does not know `<cp>`), adds the checkpoint ID and the UTC start time, and writes
     `.local/tmp/<cp>-start.json`. With no session snapshot it takes one itself: HEAD, `main`, the
     local `origin/main` (no fetch), `worktree list --porcelain`,
     `for-each-ref refs/heads refs/tags`, the stash list and the porcelain status.
   - `return <cp> <final_candidate_sha> [<evidence_tip>=HEAD]`: checks that
     `diff --name-only` stays inside `docs/track-b/evidence/<cp>/`. Runs `cat-file -e` and
     `merge-base --is-ancestor … gauntlet/<cp>` on every candidate SHA the folder cites:
     `final_candidate_sha` and the SHA on each verdict's `Candidate SHA:` line. Other 40-hex
     tokens, such as a Space revision or a zero OID, are listed, not checked. Checks that the
     verdict exists, reads `PASS` and cites `final_candidate_sha`. Lists the branches, worktrees,
     tags and stashes created since `start`, and compares the issued brief's SHA-256 with the
     canonical copy. Prints the elapsed hours, rounded to the nearest half hour, from the `start`
     time. Prints the markdown blocks plus the evidence tip for the terminal message, since a file
     cannot contain its own commit SHA. Exits 1 if any check fails.
   - `receipt <cp> <final> <tip>`, only under the suspension: runs `main`'s copy of the script
     (`git show main:scripts/gauntlet.py`), never the copy on the evidence tip, which the Lead can
     edit. It runs only the commands listed at `orchestrator-role.md:330-334` and
     `gauntlet-templates.md:186-190`, and prints every command with its raw output
     (`orchestrator-role.md:339`). It gives PASS or FAIL only for the verdict-only delta, the
     `cat-file` checks and the verdict-file check.
5. **Notes:** No locked file is edited by the script. `receipt` stays out unless the suspension
   names `orchestrator-role.md` L327-339, and even then it adds no command to the exhaustive list
   (`:337`): no source reads and no tests. Lead use needs the discovery line in § *Lockdown and
   discovery*. Citing the script from the templates is optional and would need a suspension for
   `gauntlet-templates.md`.

## 2. Integration Critic launcher `/critic`

1. **Capability:** Launches the one fresh Integration Critic. The Critic gets a generated
   assignment and the protocol, works in a clean detached worktree, and starts without the Lead's
   conversation history.
2. **Current location and control:** `engineering-role.md:41` and `:56-73`;
   `docs/track-b/gauntlet-templates.md:70-120`. The Lead writes each assignment by hand. For
   example, `docs/track-b/evidence/cp-20/integration-assignment.md` (128 lines) holds the worktree
   command, the plan's SHA-256, a 35-line verbatim excerpt and the no-Git-write rules; CP-16's
   assignment is 82 lines with no quoted excerpt. The Lead also creates and removes the worktree.
   Isolation is "cooperative" (`engineering-role.md:73`). A checkpoint can need more than one
   run: CP-20 has the evidence folders `integration-attempt-1` and `integration-2`; CP-21 created
   the worktrees `critic` and `critic-2` because an API session limit stopped the first review
   (`docs/track-b/evidence/cp-21/checkpoint-return.md:48-51`, `:96-98`). A skill does not prevent
   such a second run; it makes each run cheaper.
3. **Destination:** Skill with `context: fork`. According to the docs, a forked skill "doesn't see
   your conversation history" and receives the skill content as its prompt. The harness therefore
   isolates the Critic's starting context (no conversation history), which serves "Receive the
   artifact, never the Builder's story" (`engineering-role.md:67`). Read-only status, no Git write
   and no later messages from the Lead stay procedural (`engineering-role.md:73`). The subagent
   inherits the Lead's permission rules, `general-purpose` has Edit and Write, it receives the
   Lead's git status at startup, and the Lead can resume it with `SendMessage`. The deterministic
   steps stay in the scripts from items 1 and 4.
4. **Implementation:**
   - **Before the review:** the Lead writes a short assignment containing only the judgment
     fields: plan path, section heading, reproduction commands and tolerance. The Lead then runs
     `gauntlet.py critic-open <cp> <sha> <assignment>`. This creates
     `.local/worktrees/<cp>/critic-<n>`, checks that it is clean and that `HEAD` equals the SHA,
     and records the details in `.local/tmp/critic-open.json`.
   - **`.claude/skills/critic/SKILL.md` frontmatter:** `context: fork`,
     `agent: general-purpose`, `background: false` (forked skills run in the background by
     default; the Lead waits for the verdict in the invoking turn), and
     `allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/brief.py *)`, which pre-approves the
     injected command so that its permission check does not abort the skill.
     `disable-model-invocation` is unset, so the Lead invokes `/critic` through the Skill tool.
     The skill's description, which the Lead sees, names the `critic-open` step.
   - **Skill body:** `` !`python3 ${CLAUDE_SKILL_DIR}/brief.py` `` injects the assignment, the
     plan's SHA-256 and the verbatim excerpt (via item 4) before the subagent starts. `brief.py`
     exits 1 unless `critic-open` recorded this checkpoint, so an early invocation aborts. It also
     re-checks that the worktree is clean and that `HEAD` equals the SHA, and exits 1 otherwise.
     Fixed text follows: the protocol from `engineering-role.md:56-73` and the verdict form from
     templates §2. The Critic still confirms the excerpt against the plan itself
     (`gauntlet-templates.md:84`, `:88`). It writes its verdict to
     `.local/artifacts/<cp>/critic-<n>/integration.md`, outside the worktree, and performs no Git
     write.
   - **After the review:** the Lead runs `gauntlet.py critic-close`, which checks that the
     worktree is still clean and `HEAD` is unchanged, removes the worktree, hashes the verdict and
     copies it to `docs/track-b/evidence/<cp>/integration.md`. This is the current practice
     (`docs/track-b/evidence/cp-20/integration-assignment.md:124-128`). The Lead then commits the
     verdict as the sole Git writer (`engineering-role.md:39`).
   - **Steps:** today the Lead takes 8 (create the worktree, check it is clean, extract the
     excerpt and SHA-256, write the assignment, launch, check after, remove, commit). With the
     skill it takes 5 (write the short assignment, `critic-open`, invoke `/critic`,
     `critic-close`, commit), and the Owner takes none.
5. **Notes:** Needs the `.claude/skills/critic/` suspension, which covers `SKILL.md` and
   `brief.py`. `engineering-role.md` needs no change for the protocol, because the skill
   implements it; Lead use of the item 1 and 4 scripts needs the discovery line in § *Lockdown and
   discovery*. A failing `!` command aborts the whole skill invocation, so a dirty or moved
   worktree stops the review before it starts. The skill follows the current worktree practice
   (`.local/worktrees/…`, `AGENTS.md:65-72`), but `engineering-role.md:62` still says
   `<path-outside-repo>`. The Owner may want to align that line at a future suspension; it is not
   required. Depends on items 1 and 4.

## 3. Session start: enable the guard and report the git state

1. **Capability:** At every session start, resume, clear, compaction or fork:
   (a) when `core.hooksPath` is unset, points it at the main checkout's `.githooks`; when it is set
   but broken, prints one warning and changes nothing;
   (b) prints at most 10 lines of git state;
   (c) writes the ref snapshot that item 1's `start` reads.
2. **Current location and control:** `AGENTS.md:103-107` assumes `core.hooksPath` is set, but
   nothing sets it in a fresh clone or cloud container. `progress.md:285-292` records the Owner's
   instruction to enable it in each clone by hand (`git config core.hooksPath <clone>/.githooks`).
   Git also commits without running any hook when `core.hooksPath` points to a missing directory,
   for example after the worktree that set it is removed (tested 2026-10-01 with git 2.43.0:
   exit 0, no warning). In that case the secret guard silently stops running. The state check in
   `engineering-role.md:36` and the branch declaration in `AGENTS.md:183` are done by hand.
3. **Destination:** Hook: `SessionStart` with no matcher, so it runs for all five sources
   (`startup`, `resume`, `clear`, `compact` and `fork`), command
   `python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/session_start.py"`. Its stdout reaches the agent's
   context.
4. **Implementation:** The script:
   - finds the main checkout as the parent of
     `git rev-parse --path-format=absolute --git-common-dir`. With a bare repository or
     `--separate-git-dir` that parent is not a checkout, so the script warns and changes nothing;
   - sets `core.hooksPath` only when it is unset, to `<main>/.githooks`, after checking that
     `<main>/.githooks/pre-commit` exists, and says so in one line. If it is set but its
     `pre-commit` is missing, it prints one warning and changes nothing;
   - prints the branch, short HEAD, `main` ahead/behind `origin/main` (no fetch), the number of
     dirty files, the worktrees, any `gauntlet/*` branches and the stash count, and, if the Owner
     chooses that discovery route, one fixed line naming the helper scripts;
   - writes `.local/tmp/session-<session_id>-refs.json`.
   It uses only the standard library, always exits 0, and reports its own errors as one line.
5. **Notes:** Needs the `.claude/settings.json` and `.claude/hooks/` suspension. The script lives
   in `.claude/hooks/` because it decides what every session's context receives. It must print
   only git state and the fixed pointer line: never `progress.md`, role documents or anchors,
   because an Engineering Lead may not read `progress.md` before its verdict (`AGENTS.md:116`).
   It sets the guard only in the case the Owner's recorded instruction covers (unset). It never
   changes an existing value and never bypasses the guard (`AGENTS.md:106`). SessionStart hooks
   also run in Claude Code on the web.

## 4. Plan checklist extractor, brief checker and launch envelope

1. **Capability:**
   - `bar <plan> "<heading>" [--at SHA]` prints a plan section verbatim, from its heading to the
     next heading of the same or higher level, together with the plan's SHA-256 at that commit.
   - `check <file> --plan <plan> --at <sha>` checks that the block labelled "Verbatim bar excerpt"
     in a brief, assignment or verdict appears byte for byte in the plan at that commit.
   - `brief <brief.md>` checks the brief. All ten required fields must be present
     (`engineering-role.md:19-30`), with no `[...]` placeholders left, one checkpoint and one
     numeric timebox. The plan file must exist and the cited section must resolve. It also prints
     the brief's SHA-256.
   - `envelope <brief.md>` runs `brief`, then prints the fixed Engineering-Lead launch envelope
     with the brief inserted between its markers. It reads the envelope from
     `orchestrator-role.md` at `HEAD`, so the locked file stays the only copy.
2. **Current location and control:** `orchestrator-role.md:204` (validation before dispatch),
   `:206-236` (the launch envelope) and `:220-222` (the Lead validates the brief again);
   `engineering-role.md:58`, `:69` and `:109` (an excerpt missing from the plan invalidates
   `PASS`); `docs/track-b/gauntlet-templates.md:81-84`, `:101-103` and `:150`. Each is done by
   reading and copying by hand. The excerpt is quoted in the Critic assignment and the verdict,
   and the checklist is mapped in the return; the CP-21 brief only cites the bar
   (`docs/track-b/evidence/cp-21/issued-brief.md:57-60`). The envelope is re-assembled for every
   brief (`docs/track-b/cp-10-brief.md`, `cp-15-brief.md`,
   `pres-2-execution-brief-2026-09-29.md`). CP-16's Critic re-implemented the extraction in
   `docs/track-b/evidence/cp-16/critic-audit.py`.
3. **Destination:** Script. The work is text extraction and byte comparison.
4. **Implementation:** `scripts/bar.py` uses only the standard library and reads the plan with
   `git show <sha>:<plan>`. Headings must match exactly. `check` compares only the block labelled
   "Verbatim bar excerpt". From each of its lines it strips `^\s*>` plus one optional space, so
   bare `>` lines and indented `  >` lines compare correctly: `cp-21/integration.md` has 3 bare
   `>` lines, and `cp-20/integration.md` and `cp-20/integration-assignment.md` each have 35
   indented `  >` lines. Trailing blank lines are ignored; the CP-21 Critic notes one extra
   trailing blank line in its own extraction (`docs/track-b/evidence/cp-21/integration.md:7`). On
   failure it exits 1 and prints the first line that does not match.
5. **Notes:** No locked file is edited; `envelope` reads `orchestrator-role.md` and never writes
   it. The script checks form only: the brief's content (what to build, the timebox) stays the
   Orchestrator's decision. It does not replace the Critic's own check that the excerpt appears in
   the plan (`gauntlet-templates.md:84`). Items 1 and 2 use it. Use needs the discovery line in
   § *Lockdown and discovery*.

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
   runbook cites the script as `file::symbol`, `tests/test_42_publication_runbook.py` requires
   that reference to resolve.

## 6. Checkpoint disposition and reclamation

1. **Capability:** Adds subcommands to `scripts/gauntlet.py`:
   - `inspect [branch]`: prints the INSPECT block. For an unknown branch it reports the tip, age,
     ahead/behind, `diff --stat`, any attached worktree, and live documents citing SHAs reachable
     only from that branch.
   - `discard <cp> <k>`: creates the DISCARD tag.
   - `citations <cp>`: lists the documents to repoint.
   - `reclaim <cp> --disposition <Owner decision ref>`: deletes the branch and worktrees.
   - `land-commands <cp>`: prints the LAND commands for the Owner and never runs them.
2. **Current location and control:** `AGENTS.md:184` and `:186-193`;
   `docs/track-b/gauntlet-templates.md:195-239`; `orchestrator-role.md:348-354`. This is done by
   hand for each closed checkpoint. CP-16 recorded `branch-citations.txt` from a `git grep`
   (9 lines in `path:line:text` form).
3. **Destination:** Script. `AGENTS.md:191` itself calls this ref hygiene "tedium, not judgement".
4. **Implementation:**
   - `reclaim` requires `--disposition`, a reference to where the Owner's LAND or DISCARD decision
     is recorded, and prints it in its output. It refuses unless `evidence/<cp>` or
     `archive/<cp>-attempt-*` resolves and `merge-base --is-ancestor <tip> <tag>` holds. It
     refuses any branch that is not `gauntlet/*`, removes only worktrees under
     `.local/worktrees/<cp>/`, then runs `git worktree prune`. Finally it lists what remains under
     `.local/` for that checkpoint (`.local/worktrees/<cp>/`, `.local/artifacts/<cp>/`,
     `.local/tmp/<cp>*`), so retained recovery material is accounted for (`AGENTS.md:70-71`).
   - `citations` uses `git grep -n`.
   - `inspect` is read-only.
5. **Notes:** No locked file is edited. LAND remains authored by the Owner (`AGENTS.md:191`); the
   script only prints it. Guard 1 of `AGENTS.md:192` (no ref deleted unless its SHAs are reachable
   from a verified tag) is enforced mechanically. Guard 2 (never a branch the Owner has not
   dispositioned) stays the Owner's recorded decision: `discard` lets the agent create the archive
   tag itself, so a tag proves nothing about that decision, and the script cannot verify the
   reference it is given. It adds no new guard. Lead use needs the discovery line in § *Lockdown
   and discovery*.

## 7. Pre-review check runner

1. **Capability:** Runs the pre-review checks of `docs/track-b/publication-runbook.md` §9 in order
   and writes one dated record. The checks:
   - the CI steps parsed from `.github/workflows/tests.yml`, under Python 3.12;
   - `make verify` and `make lint-publication`;
   - rebuild determinism: `git status --porcelain` before and after
     `scripts/rebuild_presentation.py` must be identical;
   - `scripts/check_links.py`, which needs the network;
   - `scripts/publication_guard.py tree`, which is expected to fail before the `--final` build and
     is recorded that way;
   - item 11's credential-subscript check, recorded without affecting the exit code.
2. **Current location and control:** `docs/track-b/publication-runbook.md:308-330`;
   `Makefile:118-131`. These are run by hand at each publication, and each result is recorded by
   hand.
3. **Destination:** Script plus a `make prerelease` target.
4. **Implementation:** `scripts/prerelease.py` holds a list of (name, argv, expected exit code). It
   continues past failures and records the argv, exit code, duration and the last 40 lines of
   output in `reports/presentation/release-checks/<date>-prerelease.json`. It writes that record
   last, so a same-day re-run is not tripped by the previous, uncommitted record. It exits 1 on any
   unexpected result. `tests.yml` is parsed with PyYAML, which is already in `uv.lock`
   transitively, or with a small line parser. The browser checks in §10 stay out.
5. **Notes:** No locked file is edited. The script replaces the manual run and its recording; it
   adds no check beyond item 11's non-blocking listing.

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
   (`AGENTS.md:116`). Its value is small: `git diff -U0` already lists the removals, and the
   script adds only the grouping by section and the never-drop list. Use needs the discovery line
   in § *Lockdown and discovery*.

## 9. End-of-task handover packet `/handover`

1. **Capability:** Produces the handover packet that ends every non-checkpoint task.
2. **Current location and control:** `AGENTS.md:159`, and `AGENTS.md:70-71` (account for retained
   `.local/` material). The agent assembles it from memory at the end of each task.
3. **Destination:** Skill. Model invocation is left on, so the agent can load the skill when the
   task ends.
4. **Implementation:** `.claude/skills/handover/SKILL.md` with `allowed-tools` set to
   `Bash(git status *)`, `Bash(git diff *)`, `Bash(git ls-files *)` and
   `Bash(find .local -mindepth 1 -maxdepth 2)`. It injects `git status --porcelain=v1`, `git diff --stat`, `git diff`,
   `git ls-files --others --exclude-standard` and `find .local -mindepth 1 -maxdepth 2` with `!`
   blocks. The instructions: one line of reason per file, one line per retained `.local/` entry
   (kept and why, or removed), a proposed commit message, then stop and wait.
5. **Notes:** Needs the `.claude/skills/handover/` suspension. It adds no step; it replaces
   recalling the format and running the commands by hand.

## 10. Credential-store deny rules

1. **Capability:** Claude Code refuses the common direct ways of reading the credential stores or
   dumping the environment.
2. **Current location and control:** `AGENTS.md:87-93`. The rule exists only in the agent's memory.
3. **Destination:** Hook layer: `permissions.deny` in `.claude/settings.json`. No script is needed;
   Claude Code evaluates these rules before any tool runs.
4. **Implementation:** These rules:
   - `Read(~/.zshrc*)`, `Read(~/.zsh_history)`, `Read(~/.zsh_sessions/**)`
   - `Read(~/.bash_history)`, `Read(~/.claude/shell-snapshots/**)`, `Read(//proc/*/environ)`
   - `Bash(env)`, `Bash(env -0)`, `Bash(printenv *)`, `Bash(set)`
   - `Bash(export)`, `Bash(export -p)`, `Bash(declare *)`, `Bash(typeset *)`
   - `Bash(launchctl getenv *)`

   `Bash(printenv *)` also matches bare `printenv`, so no separate rule is needed.
5. **Notes:** Needs the `.claude/settings.json` suspension. According to the docs, Read deny rules
   cover Claude's file tools, recognised file commands such as `cat`, `head`, `tail` and `sed`, and
   redirections. They do not cover arbitrary subprocesses. Bash rules match command text.
   Absolute paths (`/usr/bin/env`), `sh -c`, other dumpers and interpreters
   (`python3 -c 'print(os.environ)'`) are not covered. So these rules back up `AGENTS.md:87-93`
   and `scripts/secret_guard.py` and replace neither. The guard is unaffected: Git runs it outside
   Claude's tools.

## 11. Credential-subscript check

1. **Capability:** Lists every `os.environ[...]` subscript in tracked Python files that names one
   of the credentials at `AGENTS.md:79-82`.
2. **Current location and control:** `AGENTS.md:96-100`: read a required variable with
   `os.environ.get`, because a bare subscript's `KeyError` under pytest prints the whole
   environment. Agents must remember this when writing code. Bare subscripts exist in at least 10
   files (for example `src/delu_forecast/tracking.py:54`); on 2026-10-01 none of them names a
   credential, so the check guards new code.
3. **Destination:** Script. The work is a syntax-tree search.
4. **Implementation:** `scripts/env_reads.py` parses each tracked `.py` file with `ast` and prints
   `file:line` for each `os.environ[<key>]` whose key is `DAGSHUB_USER_TOKEN`,
   `MLFLOW_TRACKING_USERNAME`, `MLFLOW_TRACKING_PASSWORD`, `ENTSOE_API_TOKEN` or `HF_TOKEN`, as a
   literal or as a module-level constant holding one. It reads code, never values, and always
   exits 0. Item 7 records its output.
5. **Notes:** No locked file is edited. It is non-blocking because `AGENTS.md:93` still shows
   `os.environ["HF_TOKEN"]` as the way to reference a stored variable; making it blocking would
   change a rule, which is the Owner's decision. Use needs the discovery line in § *Lockdown and
   discovery*.

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

## Revision record

Review of `39f05e0`, 2026-10-01: PASS WITH CORRECTIONS. Every finding is applied:

| Finding | Severity | Change |
|---|---|---|
| 1 | blocking | Item 2: `disable-model-invocation` unset; the Lead invokes `/critic`; `brief.py` aborts without `critic-open` |
| 2 | blocking | § *Lockdown and discovery*: hook script and brief renderer moved under `.claude/`; `.claude/hooks/` named; `receipt` conditional on an `orchestrator-role.md` L327-339 suspension; discovery line |
| 3 | should-fix | Summary and item 2: the harness isolates the starting context only; the rest stays procedural |
| 4 | should-fix | Item 2: verdict written to `.local/artifacts/<cp>/critic-<n>/`, copied by `critic-close` |
| 5 | should-fix | Item 2: `brief.py` re-checks clean and `HEAD`; `background: false` |
| 6 | should-fix | Summary and item 2: generated part named; the Lead still writes reproduction and tolerance; steps 8 → 5 |
| 7 | should-fix | Item 1: reachability checked on candidate SHAs only; other 40-hex tokens listed |
| 8 | should-fix | Item 1: `receipt` runs `main`'s copy and prints raw output; PASS/FAIL only for three checks |
| 9 | should-fix | Item 4: `^\s*>` normalisation, labelled block only, trailing blanks ignored |
| 10 | should-fix | Item 3: no matcher, so `fork` is included |
| 11 | should-fix | Item 3: sets `core.hooksPath` only when unset; warns otherwise; cites `progress.md:285-292` |
| 12 | should-fix | Item 10: rules widened, `Bash(printenv)` dropped, Bash gaps stated |
| 13 | should-fix | Item 6: `reclaim --disposition`; guard 2 stays the Owner's decision |
| 14 | minor | Item 6: `branch-citations.txt` recorded from a `git grep` |
| 15 | minor | Summary and item 4 / 3: "quoted, mapped"; "per fresh clone, per checkpoint" |
| 16 | minor | Item 7: "pre-review checks"; status compared before and after; record written last |
| 17 | minor | Item 5: `file::symbol` must resolve only when used |
| 18 | minor | Unsupported claim deleted; `start` reads the session snapshot; table first; item 1 effort M–L |
| Omissions | — | Elapsed hours in item 1; `envelope` in item 4; item 11; `.local/` accounting in items 6 and 9; item 8 marked weakest |
