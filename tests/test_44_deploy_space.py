"""The Owner's Space deployment refuses anything but the reviewed bundle and leaves the Space serving exactly it
(docs/deploy.md; PUBLISH_RULES 1.0 §11).

Everything here is offline: the bundle hash the review bound, the credential-value guard over every outbound file,
the plan (additions, changes, deletions), the declared-deletion refusal, the one commit and the path-and-hash
verification after it. The Hub is a fake that records every call, so a test can prove that check mode writes nothing
and that an upload makes exactly one commit with exactly the expected operations. No network, no token and no
upload: the guard is confined to this test's environment (`SECRET_GUARD_ENV_ONLY`), and every fake credential is
generated here, never a real value.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import sys

import pytest

from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_wasm_space as W  # noqa: E402
import deploy_space  # noqa: E402

#: Three entries in the shape the Hub's tree API returns: a folder, a plain file and a file stored through LFS (whose
#: `oid` is the pointer's blob, and whose content hash is `lfs.oid`).
TREE_FIXTURE = """[
  {"type": "directory", "oid": "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "size": 0, "path": "assets"},
  {"type": "file", "oid": "26ef81ba7b8d78a489e4d72915e6869e2452a6c8", "size": 34, "path": "index.html"},
  {"type": "file", "oid": "d294d839a12426821a4d8db5a256d4c58f0b7869", "size": 23,
   "lfs": {"oid": "a3d99acb90ededfc934c520f7b75e0dfe0b08a054d679556444a30f85d3d9b78", "size": 23, "pointerSize": 127},
   "xetHash": "c8c5e4deaa5659a8f1e52197da34286bf2cfea2905b9d028da8ccf34ea159f9b", "path": "assets/font.woff2"}
]"""


def _blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _plain(data: bytes) -> dict:
    return {"sha1": _blob_sha1(data), "sha256": None}


def _served(folder) -> dict:
    """The tree a Space serving exactly `folder` reports, every file plain."""
    return {path: _plain((folder / path).read_bytes()) for path in deploy_space.bundle_files(folder)}


class FakeHub:
    """Stands in for the Hub: serves trees by revision and records every call. A commit applies its operations to
    the parent's tree unless `after` overrides the tree it leaves behind."""

    def __init__(self, served: dict, after: dict | None = None, fail: Exception | None = None):
        self.calls: list[tuple] = []
        self.trees = {"r0": served}
        self.after, self.fail = after, fail

    def identity(self) -> dict:
        self.calls.append(("identity",))
        return {"sdk": "static", "private": False, "revision": "r0", "stage": "RUNNING"}

    def tree(self, revision: str) -> dict:
        self.calls.append(("tree", revision))
        return {path: dict(entry) for path, entry in self.trees[revision].items()}

    def commit(self, bundle, adds, deletes, parent, message) -> dict:
        self.calls.append(("commit", list(adds), list(deletes), parent))
        if self.fail is not None:
            raise self.fail
        tree = {path: entry for path, entry in self.trees[parent].items() if path not in deletes}
        tree.update({path: _plain((bundle / path).read_bytes()) for path in adds})
        self.trees["r1"] = self.after if self.after is not None else tree
        return {"commit": "r1", "commit_url": "https://huggingface.co/spaces/fake/commit/r1"}

    @property
    def writes(self) -> list[tuple]:
        return [call for call in self.calls if call[0] == "commit"]


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    monkeypatch.setenv("SECRET_GUARD_ENV_ONLY", "1")
    folder = tmp_path / "space-wasm"
    (folder / "public").mkdir(parents=True)
    (folder / "index.html").write_text("<!doctype html><title>demo</title>")
    (folder / "public" / "claims.json").write_text("{}\n")
    return folder


@pytest.fixture
def no_token(monkeypatch):
    """Reading HF_TOKEN fails the test: only the real Hub's commit may read it."""
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.setattr(deploy_space, "_token", lambda: pytest.fail("a token was read"))


def _upload(bundle, hub, capsys, *declare, record=None) -> tuple[int, dict]:
    argv = ["--bundle", str(bundle), "--expect", W.bundle_sha256(bundle), "--upload", *declare]
    if record is not None:
        argv += ["--record", str(record)]
    code = deploy_space.main(argv, hub=hub)
    return code, json.loads(capsys.readouterr().out)


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


def test_the_tree_parser_reads_a_plain_and_an_lfs_entry_from_fixture_json(tmp_path):
    remote = deploy_space.parse_tree(json.loads(TREE_FIXTURE))
    assert remote == {
        "index.html": {"sha1": "26ef81ba7b8d78a489e4d72915e6869e2452a6c8", "sha256": None},
        "assets/font.woff2": {"sha1": None,
                              "sha256": "a3d99acb90ededfc934c520f7b75e0dfe0b08a054d679556444a30f85d3d9b78"},
    }
    (tmp_path / "assets").mkdir()
    (tmp_path / "index.html").write_bytes(b"<!doctype html><title>demo</title>")
    (tmp_path / "assets" / "font.woff2").write_bytes(b"wOF2 fixture font bytes")
    assert deploy_space.verify(deploy_space.local_files(tmp_path), remote)["verified"]
    (tmp_path / "assets" / "font.woff2").write_bytes(b"wOF2 fixture font bytes, changed")
    assert deploy_space.verify(deploy_space.local_files(tmp_path), remote)["mismatched"] == ["assets/font.woff2"]


def test_negative_control_an_unreadable_tree_entry_fails_the_listing():
    with pytest.raises(ValueError):
        deploy_space.parse_tree([{"type": "file", "oid": "0" * 40}])
    with pytest.raises(ValueError):
        deploy_space.parse_tree([{"type": "symlink", "path": "x"}])
    lfs_without_hash = deploy_space.parse_tree([{"type": "file", "oid": "0" * 40, "path": "a.png", "lfs": {}}])
    assert not deploy_space.same({"sha1": "0" * 40, "sha256": "0" * 64}, lfs_without_hash["a.png"])


def test_the_tree_is_read_anonymously_and_across_pages(monkeypatch):
    entries = json.loads(TREE_FIXTURE)
    base = f"{deploy_space.API}/tree/r0?recursive=true"
    pages = {base: (entries[:2], '<https://huggingface.co/api/spaces/x/tree/r0?recursive=true&cursor=abc>; rel="next"'),
             "https://huggingface.co/api/spaces/x/tree/r0?recursive=true&cursor=abc": (entries[2:], None)}
    requested = []

    class Response:
        def __init__(self, body, link):
            self.body, self.headers = json.dumps(body).encode(), {"Link": link} if link else {}

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return self.body

    def urlopen(request, timeout=None):
        assert isinstance(request, str), "an anonymous read sends a bare URL: no header, no token"
        requested.append(request)
        return Response(*pages[request])

    monkeypatch.setattr(deploy_space.urllib.request, "urlopen", urlopen)
    remote = deploy_space.Hub().tree("r0")
    assert requested == list(pages) and set(remote) == {"index.html", "assets/font.woff2"}


def test_check_mode_writes_nothing_reads_no_token_and_lists_the_deletion_set(bundle, no_token):
    served = _served(bundle) | {"style.css": _plain(b"body {}\n")}
    hub = FakeHub(served)
    record, code = deploy_space.deploy(bundle, W.bundle_sha256(bundle), hub)
    assert code == 0 and hub.writes == [] and [c[0] for c in hub.calls] == ["identity", "tree"]
    assert record["planned_deletes"] == ["style.css"] and not record["served_equals_bundle"]
    assert record["planned_adds"] == [] and record["planned_changes"] == []
    assert record["mode"].startswith("check only")


def test_check_mode_reports_whether_the_declared_deletion_set_matches(bundle, no_token):
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n")})
    record, code = deploy_space.deploy(bundle, W.bundle_sha256(bundle), hub, declared=["style.css"])
    assert code == 0 and record["declared_matches"]
    record, code = deploy_space.deploy(bundle, W.bundle_sha256(bundle), hub, declared=[])
    assert code == 1 and record["declared_matches"] is False and hub.writes == []


def test_negative_control_an_extra_remote_file_is_deleted_in_the_same_single_commit(bundle, capsys, tmp_path):
    served = _served(bundle) | {"style.css": _plain(b"body {}\n")}
    del served["public/claims.json"]
    hub = FakeHub(served)
    code, record = _upload(bundle, hub, capsys, "--delete", "style.css", record=tmp_path / "record.json")
    assert code == 0 and record["status"] == "deployed" and record["verified"]
    assert hub.writes == [("commit", ["public/claims.json"], ["style.css"], "r0")]
    assert record["before_revision"] == "r0" and record["after_revision"] == "r1" and record["commit"] == "r1"
    assert json.loads((tmp_path / "record.json").read_text()) == record


def test_negative_control_delete_none_is_refused_before_any_write_when_a_remote_file_is_extra(bundle, capsys):
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n")})
    with pytest.raises(SystemExit, match=r"deletion set is \['style.css'\], not the declared \[\]"):
        _upload(bundle, hub, capsys, "--delete-none")
    assert hub.writes == []


def test_negative_control_a_missing_remote_file_is_planned_as_an_addition(bundle):
    served = _served(bundle)
    del served["public/claims.json"]
    record, _ = deploy_space.deploy(bundle, W.bundle_sha256(bundle), FakeHub(served))
    assert record["planned_adds"] == ["public/claims.json"] and record["planned_deletes"] == []


def test_negative_control_a_changed_remote_file_is_planned_as_a_change(bundle):
    served = _served(bundle)
    served["index.html"] = _plain(b"<!doctype html><title>old</title>")
    served["public/claims.json"] = {"sha1": None, "sha256": hashlib.sha256(b"{\"old\": 1}\n").hexdigest()}  # LFS
    record, _ = deploy_space.deploy(bundle, W.bundle_sha256(bundle), FakeHub(served))
    assert record["planned_changes"] == ["index.html", "public/claims.json"] and record["planned_adds"] == []


def test_negative_control_declaring_too_few_deletions_is_refused_before_any_write(bundle, capsys):
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n"), "old.js": _plain(b"0;\n")})
    with pytest.raises(SystemExit, match=r"\['old.js', 'style.css'\], not the declared \['style.css'\]"):
        _upload(bundle, hub, capsys, "--delete", "style.css")
    assert hub.writes == []


def test_negative_control_declaring_too_many_deletions_is_refused_before_any_write(bundle, capsys):
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n")})
    with pytest.raises(SystemExit, match=r"\['style.css'\], not the declared \['old.js', 'style.css'\]"):
        _upload(bundle, hub, capsys, "--delete", "style.css", "--delete", "old.js")
    assert hub.writes == []


def test_a_deletion_only_commit_carries_only_the_delete(bundle, capsys):
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n")})
    code, record = _upload(bundle, hub, capsys, "--delete", "style.css")
    assert code == 0 and record["verified"] and hub.writes == [("commit", [], ["style.css"], "r0")]


def test_an_identical_space_gets_no_commit_and_is_still_verified(bundle, capsys):
    hub = FakeHub(_served(bundle))
    code, record = _upload(bundle, hub, capsys, "--delete-none")
    assert code == 0 and record["status"] == "already identical" and record["commit"] is None
    assert hub.writes == [] and hub.calls[-1] == ("tree", "r0") and record["verified"]


def test_negative_control_an_extra_file_after_the_commit_fails_verification(bundle, capsys, tmp_path):
    after = _served(bundle) | {"style.css": _plain(b"body {}\n")}
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n")}, after=after)
    code, record = _upload(bundle, hub, capsys, "--delete", "style.css", record=tmp_path / "record.json")
    assert code == 1 and record["verified"] is False and record["extra"] == ["style.css"]
    assert record["status"] == "committed, not verified" and len(hub.writes) == 1
    assert json.loads((tmp_path / "record.json").read_text())["extra"] == ["style.css"]


def test_negative_control_a_wrong_hash_after_the_commit_fails_verification(bundle, capsys):
    after = _served(bundle) | {"index.html": _plain(b"<!doctype html><title>stale</title>")}
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n")}, after=after)
    code, record = _upload(bundle, hub, capsys, "--delete", "style.css")
    assert code == 1 and record["verified"] is False and record["mismatched"] == ["index.html"]
    assert record["missing"] == [] and record["extra"] == []


def test_negative_control_a_failed_commit_records_only_the_type_and_the_status(bundle, capsys):
    class HubError(Exception):
        def __init__(self, text):
            super().__init__(text)
            self.response = type("Response", (), {"status_code": 412})()

    fake_value = "fixture-" + secrets.token_hex(16)
    hub = FakeHub(_served(bundle) | {"style.css": _plain(b"body {}\n")},
                  fail=HubError(f"412 at https://huggingface.co/api/x?token={fake_value}"))
    code, record = _upload(bundle, hub, capsys, "--delete", "style.css")
    assert code == 1 and record["status"] == "failed" and record["failed_step"] == "commit"
    assert record["error_type"] == "HubError" and record["http_status"] == 412 and record["commit"] is None
    assert fake_value not in json.dumps(record) and not record["verified"]


def test_negative_control_an_upload_without_a_declared_deletion_set_is_refused(bundle, capsys):
    hub = FakeHub(_served(bundle))
    with pytest.raises(SystemExit) as raised:
        deploy_space.main(["--bundle", str(bundle), "--expect", W.bundle_sha256(bundle), "--upload"], hub=hub)
    assert raised.value.code == 2 and hub.calls == []
    with pytest.raises(SystemExit, match="declared deletion set"):
        deploy_space.deploy(bundle, W.bundle_sha256(bundle), hub, upload=True)
    assert hub.calls == []
