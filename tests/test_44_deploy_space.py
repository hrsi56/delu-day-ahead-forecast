"""The Owner's Space upload refuses anything but the reviewed bundle (docs/deploy.md; PUBLISH_RULES 1.0 §11).

Only the offline checks run here -- the bundle hash the review bound and the credential-value guard over every
outbound file. No network, no token and no upload: the guard is confined to this test's environment
(`SECRET_GUARD_ENV_ONLY`), and its fake credential is generated here, never a real value.
"""

from __future__ import annotations

import secrets
import sys

import pytest

from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_wasm_space as W  # noqa: E402
import deploy_space  # noqa: E402


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    monkeypatch.setenv("SECRET_GUARD_ENV_ONLY", "1")
    folder = tmp_path / "space-wasm"
    (folder / "public").mkdir(parents=True)
    (folder / "index.html").write_text("<!doctype html><title>demo</title>")
    (folder / "public" / "claims.json").write_text("{}\n")
    return folder


def test_the_reviewed_bundle_passes_the_offline_checks(bundle):
    record = deploy_space.check_bundle(bundle, W.bundle_sha256(bundle))
    assert record["credential_guard"] == "passed" and record["files"] == 2


def test_negative_control_a_changed_bundle_is_refused(bundle):
    expected = W.bundle_sha256(bundle)
    (bundle / "index.html").write_text("<!doctype html><title>changed</title>")
    with pytest.raises(SystemExit, match="is not the reviewed"):
        deploy_space.check_bundle(bundle, expected)


def test_negative_control_a_credential_value_in_the_bundle_is_blocked_without_printing_it(bundle, monkeypatch, capsys):
    value = "fixture-" + secrets.token_hex(16)
    monkeypatch.setenv("DEPLOY_FIXTURE_TOKEN", value)
    (bundle / "public" / "claims.json").write_text('{"leak": "%s"}\n' % value)
    with pytest.raises(SystemExit) as raised:
        deploy_space.check_bundle(bundle, W.bundle_sha256(bundle))
    message = str(raised.value)
    assert "DEPLOY_FIXTURE_TOKEN" in message and value not in message
    assert value not in capsys.readouterr().out


def test_negative_control_a_folder_without_the_page_is_refused(tmp_path):
    with pytest.raises(SystemExit, match="no index.html"):
        deploy_space.check_bundle(tmp_path, "0" * 64)
