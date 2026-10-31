# Server-side protections for `hrsi56/delu-day-ahead-forecast` (CP-18a item 7, P0-7)

These files are the exact configuration of three GitHub repository rulesets and the secret-scanning setting, in
the format of GitHub's REST API (`POST /repos/{owner}/{repo}/rulesets`, `PATCH /repos/{owner}/{repo}`). They give
boundaries that no local process can bypass: `main` cannot be force-pushed or deleted, the preserved tags cannot
be moved or deleted, `gauntlet/*` branches cannot be created on `origin`, and known token formats are refused at
push time.

**Applying them is the Owner's action.** No agent runs the commands below: they change GitHub state
(AGENTS.md § *Git and publication authority*). They are written here, not run.

| File | Ruleset | Target and refs | Rules | Bypass actors |
|---|---|---|---|---|
| `main.json` | main | branch `refs/heads/main` | `non_fast_forward` (block force pushes), `deletion` (restrict deletions) | none |
| `preserved-tags.json` | preserved tags | tag `refs/tags/land/*`, `refs/tags/evidence/*`, `refs/tags/archive/*` | `update` (restrict updates), `deletion` (restrict deletions) | none |
| `never-pushed.json` | never pushed | branch `refs/heads/gauntlet/*` | `creation` (restrict creations) | none |
| `security-and-analysis.json` | (repository setting) | the repository | secret scanning on, push protection on | n/a |

## Why each rule, and what it leaves alone

- **main.** Force pushes and deletion of `main` are history rewriting, which AGENTS.md reserves to the Owner and
  forbids to the daily pipeline outright. There is deliberately **no pull-request requirement, no status-check
  requirement and no `update` restriction**: the Owner lands by hand and pushes directly, and the daily pipeline
  commits its data-only records and fast-forwards `main` with the workflow token. An ordinary fast-forward push
  passes every rule here, from any actor.
- **preserved tags.** `land/<cp>`, `evidence/<cp>` and `archive/<cp>-attempt-<k>` keep every SHA that a verdict,
  a checkpoint return or the defect register cites reachable (AGENTS.md § *Branch and ref lifecycle*: tag before
  delete). Creating a new tag at LAND is not restricted; moving or deleting one is.
- **never pushed.** `gauntlet/<checkpoint>` branches are local and disposable and are never pushed. Creation is
  restricted, so a mistaken push is refused. The rule does not touch a branch that already exists on `origin`; the
  first check below confirms there is none.
- **No bypass actors** in any ruleset: not the Owner, not an app, not the Actions token. Changing one of these
  boundaries takes a deliberate ruleset edit, which is the point. The Claude GitHub App keeps its existing access;
  it is not added as a bypass actor.
- **Secret scanning with push protection** refuses pushes that hold known token formats. It does not recognise the
  DagsHub token (a bare 40-character hex string); `scripts/leak_scan.py` (fingerprints, in the hooks and as the
  first CI step) and `scripts/secret_guard.py` (values) cover that. A push-protection false positive on a daily
  push fails closed, and the day is published as failed.

## Before applying

Run from the Owner's checkout, with `gh` signed in as the repository owner. Nothing here opens a pager or editor.

```sh
export GH_PAGER=cat GIT_PAGER=cat
REPO=hrsi56/delu-day-ahead-forecast

# 1. No gauntlet/* branch is on origin (expected: no output).
git ls-remote --heads origin 'refs/heads/gauntlet/*'

# 2. The existing rulesets (expected: none with these names; otherwise update that one with PUT, below).
gh api "repos/$REPO/rulesets" --jq '.[] | {id, name, target, enforcement}'

# 3. Confirm under Settings > Rules > Rulesets that branch and tag rulesets are offered for this repository.
```

## Apply (written, not run)

```sh
export GH_PAGER=cat
REPO=hrsi56/delu-day-ahead-forecast
gh api --method POST "repos/$REPO/rulesets" --input reports/cp18a/rulesets/main.json
gh api --method POST "repos/$REPO/rulesets" --input reports/cp18a/rulesets/preserved-tags.json
gh api --method POST "repos/$REPO/rulesets" --input reports/cp18a/rulesets/never-pushed.json
gh api --method PATCH "repos/$REPO" --input reports/cp18a/rulesets/security-and-analysis.json
```

`POST` creates a new ruleset each time it runs. To change one that already exists, use its id from the listing:
`gh api --method PUT "repos/$REPO/rulesets/<id>" --input <file>`. To suspend one, PUT the same file with
`"enforcement": "disabled"`; `gh api --method DELETE "repos/$REPO/rulesets/<id>"` removes it.

## Check the configuration

```sh
gh api "repos/$REPO/rulesets" --jq '.[] | {id, name, target, enforcement}'
# expected: main (branch), preserved tags (tag), never pushed (branch), each "active"
gh api "repos/$REPO/rules/branches/main" --jq '[.[].type] | sort'
# expected: ["deletion", "non_fast_forward"]
gh api "repos/$REPO/rulesets/<id>" --jq '{name, target, conditions, rules: [.rules[].type], bypass_actors}'
# for each id: the refs, rule types and empty bypass list of the matching JSON file here
gh api "repos/$REPO" --jq '.security_and_analysis | {secret_scanning, secret_scanning_push_protection}'
# expected: both {"status": "enabled"}
```

## Acceptance (the Owner, by hand)

These are P0-7's acceptance steps. Run them from the Owner's own checkout, where the pre-push hooks are active,
while the daily pipeline is not pushing. Every probe points at a commit that is already public, so nothing new
is published.

```sh
export GIT_PAGER=cat
git fetch --quiet origin
MAIN_TIP="$(git rev-parse origin/main)"

# 1. Preserved tags. Creating the probe tag is allowed; deleting or moving it must be rejected.
git push origin "$MAIN_TIP:refs/tags/archive/ruleset-probe-attempt-0"            # expected: accepted
git push origin ":refs/tags/archive/ruleset-probe-attempt-0"                     # expected: REJECTED (deletion)
git push --force origin "$MAIN_TIP~1:refs/tags/archive/ruleset-probe-attempt-0"  # expected: REJECTED (update)

# 2. Never pushed: creating a gauntlet/* branch must be rejected.
git push origin "$MAIN_TIP:refs/heads/gauntlet/ruleset-probe"                    # expected: REJECTED (creation)

# 3. Main: a force push of a fake commit must be rejected. The fake commit has main's exact tree on main's parent,
#    so it differs from main only in history. It is built with commit-tree: no local branch or file changes.
PROBE="$(git commit-tree "$MAIN_TIP^{tree}" -p "$MAIN_TIP~1" -m "ruleset probe: must be rejected")"
git push --force-with-lease="main:$MAIN_TIP" origin "$PROBE:refs/heads/main"     # expected: REJECTED (non_fast_forward)
git fetch --quiet origin && test "$(git rev-parse origin/main)" = "$MAIN_TIP" && echo "main unchanged"
```

- Step 1 leaves `archive/ruleset-probe-attempt-0` on `origin`, pointing at a public `main` commit. It can be
  removed only by suspending the "preserved tags" ruleset first, which is the Owner's call; leaving it is
  harmless.
- If step 3 is ever **accepted**, the rule is not active. Restore `main` at once with
  `git push --force-with-lease="main:$PROBE" origin "$MAIN_TIP:refs/heads/main"`, then fix the ruleset before
  anything else pushes.
- A probe counts only when GitHub answers it. A rejection from a local hook (`secret-guard`, `leak-scan` or
  `publication-guard` in the output) never reached the server, so that probe is inconclusive; never bypass the
  hook to run it.
- A rejected probe prints GitHub's rule violation (for example `GH013: Repository rule violations found`). Record
  each probe's outcome and the configuration check above in the CP-18 record; the Orchestrator records the
  configuration in `progress.md`.
