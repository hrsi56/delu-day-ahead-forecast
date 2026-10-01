# Automation plan: scripts, skills and hooks

| Item | Destination | Saving | Effort |
|---|---|---|---|
| 1. Checkpoint identity, return and receipt verifier | Script | ~45 hand-written return lines and 8–10 receipt commands per checkpoint, for both Lead and Orchestrator; removes the most common causes of an invalid `PASS`. Receipt mode waits for an Owner ruling | M |
| 2. Plan checklist extractor and brief checker | Script | The checklist is copied by hand into 4 documents per checkpoint and byte-checked twice; brief validation is done by reading, twice; anchor identities are hashed by hand for each brief | S |
| 3. Session start hook | Hook (`SessionStart`) | The guard instruction, which recurs per cloud session or fresh clone (locally it is set once), and 3–5 state commands per session; closes a gap where the secret guard silently stops running | S |
| 4. Checkpoint disposition and reclamation | Script | ~12 commands and a citation search per closed checkpoint | S–M |
| 5. Integration Critic launcher `/critic` | Skill (`context: fork`) | The assignment boilerplate beyond item 2's excerpt, plus one command: Lead actions per Critic run go from 6 to 5, Owner actions stay 0. Assignments today are 82–128 lines. The prompt is generated and history isolation holds (forks excluded); read-only stays cooperative | S, after 1 and 2 |
| 6. Post-deploy publication receipt | Script | Identity records for 5 surfaces are built by hand at each publication; the future daily pipeline can reuse the script | M |
| 7. Pre-review check runner | Script + `make prerelease` | ~8 checks run and recorded one at a time per publication | S |
| 8. `progress.md` omission diff | Script | Groups the removals in the existing `git diff` by section and flags removals from protected sections | S |
| 9. Credential-store deny rules | Settings (`permissions.deny`) | Turns a rule that must be remembered in every session into a harness setting, for the command forms it lists | XS |

Role-maintenance analysis, 2026-10-01, revised after an independent review of `39f05e0`. Proposal
only: nothing below is implemented. Claude Code capabilities were re-checked on 2026-10-01 against
code.claude.com/docs/en/ (skills, hooks, permissions, sub-agents, cloud-environments) and are cited
inline as page#anchor; what the docs do not settle is marked UNVERIFIED.

**Lockdown, stated once.** Every hook, permission rule and skill lives under `.claude/**`, which
`AGENTS.md:23-24` locks as agent configuration. Items 3, 5 and 9 need one Owner suspension naming
`.claude/settings.json`, `.claude/hooks/session_start.py` and `.claude/skills/critic/`. It must
expressly authorize the hook's automatic write of `core.hooksPath`, because `AGENTS.md:106`
forbids "changing `core.hooksPath`", and it covers the helper-index line the hook prints. Once
created, those files are protected by the same lock. Three limits stay with the Owner:

- Item 1's receipt mode needs an Owner ruling on `orchestrator-role.md:327-339` before the
  Orchestrator adopts it. The two locked lists differ: `docs/track-b/gauntlet-templates.md:186-190`
  adds `status --porcelain=v1` and `head -5` of the verdict to `orchestrator-role.md:330-334`,
  drops its `diff --stat`, `worktree list`, `tag --list` and `cat-file -e`, and has a different
  `log` form.
- REPOINT of any locked document that item 4's `citations` lists needs its own suspension.
- Covering Codex sessions would need `.codex/environments/environment.toml`, which is locked.

Items 1, 2, 4, 6, 7 and 8 (the scripts and the Makefile target) create or edit no locked file.

Build order: 2 → 1 → 3 → 5 → 4, then 6, 7, 8 and 9.

---

## 1. Checkpoint identity, return and receipt verifier

1. **Capability:** Records the repository topology once, when a checkpoint starts. At return,
   checks the evidence and prints the *Identity* and *Repository state* blocks, ready to paste. In
   receipt mode, prints each of the Orchestrator's listed commands verbatim, with its raw output
   and exit code.
2. **Current location and control:** `engineering-role.md:36` (verify state), `:45-52` (two SHAs,
   verdict-only delta), `:107` (reachability before return); `docs/track-b/gauntlet-templates.md:134-145`
   and `:183-193`; `orchestrator-role.md:327-339`. These run by hand, from memory, at start, return
   and receipt. CP-21 spent 45 hand-written lines on these blocks
   (`docs/track-b/evidence/cp-21/checkpoint-return.md:16-60`); CP-16 kept ad-hoc `main-state.txt`
   and `handover-state.json`.
3. **Destination:** Script: pure git, no judgment, and the same inputs always give the same output.
4. **Implementation:** `scripts/gauntlet.py` (stdlib and git):
   - `start <cp>`: writes `.local/tmp/<cp>-start.json` with HEAD, `main`, the local `origin/main`
     (no fetch), `worktree list --porcelain`, `for-each-ref refs/heads refs/tags`, the stash list
     and the porcelain status. It never overwrites it: this is the checkpoint's only baseline.
   - `return <cp> <final_candidate_sha> [<evidence_tip>=HEAD]`: checks that `diff --name-only`
     stays inside `docs/track-b/evidence/<cp>/`. Runs `cat-file -e` and
     `merge-base --is-ancestor … gauntlet/<cp>` only on the SHAs in the return's *Identity* block
     and the verdict's *Candidate SHA*, skipping values labelled revision, Space or Hub, which are
     Hugging Face revisions (`docs/track-b/evidence/pres-2/baseline.md:81`,
     `docs/track-b/evidence/pres-3/publication-packet.md:483`). Checks that the verdict exists,
     reads `PASS` and cites `final_candidate_sha`; lists the branches, worktrees, tags and stashes
     created since `start`; compares the issued brief's SHA-256 with the canonical copy. Prints the
     blocks plus the evidence tip for the terminal message, since a file cannot contain its own
     commit SHA. Exits 1 if any check fails.
   - `receipt <cp> <final> <tip>`: runs `main`'s copy,
     `git show main:scripts/gauntlet.py | python3 - receipt …`, because `scripts/` is unlocked and
     the party being checked can edit it on `gauntlet/<cp>`. It prints each command listed at
     `orchestrator-role.md:330-334` and `docs/track-b/gauntlet-templates.md:186-190` verbatim, with
     its raw output and exit code (`orchestrator-role.md:339`), and adds no command.
5. **Notes:** No locked file is edited. Receipt mode waits for the Owner ruling named above;
   `orchestrator-role.md:337` declares the list exhaustive: no source reads and no tests.
   Discoverability: the Lead finds `start` and `return` through item 3's helper-index line; after
   the ruling, the Orchestrator records `receipt` in `progress.md` Setup State.

## 2. Plan checklist extractor and brief checker

1. **Capability:**
   - `bar <plan> "<heading>" [--at SHA]` prints a plan section verbatim, from its heading to the
     next heading of the same or higher level, together with the plan's SHA-256 at that commit.
   - `check <file> --source <file>@<sha> [--source …]` checks that every `>`-quoted block in a
     brief, assignment or verdict appears byte for byte in one of the sources at its commit.
   - `brief <brief.md>` checks that all ten required fields are present (`engineering-role.md:19-30`),
     with no `[...]` placeholders left, one checkpoint and one numeric timebox, and that the plan
     file exists and the cited section resolves. It prints the brief's SHA-256.
   - `identity <file> [--at SHA]` prints the file's revision line and SHA-256, the identity a
     publication brief names (`AGENTS.md:130-131`).
2. **Current location and control:** `orchestrator-role.md:204` (validation before dispatch) and
   `:220-222` (the Lead validates the brief again); `engineering-role.md:58`, `:69` and `:109`
   (an excerpt missing from the plan invalidates `PASS`); `docs/track-b/gauntlet-templates.md:81-84`,
   `:101-103` and `:150`. Each is done by reading and copying by hand. CP-16's Critic
   re-implemented the extraction (`docs/track-b/evidence/cp-16/critic-audit.py:18-21`). Anchor
   identities are hashed by hand (`docs/track-b/evidence/cp-21/checkpoint-return.md:20-21`). The
   PRES-2 verdict quotes two files (`docs/track-b/evidence/pres-2/integration.md:9-27`); the CP-20
   assignment indents its quote (`docs/track-b/evidence/cp-20/integration-assignment.md:18-52`).
3. **Destination:** Script. The work is text extraction, hashing and byte comparison.
4. **Implementation:** `scripts/bar.py` uses only the standard library and reads each source with
   `git show <sha>:<file>`. Headings must match exactly. Leading whitespace, then the `>` and one
   following space, are stripped before comparison; each quote block must match within one source.
   On failure it exits 1 and prints the first line that does not match.
5. **Notes:** No locked file is edited. It checks form only; the brief's content stays the
   Orchestrator's decision. Items 1 and 5 use it. Discoverability: item 3's helper-index line.

## 3. Session start hook

1. **Capability:** At every session start, resume, clear, compaction or fork: (a) points
   `core.hooksPath` at the main checkout's `.githooks` when it is unset or its directory is
   missing; (b) prints at most 10 lines of git state and one helper-index line.
2. **Current location and control:** `AGENTS.md:103-107` assumes `core.hooksPath` is set, but
   nothing sets it in a fresh clone or cloud container. Locally it is set once
   (`progress.md:285-287`); each cloud clone must set it again (`progress.md:292`), and this
   session needed the Owner's instruction. Git also commits without running any hook when
   `core.hooksPath` points to a missing directory, for example after the worktree that set it is
   removed (tested 2026-10-01): the secret guard silently stops running. The state check
   (`engineering-role.md:36`) and the branch declaration (`AGENTS.md:183`) are done by hand.
3. **Destination:** Hook: `SessionStart` with matcher `startup|resume|clear|compact|fork`
   (hooks#sessionstart), command `python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/session_start.py"`
   (hooks#reference-scripts-by-path). Its plain stdout reaches the agent's context
   (hooks#exit-code-0).
4. **Implementation:** The script (stdlib only; always exits 0; its own errors in one line):
   - finds the main checkout with `git rev-parse --path-format=absolute --git-common-dir`;
   - reads the value only with `git config --get core.hooksPath`, never `--list`, which would also
     print the container's injected `GIT_CONFIG_*` entries (`progress.md:293-294`);
   - writes `core.hooksPath` only when it is unset or its directory is missing, and says so;
   - prints the branch, short HEAD, `main` ahead/behind `origin/main` (no fetch), the number of
     dirty files, the worktrees, any `gauntlet/*` branches and the stash count;
   - prints one helper-index line: `scripts/gauntlet.py` (`start`, `return`, `critic-open`,
     `critic-close`) and `scripts/bar.py` (`bar`, `check`, `brief`, `identity`), each with `--help`.
5. **Notes:** Needs the suspension for `.claude/settings.json` and `.claude/hooks/session_start.py`,
   since the script sets how agents run (`AGENTS.md:23-24`); it expressly authorizes the write,
   which only restores the guard (`AGENTS.md:106`). The hook prints only git state and the helper
   line, never `progress.md`, role documents or anchors (`AGENTS.md:116`). It writes no ref
   snapshot: it re-fires on resume, compaction and fork (hooks#sessionstart), so item 1's `start`
   is the only baseline. Cloud sessions with one repository run it from `.claude/settings.json`
   (cloud-environments#what-carries-over-from-your-setup). Codex sessions get no guard:
   `.codex/environments/environment.toml:5-6` has `script = ""` and is locked (`AGENTS.md:23-24`).
   Discoverability: none needed; it runs automatically.

## 4. Checkpoint disposition and reclamation

1. **Capability:** Adds subcommands to `scripts/gauntlet.py`. `inspect [branch]` prints the
   INSPECT block; for an unknown branch it reports the tip, age, ahead/behind, `diff --stat`, any
   attached worktree, and live documents citing SHAs reachable only from that branch.
   `discard <cp> <k>` creates the DISCARD tag. `citations <cp>` lists the documents to repoint.
   `reclaim <cp>` deletes the branch and worktrees, enforcing the tag guard. `land-commands <cp>`
   prints the LAND commands for the Owner and never runs them.
2. **Current location and control:** `AGENTS.md:184` and `:186-193`;
   `docs/track-b/gauntlet-templates.md:195-239`; `orchestrator-role.md:348-354`. This is done by
   hand for each closed checkpoint. CP-16's `docs/track-b/evidence/cp-16/branch-citations.txt` is
   `git grep -n` output; it lists `capstone_v21.md` twice and an amendment sheet, all locked.
3. **Destination:** Script. `AGENTS.md:191` itself calls this ref hygiene "tedium, not judgement".
4. **Implementation:** `reclaim` refuses unless `evidence/<cp>` or `archive/<cp>-attempt-*`
   resolves and `merge-base --is-ancestor <tip> <tag>` holds. It refuses any branch that is not
   `gauntlet/*`, removes only worktrees under `.local/worktrees/<cp>/`, then runs
   `git worktree prune`. `citations` uses `git grep -n`. `inspect` is read-only.
5. **Notes:** The script edits no locked file, but `citations` may list locked documents;
   repointing those needs a suspension. LAND remains authored by the Owner (`AGENTS.md:191`); the
   script only prints it. It enforces the tag guard; the Owner-disposition guard (`AGENTS.md:192`)
   stays procedural, because an agent's own DISCARD tag satisfies the tag check. Discoverability:
   the Orchestrator records it in `progress.md` Setup State.

## 5. Integration Critic launcher `/critic`

1. **Capability:** Launches the one fresh Integration Critic from a generated prompt. The Critic
   gets the assignment and protocol, works in a clean detached worktree, and does not see the
   Lead's conversation.
2. **Current location and control:** `engineering-role.md:41` and `:56-73`;
   `docs/track-b/gauntlet-templates.md:70-120`. The Lead writes each assignment by hand (the four
   under `docs/track-b/evidence/cp-16/` and `cp-20/` are 82–128 lines), then creates and removes
   the worktree. `docs/track-b/evidence/cp-20/integration-assignment.md` holds the worktree
   command, the plan's SHA-256, a ~30-line verbatim excerpt and the no-Git-write rules. Isolation
   is "cooperative" (`engineering-role.md:73`). CP-20's first Critic returned FAIL
   (`docs/track-b/evidence/cp-20/integration-attempt-1/integration.md:1`); an API limit stopped
   CP-21's first before any verdict (`docs/track-b/evidence/cp-21/checkpoint-return.md:48-49`).
3. **Destination:** Skill with `context: fork`. The forked subagent "doesn't see your conversation
   history" and gets the skill content as its prompt (skills#run-skills-in-a-subagent): the prompt
   is generated, and history isolation holds, forks excluded, since a conversation fork inherits
   the history (sub-agents#fork-the-current-conversation). Read-only stays cooperative
   (`engineering-role.md:73`): the subagent starts in the Lead's working directory
   (sub-agents#write-subagent-files), a background subagent keeps `Bash`, `Edit` and `Write`
   (sub-agents#available-tools), and `allowed-tools` "does not restrict which tools are available"
   (skills#pre-approve-tools-for-a-skill).
4. **Implementation:**
   - **Before:** the Lead writes a short assignment with only the judgment fields: plan path,
     section heading, artifact paths, decision-bearing inputs (`engineering-role.md:58`),
     reproduction commands and tolerance. `gauntlet.py critic-open <cp> <sha> <assignment>` creates
     `.local/worktrees/<cp>/critic-<n>`, checks that it is clean and that `HEAD` equals the SHA, and
     records the details in `.local/tmp/critic-open.json`.
   - **`.claude/skills/critic/SKILL.md`:** frontmatter `context: fork`, `agent: general-purpose`,
     `allowed-tools: Bash(python3 ${CLAUDE_PROJECT_DIR}/scripts/gauntlet.py *)`. The body's
     `` !`python3 ${CLAUDE_PROJECT_DIR}/scripts/gauntlet.py critic-brief` `` injects the assignment,
     the plan's SHA-256 and the excerpt (via item 2), and extracts the protocol
     (`engineering-role.md:56-73`) and the verdict form (templates §2) at run time with
     `git show HEAD:…`, so SKILL.md copies neither. Both places use `${CLAUDE_PROJECT_DIR}`
     (skills#available-string-substitutions): injected commands run in the session's current
     directory, which moves with `cd` (skills#how-injected-commands-run). The fixed text tells the
     Critic to run every command as `git -C <wt> …` or `cd <wt> && …`, since it starts in the
     Lead's working directory (sub-agents#write-subagent-files). It writes
     `docs/track-b/evidence/<cp>/integration.md` and performs no Git write.
   - **After:** `gauntlet.py critic-close` checks that the worktree is still clean and `HEAD` is
     unchanged, removes the worktree and hashes the verdict. The Lead commits the verdict as the
     sole Git writer (`engineering-role.md:39`). The Lead's five actions: assignment,
     `critic-open`, `/critic`, `critic-close`, commit.
5. **Notes:** Needs the `.claude/skills/critic/` suspension. Model invocation stays on: with
   `disable-model-invocation: true`, "Only you can invoke the skill"
   (skills#control-who-invokes-a-skill), so the Owner would relay every run, against
   `engineering-role.md:40` and `orchestrator-role.md:200`. The launch stays guarded: `critic-brief`
   exits non-zero when no `critic-open` record matches a clean worktree at its SHA, and a failed
   injected command "aborts the entire skill invocation" (skills#when-an-injected-command-fails).
   The Orchestrator never invokes it (`orchestrator-role.md:37`). `engineering-role.md:62` still
   says `<path-outside-repo>` where practice is `.local/worktrees/…` (`AGENTS.md:65-72`); the Owner
   may align it at a future suspension. Depends on items 1 and 2. Discoverability: with model
   invocation on, the skill's description is always in context (skills#control-who-invokes-a-skill).

## 6. Post-deploy publication receipt

1. **Capability:** Collects the actual public identity of every surface: `origin` `main`
   (`git ls-remote`); the bytes Pages serves, hashed with SHA-256 and compared with
   `git show <landing>:docs/index.html`; the Space's revision and a per-file check, reusing
   `scripts/deploy_space.py` check mode, and the served Space page; the MLflow mirror, via
   `scripts/verify_mlflow_mirror.py`; the links, via `scripts/check_links.py`. It writes dated
   records under `reports/presentation/release-checks/` and prints the packet's §8 table: intended
   identity, observed identity, UTC time, result and outstanding action.
2. **Current location and control:** `docs/track-b/publication-runbook.md:49-52` and `:54-96`;
   `docs/track-b/publication-packet-template.md:164-190`. These records are built by hand at each
   release. No script in `scripts/` produces `2026-09-29-postdeploy-pages-identity.json`,
   `-space-identity.json` or `-summary.json`. The Space record has `"exact_bytes_match": false` and
   `"bytes_match_after_removing_only_hosting_injection": true`
   (`reports/presentation/release-checks/2026-09-29-postdeploy-space-identity.json:6-11`).
3. **Destination:** Script. The work is anonymous HTTP requests and hashes. The standing
   daily-publication exception (`AGENTS.md:162-175`) requires automated validation that fails
   closed, and this script can serve it.
4. **Implementation:** The script takes `--landing <sha>`, `--bundle <dir>` and
   `--expect <sha256>`. Each surface is checked independently, keeping the first failure and every
   retry (`docs/track-b/publication-runbook.md:90-91`). For the Space page it removes only the
   Hugging Face `window.huggingface` creator-metadata script and records both hashes, `sha256` as
   served and `normalized_sha256`, as the 2026-09-29 record does. It exits 1 on any other mismatch.
   The browser checks stay in `scripts/check_reader_paths.py`, which runs in a separate Playwright
   environment (`scripts/check_reader_paths.py:10-11`); the receipt only cites their records.
5. **Notes:** Read-only and network-bound, with no credential. No locked file is edited.
   Discoverability: `docs/track-b/publication-runbook.md` (unlocked) cites the script; the reference
   should be written as `file::symbol`, so `tests/test_42_publication_runbook.py` checks it.

## 7. Pre-review check runner

1. **Capability:** Runs the offline checks of `docs/track-b/publication-runbook.md` §9 in order
   and writes one dated record: `uv run pytest -q` on Python 3.13
   (`docs/track-b/publication-runbook.md:312`); the CI steps parsed from
   `.github/workflows/tests.yml`, under Python 3.12; `make verify` and `make lint-publication`;
   rebuild determinism (`scripts/rebuild_presentation.py`, then an empty `git status --porcelain`);
   `scripts/check_links.py`; and `scripts/publication_guard.py tree`, which is expected to fail
   before the `--final` build and is recorded that way.
2. **Current location and control:** `docs/track-b/publication-runbook.md:308-330`;
   `Makefile:118-131`. These are run by hand at each publication, and each result is recorded by
   hand.
3. **Destination:** Script plus a `make prerelease` target.
4. **Implementation:** `scripts/prerelease.py` holds a list of (name, argv, expected exit code). It
   continues past failures and records the argv, exit code, duration and the last 40 lines of
   output in `reports/presentation/release-checks/<date>-prerelease.json`. It exits 1 on any
   unexpected result. `tests.yml` is parsed with PyYAML, which is already in `uv.lock`
   transitively, or with a small line parser. The standard's §10 browser checks
   (`docs/track-b/publication-runbook.md:318-329`) stay out.
5. **Notes:** No locked file is edited. It replaces the manual run and its recording and adds no
   check. Discoverability: `docs/track-b/publication-runbook.md` §9 (unlocked) cites it as
   `file::symbol`.

## 8. `progress.md` omission diff

1. **Capability:** Compares `progress.md` with the last delivered version (`HEAD`, or
   `--against <ref>`). It confirms that the seven required sections are present and in order,
   groups every removed bullet by section, and lists separately the removals from the sections that
   may never be dropped: Setup State, Strategic Anchors, Standing Scope Decisions, Blockers / Open
   Questions and Notes for Future Sessions (`orchestrator-role.md:383-388` and `:391`).
2. **Current location and control:** `orchestrator-role.md:372-394`. The Orchestrator already
   verifies its diff (`orchestrator-role.md:293`), so `git diff` lists the removals; grouping and
   protected-section checks are done by reasoning over the 1,140-line file at each update.
3. **Destination:** Script.
4. **Implementation:** `scripts/progress_diff.py` splits the file on `## ` headings and into
   bullet blocks by indentation, then prints the set difference grouped by section. It always
   exits 0, because deciding whether each removal was resolved or pruned stays the Orchestrator's
   judgment.
5. **Notes:** No locked file is edited (`progress.md` is program state, `AGENTS.md:46-47`). It
   reads `progress.md`, so only the Orchestrator uses it, and it must never be wired into a hook
   (`AGENTS.md:116`). Discoverability: the Orchestrator records it in `progress.md` Setup State.

## 9. Credential-store deny rules

1. **Capability:** Claude Code refuses the listed ways of reading the credential stores or dumping
   the environment.
2. **Current location and control:** `AGENTS.md:87-93`. The rule exists only in the agent's memory.
3. **Destination:** Settings: `permissions.deny` in `.claude/settings.json`. A permission rule is
   not a hook, and no script is needed.
4. **Implementation:** A trailing ` *` also matches the bare command, so `Bash(printenv *)` covers
   `printenv` (permissions#wildcard-patterns); parentheses inside a rule are literal
   (permissions#permission-rule-syntax). The rules:
   - `Read(~/.zshrc)`, `Read(~/.zshrc.*)`, `Read(~/.zshrc~)`, `Read(~/.zshenv)`,
     `Read(~/.zprofile)`, `Read(~/.zsh_history)`, `Read(~/.zsh_sessions/**)`,
     `Read(~/.bash_profile)`, `Read(~/.bashrc)`, `Read(~/.profile)`, `Read(~/.bash_history)`,
     `Read(~/.claude/shell-snapshots/**)` (UNVERIFIED: this path does not appear in the docs)
   - `Bash(env)`, `Bash(env -0)`, `Bash(/usr/bin/env)`, `Bash(sh -c env)`, `Bash(printenv *)`,
     `Bash(export)`, `Bash(export -p)`, `Bash(declare -p *)`, `Bash(declare -x *)`,
     `Bash(typeset *)`, `Bash(set)`, `Bash(ps eww *)`, `Bash(python3 -c *print(os.environ)*)`,
     `Bash(launchctl getenv *)`
5. **Notes:** Needs the `.claude/settings.json` suspension. "Bash rules match the whole command
   text" (permissions#bash), and a deny rule "isn't a security boundary around the program"
   (permissions#bash-rule-limits): another spelling of the same command still runs. Read deny rules
   cover Claude's file tools, file commands Claude Code recognizes (`cat`, `head`, `tail`, `sed`,
   `tee`) and redirection targets, but not arbitrary subprocesses (permissions#read-and-edit). The
   rules back up the written rule and `scripts/secret_guard.py`, which Git runs outside Claude's
   tools, and replace neither. Discoverability: none needed; the harness applies them.

---

## Considered and left as is

- **Lockdown edit guard** (PreToolUse on edits to locked paths): it would also block edits the
  Owner has authorized, so every suspension would need an Owner toggle. That adds a step.
- **`git push` or commit-to-`main` guard:** the Owner authorizes pushes per task, and the daily
  pipeline pushes to `main`. A deny or ask rule would add an approval to every authorized push.
  The pre-push hook already guards against secrets and placeholders.
- **Stop hook that runs the tests:** it adds a step to every turn; tests are the Lead's and CI's.
- **Injecting `progress.md` or the role documents at session start:** a hook cannot know the
  session's role, so this would break the Lead's isolation (`AGENTS.md:116`).
- **Interview-answer capture:** `scripts/qa_append.py` already makes it deterministic.
- **Duplicate test runs in CI** (`.github/workflows/tests.yml:22-35`): they cost CI minutes, not
  agent or Owner work.
- **End-of-task handover packet `/handover`:** it duplicates `AGENTS.md:159` into a locked skill,
  and the saving is marginal.
