"""Brief W2: the record-level export diff separates byte identity from content preservation.

A registry change may alter only names, descriptions and tags. Parameters, metric history points and
datasets must be byte-identical, and so must every artifact digest, except that `summary.json` and
`README.md` carry the run's name (and `summary.json` its tags), so their bytes change with the name
by construction. For those two, the diff proves content preservation at the digest: putting the old
name and tags back reproduces the old SHA-256 exactly. The committed W2 record is the proof for the
registry's introduction; the negative controls show that any other change fails.
"""

from __future__ import annotations

import copy
import json
import sys

import pytest

from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import mlflow_export as E  # noqa: E402

RECORD = REPO_ROOT / "reports" / "presentation" / "release-checks" / "2026-09-28-registry-export-diff.json"


@pytest.fixture(scope="module")
def committed() -> dict[str, dict]:
    return {name: json.loads((E.EXPORT_DIR / f"{name}.json").read_text())
            for name in ("manifest", *E.G.parent_run_keys())}


def _run(files: dict[str, dict], key: str) -> dict:
    return next(run for name, content in files.items() if name != "manifest"
                for run in content["runs"] if run["run_key"] == key)


def _set_artifact(run: dict, path: str, content: str) -> None:
    art = next(art for art in run["artifacts"] if art["path"] == path)
    art.update(content=content, sha256=E.sha256_text(content), bytes=len(content.encode("utf-8")))


def _rename(files: dict[str, dict], key: str, name: str) -> dict[str, dict]:
    """A copy of the export in which one run is renamed, as a registry change would rename it."""
    new = copy.deepcopy(files)
    run = _run(new, key)
    run["run_name"] = name
    run["tags"]["delu.public_name"] = name
    summary = json.loads(next(a["content"] for a in run["artifacts"] if a["path"] == "summary.json"))
    summary.update(run_name=name, tags=run["tags"])
    _set_artifact(run, "summary.json", E._canonical(summary) + "\n")
    readme = next(a["content"] for a in run["artifacts"] if a["path"] == "README.md")
    _set_artifact(run, "README.md", f"# {name}\n" + readme.split("\n", 1)[1])
    return new


def test_a_rename_is_identity_only_and_restoring_it_reproduces_the_old_digests(committed):
    report = E.diff_exports(committed, _rename(committed, "cp20/HG", "renamed"))
    assert report["only_identity"], report["substantive_changes"]
    assert report["identity_changes"]["cp20/HG"]["artifacts_identity_only"] == ["README.md", "summary.json"]
    checked = report["checked"]
    assert checked["artifacts_old_digest_on_restoring_identity"] == 2
    assert checked["artifacts_digest_unchanged"] == checked["artifacts"] - 2


def test_negative_control_a_changed_number_inside_summary_json_fails(committed):
    new = _rename(committed, "cp20/HG", "renamed")
    run = _run(new, "cp20/HG")
    summary = json.loads(next(a["content"] for a in run["artifacts"] if a["path"] == "summary.json"))
    metric = sorted(summary["metrics"])[0]
    summary["metrics"][metric][0]["value"] += 1e-9
    _set_artifact(run, "summary.json", E._canonical(summary) + "\n")
    report = E.diff_exports(committed, new)
    assert not report["only_identity"] and "cp20/HG: artifact summary.json" in report["substantive_changes"]


def test_negative_control_a_changed_readme_body_fails(committed):
    new = _rename(committed, "cp20/HG", "renamed")
    run = _run(new, "cp20/HG")
    readme = next(a["content"] for a in run["artifacts"] if a["path"] == "README.md")
    _set_artifact(run, "README.md", readme.replace("Development evidence", "Confirmatory evidence"))
    report = E.diff_exports(committed, new)
    assert "cp20/HG: artifact README.md" in report["substantive_changes"]


def test_negative_control_a_changed_metric_point_parameter_or_chart_fails(committed):
    new = copy.deepcopy(committed)
    run = _run(new, "cp20/HG")
    metric = sorted(run["metrics"])[0]
    run["metrics"][metric][0]["value"] += 1e-9
    run["params"][sorted(run["params"])[0]] = "changed"
    chart = next(art for art in run["artifacts"] if art["path"].endswith(".svg"))
    _set_artifact(run, chart["path"], chart["content"].replace("</svg>", "<g/></svg>"))
    problems = E.diff_exports(committed, new)["substantive_changes"]
    assert {"cp20/HG: metrics", "cp20/HG: params", f"cp20/HG: artifact {chart['path']}"} <= set(problems)


def test_the_committed_w2_record_proves_the_registry_introduction():
    record = json.loads(RECORD.read_text())
    assert record["only_identity"] and record["substantive_changes"] == []
    assert record["against"] == "af0abb0" and record["to"] == "0f93205"
    checked = record["checked"]
    assert checked["artifacts"] == checked["artifacts_digest_unchanged"] + checked["artifacts_old_digest_on_restoring_identity"]
