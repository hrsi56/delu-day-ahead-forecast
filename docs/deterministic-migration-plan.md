Status: proposal for Owner review — not ratified, no governance effect.

# Deterministic-migration plan: moving guardrails and workflows out of LLM memory

| Field | Value |
|---|---|
| Date | 2026-10-01 |
| Authority | ROLE-MAINTENANCE analysis (`AGENTS.md:118`), authorized by the Owner. Read-only except for this one file. |
| Base | `main` at `940eb98` |
| Inputs | (1) The repository, which governs. (2) A Claude Code Insights report: LLM-generated, 114 sessions across several projects. Only findings about this repository are used, and they are treated as hypotheses. (3) A Claude Code health check ("doctor") of the Owner's Mac, used in the appendix only. |
| Effect | None. Nothing here amends a locked file. Each change waits for an Owner decision and, where named, a Lockdown suspension. |

**Reading conventions**

- `path:line` cites the repository at `940eb98`.
- "Report" means the Insights report, and "doctor" the health check.
- Layers:
  - **script**: a deterministic program in `scripts/`;
  - **skill**: a Claude Code skill;
  - **CH**: a Claude Code hook;
  - **GH**: a git hook in `.githooks/`;
  - **CI**: `.github/workflows/`;
  - **server**: GitHub repository settings;
  - **Owner**: a manual Owner action.
- Documentation tags:
  - **[S]**: the Claude Code settings reference bundled with Claude Code 2.1.286 in the cloud container. That is the settings JSON schema and the `update-config` reference sections "Hook Events", "Hook Structure", "Hook JSON Output", "Permission Rule Syntax", "Settings File Locations" and "Constructing a Hook".
  - **[W]**: the bundled `session-start-hook` reference for Claude Code on the web, sections "Hook Basics", "Environment Variables" and "Wrap up".
  - **[O]**: behaviour observed in the cloud container's own harness hooks. It is not documentation.
  - **unverified**: not confirmed from documentation reachable in this session. The task forbade network calls, so the online documentation was not read. Each unverified item has an acceptance test that settles it before anyone relies on it.

---

## 0. Executive summary

1. **Only two layers enforce anything today:** the git hooks and the CI test suite. Every other rule lives in prose that an agent must remember. The git guard is inactive in a fresh clone, because nothing sets `core.hooksPath`. Where no credential values are present it passes everything (`scripts/secret_guard.py:133-134`).
2. **Three P0 items cover every actor:** Claude, Codex, the Owner at the terminal, and the daily pipeline.
   - P0-1: activate the guard in every clone.
   - P0-2: add a value-free leak scan (salted fingerprints and environment-dump shapes) to the hooks and CI.
   - P0-7: add server-side GitHub rulesets.
3. **Claude hooks are accident guards, not a security boundary.** PreToolUse, Stop and UserPromptSubmit hooks can mechanically refuse what `AGENTS.md` forbids (P0-4) and enforce the Lockdown (P0-5). An Owner-only, session-bound authorization record supplies the exceptions (P0-6). An agent with Bash can evade a hook, so the hard boundaries remain the server rules and the credentials.
4. **The environment-dump class that leaked the DagsHub token is still open.** There are 13 live bare `os.environ[...]` reads in `src/`, `scripts/` and `tests/`. P0-3 adds an AST lint and a pytest redaction plugin, with a fake-fixture proof.
5. **CP-21 stall, from the record:** a bare `git commit` (`docs/track-b/gauntlet-templates.md:215`) hung in an unconfigured editor. Separately, the Owner's "do the LAND" instruction contradicted three locked texts.
   - **Recommendation: Option A.** The Owner runs `scripts/land.py`, and no governance text changes.
   - Option B, agent-executed LAND, comes with its exact `AGENTS.md` text.
6. **A checkpoint ledger** lives in `.local/` as the Lead's working notes. It is not program state.
   - Resume works on the same machine only.
   - Moving a checkpoint between the Mac and the cloud needs the Owner to transfer a git bundle.
7. **Most P2 items need the role files amended first.**
   - The Integration Critic cap contradicts `engineering-role.md:32` and `:40`.
   - Hebrew status updates contradict "Reply in English" in `orchestrator-role.md:460` and `engineering-role.md:134`.
8. **The daily pipeline stays outside the Claude hooks.** It must be a deterministic script with the git hooks active in its clone. P0-8 adds six requirements to the CP-18 brief.
9. **Packaging:** two Lockdown suspensions (SUSP-1 for `.claude/**`, SUSP-2 for governance text), two maintenance tasks that touch no locked file, and Owner-only GitHub settings.
10. **Nine Owner decisions**, D1 to D9 below, each with a recommendation.

---

## 1. Owner decisions required

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | Publish salted SHA-256 fingerprints of the credential values, so the leak scan works without the values (P0-2) | (a) Full-value and prefix fingerprints. (b) Full-value only. (c) No fingerprints: the value guard covers machines that hold values, and patterns cover the rest. | **(a).** Only for values with at least 128 bits of estimated entropy; the generator refuses anything weaker. A preimage attack on SHA-256 of a 128-bit secret is infeasible, and the salt prevents correlation. The prefix fingerprint catches a value truncated by a repr. |
| D2 | Extend the locked set to the guard tooling: `.githooks/**`, `scripts/secret_guard.py`, `scripts/publication_guard.py`, `scripts/leak_scan.py`, `scripts/credential_fingerprints.py`, `scripts/land.py`, `scripts/checkpoint_state.py`, `.github/workflows/**` | (a) All of them. (b) Hooks and guard scripts only. (c) No extension. | **(a)**, ratified in SUSP-2 *after* MT-1 and MT-2 land. Otherwise every later fix to the guards needs its own suspension before the guards exist. An agent that can edit the guard can unguard itself. |
| D3 | The form of an Owner authorization or suspension record (P0-6) | (R1) A directive line in the Owner's prompt, captured by a UserPromptSubmit hook. (R2) The same directive, signed with an Owner SSH key that requires Touch ID for each signature. (R3) No record: conversation only, as today. | **R1 now**, R2 later if forged directives become a concern. Cross-session messages may arrive as user turns (unverified). |
| D4 | LAND (P1-2, P1-3) | (A) The Owner runs `scripts/land.py`. Preflight, squash, the hand commit and both tags are scripted around the Owner's commit; RECLAIM is handed to an agent. No governance change. (B) An agent executes LAND from a recorded approval, with the `AGENTS.md` text in P1-3. | **A.** It removes both causes of the CP-21 stall and keeps "authored, not generated" (`AGENTS.md:187`). B moves the irreversible public act to an agent and needs SUSP-2. |
| D5 | Integration Critic round cap (P2-1) | (a) Default cap 2, kept in the ledger, with an Owner override per checkpoint; amend `engineering-role.md:32,40` and add a field to templates §1. (b) A per-brief field only, with no default. (c) No cap. | **(a).** After the cap the Lead returns `INCOMPLETE` with the open findings, which `engineering-role.md:101` already allows. |
| D6 | Response language (P2-5) | (a) Amend both role-file Language sections: Hebrew to Yarden, English artifacts, never a third language; plus a deterministic script detector in a Stop hook. (b) A project `language` setting [S]. (c) A user-scope `language` setting on the Mac only. | **(a).** (b) would also turn briefs and returns into Hebrew, against the role files. (c) never reaches cloud sessions. `CLAUDE.md` stays a pointer (`AGENTS.md:123`). |
| D7 | "No rendering for self-verification" as policy (P2-2) | (a) A rule in `engineering-role.md` with an exemption for a phase the brief names as browser or visual acceptance; a CH guard enforces it. (b) The CH guard only, with no policy text. (c) Neither. | **(a).** `AGENTS.md:151` scopes the rule to Q&A entries only. PUBLISH_RULES §§9–10 require real browser acceptance, hence the exemption. |
| D8 | GitHub-side boundaries (P0-7) | (a) Rulesets: no force-push or deletion of `main`; preserved tags immutable; `gauntlet/*` cannot be created. Plus secret scanning with push protection. Keep the Claude GitHub App's write access, which authorized tasks like this one need. (b) As (a), with the App read-only. (c) Nothing server-side. | **(a).** These are the only rules no local process can bypass. |
| D9 | Resuming a checkpoint across machines (P1-5) | (a) Same machine only; cross-machine through an Owner-transferred `git bundle` plus the ledger. (b) An amendment allowing a `gauntlet/*` push to a private remote. (c) Same machine only, nothing else. | **(a).** `AGENTS.md:160-161` keeps candidates unpushed, and (a) needs no amendment. |

The open CP-18 decision on where the daily pipeline runs (`docs/track-b/final-product-space-plan-2026-09-30.md:399`) is not re-decided here. P0-8 lists what any choice must satisfy.

### 1.1 Conflicts with `AGENTS.md` found during this analysis

| # | Conflict | Resolution in this plan |
|---|---|---|
| C1 | This task's single commit and push contradict `AGENTS.md:157-159` | It is the Owner's own task-scoped publication authorization, named as the prompt's sole exception. It is not a delegation. |
| C2 | The cloud environment's default is to open a pull request after a push | Not done. `AGENTS.md:157` forbids it and the Owner excluded it. |
| C3 | The cloud harness Stop hook tells agents to "commit and push" uncommitted work [O] | It contradicts `AGENTS.md:157-159` in every cloud session. P0-4 counters it deterministically. |
| C4 | The Owner wants Hebrew status updates; both role files say "Reply in English" (`orchestrator-role.md:460`, `engineering-role.md:134`) | D6 |
| C5 | The Critic cap requested here contradicts `engineering-role.md:32` and `:40` ("never impose an arbitrary round count") | D5 |
| C6 | The report's agent-LAND rule and its new `CLAUDE.md` rules contradict `AGENTS.md:123` and `:191` | Rejected (§7). Agent LAND is offered only as Option B. |
| C7 | Cross-machine resume needs the `gauntlet/*` work to leave the machine; `AGENTS.md:160-161` keeps it local, and `.local/` is machine-local (`AGENTS.md:65-72`) | D9 |
| C8 | `AGENTS.md:103` says `core.hooksPath` "points at `.githooks/`" as a fact. In a fresh clone it is unset (`progress.md:285-292`). | P0-1 makes the stated state true. SUSP-2 adds one sentence on how it is established. |
| C9 | `AGENTS.md:65-72` puts scratch files in `.local/`, while this task allowed exactly one new file | No scratch file was created. The commit message went to `git commit -F -` on standard input. |

---

## 2. Inventory of existing mechanisms

| Mechanism | Where | Trigger | What it enforces | Who it covers | Gap |
|---|---|---|---|---|---|
| `pre-commit`, `commit-msg` hooks | `.githooks/pre-commit:5-12`, `.githooks/commit-msg:5-12` | `git commit`, only when `core.hooksPath` is set | A credential value in staged blobs or the message. Fails closed when python3 is missing (`:11-12`). | Anyone committing in an activated clone | Inactive in fresh clones. A no-op where no values are present. |
| `pre-push` hook | `.githooks/pre-push:7-29` | `git push` | The secret guard on outgoing commits, then the publication guard (`:21-28`) | Anyone pushing from an activated clone | Same activation gap |
| `scripts/secret_guard.py` | `:12-14` (sources), `:54-68` (`credentials()`), `:110-127` (outgoing set), `:133-134` (no values: exit 0) | Called by the hooks | Value-based scan: environment, `launchctl getenv`, `~/.zshrc` exports. Values of 12 characters or more (`:30`). | As above | No values in CI or in a cloud session without configured variables: passes everything. No pattern or dump detection, by design (`docs/track-b/credential-exposure-2026-09-24.md:20-27`). |
| `scripts/publication_guard.py` | `:29` (`refs/heads/main`), `:61-80` (pre-push), `:72` (other refs skipped) | pre-push; CI on `main` (`.github/workflows/tests.yml:39-41`) | No placeholder page and no non-final build record on `main` | Pushes to `main` | Checks only `main`, as intended |
| `scripts/governance_selftest.py` | `:39-48` (corpus), `:177-190` (self-test) | Manual only. Not in the Makefile, CI or tests. | D-CP0-20: no role is denied the means for an obligation | Whoever runs it | Not automated |
| `scripts/verify_release.py` | `:1-15` | `make verify`; CI (`tests.yml:31-32`) | Cross-surface parity, zero runtime calls, link discipline | Every push | — |
| `scripts/lint_publication.py` | `:1-21` | `make lint-publication`; CI through `tests/test_37_publication_lint.py` | Publication Standard §§4–5 | Every push | — |
| `scripts/check_links.py` | `:1-18` | Manual (needs the network); `tests/test_33_check_links_gate.py` uses a mocked probe | External links answer 200 | Manual | — |
| `scripts/qa_append.py` | `:1-24` | The Orchestrator files Q&A entries | Deterministic `.docx` append with RTL markup | Orchestrator | — |
| `Makefile` | `:1-131` | `make <target>` | Build, verify and lint targets; `publication-guard` (`:128-131`) | Human and agents | No `hooks` or bootstrap target |
| CI `invariant-tests` | `.github/workflows/tests.yml:3-4`, `:17-41` | Every push, every branch | pytest, `verify_release`, WASM equivalence, publication guard on `main` | Every push, after it is public | No leak scan, no check of locked paths |
| Codex environment | `.codex/environments/environment.toml:1`, `:5-6` | A Codex session starts | Setup script is empty. The file is autogenerated. | Codex | Does not activate the hooks |
| Secret-guard tests | `tests/test_28_secret_guard.py:1-8`, `:25-35` | CI | The guard blocks a random fake token and never prints it | CI | — |
| CP-16 conftest | `tests/cp16/conftest.py:3-10` | pytest | Skips the two CP-16 tests that read `os.environ['CP16_LEDGER']` | pytest | Fixes two tests, not the class |
| Cloud harness Stop hook (user scope, outside the repository) | [O] | Every stop in a cloud session | Tells the agent to commit and push uncommitted or unpushed work | Cloud Claude | Contradicts `AGENTS.md:157-159` |
| `.claude/` | Absent | — | — | — | Every Claude hook, skill or agent definition proposed here is a new file in the locked set (`AGENTS.md:23-24`) |

---

## 3. Friction → root cause → existing coverage → gap

| # | Friction (evidence) | Root cause (record) | Existing coverage | Gap |
|---|---|---|---|---|
| F1 | DagsHub token published in CP-20 evidence. The report says "committed CI log"; the record says a Critic guard log under `docs/track-b/evidence/cp-20/` (`credential-exposure-2026-09-24.md:8-12`). **The record wins.** | Two tests read `os.environ['CP16_LEDGER']` bare. pytest printed a truncated `environ(...)` repr. The pre-push scan was pattern-based and missed a bare 40-character hex value (`:25-27`). | The value guard (`secret_guard.py`); the CP-16 conftest skip | Fresh clones; no values in cloud or CI; 13 bare reads remain; no rule about dumps in logs or artifacts; no CI scan |
| F2 | The guard must be enabled by hand in every clone (`progress.md:285-292`) | Git does not activate hooks from a clone | None | P0-1 |
| F3 | CP-21 LAND stall. The report: "No response requested" three times. The record: interrupted, then executed by a separate session (`cp-21-landing-2026-09-30.md:11-18`). | The editor (`:8-10`) and a rule conflict (P1-1) | The Owner set a global editor (`:22-23`) | P1-1 to P1-3 |
| F4 | Checkpoints cut off mid-Critic and mid-release by session limits (report, "Where Things Go Wrong") | No durable, machine-readable phase state. `workbench.md` is retired (`AGENTS.md:121`). | Lead notes (free-form) | P1-4, P1-5 |
| F5 | A follow-up chart-label request lost in the v4 publication checkpoint (report) | No queue for requests made mid-checkpoint | None | P2-3 |
| F6 | Over-verification: a CP-3B review loop cut short; rendering for self-checks (report, "How You Use Claude Code") | No round cap; rendering is barred only for Q&A (`AGENTS.md:151`) | None (`engineering-role.md:40` forbids caps) | P2-1, P2-2 |
| F7 | Status updates in Chinese or Arabic during the CP-21 closure (report) | No language check; the role files require English | None | P2-5 |
| F8 | A `git commit` blocked in vim; zsh quoting errors; a missing Playwright WebKit cache (report) | A bare `git commit` in templates §4 (`:215`); no session preflight | The Owner's global editor | P2-4 |
| F9 | Lockdown overhead (report) | Suspension is conversational. Neither enforcement nor a cheap record exists. | Prose (`AGENTS.md:1-37`) | P0-5, P0-6 |
| F10 | Cloud sessions are told to push by the harness [O] | A user-scope Stop hook with no project-level counter | Prose (`AGENTS.md:157`) | P0-4 |

---

## 4. Components

### 4.0 Mechanism semantics this plan relies on

**A Claude hook is an accident guard, not a security boundary.** A hook pattern-matches a tool call. An agent with Bash can write the same action in a form the pattern does not recognise: `python -c` with `subprocess`, encoded strings, a script file. Every CH component below is designed to stop honest mistakes and drift, and says so. The boundaries that hold against a determined agent are the server rules (P0-7) and which credentials a session can reach.

| # | Mechanism | Used by | Source | Status |
|---|---|---|---|---|
| M1 | Events `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SessionStart`, `SessionEnd`, `PreCompact`, `ConfigChange` | All CH | [S] schema `hooks` keys | Verified |
| M2 | Matcher is a tool-name string, with `A\|B` alternation | All PreToolUse | [S] "Hook Structure", "Common tool matchers" | `\|` verified. Regex such as `mcp__github__.*` unverified, so the guard also filters on `tool_name` itself. |
| M3 | `if` pre-filter in permission-rule syntax (`Bash(git *)`) | Not relied on | [S] schema `if` | Verified. Not used, because compound commands may slip it (unverified). |
| M4 | PreToolUse `hookSpecificOutput.permissionDecision: "deny"` with `permissionDecisionReason`; `decision: "block"` is deprecated for PreToolUse | P0-4, P0-5, P2 | [S] "Hook JSON Output" | Verified |
| M5 | `decision: "block"` with `reason` for Stop, PostToolUse and UserPromptSubmit | P0-5, P2-5 | [S] "Hook JSON Output" | Verified |
| M6 | Exit code 2 is a "blocking error" | Fail-closed wrapper | [S] schema `asyncRewake`; [O] the harness Stop hook exits 2 to block | "Blocking" verified. The exact effect for PreToolUse is unverified; acceptance test T-M6. |
| M7 | Other non-zero exits and timeouts are non-blocking | Failure modes | — | Unverified. The design assumes fail-open, keeps guards fast, and uses exit 2 for "cannot run". |
| M8 | `stop_hook_active` in the Stop input | Loop guards | [O] the harness Stop hook reads it and exits 0 when true | Observed; documentation section unverified |
| M9 | Per-command `timeout` in seconds | All CH | [S] schema `timeout` | Verified. Default and on-timeout behaviour unverified. |
| M10 | `additionalContext` (into the model's context) and `systemMessage` (shown to the user) | P2-4, P0-6 | [S] "Hook JSON Output" | Verified. Whether `systemMessage` also enters the model's context is unverified. |
| M11 | SessionStart input `source` = `startup\|resume\|clear\|compact`; `$CLAUDE_PROJECT_DIR`, `$CLAUDE_ENV_FILE`, `$CLAUDE_CODE_REMOTE` | P0-1, P2-4 | [W] "Hook Basics", "Environment Variables" | Verified |
| M12 | A committed `.claude/settings.json` applies to cloud sessions once it is on the cloned branch | Coverage | [W] "Wrap up": a session-start hook merged into the default branch is used by all future sessions | Verified for SessionStart. Assumed for the other hooks in the same file; acceptance test T-M12. |
| M13 | Precedence: user < project < local < flag < policy | Conflicts | [S] `enabledPlugins` description; "Settings File Locations" | Verified for scalar keys. Whether hook arrays from several scopes all run is unverified; [O] the cloud's user-scope hooks run in sessions. |
| M14 | `disableAllHooks` and `allowManagedHooksOnly` (managed only) | Kill switch; bypass risk | [S] schema | Verified that they exist. Which scope wins for `disableAllHooks` is unverified. |
| M15 | `permissions.deny` with `Read(path)` rules | P0-4 | [S] "Permission Rule Syntax" | Verified. `~` expansion and behaviour in `bypassPermissions` mode are unverified. |
| M16 | The `env`, `language` and `skillOverrides` keys | P2-4, P2-5, appendix | [S] schema | Verified |
| M17 | SKILL.md frontmatter `name` and `description` | P1-5 | [W] the bundled skill's own frontmatter | Observed. Other keys unverified. |
| M18 | UserPromptSubmit input carries the prompt text | P0-6, P2-3 | — | **Unverified, and a core assumption.** First acceptance test (T-M18). |
| M19 | PreToolUse fires for subagent tool calls, and the launcher is named `Agent` or `Task` | P2-1 | — | Unverified |
| M20 | Hooks and deny rules apply in `bypassPermissions` mode, which the Owner's sessions use (doctor) | All CH | — | Unverified. Acceptance test T-M20, and every other acceptance test, runs in that mode. |
| M21 | Settings edits can take effect mid-session | P0-5 | [S] "Constructing a Hook", step 6 (the settings watcher) | Verified. The guard must protect its own configuration. |
| M22 | Codex loads none of the above | Coverage | — | By construction. Codex's own approval and sandbox modes are unverified. |

#### 4.0.1 Proposed `.claude/settings.json` (every CH component; created under SUSP-1)

```json
{
  "env": { "GIT_EDITOR": "true" },
  "permissions": {
    "deny": [
      "Read(~/.zshrc)", "Read(~/.zshrc.*)", "Read(~/.zsh_history)", "Read(~/.bash_history)",
      "Read(~/.zsh_sessions/**)", "Read(~/.claude/shell-snapshots/**)"
    ]
  },
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh session_start", "timeout": 30 } ] }
    ],
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh prompt", "timeout": 10 } ] }
    ],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh pre", "timeout": 10 } ] },
      { "matcher": "Write|Edit|NotebookEdit|Read|Grep|Glob", "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh pre", "timeout": 10 } ] },
      { "matcher": "Agent|Task", "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh pre", "timeout": 10 } ] },
      { "matcher": "mcp__github__.*|mcp__Claude_Browser__.*|mcp__claude-in-chrome__.*", "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh pre", "timeout": 10 } ] }
    ],
    "PostToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh post", "timeout": 10 } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh stop", "timeout": 20 } ] }
    ],
    "SessionEnd": [
      { "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run.sh session_end", "timeout": 10 } ] }
    ]
  }
}
```

`GIT_EDITOR=true` makes an agent's message-less `git commit` or `git tag -a` abort at once with an empty message, instead of hanging (F8). It applies only to processes Claude Code starts, so the Owner's terminal keeps its own editor.

`.claude/hooks/run.sh` is POSIX `sh`, so it behaves the same on macOS and Linux. It fails closed, using the same interpreter discovery as `.githooks/pre-commit:6-10`:

```sh
#!/bin/sh
# Fail closed: a guard that cannot run blocks (exit 2). SessionStart and SessionEnd cannot block.
here="$(cd "$(dirname "$0")" && pwd)"
for py in python3 /usr/bin/python3; do
  if command -v "$py" >/dev/null 2>&1; then exec "$py" "$here/guard.py" "$@"; fi
done
echo "claude-guard: python3 not found; refusing (AGENTS.md)" >&2
exit 2
```

`guard.py` uses the standard library only, makes no network call, and runs no git command except `git rev-parse` and `git status`. It never prints environment values. The suggestion to read JSON with `jq` is dropped, because `jq` is not guaranteed on the Mac.

### 4.1 P0 — Secrets and hard gates

#### P0-1 Guard activation in every clone

| Field | Content |
|---|---|
| 1. Capability | `.githooks/` is active in every clone and worktree before any commit or push |
| 2. Current state | Activation is a manual `git config` (`.githooks/pre-commit:2-3`). `AGENTS.md:103` asserts it as a fact; `progress.md:285-292` records that fresh clones must re-enable it. The Makefile and CI never set it. The Codex setup script is empty (`.codex/environments/environment.toml:5-6`). It was unset in this container until this task's own step 1. |
| 3. Target layer | **CH SessionStart** (Claude, local and cloud), **Codex setup script** (Owner, through the Codex app), and **`make hooks`** (human, the daily pipeline). Git cannot activate hooks from a clone, so each actor's own bootstrap is the lowest layer that can. |
| 4. Implementation | `session_start` mode of `guard.py`: let `want = $CLAUDE_PROJECT_DIR/.githooks` and `have = git config --get core.hooksPath`. If unset, set it to `want`. If it equals `want` or `.githooks`, it is active. Otherwise report `MISMATCH` and **never overwrite**. Changing a set value belongs to the Owner (`AGENTS.md:106`). Emit one `additionalContext` line, such as `secret guard: active`. Makefile target: `hooks:` → `git config core.hooksPath "$$(git rev-parse --show-toplevel)/.githooks"` then `git config --get core.hooksPath`. Codex: the Owner sets the same command as the Codex environment's setup script. Linked worktrees, such as Critic snapshots, share the repository config. |
| 5. Coverage | Local Claude ✔. Cloud Claude ✔ (M12). Codex ✔ only after the Owner's setup script. Human ✔ through `make hooks`; the Owner's Mac clone is already active (`progress.md:285-287`). |
| 6. Governance | `.claude/settings.json` and `.claude/hooks/*` are locked (SUSP-1). The Makefile target is not locked (MT-1). The Codex setup is agent configuration, but the Owner's own action needs no suspension. |
| 7. Failure modes | SessionStart cannot block a session (M11), so this step fails open. Once active, the git hooks fail closed (`.githooks/pre-commit:11-12`), and the CI scan (P0-2) catches what an inactive clone lets through. A mismatch never auto-overwrites. Cloud clones are fresh each session, so the hook runs every time. Not a Claude session, so the daily pipeline runs `make hooks` itself (P0-8). |
| 8. Acceptance | In a scratch clone under `.local/tmp/`: run the hook with `CLAUDE_PROJECT_DIR` pointing at it, and `core.hooksPath` equals `<clone>/.githooks`. A second run is idempotent. Preset another value, and the output is `MISMATCH` with the value unchanged. Then stage a file holding a random fake token exported as `GUARD_FIXTURE_TOKEN`, as `tests/test_28_secret_guard.py:25-35` does: the commit is blocked. |
| 9. Effort / deps | S. Needs SUSP-1 for the CH part, and MT-1 for the Makefile. |

#### P0-2 Value-free leak scan (fingerprints and dump shapes) in the git hooks and CI

| Field | Content |
|---|---|
| 1. Capability | Block credential values where the values are unavailable (CI, Codex, a cloud session without configured variables), and block environment dumps in any committed file. The value guard is left exactly as it is. |
| 2. Current state | With no values found, `secret_guard.py:133-134` returns 0 and passes everything. CI has no scan (`tests.yml:17-41`). The pattern scan that missed the token was replaced by the value scan (`credential-exposure-2026-09-24.md:20-27`). |
| 3. Target layer | A new **script**, `scripts/leak_scan.py` (standard library only). **GH**: called by `pre-commit`, `commit-msg` and `pre-push` *after* `secret_guard.py`. **CI**: the first step, over the pushed range and the tree. GH and CI cover every actor. CI acts after publication, but turns an exposure into a red check within minutes. |
| 4. Implementation | **F1 fingerprints.** Committed `.githooks/credential-fingerprints.json` with one entry per name: `{name, length, alphabet, salt, sha256(salt‖value), prefix_len, sha256(salt‖prefix)}`. Generated only by the Owner on the Mac: `scripts/credential_fingerprints.py write` reads the values inside the process from the same sources as `secret_guard.py:54-68`, refuses any value below 128 bits (`length × log2(alphabet)`), and prints names only. Scan: for each entry, find runs of `[alphabet]{length,}`, hash every window of `length` (and of `prefix_len`), compare, and report the name and path, never the value. **F2 dump shapes.** A Python environ repr (regex `environ\(\{'[A-Za-z_]+': '`); `declare -x NAME=` and `export NAME=` lines and `NAME=value` lines whose name matches `secret_guard.CREDENTIAL_NAME` (`:28`); a `securityToken=` query value that is not a placeholder (`AGENTS.md:101-102`). **F3 known prefixes** as a cheap backstop, never the only layer. Modes: `pre-commit`, `commit-msg <file>`, `pre-push <remote>` (the same outgoing set as `secret_guard.py:110-127`), `ci <before> <after>`, `tree`. CI step, placed before `uv sync`: `python3 scripts/leak_scan.py ci "${{ github.event.before }}" "${{ github.sha }}"`, with `fetch-depth: 0` on checkout. For a new branch (`before` = 40 zeros), it scans the tree. |
| 5. Coverage | Every actor in an activated clone: local and cloud Claude, Codex, the human, the daily pipeline. CI covers every push, wherever it came from. |
| 6. Governance | New scripts, the fingerprint file, edits to `.githooks/*` and `tests.yml`, and new tests. None is locked today, so they ship as MT-1 (an Owner-authorized maintenance task). If D2 is ratified first, they need a suspension. Generating fingerprints reads values, so it is an Owner-only action. |
| 7. Failure modes | Fingerprint file absent: F1 is skipped with a notice and F2 and F3 still run. File malformed: fails closed. Unreadable CI range: fails closed. False positives: F1 none in practice; F2 can hit documentation that quotes a literal dump, so documents use the escaped regex form, as here; F3 can hit fixtures, so tests generate fakes at run time, like `test_28`. Rotation: the list is append-only, so a revoked value stays detectable. Truncation shorter than `prefix_len` is missed, as it is by the value guard. Same `sh` and stdlib behaviour on macOS and Linux. Daily data-only records cannot match a fingerprint. |
| 8. Acceptance | Fake fixtures only. A token generated at test time plus a test fingerprint file, then a staged file holding the token: blocked, naming the fake entry, and the token is absent from stderr. A file holding only the first half: blocked by the prefix. A file with `FAKE_TOKEN_000000000000` and no fingerprint: passes F1. A runtime-built environ-repr line: blocked by F2. This plan's escaped regex: passes. `ci` mode with an all-zero `before`: scans the tree. A low-entropy value given to `write`: refused. |
| 9. Effort / deps | M. Depends on D1; the Owner generates fingerprints once after MT-1. |

#### P0-3 Environment-dump prevention at the source

| Field | Content |
|---|---|
| 1. Capability | Make the bare `os.environ[...]` KeyError class impossible to merge, and keep the environment out of pytest failure output |
| 2. Current state | Prose only (`AGENTS.md:96-100`). `tests/cp16/conftest.py:6-10` skips two tests. Live bare reads: `src/cp21/execution.py:216`, `src/cp21/daily.py:81`, `src/delu_forecast/tracking.py:54`, `src/cp20/extract.py:516`, `src/cp20/execution.py:35,123`, `src/cp20/probe.py:22`, `scripts/cp16_v2.py:51`, `scripts/cp20_weather.py:127`, `scripts/cp21_blocks.py:136`, `tests/cp16/test_state_results.py:19,94`, `tests/cp16/reproduce_components.py:16`. Frozen copies exist under `models/champion/code/` and `docs/track-b/evidence/`. The likely mechanism, settled by the acceptance test: pytest's long traceback prints the arguments of the failing `os._Environ.__getitem__` frame, which is the environment's repr. |
| 3. Target layer | **CI test plus pytest plugin.** Tests are where the leak happened, and CI runs them for every push from every actor. |
| 4. Implementation | (a) `tests/test_NN_environ_access.py`: walk the AST of `src/`, `scripts/`, `app/`, `space*/` and `tests/`, and fail on any `Subscript(Load)` of `os.environ` (or `environ` imported from `os`). `.get`, `os.getenv` and assignments are fine. An explicit allowlist covers the hash-frozen CP-16 tests (`tests/cp16/conftest.py:3-4`); `models/champion/code/**` and `docs/track-b/evidence/**` are not scanned. Each entry carries a reason, and CI prints the count. (b) A plugin, `tests/environ_redact.py`, registered with `-p` in `pytest.ini` so no hash-bound file changes. A `pytest_runtest_makereport` hookwrapper rewrites any failed report's text from `environ({` to the end of that line as `environ(<redacted>)`, and `pytest_collectreport` does the same. (c) Optionally `--tb=short`, kept only if the acceptance test shows it is needed. |
| 5. Coverage | CI for every push; locally whenever tests run, for every actor |
| 6. Governance | Tests, `pytest.ini` and the plugin are not locked (MT-1). Fixing the live call sites changes reviewed checkpoint code, so it goes through an ordinary checkpoint. Until then those sites stay on the allowlist with the reason "fix pending". The lint gates new code from day one. |
| 7. Failure modes | The allowlist can grow, so every entry needs a reason and the count is printed. Dynamic access (`getattr(os, "environ")[k]`) evades the lint; acceptable. Redaction touches only the environ repr. Failures are test failures, so CI fails closed. The daily pipeline is unaffected. |
| 8. Acceptance | Lint over a fixture tree: `os.environ['FAKE_MISSING']` fails with file and line; `.get` passes. A child pytest run whose environment holds `FAKE_TOKEN_000000000000`, with a test reading a missing variable: with the plugin, the output lacks the fake; without it (negative control), the output contains it. That proves both the mechanism and the fix. |
| 9. Effort / deps | S–M. MT-1, plus a later checkpoint for the call sites. |

#### P0-4 Agent command guard

| Field | Content |
|---|---|
| 1. Capability | Refuse, for agent tool calls, what `AGENTS.md` forbids: `--no-verify`; any change to `core.hooksPath`, `git -c core.hooksPath=…` or git aliases; `env`, `printenv`, `set`, `export -p`, `launchctl getenv`; reading `~/.zshrc`, its backups, shell history or shell snapshots; any `git push` or tag push; `gh` mutations and GitHub MCP mutations; `git commit` except on `gauntlet/*`; commits, merges, rebases, resets, reverts, cherry-picks or stash drops on `main`; history rewriting and destructive operations (`reset --hard`, `clean`, `filter-branch`, `push --force`, `tag -d`, and `branch -D` other than a dispositioned `gauntlet/*` whose tag resolves) |
| 2. Current state | Prose: `AGENTS.md:87-90`, `103-107`, `155-161`, `177`, `191`. In cloud sessions the harness Stop hook pushes the other way [O] (C3). |
| 3. Target layer | **CH PreToolUse** (Bash; Read, Grep and Glob; Write, Edit and NotebookEdit; `mcp__github__*`), plus **`permissions.deny`** for credential-file reads (M15). Git hooks cannot do this: they cannot tell an agent from the Owner or the daily pipeline, and both of those legitimately commit and push to `main` (`AGENTS.md:158`, `162-175`). **Accident guard only** (§4.0). |
| 4. Implementation | `guard.py pre` normalises the command. It splits on `;`, `&&`, `\|\|`, `\|`, `&` and newlines; unwraps `sh -c`, `bash -c`, `zsh -c`, `eval`, `$(…)` and backticks recursively; strips leading `VAR=value`, `command`, `env` with assignments, and `sudo`; and parses `git -C dir` and `-c k=v`. Rules then match on `argv`, never on substrings, so `rg "git push" docs/` is allowed. For `Read` and `Grep`, paths are resolved with `realpath` and compared with `$HOME/.zshrc*`, history files and snapshot directories. A deny is emitted as JSON (M4), e.g. `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"AGENTS.md § Git and publication authority: agents never push. Present the diff and a proposed commit message, or ask the Owner for an authorization record."}}`. `gh` CLI: read forms (`gh pr view`, `gh pr list`, `gh run list`, `gh run view`, `gh api` with no `-X`/`--method` other than GET and no `-f`/`-F`) are allowed; every other `gh` subcommand is denied. GitHub MCP: read tools (`get_*`, `list_*`, `search_*`, `pull_request_read`, `issue_read`) are allowed; every other `mcp__github__*` tool is denied unless a record allows it. An action matching an active P0-6 record is allowed and counted. |
| 5. Coverage | Local Claude ✔. Cloud Claude ✔ (M12). Codex ✗ (M22). Human ✗, by design. Daily pipeline ✗, by design: it must not be an LLM session (P0-8). |
| 6. Governance | `.claude/settings.json` and `.claude/hooks/guard.py` (SUSP-1). No text change: the guard enforces existing rules. |
| 7. Failure modes | A missing interpreter blocks (exit 2, M6). A timeout may fail open (M7), so the guard stays under 200 ms and makes no network or slow git call. A guard that is too strict blocks legitimate work: near-miss tests guard against that, and an Owner record unblocks a single action (this task would have needed `OWNER-AUTHORIZE push ref=<branch> count=1`). Interplay with the harness Stop hook: it asks for a push, the guard denies it, and the harness hook lets the next stop through (`stop_hook_active`, M8), so there is no loop. Behaviour in `bypassPermissions` mode (M20) and in subagents (M19) is unverified and tested explicitly. |
| 8. Acceptance | A table-driven test pipes fake `tool_input` JSON into `guard.py`. Every forbidden form, including `sh -c 'git push'`, `FOO=1 git push`, `git -c core.hooksPath=/dev/null commit` and `env`, is denied with a citation. Near-misses (`git status`, `git log --grep=push`, `rg "git push" docs`, `env -i python3 x.py`) are allowed. In a fixture repo, `git commit -m x` is denied on `main` and allowed on `gauntlet/cp-x`. A record with `count=1` allows one push, then denies. A live check in the Owner's real permission mode: `git push --dry-run origin HEAD` is denied. |
| 9. Effort / deps | M. Needs SUSP-1, and P0-6 for exceptions. |

#### P0-5 Lockdown guard

| Field | Content |
|---|---|
| 1. Capability | Prevent agent edits to the locked set, including the hook configuration itself, unless an Owner suspension record names the file. Detect any edit that slipped through before the turn ends. |
| 2. Current state | Prose (`AGENTS.md:1-37`). There is no machine-readable list and no detection. |
| 3. Target layer | **CH PreToolUse** (Write, Edit and NotebookEdit, plus Bash write heuristics); a **CH Stop** detector over `git status`, which is state-based and so catches what a Bash call slipped past the patterns; and a **CI** consistency test plus an informational CI report. A machine-readable manifest backs all three. |
| 4. Implementation | **Manifest** `.claude/governance/locked-paths` (globs): `AGENTS.md`, `CLAUDE.md`, `engineering-role.md`, `orchestrator-role.md`, `notebooklm-role.md`, `docs/track-b/gauntlet-templates.md`, `capstone_[Vv]*.md`, `capstone_M4_v2-plan.md`, `syllabus_v*.md`, `program-stage-sequence.md`, `docs/track-b/anchors/**`, `docs/PUBLISH_RULES.md`, `docs/track-b/publication-standard-v1.md`, `docs/track-b/rule-inventory.md`, `docs/track-b/cp-0-defects.md`, `docs/track-b/capstone_*-to-*-amendments.md`, `.claude/**`, `.codex/**`, plus the D2 additions. The manifest is a **floor, not the definition**: `AGENTS.md` locks categories ("all … ratified anchors regardless of filename", "any file that configures how agents run"), and the "stage-gated companion plan" (`AGENTS.md:16`) has no filename the Owner has named. A CI test checks that every backticked path or glob in `AGENTS.md:8-24` appears in the manifest. **PreToolUse:** a write to a manifest path is denied unless an active suspension names it. For Bash, a locked path combined with a write verb (`>`, `>>`, `tee`, `sed -i`, `perl -i`, `mv`, `cp`, `rm`, `git checkout --`, `git restore`, `git apply`, `patch`, `truncate`) is denied. Writes to `.claude/**` and `.claude/settings.local.json` are always denied without a suspension, so the guard protects its own configuration (M21). **Stop:** take `git status --porcelain=v1 -z` (tracked and untracked) ∩ manifest, minus the files active suspensions name. If that set is non-empty and `stop_hook_active` is false, return `{"decision":"block","reason":"Locked file <path> changed without a suspension: restore it or HALT and request one (AGENTS.md:26-30)"}`. If `stop_hook_active` is true, return only a `systemMessage` warning, so there is no loop. **Operational-record exception** (`AGENTS.md:57-61`): `progress.md` is not in the manifest. For `docs/track-b/cp-0-defects.md` the first version does not deny; instead the Stop hook shows the Owner its diff stat, because "status fields only" cannot be checked reliably. **CI:** list the locked paths each push changed. Informational, because the Owner's own ratification commits are legitimate. |
| 5. Coverage | Local and cloud Claude ✔. Codex ✗. Human ✗ (the Owner is exempt). CI report for every push. |
| 6. Governance | `.claude/**` (SUSP-1). The manifest is new text inside the lock; `AGENTS.md` stays authoritative. |
| 7. Failure modes | A glob mismatch is caught by the consistency test. `git stash` hides changes from `status` (residual risk; mentioned in the Stop message). A deleted locked file shows as `D`, so it is caught. `.claude/settings.local.json` should **not** be added to `.gitignore`, so that its creation stays visible to `git status`. |
| 8. Acceptance | An Edit to `AGENTS.md` is denied; with a suspension record naming `AGENTS.md` it is allowed; an Edit to `README.md` is allowed. `sed -i s/a/b/ AGENTS.md` is denied. A Write to `.claude/settings.local.json` is denied. Stop over a temp repo with a modified locked file: a block JSON; again with `stop_hook_active: true`: a `systemMessage` only. Consistency test negative control: removing one manifest line makes it fail. |
| 9. Effort / deps | M. Needs SUSP-1 and P0-6. |

#### P0-6 Owner authorization and suspension record

| Field | Content |
|---|---|
| 1. Capability | A machine-readable, task-scoped record that only the Owner can create, consumed by P0-4 and P0-5 (and by P1-3 if chosen), and spent at the end of the task |
| 2. Current state | Conversational only: the HALT procedure and suspension semantics are in `AGENTS.md:26-37`. This task's own authorization is prose in the prompt. `cp-21-landing-2026-09-30.md:19-21` records a task-specific instruction that authorized Owner-reserved operations. |
| 3. Target layer | **CH UserPromptSubmit** captures; **PreToolUse** consults; **PostToolUse** consumes; **SessionEnd** spends. UserPromptSubmit fires on a user's prompt, which an agent cannot emit, so the record derives from the Owner's own words and binds to the `session_id`. |
| 4. Implementation | Directive lines, at the start of a line in the Owner's prompt: `OWNER-SUSPEND files=AGENTS.md,engineering-role.md objective="…"`; `OWNER-AUTHORIZE push ref=<branch> remote=origin count=1`; `OWNER-AUTHORIZE critic-round cp=<cp> count=1`; (Option B only) `OWNER-AUTHORIZE land cp=<cp> evidence_tip=<40 hex> message_sha256=<64 hex>`; `OWNER-REVOKE all`. Record file: `.local/owner-records/<session_id>/<n>.json` = `{schema, kind, scope, session_id, created_at, prompt_sha256, uses_left, expires_at, spent_at, spent_reason}`. The prompt text itself is not stored. Scopes match exactly, with no globs beyond the explicit file list, and only in the same session. PostToolUse decrements `uses_left` after a successful matching call. The hook echoes every parsed record to the Owner as a `systemMessage`, and every unparsed directive as "nothing granted". **"Spent at terminal return"** cannot be observed by a machine, so it is approximated by the first of: SessionEnd, `uses_left` = 0, `OWNER-REVOKE`, or `expires_at` (default 12 h). The Stop hook shows active records, so the Owner can revoke when a task returns early. **Option R2:** the directive is signed (`ssh-keygen -Y sign -n delu-owner`) with an Owner key that needs Touch ID for each signature, and verified against an allowed-signers file under `.claude/governance/`. In the cloud, the Owner pastes the signed block. |
| 5. Coverage | Local and cloud Claude ✔. Codex ✗. Human: not needed. |
| 6. Governance | `.claude/hooks/*` (SUSP-1). The records put `AGENTS.md:32-37` into practice without changing it. Making the record the *only* valid form of suspension would be an amendment (D3, SUSP-2). |
| 7. Failure modes | M18 is unverified; if UserPromptSubmit cannot see the prompt, R1 is not possible and the plan falls back to R2. Cross-session messages may reach the hook as user turns (unverified), and R2 closes that hole. Agent writes to `.local/owner-records/` are denied by P0-4; that is an accident guard only, so R2 is the remedy if it matters. A deleted directory means nothing is granted, so it fails closed. Cloud records die with the container, which is what we want. |
| 8. Acceptance | UserPromptSubmit JSON carrying a directive creates the record, and the echo shows its scope. A push to the named ref is allowed once, then denied. A push to another ref is denied. SessionEnd marks the record spent. An agent Write to the record directory is denied. A malformed directive creates no record. |
| 9. Effort / deps | M for R1; an extra S for R2. D3. |

#### P0-7 Server-side protections

| Field | Content |
|---|---|
| 1. Capability | Boundaries no local process can bypass: no force-push or deletion of `main`; preserved tags are immutable; `gauntlet/*` is never on `origin`; known token formats are refused at push time |
| 2. Current state | Prose: `AGENTS.md:160-161`, `174`, `189`, `192`. The GitHub settings could not be inspected from here (unverified). |
| 3. Target layer | **Server** (GitHub repository rulesets, secret scanning). The Owner sets these. |
| 4. Implementation | Ruleset "main": `refs/heads/main`, block force pushes, restrict deletions; no pull-request requirement, because the Owner and the daily pipeline push directly. Ruleset "preserved tags": `refs/tags/land/*`, `refs/tags/evidence/*`, `refs/tags/archive/*`, restrict updates and deletions. Ruleset "never pushed": `refs/heads/gauntlet/*`, restrict creations. No bypass actors. Secret scanning with push protection on. Keep the Claude GitHub App's write access (D8). |
| 5. Coverage | Every actor, for these operations: agents, Codex, the human, the pipeline |
| 6. Governance | No repository file and no suspension; an Owner action. The Orchestrator records the configuration in `progress.md`. |
| 7. Failure modes | Whether every rule type is available on a personal public repository is unverified; confirm under Settings → Rules. A push-protection false positive on a daily push fails closed, and the day is published as failed (`AGENTS.md:171`). A wrong tag needs a deliberate ruleset edit by the Owner, which is the point. |
| 8. Acceptance | The Owner, by hand: push a throwaway `archive/ruleset-probe-attempt-0`, then try to delete it: rejected. Push `gauntlet/ruleset-probe`: rejected. From a scratch clone, force-push a fake commit to `main`: rejected. |
| 9. Effort / deps | S. Owner-only. D8. |

#### P0-8 Daily-pipeline compatibility

| Field | Content |
|---|---|
| 1. Capability | None of P0-1 to P0-7 may break the standing exception (`AGENTS.md:162-175`), and the pipeline must itself be guarded |
| 2. Current state | The exception was approved on 2026-09-30. The pipeline belongs to CP-18 (`final-product-space-plan-2026-09-30.md:495-502`). Where it runs is still open: the Owner's machine unattended, or GitHub Actions (`:399`, `:530`). PUBLISH_RULES grants no unattended authority by itself (`docs/PUBLISH_RULES.md:510-517`). The exception's conditions: fail-closed validation; the secret guard and pre-push guards never bypassed (`AGENTS.md:170-173`). |
| 3. Target layer | **Requirements for the CP-18 brief** (no file now), plus an allowlist check in **GH and CI**. |
| 4. Implementation | **R1.** The pipeline is a deterministic script, not an LLM session, so the Claude hooks never see it. If an LLM is ever involved, it holds no push authority. **R2.** Its clone runs `make hooks` (or the Actions job sets `core.hooksPath`) before any commit, so the secret guard, leak scan and publication guard run on every daily push. **R3.** On Actions, the value guard sees values only if the step's environment holds them; the fingerprint scan (P0-2) works either way. **R4.** Each daily commit carries a trailer, `Delu-Daily: <delivery date>`. A pre-push and CI check refuses a trailer-bearing commit that touches anything outside the data paths the CP-18 brief names (`AGENTS.md:166`, `168`). **R5.** It only fast-forwards `main`, so the P0-7 rules never block it. **R6.** A failure is published as failed or stale (`AGENTS.md:171`), never retried around a guard. |
| 5. Coverage | The pipeline, on whichever host the Owner chooses |
| 6. Governance | Part of the CP-18 brief. The R4 check is code in MT-1 or CP-18. No suspension now. |
| 7. Failure modes | The Mac asleep at the gate: shown as stale (plan `:530` already notes that Actions is unreliable for a hard deadline). Hooks inactive in an Actions clone: caught by the R2 acceptance test. Whether pushes made with Actions' default token trigger other workflows is unverified, so CI on daily commits may need an explicit call. |
| 8. Acceptance | On top of the CP-18 negative controls already planned (`final-product-space-plan-2026-09-30.md:505-512`): a daily commit touching a path outside the allowlist is refused by pre-push and by CI, and a daily bundle holding a fake fingerprinted token is refused. |
| 9. Effort / deps | S now (requirements); M inside CP-18 |

### 4.2 P1 — LAND and resumable checkpoints

#### P1-1 Diagnosis of the CP-21 stall, from the repository record

| # | Finding | Evidence | Deterministic fix |
|---|---|---|---|
| 1 | The Owner's hand `git commit` hung in the default editor, because none was configured | `cp-21-landing-2026-09-30.md:8-10`. The template prescribes a bare `git commit` (`gauntlet-templates.md:215`). | P1-2 uses `git commit -e -F <proposed message>` in the Owner's editor (nano, `cp-21-landing-2026-09-30.md:22-23`). `GIT_EDITOR=true` for agents (§4.0.1). |
| 2 | The Owner's instruction "do the LAND for me; you have full approval" went to the Orchestrator session, which "was interrupted before it acted" | `cp-21-landing-2026-09-30.md:11-13` | — |
| 3 | The instruction contradicted three locked texts, each saying no authorization grants it: "LAND is owner-authored by hand and never delegated … never offer to"; "you may never delegate the landing commit"; "Never delegated, never agent-executed". `AGENTS.md:155` adds that no brief, authorization or PASS grants publication. | `AGENTS.md:191`, `orchestrator-role.md:353-354`, `gauntlet-templates.md:210` | An agent has no deterministic way to settle "the Owner said X" against "the rule says nobody may authorize X". An empty or "no response" turn is a plausible symptom. This is a hypothesis: the record does not quote the agent's replies, and the report's "three times" cannot be checked against it. Option A removes the conflict. Option B removes it by amendment. |
| 4 | A separate session then committed, tagged and pushed, and the record calls the instruction task-specific, not an amendment | `cp-21-landing-2026-09-30.md:14-21` | A precedent, with no mechanism. P0-6 gives such instructions a recorded form. |
| 5 | Both tags are lightweight | `cp-21-landing-2026-09-30.md:58` | Any automation must push the tags by name. `--follow-tags` pushes only annotated tags (§7). |

#### P1-2 LAND Option A: an Owner-run script (no governance change)

| Field | Content |
|---|---|
| 1. Capability | Turn LAND into a short, verified sequence the Owner runs by hand. The commit stays authored by hand, and RECLAIM is handed to an agent. |
| 2. Current state | Manual commands in templates §4 (`gauntlet-templates.md:197-237`); the receipt commands are at `orchestrator-role.md:330-336`. |
| 3. Target layer | **Script** run by the Owner, plus a PreToolUse rule refusing the `stage` and `tag` subcommands to agents. A script is the lowest layer that makes the checks deterministic while leaving the act with the Owner, as `AGENTS.md:187` and `:191` require. |
| 4. Implementation | `scripts/land.py` (stdlib and git only): `preflight <cp> --final <sha> --evidence-tip <sha>` (read-only; agent or Owner) runs the templates §4 receipt and INSPECT checks: `docs/track-b/evidence/<cp>/integration.md` exists and reads PASS at `final_candidate_sha`; `git diff --name-only final..tip` lies within `docs/track-b/evidence/<cp>/`; the branch is ahead of `main` and 0 behind; `main` equals the local `origin/main` (the Owner fetches first); the tree is clean; `core.hooksPath` is active; `land/<cp>` and `evidence/<cp>` are absent; `leak_scan.py` passes over `main..tip`. `stage <cp>` (Owner): `git checkout main && git merge --squash gauntlet/<cp>`, check that the index tree equals the evidence tip's tree, write the return's proposed message (templates §3, `:172`) to `.local/land/<cp>/COMMIT_MSG`, then **stop** and print `git commit -e -F .local/land/<cp>/COMMIT_MSG`. `tag <cp>` (Owner, after the commit): check `HEAD` has a single parent equal to the previous `main`, and a tree equal to the evidence tip's tree; create `land/<cp>` at `HEAD` and `evidence/<cp>` at the tip; verify both resolve; print the push command `git push origin main land/<cp> evidence/<cp>` for the Owner to type. `verify-remote <cp>`: compare `git ls-remote` with the local refs. `handoff <cp>`: print the RECLAIM packet. `reclaim <cp>` (agent; `AGENTS.md:191` makes RECLAIM agent-executed): refuses unless `evidence/<cp>` or an `archive/<cp>-*` tag resolves and `git rev-list gauntlet/<cp> --not --tags` is empty (`AGENTS.md:192`); then deletes the branch, removes the worktrees the checkpoint created, and prunes. |
| 5. Coverage | The Owner at the terminal (Mac). Claude may run `preflight` and `reclaim`. Codex may run `preflight`. |
| 6. Governance | `scripts/land.py` is not locked (MT-2), unless D2 is ratified first. Optionally, one pointer line in templates §4 to the script (SUSP-2). No `AGENTS.md` change. |
| 7. Failure modes | Every check fails closed, before any ref changes. A stale `origin/main` is detected because the script compares refs; the Owner fetches. Interrupted between `stage` and the commit: the index holds the squash, and re-running `stage` refuses, with instructions to reset by hand. Owner-only. The script runs no `git push` itself. |
| 8. Acceptance | A fixture repo with a fake `gauntlet/cp-x`, a verdict file and a two-SHA chain. `preflight` passes. A verdict reading FAIL is refused. A non-evidence delta is refused. `stage` leaves exactly the squash staged. After a scripted commit, `tag` creates both tags. `reclaim` refuses before the tags exist and succeeds after. No subcommand touches a remote. |
| 9. Effort / deps | M. MT-2, plus P0-2 for the scan step. |

#### P1-3 LAND Option B: agent-executed LAND from a recorded approval (needs an `AGENTS.md` amendment)

**This plan does not edit `AGENTS.md`.** Under the HALT procedure (`AGENTS.md:26-30`), the exact text that would change is:

| File:line | Current text | Proposed text |
|---|---|---|
| `AGENTS.md:157` | "… `origin` is a public repository; treat every push as an irreversible public act that only its owner may take." | Append: "The only exceptions are the standing daily-publication exception below and the single LAND push that a recorded Owner LAND approval authorizes (§ *Branch and ref lifecycle*)." |
| `AGENTS.md:158` | "- **Never commit to `main`.** `main` is written by Yarden, by hand, after his own review." | Insert after that sentence: "The exceptions are the standing daily-publication exception below and a squash commit made under a recorded Owner LAND approval, whose message is the approved message byte for byte." |
| `AGENTS.md:162` | "It is the only exception to "never publish" and "never commit to `main`"." | "Together with a recorded Owner LAND approval (§ *Branch and ref lifecycle*), it is one of the two exceptions to "never publish" and "never commit to `main`"." |
| `AGENTS.md:187` | "**LAND** — Yarden runs `git merge --squash gauntlet/<cp>`, reviews the staged tree, and commits **by hand**;" | "**LAND** — Yarden either runs `git merge --squash gauntlet/<cp>`, reviews the staged tree and commits **by hand**, or records a LAND approval (below) for an agent to execute;" The rest of the bullet is unchanged. |
| `AGENTS.md:191` | "… **LAND is owner-authored by hand and never delegated.** Agents never merge, squash, rebase, fast-forward, or cherry-pick into `main`, and never offer to." | "… **LAND is owner-decided.** The Owner lands by hand, or records one LAND approval in their own words. The approval names the checkpoint, the `evidence_tip_sha` and the SHA-256 of the exact commit message. Under that approval, and only for that checkpoint, a session other than that checkpoint's Lead runs `scripts/land.py run` end to end: preflight, squash, the commit with the approved message unchanged, both tags, one push of `main`, `land/<cp>` and `evidence/<cp>`, and post-push verification. Any preflight mismatch stops the run before the commit. The approval is single-use and is spent at that push. Outside such an approval, agents never merge, squash, rebase, fast-forward, or cherry-pick into `main`, and never offer to." |
| Consistency, same suspension | `orchestrator-role.md:351-354` ("**LAND** (yours, by hand …)" and "you may never delegate the landing commit"); `gauntlet-templates.md:210` ("**LAND — owner, by hand. Never delegated, never agent-executed.**"); `docs/track-b/rule-inventory.md` (the corresponding rule rows) | Same meaning: "by hand, or by a recorded Owner LAND approval executed with `scripts/land.py run`". |

**Mechanics.** The directive is `OWNER-AUTHORIZE land …` (P0-6, preferably R2). `land.py run` refuses unless the approval's tip and message hash match. The P0-4 push rule allows exactly one push of those three refs.

**Trade-off.** "Authored, not generated" (`AGENTS.md:187`) survives only as "the Owner approved these exact bytes". Every guard here is an accident guard, so a recorded approval is only as strong as P0-6. Recommendation: Option A (D4).

| Field | Content |
|---|---|
| 1. Capability | An agent executes the whole LAND, push included, from one recorded Owner approval |
| 2. Current state | Forbidden (`AGENTS.md:157-158`, `187`, `191`; `orchestrator-role.md:353-354`; `gauntlet-templates.md:210`). The only precedent is the task-specific instruction recorded at `cp-21-landing-2026-09-30.md:19-21`. |
| 3. Target layer | **Script** (`land.py run`), with a CH record (P0-6) and the P0-4 push exception. Server rules (P0-7) still apply. |
| 4. Implementation | `land.py run <cp> --approval <record>`: everything in P1-2's `preflight`; check that `sha256(COMMIT_MSG)` equals the approved hash; squash; `git commit -F` (no editor); both tags; `git push origin main land/<cp> evidence/<cp>` (one push; the git hooks run); `verify-remote`; mark the record spent. Any mismatch stops the run before the commit. |
| 5. Coverage | Local and cloud Claude. Codex ✗, because no record mechanism exists there. Human: unchanged; the Owner may still land by hand. |
| 6. Governance | SUSP-2 (the texts above) plus SUSP-1 (the record kind) plus D2 (lock `land.py`) |
| 7. Failure modes | A partial run (committed, not pushed) leaves local state the Owner inspects; the script never retries a push around a hook. A forged approval is possible under R1, so R2 is advised. A stale `origin/main` makes preflight refuse. |
| 8. Acceptance | Fixture remote (a bare repository under `.local/tmp/`): an approved run lands, tags, pushes and verifies. A wrong message hash refuses before the commit. A second run with the same record is refused. |
| 9. Effort / deps | M on top of P1-2. D3 (R2 preferred), D4 = B. |

#### P1-4 Checkpoint ledger (`CHECKPOINT_STATE`)

| Field | Content |
|---|---|
| 1. Capability | Durable, machine-readable phase state for one checkpoint, so that a new session resumes in one step without becoming program state |
| 2. Current state | The Lead keeps free-form notes (`AGENTS.md:121`). `workbench.md` was retired and is git-ignored (`.gitignore`). `progress.md` belongs to the Orchestrator, whose contract allows "one tracking document, not two" (`orchestrator-role.md:378`). |
| 3. Target layer | A **script** (sole writer path) plus a **skill** (P1-5) plus a CH guard against direct edits. A script gives atomic writes and validation that prompt text cannot. |
| 4. Implementation | **Location:** `.local/checkpoints/<cp>/state.json`. It is the Lead's recovery material (`AGENTS.md:65-72`), never committed: a commit after the final candidate would break the verdict-only delta (`engineering-role.md:45-50`). **Schema v1:** `{schema: 1, checkpoint, brief: {path, sha256}, plan_anchor: {file, sha256}, branch: "gauntlet/<cp>", phases: [{name, status: pending\|in_progress\|done\|failed\|skipped, started_at, finished_at, sha, evidence: [path]}], final_candidate_sha, evidence_tip_sha, critic: {cap: 2, rounds_used, open_findings: [{id, summary}]}, pending_user_requests: [{id, received_at, prompt_sha256, excerpt, status: open\|done\|deferred\|not_a_request, how}], next_action: {command, reason}, timebox_hours, rev, updated_at}`. **Phases:** `brief_verified`, `state_verified`, `plan_aloud`, `build`, `tests`, `candidate_frozen`, `integration_critic`, `verdict_committed`, `return_drafted`, `returned`. **Forbidden fields:** anything about milestones, tracks, the next checkpoint or acceptance, so it cannot become program state. **Writer:** `scripts/checkpoint_state.py` (`init`, `phase`, `critic-start`, `critic-result`, `request-add`, `request-resolve`, `next`, `validate`, `show`). Atomic: an `fcntl` lock file, `--expect-rev N` compare-and-swap, temp file in the same directory, `fsync`, `os.replace`, directory `fsync`. A PreToolUse rule denies Write and Edit on `state.json`, forcing the script path. "Lead only" stays procedural: bounded subagents get no ledger path in their brief, and whether hook input distinguishes a subagent is unverified (M19). **Validate:** schema; legal statuses and order; every `sha` passes `git cat-file -e`; evidence paths exist; `brief.sha256` matches the file; `rounds_used ≤ cap` unless an Owner record exists; if both terminal SHAs are set, the delta lies within `docs/track-b/evidence/<cp>/`. |
| 5. Coverage | Local Claude ✔. Cloud Claude: within one container only (P1-5). Codex: can call the script; no guard. Human: can read it. |
| 6. Governance | The script is not locked (MT-2) unless D2 comes first. The guard rule is SUSP-1. No text change, since the ledger is working notes. The Orchestrator's receipt stays the exhaustive command list (`orchestrator-role.md:337`) and never reads the ledger as authority. |
| 7. Failure modes | A crash mid-write leaves the old file intact (atomic replace). Concurrent writers: CAS refuses. Clock skew is harmless (`rev` orders). `.local/` deleted: the ledger is lost, but evidence stays on the branch, as designed. Works on macOS and Linux (POSIX `fcntl`). |
| 8. Acceptance | `init` then phases in order: `validate` passes. Hand-editing `status` to an illegal value: `validate` fails. Two writers with the same `--expect-rev`: one wins and one is refused. A fake SHA: `validate` fails. Kill `-9` during a write: the old file stays readable. |
| 9. Effort / deps | M. MT-2, plus SUSP-1 for the guard rule. |

#### P1-5 Resume skill and resume paths

| Field | Content |
|---|---|
| 1. Capability | Resume an interrupted checkpoint from the ledger in one step, and state plainly which paths cannot work |
| 2. Current state | Relaunches with fresh briefs (report, "How You Use Claude Code"). Cloud sessions are fresh shallow clones without `.local/`, credentials or local branches (`progress.md:289-291`). |
| 3. Target layer | **Skill** `.claude/skills/checkpoint-resume/SKILL.md`, with the validation in the script. The skill only sequences deterministic commands. |
| 4. Implementation | Frontmatter (M17): `name: checkpoint-resume`; `description: Resume an interrupted Track B checkpoint from .local/checkpoints/<cp>/state.json. Use only in an ENGINEERING-LEAD session holding the same brief.` Steps: (1) `python3 scripts/checkpoint_state.py validate <cp>`, and stop on failure. (2) Check `brief.sha256` against the brief in hand, and stop on mismatch. (3) `show`: phases, open findings, pending requests. (4) Resolve pending requests first (P2-3). (5) Re-verify the evidence of every `done` phase with `git cat-file -e` and the evidence paths; re-run any `in_progress` phase from its start. (6) Run `next_action.command`. (7) After each phase, call `phase … done` with its evidence. Never read `progress.md` (`AGENTS.md:116`). |
| 5. Coverage and resume paths | **Same machine, new session:** ✔. Ledger, branch and worktrees are all local. **Local → cloud:** ✗ by default. `gauntlet/*` is never pushed (`AGENTS.md:160-161`), and `.local/` is absent in the cloud. **Owner action:** `git bundle create` of `main..gauntlet/<cp>`, uploaded into the cloud session with the ledger. Large caches do not travel (CP-21's `.local/artifacts/cp-21/` was 62 MB, `cp-21-landing-2026-09-30.md:127`), so only phases without heavy compute resume. **Cloud → local:** ✗ by default, because the agent may not push. The agent produces a bundle and the ledger and sends them as a chat attachment. **Owner action:** `git fetch <bundle> gauntlet/<cp>:gauntlet/<cp>`. Attachment size limits are unverified. **Cloud → cloud:** same as local → cloud; containers are ephemeral. Codex: same-machine only. |
| 6. Governance | `.claude/skills/**` (SUSP-1). The cross-machine paths need no amendment under D9(a). |
| 7. Failure modes | A brief hash mismatch stops the resume. Missing worktrees are recreated from the branch, never from the ledger. The bundle's prerequisite commit must exist on the receiving side, so the skill prints it. |
| 8. Acceptance | Interrupt a fixture checkpoint mid-`tests`; a new session invokes the skill, which validates, re-runs `tests` and continues. With a corrupted ledger it stops before acting. A bundle round trip in two scratch clones reproduces the same tip SHA. |
| 9. Effort / deps | S. P1-4, SUSP-1. |

### 4.3 P2 — Token efficiency and ergonomics

#### P2-1 Integration Critic round cap

| Field | Content |
|---|---|
| 1. Capability | At most N Integration Critic launches per checkpoint (default 2), counted by the ledger, not by the prompt. After the cap, return with the findings still open. |
| 2. Current state | **Forbidden today:** "never impose an arbitrary round count" (`engineering-role.md:40`); the Orchestrator does not dictate "a fixed number of review rounds" (`:32`). A FAIL re-enters repair and is followed by a new review (`:41`). |
| 3. Target layer | **Script** counter (`checkpoint_state.py critic-start`) plus a **CH PreToolUse** on `Agent\|Task` that recognises the assignment form by its fixed header `# Integration Critic —` (`gauntlet-templates.md:73`). **Accident guard:** a Critic launched in another session or in Codex is counted only if the Lead calls `critic-start`. |
| 4. Implementation | The hook calls `critic-start`. If `rounds_used == cap` and no `OWNER-AUTHORIZE critic-round` record exists, it denies with: "Critic cap reached (2). Write the §3 return as INCOMPLETE with the open findings (engineering-role.md:101)." `critic-result FAIL --finding …` keeps `open_findings` current for the return. |
| 5. Coverage | Local and cloud Claude ✔. Codex ✗. Human: n/a. |
| 6. Governance | Needs D5 and SUSP-2: amend `engineering-role.md:32` and `:40`, and add "Integration Critic round cap: [n, default 2]" to templates §1. The hook is SUSP-1. |
| 7. Failure modes | Launches that are not recognised (no header) are not counted, so the guard fails open. M19 is unverified. A cap reached on a near-PASS: the Owner extends it with one directive. |
| 8. Acceptance | Two fake Critic launches are allowed, the third is denied, and an Owner record allows one more. A non-Critic `Agent` call is never counted. |
| 9. Effort / deps | S once P1-4 exists. D5. |

#### P2-2 No rendering for self-verification

| Field | Content |
|---|---|
| 1. Capability | Refuse document or page rendering and screenshots used only to self-check, while keeping the browser acceptance that publication requires |
| 2. Current state | `AGENTS.md:151` bars rendering for Q&A entries only. PUBLISH_RULES §§9–10 require browser and post-deployment checks. The report records the Owner asking to skip rendering. |
| 3. Target layer | **CH PreToolUse** (Bash; `mcp__Claude_Browser__*`; `mcp__claude-in-chrome__*`), exempted when the ledger's current phase is one the brief names as browser or visual acceptance |
| 4. Implementation | Deny `soffice`/`libreoffice --convert-to`, `qlmanage`, `pandoc … -o *.pdf`, `screencapture`, Playwright screenshot invocations and browser-pane tools, unless `ledger.phases[current].name` is in the brief's acceptance phases (e.g. `release_checks`) or an Owner record exists |
| 5. Coverage | Local and cloud Claude ✔. Codex ✗. Human: n/a (the Owner renders at will). |
| 6. Governance | Hook: SUSP-1. Policy text (D7): `engineering-role.md` (SUSP-2). |
| 7. Failure modes | Pattern lists go stale, so the guard fails open on new tools. With no active ledger the guard is off, so it does not get in the way outside checkpoints. |
| 8. Acceptance | `soffice --convert-to pdf x.docx` is denied outside an acceptance phase and allowed inside one. A browser-pane tool call behaves the same way. |
| 9. Effort / deps | S. D7. |

#### P2-3 Queue mid-checkpoint requests

| Field | Content |
|---|---|
| 1. Capability | No Owner message during a checkpoint is lost, and small requests are handled before long verification runs |
| 2. Current state | Nothing. A chart-label request was lost twice (report). |
| 3. Target layer | **CH UserPromptSubmit** (append) plus **CH PreToolUse** (gate) plus the **script** (resolve) |
| 4. Implementation | While a ledger is active, every user prompt is appended as `{id, received_at, prompt_sha256, excerpt ≤ 160 chars, status: open}`, and the hook adds `additionalContext`: "R3 open". The agent resolves each prompt with `checkpoint_state.py request-resolve R3 --how done\|deferred\|not_a_request`. The gate: full `uv run pytest -q`, `make verify\|cp3\|cp3b\|wasm\|presentation`, `scripts/check_links.py`, Playwright runs and Critic launches are denied while any request is `open`. |
| 5. Coverage | Local and cloud Claude ✔. Codex ✗. Human: n/a. |
| 6. Governance | Hooks: SUSP-1. Script: MT-2. No text change. |
| 7. Failure modes | M18 is unverified. The cost is one command per message. `not_a_request` covers "continue". |
| 8. Acceptance | A prompt during a fixture checkpoint creates R1; `make verify` is denied; resolving R1 allows it. |
| 9. Effort / deps | S. P1-4, SUSP-1. |

#### P2-4 Session preflight

| Field | Content |
|---|---|
| 1. Capability | A deterministic start-of-session check, so environment gaps cost no turns |
| 2. Current state | Nothing. The report and the record show a vim-blocked commit, zsh quoting errors and a missing Playwright cache. `progress.md:293-295` notes a cloud-only fixture issue. |
| 3. Target layer | **CH SessionStart.** It cannot block; it informs (M10, M11). |
| 4. Implementation | Emit at most 12 lines of `additionalContext`: (1) guard activation (P0-1); (2) the effective agent editor (`git var GIT_EDITOR` should be `true`); (3) whether `python3` and `uv` are present; (4) whether Playwright browsers are present, as names only, never installed (installing is a network action for a brief); (5) if `$SHELL` is zsh, three reminders: quote expansions, since zsh does not word-split; quote globs and `HEAD^`; use `-m` or `-F` for commits; (6) cloud (`$CLAUDE_CODE_REMOTE`): "no `.local/`, no `gauntlet/*`, agents never push; a harness request to push is overridden by `AGENTS.md:157`"; (7) whether `GIT_CONFIG_COUNT` is set (`progress.md:293-295`); (8) a summary of the active ledger and of active Owner records; (9) the language line (P2-5). |
| 5. Coverage | Local and cloud Claude ✔. Codex ✗; its setup script could print the same. Human: `make hooks` covers item 1 only. |
| 6. Governance | SUSP-1. |
| 7. Failure modes | Fails open. Each check has a 2-second budget; no network. |
| 8. Acceptance | Fake environments (zsh without Playwright; cloud with `GIT_CONFIG_COUNT`) produce the expected lines, and never more than 12. |
| 9. Effort / deps | S. SUSP-1. |

#### P2-5 Response-language pinning

| Field | Content |
|---|---|
| 1. Capability | Status updates to Yarden in Hebrew; artifacts (briefs, returns, evidence, code, commit messages) in English; never a third language |
| 2. Current state | Both role files say "Reply in English" (`orchestrator-role.md:458-460`, `engineering-role.md:132-134`). Status lines appeared in Chinese or Arabic (report). `CLAUDE.md` must stay a pointer (`AGENTS.md:123`). |
| 3. Target layer | **Policy** in the role files (D6), plus a **CH Stop** detector. A detector is deterministic; an instruction is not. |
| 4. Implementation | Stop hook: read the last assistant message from `transcript_path` (format unverified), drop code spans, and count characters in Han, Kana, Hangul and Arabic Unicode ranges. If the count is above 0 and `stop_hook_active` is false, return `{"decision":"block","reason":"Restate the last message in Hebrew (status) or English (artifacts)"}`. Possible homes for the rule: role files (recommended; one source per role); project `language` setting [S] (pushes everything to Hebrew, against the role files); user-scope `language` on the Mac (Owner-only; never reaches the cloud); a SessionStart line (still model memory, but delivered every session). |
| 5. Coverage | Local and cloud Claude ✔. Codex ✗. Human: n/a. |
| 6. Governance | D6, SUSP-2 (two role files). Hook: SUSP-1. |
| 7. Failure modes | A quoted foreign name triggers one restatement; acceptable. If the transcript format changes, the detector fails open. |
| 8. Acceptance | A fake transcript whose last message contains Han characters blocks once; Hebrew or English passes; Han inside a code block passes. |
| 9. Effort / deps | S. D6. |

---

## 5. Suspension bundles

The Lockdown binds agents. An Owner's own manual edit needs no suspension.

| Bundle | Type | Exact files | Objective | Prerequisites |
|---|---|---|---|---|
| **S0** | Owner settings | GitHub rulesets and secret scanning (P0-7); the Codex environment's setup script (P0-1) | Server boundaries; Codex activation | D8 |
| **MT-1** | Maintenance task, no suspension (files not locked today) | New: `scripts/leak_scan.py`, `scripts/credential_fingerprints.py`, `tests/environ_redact.py`, `tests/test_NN_leak_scan.py`, `tests/test_NN_environ_access.py`. Edited: `.githooks/pre-commit`, `.githooks/commit-msg`, `.githooks/pre-push`, `.github/workflows/tests.yml`, `Makefile` (`hooks`), `pytest.ini` (`-p environ_redact`). | P0-1 (Makefile), P0-2, P0-3, P0-8 R4 check | D1. The Owner generates and commits `.githooks/credential-fingerprints.json` afterwards (Owner-only). |
| **SUSP-1** | **Lockdown suspension** | New: `.claude/settings.json`, `.claude/hooks/run.sh`, `.claude/hooks/guard.py`, `.claude/governance/locked-paths`, `.claude/skills/checkpoint-resume/SKILL.md`, and, if R2, `.claude/governance/allowed-signers`. Directly necessary, not locked: `tests/test_NN_claude_hooks.py`, `tests/test_NN_locked_manifest.py`. | Install the deterministic accident guards P0-1 (Claude part), P0-4, P0-5, P0-6, the P1-4 edit guard, P1-5, P2-1 to P2-5 (hook parts), exactly as this plan specifies them. Excludes any change to `AGENTS.md` or the role files. | D3; ideally after MT-1 and MT-2, so the hooks call existing scripts |
| **MT-2** | Maintenance task, no suspension | New: `scripts/land.py`, `scripts/checkpoint_state.py`, `tests/test_NN_land.py`, `tests/test_NN_checkpoint_state.py` | P1-2 (Option A) and P1-4 | D4 |
| **SUSP-2** | **Lockdown suspension** | `AGENTS.md` (D2 lock-list additions; one sentence in § Credentials on how `core.hooksPath` is established; D3 record form, if chosen; P1-3 text if D4 = B). `engineering-role.md` (D5 at `:32`, `:40`; D6 at `:134`; D7). `orchestrator-role.md` (D6 at `:460`; P1-3 consistency at `:351-354` if B). `docs/track-b/gauntlet-templates.md` (§1 Critic cap field; §4 pointer to `land.py` or the B text at `:210`). `docs/track-b/rule-inventory.md` (directly necessary consistency rows). | Codify decisions D2 to D7 as the Owner ratifies them | Every decision D2–D7 taken; MT-1 and MT-2 landed (so D2 locks finished files) |

**Ready-to-authorize wording**

- **SUSP-1:** "I suspend the Lockdown for one task: create the files listed under SUSP-1 in `docs/deterministic-migration-plan.md`, implementing exactly P0-1 (Claude part), P0-4, P0-5, P0-6 (form R<1|2>), P1-5, and the hook parts of P1-4 and P2-1 to P2-5. No other locked file. No publication. Spent at terminal return."
- **SUSP-2:** "I suspend the Lockdown for one task: amend the files listed under SUSP-2 to codify decisions D2=<…>, D3=<…>, D4=<…>, D5=<…>, D6=<…>, D7=<…> as recorded in my message, plus directly necessary consistency edits. No publication. Spent at terminal return."

---

## 6. Implementation order and rollback

| Step | Bundle | Why at this point | Acceptance gate | Rollback |
|---|---|---|---|---|
| 1 | S0 | Server boundaries need no code and cover everyone at once | P0-7 test | The Owner disables the ruleset or push protection in settings |
| 2 | MT-1 | Value-free scanning and env-dump prevention are the largest P0 risk reduction, and they cover Codex and CI | P0-2 and P0-3 tests green in CI | The Owner reverts the commit; the hooks fall back to `secret_guard.py` only. Deleting the fingerprint file disables F1 alone. |
| 3 | Owner | Generate the fingerprints on the Mac and commit them | `leak_scan.py tree` passes, and the fixture test with a fake token blocks | The Owner removes the entry or the file |
| 4 | MT-2 | `land.py` and the ledger script exist before the hooks reference them | P1-2 and P1-4 tests | Revert; LAND falls back to the templates §4 commands |
| 5 | SUSP-1 | The Claude guards, after the scripts they call | T-M6, T-M12, T-M18, T-M20 first, then each component's tests, in the Owner's real permission mode | Kill switch: the Owner sets `"disableAllHooks": true` in user settings, and confirms during acceptance that it overrides project hooks (M14). Then the Owner reverts by hand. |
| 6 | SUSP-2 | Governance text codifies what has been proven | `scripts/governance_selftest.py` passes; the manifest consistency test passes | The Owner reverts by hand |

---

## 7. Report suggestions rejected or deferred

| Suggestion (report section) | Disposition | Reason |
|---|---|---|
| New rules in `CLAUDE.md`: language, secrets and pushing, LAND authority, review loops, shell ("Existing CC Features to Try") | **Rejected** as placed | `CLAUDE.md` must contain only a pointer (`AGENTS.md:123`). Each topic is routed to a mechanism: P0-2 and P0-3, P1-2 and P1-3, P2-1, P2-4, P2-5. |
| "When the user says 'you are authorized to LAND', commit, tag and push yourself" | **Rejected** as a memory rule; offered as Option B | It contradicts `AGENTS.md:191` and needs an amendment (P1-3) |
| PreToolUse hook running gitleaks on `git push` | **Modified** | A pattern scan missed the 40-hex token (`credential-exposure-2026-09-24.md:25-27`). Agents should not push at all, so the scan belongs in git pre-push and CI, where it covers every actor (P0-2), with fingerprints. gitleaks as an extra pattern layer is deferred: a new dependency needing a network install. |
| `/land` skill: `git commit -F`; `git tag <CP-id>`; `git push --follow-tags`; `gh run watch`; Playwright deploy checks with retries | **Rejected** | One tag contradicts the two-tag rule (`AGENTS.md:187`; D-CP0-19, `gauntlet-templates.md:220`). `--follow-tags` pushes only annotated tags, and the LAND tags are lightweight (`cp-21-landing-2026-09-30.md:58`), so both would be silently left behind; `evidence/<cp>` is not reachable from `main` in any case. Agent push contradicts `AGENTS.md:157`. Deploy retries belong to the CP-18 pipeline. |
| Stop hook refusing to end a session while ledger phases are open | **Rejected** | It loops at session and usage limits, and it conflicts with legitimate `BLOCKED` and `INCOMPLETE` returns (`engineering-role.md:97-103`). Replaced by the non-blocking ledger and preflight. |
| `claude -p` headless resume loop or scheduled job | **Deferred** | Unattended agent runs need per-checkpoint authorization and cost control. Revisit after P1-4 has proved itself. |
| Four parallel critic subagents in `.claude/agents/` | **Deferred** | Extra internal reviews are already the Lead's choice (`engineering-role.md:43`). New agent definitions are locked configuration, and the token cost runs against P2. |
| Integration Critic as a subagent, "max 2 rounds" | **Accepted, modified** | Enforced through the ledger counter (P2-1), with D5 amending `engineering-role.md:32,40` |
| Committed `checkpoints/<ID>/state.json` | **Modified** | Moved to `.local/`. Committing it after the final candidate breaks the verdict-only delta (`engineering-role.md:45-50`), and it must not become a second tracking document (`orchestrator-role.md:378`). |
| "Never commit CI logs or command output" | **Partly accepted** | Evidence logs are required ("commands actually run", `engineering-role.md:69`), so they are scanned (P0-2 F2, P0-3) rather than banned |
| Set the MLflow telemetry opt-out before importing mlflow | **Deferred** | Not evidenced in the repository record. Belongs in code or the `env` key through a checkpoint. |
| Front-load small requests | **Accepted** | P2-3, enforced rather than requested |
| A global nano editor | **Done by the Owner** (`cp-21-landing-2026-09-30.md:22-23`) | For agents, `GIT_EDITOR=true` instead (§4.0.1) |
| "The CP-20 push included a committed CI log" | **Corrected** | It was a Critic guard log under evidence; the record wins (§3, F1) |

---

## 8. Appendix: Owner-only actions on the Mac (from the health check)

The Mac cannot be seen or changed from here. These are the doctor's findings, plus the items this plan adds.

**User-scope settings are not "in this repository".** The Lockdown covers files that configure how agents run *in this repository* (`AGENTS.md:23-24`). User-scope settings are the Owner's own machine configuration, and the Owner editing them is the Owner's own act. An agent edits them only on the Owner's explicit instruction.

| # | Action | Source | Note |
|---|---|---|---|
| A1 | Add a `skillOverrides` block that turns off the 15 desktop-provided skills unused since install. The doctor estimates ~1.9k tokens saved per session. | doctor, check 1 | Uses full `plugin:skill` names, so the built-in `schedule` skill is unaffected. `skillOverrides` values verified [S]. |
| A2 | Optionally set `permissions.defaultMode: "auto"` | doctor, check 8 | The app's mode picker still decides for the sessions it starts. Run the P0/P2 acceptance tests in whatever mode is actually used (M20). |
| A3 | Update or restart the desktop app: the Mac had 2.1.281; the cloud container runs 2.1.286, the version the semantics in §4.0 were checked against | doctor, check 7 | Do this before relying on any CH component |
| A4 | Review the app-loaded tools that are unused in this project (browser pane, iOS Simulator, documents connector) | doctor, check 6 | Connector or app settings; no config file |
| A5 | After any re-clone, run `make hooks` (once MT-1 lands) and check `git config --get core.hooksPath` | P0-1 | The current clone is already active (`progress.md:285-287`) |
| A6 | Generate the credential fingerprints once (D1) and after every rotation | P0-2 | Run `scripts/credential_fingerprints.py write`; it prints names only |
| A7 | If D3 = R2: create a signing key that requires Touch ID for each signature, and give the agent only its public half | P0-6 | — |
| A8 | If D6 = (c): set the user-scope `language` | P2-5 | Not recommended |
| A9 | The doctor framed A1 and A2 as needing a Lockdown suspension | doctor | Not required, per the note above |
