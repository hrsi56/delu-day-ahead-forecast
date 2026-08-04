from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = REPO_ROOT / "scripts" / "gauntlet_protocol.py"
SNAPSHOT_PATH = REPO_ROOT / "scripts" / "gauntlet_critic_snapshot.sh"
SCHEMA_PATH = REPO_ROOT / "docs" / "track-b" / "schemas" / "critic-verdict.schema.json"
PLAN_EXCERPT = "Exact acceptance bar for the test checkpoint."

SPEC = importlib.util.spec_from_file_location("gauntlet_protocol", PROTOCOL_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import machinery invariant.
    raise RuntimeError("Cannot load gauntlet_protocol.py")
PROTOCOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROTOCOL)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_json(value))


def run_command(
    arguments: list[str], *, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=str(cwd) if cwd is not None else None,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def parse_key_values(output: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


class GitRepoCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / "repo"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str, check: bool = True) -> str:
        result = run_command(["git", "-C", str(self.repo), *arguments])
        if check and result.returncode != 0:
            self.fail(
                f"git {' '.join(arguments)} failed\nstdout={result.stdout}\nstderr={result.stderr}"
            )
        return result.stdout.strip()

    def initialize_repo(
        self, *, ignored_evidence: bool = True, checkpoint_branch: bool = True
    ) -> tuple[str, str]:
        self.repo.mkdir()
        result = run_command(["git", "init", "-q", str(self.repo)])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.git("symbolic-ref", "HEAD", "refs/heads/main")
        self.git("config", "user.name", "Gauntlet Test")
        self.git("config", "user.email", "gauntlet@example.invalid")

        scripts = self.repo / "scripts"
        schema_dir = self.repo / "docs" / "track-b" / "schemas"
        scripts.mkdir(parents=True)
        schema_dir.mkdir(parents=True)
        shutil.copyfile(SNAPSHOT_PATH, scripts / SNAPSHOT_PATH.name)
        shutil.copyfile(PROTOCOL_PATH, scripts / PROTOCOL_PATH.name)
        shutil.copyfile(SCHEMA_PATH, schema_dir / SCHEMA_PATH.name)
        (self.repo / ".gitignore").write_text(
            "/.gauntlet/\n" if ignored_evidence else "",
            encoding="utf-8",
        )
        (self.repo / "candidate.txt").write_text("candidate\n", encoding="utf-8")
        (self.repo / "capstone_V6_4.md").write_text(
            f"# Test capstone\n\n{PLAN_EXCERPT}\n",
            encoding="utf-8",
        )
        (self.repo / "plans").mkdir()
        (self.repo / "plans" / "nested-capstone.md").write_text(
            f"# Nested test capstone\n\n{PLAN_EXCERPT}\n",
            encoding="utf-8",
        )
        self.git(
            "add",
            ".gitignore",
            "candidate.txt",
            "capstone_V6_4.md",
            "plans/nested-capstone.md",
            "scripts",
            "docs",
        )
        self.git("commit", "-q", "-m", "candidate")
        if checkpoint_branch:
            self.git("checkout", "-q", "-b", "gauntlet/CP-1")
        commit_sha = self.git("rev-parse", "HEAD")
        tree_sha = self.git("rev-parse", "HEAD^{tree}")
        return commit_sha, tree_sha

    def candidate_blob(self, candidate_sha: str, relative_path: str) -> bytes:
        result = subprocess.run(
            ["git", "-C", str(self.repo), "show", f"{candidate_sha}:{relative_path}"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        return result.stdout


class SnapshotShellTests(GitRepoCase):
    def setUp(self) -> None:
        super().setUp()
        self.candidate_sha, self.tree_sha = self.initialize_repo()

    def create_snapshot(self, run_id: str) -> tuple[Path, Path, dict[str, str]]:
        evidence_root, _ = PROTOCOL.initialize_evidence_root(
            str(self.repo), "CP-1", run_id
        )
        snapshot = self.base / f"snapshot-{run_id}"
        manifest = evidence_root / "integrity-manifest.json"
        result = run_command(
            [
                "bash",
                str(SNAPSHOT_PATH),
                "create",
                self.candidate_sha,
                str(snapshot),
                str(manifest),
                run_id,
            ],
            cwd=self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return snapshot, manifest, parse_key_values(result.stdout)

    def verify_from_detached_snapshot(
        self, snapshot: Path, manifest: Path, pre_hash: str
    ) -> subprocess.CompletedProcess[str]:
        detached_helper = snapshot / "scripts" / "gauntlet_critic_snapshot.sh"
        return run_command(
            [
                "bash",
                str(detached_helper),
                "verify",
                self.candidate_sha,
                str(snapshot),
                str(manifest),
                pre_hash,
            ],
            cwd=snapshot,
        )

    def test_create_and_verify_from_detached_snapshot(self) -> None:
        snapshot, manifest, created = self.create_snapshot("critic-001")
        self.assertEqual(created["candidate_sha"], self.candidate_sha)
        self.assertEqual(created["tree_sha"], self.tree_sha)
        self.assertEqual(created["critic_run_id"], "critic-001")
        self.assertEqual(created["pre_review_manifest_sha256"], digest_file(manifest))

        create_record = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(create_record["checkpoint"], "CP-1")
        self.assertEqual(create_record["evidence_run_path"], str(manifest.parent))
        self.assertEqual(
            create_record["create"]["tools"]["snapshot_helper"]["repo_relative_path"],
            "scripts/gauntlet_critic_snapshot.sh",
        )
        self.assertEqual(create_record["create"]["checks"]["status"]["raw_output"], "")

        verified = self.verify_from_detached_snapshot(
            snapshot, manifest, created["pre_review_manifest_sha256"]
        )
        self.assertEqual(verified.returncode, 0, verified.stderr)
        verification = parse_key_values(verified.stdout)
        self.assertEqual(
            verification["final_integrity_manifest_sha256"], digest_file(manifest)
        )
        final_record = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertIsNotNone(final_record["verify"])
        self.assertEqual(final_record["create"]["tools"], final_record["verify"]["tools"])
        self.assertFalse((manifest.parent / ".integrity-manifest.verify.lock").exists())
        self.assertEqual(self.git("-C", str(snapshot), "status", "--porcelain=v1"), "")

    def test_dirty_snapshot_rejects_verify_without_mutating_manifest(self) -> None:
        snapshot, manifest, created = self.create_snapshot("critic-dirty")
        before = manifest.read_bytes()
        (snapshot / "rogue.txt").write_text("dirty\n", encoding="utf-8")
        verified = self.verify_from_detached_snapshot(
            snapshot, manifest, created["pre_review_manifest_sha256"]
        )
        self.assertNotEqual(verified.returncode, 0)
        self.assertIn("not clean", verified.stderr)
        self.assertEqual(manifest.read_bytes(), before)

    def test_private_manifest_create_cannot_bypass_snapshot_checks(self) -> None:
        run_id = "critic-direct-create"
        evidence_root, _ = PROTOCOL.initialize_evidence_root(
            str(self.repo), "CP-1", run_id
        )
        snapshot = self.base / "snapshot-direct-create"
        added = run_command(
            [
                "git",
                "-C",
                str(self.repo),
                "worktree",
                "add",
                "--detach",
                str(snapshot),
                self.candidate_sha,
            ]
        )
        self.assertEqual(added.returncode, 0, added.stderr)
        (snapshot / "rogue.txt").write_text("dirty\n", encoding="utf-8")
        manifest = evidence_root / "integrity-manifest.json"
        helper = self.repo / "scripts" / "gauntlet_critic_snapshot.sh"
        protocol = self.repo / "scripts" / "gauntlet_protocol.py"
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "not clean"):
            PROTOCOL.create_integrity_manifest(
                str(manifest),
                run_id,
                self.candidate_sha,
                self.tree_sha,
                str(snapshot),
                str(helper),
                digest_file(helper),
                str(protocol),
                digest_file(protocol),
            )
        self.assertFalse(manifest.exists())

    def test_private_manifest_verify_cannot_bypass_snapshot_checks(self) -> None:
        snapshot, manifest, created = self.create_snapshot("critic-direct-verify")
        before = manifest.read_bytes()
        (snapshot / "rogue.txt").write_text("dirty\n", encoding="utf-8")
        helper = snapshot / "scripts" / "gauntlet_critic_snapshot.sh"
        protocol = snapshot / "scripts" / "gauntlet_protocol.py"
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "not clean"):
            PROTOCOL.verify_integrity_manifest(
                str(manifest),
                created["pre_review_manifest_sha256"],
                self.candidate_sha,
                self.tree_sha,
                str(snapshot),
                str(helper),
                digest_file(helper),
                str(protocol),
                digest_file(protocol),
            )
        self.assertEqual(manifest.read_bytes(), before)

    def test_manifest_tamper_rejects_verify(self) -> None:
        snapshot, manifest, created = self.create_snapshot("critic-tamper")
        manifest.write_bytes(manifest.read_bytes() + b" \n")
        tampered = manifest.read_bytes()
        verified = self.verify_from_detached_snapshot(
            snapshot, manifest, created["pre_review_manifest_sha256"]
        )
        self.assertNotEqual(verified.returncode, 0)
        self.assertIn("SHA-256 mismatch", verified.stderr)
        self.assertEqual(manifest.read_bytes(), tampered)

    def test_existing_verify_lock_fails_closed(self) -> None:
        snapshot, manifest, created = self.create_snapshot("critic-lock")
        before = manifest.read_bytes()
        lock = manifest.parent / ".integrity-manifest.verify.lock"
        lock.write_text("held\n", encoding="utf-8")
        verified = self.verify_from_detached_snapshot(
            snapshot, manifest, created["pre_review_manifest_sha256"]
        )
        self.assertNotEqual(verified.returncode, 0)
        self.assertIn("already locked", verified.stderr)
        self.assertEqual(manifest.read_bytes(), before)

    def test_two_process_verify_allows_exactly_one_success(self) -> None:
        snapshot, manifest, created = self.create_snapshot("critic-concurrent")
        detached_helper = snapshot / "scripts" / "gauntlet_critic_snapshot.sh"
        command = [
            "bash",
            str(detached_helper),
            "verify",
            self.candidate_sha,
            str(snapshot),
            str(manifest),
            created["pre_review_manifest_sha256"],
        ]
        processes = [
            subprocess.Popen(
                command,
                cwd=str(snapshot),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for _ in range(2)
        ]
        results = [process.communicate(timeout=20) for process in processes]
        return_codes = sorted(process.returncode for process in processes)
        self.assertEqual(return_codes, [0, 1], results)
        final_record = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertIsNotNone(final_record["verify"])
        self.assertFalse((manifest.parent / ".integrity-manifest.verify.lock").exists())

    def test_create_rejects_candidate_with_different_committed_tool(self) -> None:
        candidate_tool = self.repo / "scripts" / "gauntlet_protocol.py"
        candidate_tool.write_bytes(candidate_tool.read_bytes() + b"\n# candidate drift\n")
        self.git("add", "scripts/gauntlet_protocol.py")
        self.git("commit", "-q", "-m", "drift tool")
        self.candidate_sha = self.git("rev-parse", "HEAD")
        evidence_root, _ = PROTOCOL.initialize_evidence_root(
            str(self.repo), "CP-1", "critic-tool-drift"
        )
        result = run_command(
            [
                "bash",
                str(SNAPSHOT_PATH),
                "create",
                self.candidate_sha,
                str(self.base / "snapshot-tool-drift"),
                str(evidence_root / "integrity-manifest.json"),
                "critic-tool-drift",
            ],
            cwd=self.repo,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match committed candidate copy", result.stderr)
        self.assertFalse((evidence_root / "integrity-manifest.json").exists())


class EvidenceRootAndRefTests(GitRepoCase):
    def test_init_is_ignored_unique_and_not_symlinked(self) -> None:
        self.initialize_repo()
        root, support = PROTOCOL.initialize_evidence_root(
            str(self.repo), "CP-1", "run-001"
        )
        self.assertEqual(
            root, self.repo / ".gauntlet" / "evidence" / "CP-1" / "run-001"
        )
        self.assertEqual(
            support,
            self.repo
            / ".gauntlet"
            / "evidence"
            / "CP-1"
            / "_support"
            / "run-001",
        )
        self.assertEqual(root.stat().st_mode & 0o777, 0o700)
        self.assertEqual(support.stat().st_mode & 0o777, 0o700)
        with self.assertRaises(PROTOCOL.ProtocolError):
            PROTOCOL.initialize_evidence_root(str(self.repo), "CP-1", "run-001")

    def test_init_cli_prints_both_owned_paths(self) -> None:
        self.initialize_repo()
        result = run_command(
            [
                "python3",
                str(PROTOCOL_PATH),
                "init-evidence",
                "--repo-root",
                str(self.repo),
                "--checkpoint",
                "CP-1",
                "--run-id",
                "run-cli",
            ]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        values = parse_key_values(result.stdout)
        self.assertEqual(
            values["evidence_root"],
            str(self.repo / ".gauntlet" / "evidence" / "CP-1" / "run-cli"),
        )
        self.assertEqual(
            values["support_root"],
            str(
                self.repo
                / ".gauntlet"
                / "evidence"
                / "CP-1"
                / "_support"
                / "run-cli"
            ),
        )

    def test_init_rejects_unignored_root(self) -> None:
        self.initialize_repo(ignored_evidence=False)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "not ignored"):
            PROTOCOL.initialize_evidence_root(str(self.repo), "CP-1", "run-001")

    def test_init_rejects_symlink_escape(self) -> None:
        self.initialize_repo()
        outside = self.base / "outside"
        outside.mkdir()
        os.symlink(outside, self.repo / ".gauntlet")
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "symlink"):
            PROTOCOL.initialize_evidence_root(str(self.repo), "CP-1", "run-001")

    def test_init_rejects_symlinked_support_ancestor(self) -> None:
        self.initialize_repo()
        checkpoint_root = self.repo / ".gauntlet" / "evidence" / "CP-1"
        checkpoint_root.mkdir(parents=True)
        outside = self.base / "outside-support"
        outside.mkdir()
        os.symlink(outside, checkpoint_root / "_support")
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "symlink"):
            PROTOCOL.initialize_evidence_root(str(self.repo), "CP-1", "run-001")

    def test_init_preflight_leaves_no_half_pair_on_reuse(self) -> None:
        self.initialize_repo()
        checkpoint_root = self.repo / ".gauntlet" / "evidence" / "CP-1"
        preexisting_support = checkpoint_root / "_support" / "run-half"
        preexisting_support.mkdir(parents=True)
        evidence_run = checkpoint_root / "run-half"
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "reuse"):
            PROTOCOL.initialize_evidence_root(str(self.repo), "CP-1", "run-half")
        self.assertFalse(evidence_run.exists())
        self.assertTrue(preexisting_support.is_dir())

        preexisting_run = checkpoint_root / "run-half-2"
        preexisting_run.mkdir()
        support_run = checkpoint_root / "_support" / "run-half-2"
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "reuse"):
            PROTOCOL.initialize_evidence_root(str(self.repo), "CP-1", "run-half-2")
        self.assertTrue(preexisting_run.is_dir())
        self.assertFalse(support_run.exists())

    def test_ref_requires_checkpoint_branch_and_current_head(self) -> None:
        commit_sha, _ = self.initialize_repo(checkpoint_branch=False)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "current branch"):
            PROTOCOL.create_evidence_ref(
                str(self.repo), "CP-1", "run-main", "piece", commit_sha
            )
        self.git("checkout", "-q", "-b", "gauntlet/CP-1")
        ref, _, _ = PROTOCOL.create_evidence_ref(
            str(self.repo), "CP-1", "run-good", "piece", commit_sha
        )
        self.assertEqual(ref, "refs/gauntlet-evidence/CP-1/run-good/piece")
        with self.assertRaises(PROTOCOL.ProtocolError):
            PROTOCOL.create_evidence_ref(
                str(self.repo), "CP-1", "run-good", "piece", commit_sha
            )
        (self.repo / "candidate.txt").write_text("new candidate\n", encoding="utf-8")
        self.git("add", "candidate.txt")
        self.git("commit", "-q", "-m", "new head")
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "current checkpoint HEAD"):
            PROTOCOL.create_evidence_ref(
                str(self.repo), "CP-1", "run-old", "piece", commit_sha
            )

    def test_ref_verify_is_read_only_on_other_branch(self) -> None:
        commit_sha, _ = self.initialize_repo()
        ref, _, _ = PROTOCOL.create_evidence_ref(
            str(self.repo), "CP-1", "run-verify", "piece", commit_sha
        )
        self.git("checkout", "-q", "main")
        verified_ref, verified_sha, _ = PROTOCOL.verify_evidence_ref(
            str(self.repo), "CP-1", "run-verify", "piece", commit_sha
        )
        self.assertEqual((verified_ref, verified_sha), (ref, commit_sha))

    def test_ref_rejects_git_unsafe_identifier(self) -> None:
        commit_sha, _ = self.initialize_repo()
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "Git-safe"):
            PROTOCOL.create_evidence_ref(
                str(self.repo), "CP-1", "run-unsafe", "bad..piece", commit_sha
            )


class VerdictValidationTests(GitRepoCase):
    CREATE_TIME = "2026-01-01T00:00:00Z"
    VERIFY_TIME = "2026-01-01T00:00:01Z"
    VERDICT_TIME = "2026-01-01T00:00:02Z"

    def setUp(self) -> None:
        super().setUp()
        self.candidate_sha, self.tree_sha = self.initialize_repo()

    def make_manifest(
        self, run_root: Path, run_id: str, candidate_sha: str, tree_sha: str
    ) -> tuple[Path, str]:
        tools = {
            "snapshot_helper": {
                "repo_relative_path": "scripts/gauntlet_critic_snapshot.sh",
                "sha256": digest_bytes(
                    self.candidate_blob(candidate_sha, "scripts/gauntlet_critic_snapshot.sh")
                ),
            },
            "protocol_helper": {
                "repo_relative_path": "scripts/gauntlet_protocol.py",
                "sha256": digest_bytes(
                    self.candidate_blob(candidate_sha, "scripts/gauntlet_protocol.py")
                ),
            },
        }
        checks = {
            "head_sha": candidate_sha,
            "tree_sha": tree_sha,
            "detached_head": True,
            "workbench_absent": True,
            "tracked_diff": {
                "command": "git diff --quiet --exit-code",
                "exit_code": 0,
            },
            "index_diff": {
                "command": "git diff --cached --quiet --exit-code",
                "exit_code": 0,
            },
            "status": {
                "command": "git status --porcelain=v1 --untracked-files=all --ignored=matching",
                "raw_output": "",
                "raw_output_sha256": digest_bytes(b""),
            },
        }
        manifest = {
            "record_type": "gauntlet_snapshot_integrity_manifest",
            "schema_version": "1.0",
            "run_id": run_id,
            "checkpoint": "CP-1",
            "candidate_sha": candidate_sha,
            "candidate_tree": tree_sha,
            "snapshot_path": str(self.base / "deleted-snapshots" / run_id),
            "evidence_run_path": str(run_root),
            "create": {
                "recorded_at_utc": self.CREATE_TIME,
                "tools": tools,
                "checks": checks,
            },
            "verify": None,
        }
        pre_hash = digest_bytes(canonical_json(manifest))
        manifest["verify"] = {
            "recorded_at_utc": self.VERIFY_TIME,
            "pre_review_manifest_sha256": pre_hash,
            "tools": copy.deepcopy(tools),
            "checks": copy.deepcopy(checks),
        }
        path = run_root / "integrity-manifest.json"
        write_json(path, manifest)
        return path, digest_file(path)

    def make_run(
        self,
        run_id: str,
        piece: str,
        *,
        record_type: str = "component_critic_verdict",
        verdict: str = "PASS",
        candidate_sha: str | None = None,
        tree_sha: str | None = None,
        plan_filename: str = "capstone_V6_4.md",
        plan_version: str = "6.4",
        recorded_at: str | None = None,
        components: list[dict[str, str]] | None = None,
    ) -> tuple[Path, dict[str, object]]:
        candidate_sha = candidate_sha or self.candidate_sha
        tree_sha = tree_sha or self.git("rev-parse", f"{candidate_sha}^{{tree}}")
        evidence_ref, _, _ = PROTOCOL.create_evidence_ref(
            str(self.repo), "CP-1", run_id, piece, candidate_sha
        )
        run_root, support = PROTOCOL.initialize_evidence_root(
            str(self.repo), "CP-1", run_id
        )
        files = {
            "artifact": b"artifact\n",
            "input": b"input\n",
            "stdout": b"command output\n",
            "stderr": b"",
            "evidence": b"recomputed evidence\n",
        }
        paths: dict[str, Path] = {}
        for name, payload in files.items():
            path = support / f"{name}.log"
            path.write_bytes(payload)
            paths[name] = path
        manifest_path, manifest_hash = self.make_manifest(
            run_root, run_id, candidate_sha, tree_sha
        )
        schema_hash = digest_bytes(
            self.candidate_blob(
                candidate_sha, "docs/track-b/schemas/critic-verdict.schema.json"
            )
        )
        plan_hash = digest_bytes(self.candidate_blob(candidate_sha, plan_filename))
        record: dict[str, object] = {
            "record_type": record_type,
            "schema_version": "1.0",
            "run_id": run_id,
            "checkpoint": "CP-1",
            "piece": piece,
            "critic_id": f"critic-{run_id}",
            "verdict": verdict,
            "candidate": {
                "commit_sha": candidate_sha,
                "tree_sha": tree_sha,
                "evidence_ref": evidence_ref,
            },
            "verdict_schema": {
                "repo_relative_path": "docs/track-b/schemas/critic-verdict.schema.json",
                "sha256": schema_hash,
            },
            "artifact": {
                "status": "HASHED",
                "name": "artifact",
                "path": str(paths["artifact"]),
                "sha256": digest_file(paths["artifact"]),
            },
            "plan": {
                "filename": plan_filename,
                "version": plan_version,
                "sha256": plan_hash,
                "bar_citation": f"§12 {piece}",
                "bar_excerpt": PLAN_EXCERPT,
            },
            "inputs": {
                "status": "HASHED",
                "items": [
                    {
                        "name": "fixture",
                        "path": str(paths["input"]),
                        "sha256": digest_file(paths["input"]),
                    }
                ],
            },
            "commands": [
                {
                    "command": "python -m unittest acceptance",
                    "exit_code": 0,
                    "stdout_path": str(paths["stdout"]),
                    "stdout_sha256": digest_file(paths["stdout"]),
                    "stderr_path": str(paths["stderr"]),
                    "stderr_sha256": digest_file(paths["stderr"]),
                }
            ],
            "expected_output": "acceptance oracle passes",
            "tolerance": "exact",
            "integrity_manifest": {
                "path": str(manifest_path),
                "sha256": manifest_hash,
            },
            "evidence": [
                {
                    "description": "independent recomputation",
                    "path": str(paths["evidence"]),
                    "sha256": digest_file(paths["evidence"]),
                }
            ],
            "largest_meaningful_gap": "none after independent acceptance",
            "next_acceptance_test": "rerun the exact oracle on candidate change",
            "recorded_at_utc": recorded_at or self.VERDICT_TIME,
        }
        if record_type == "integration_critic_verdict":
            record["component_verdicts"] = components or []
        verdict_path = run_root / "critic-verdict.json"
        write_json(verdict_path, record)
        return verdict_path, record

    def rewrite(self, path: Path, record: dict[str, object]) -> None:
        write_json(path, record)

    def component_binding(
        self, path: Path, record: dict[str, object], *, piece: str | None = None
    ) -> dict[str, str]:
        candidate = record["candidate"]
        assert isinstance(candidate, dict)
        return {
            "piece": piece or str(record["piece"]),
            "path": str(path),
            "sha256": digest_file(path),
            "candidate_sha": str(candidate["commit_sha"]),
            "candidate_tree": str(candidate["tree_sha"]),
        }

    def test_component_verdict_and_cli_validate(self) -> None:
        path, original = self.make_run("component-good", "temporal")
        support_root = (
            self.repo
            / ".gauntlet"
            / "evidence"
            / "CP-1"
            / "_support"
            / "component-good"
        )
        artifact = original["artifact"]
        inputs = original["inputs"]
        commands = original["commands"]
        evidence = original["evidence"]
        assert isinstance(artifact, dict)
        assert isinstance(inputs, dict) and isinstance(inputs["items"], list)
        assert isinstance(commands, list) and isinstance(commands[0], dict)
        assert isinstance(evidence, list) and isinstance(evidence[0], dict)
        owned_paths = [
            Path(str(artifact["path"])),
            Path(str(inputs["items"][0]["path"])),
            Path(str(commands[0]["stdout_path"])),
            Path(str(commands[0]["stderr_path"])),
            Path(str(evidence[0]["path"])),
        ]
        self.assertTrue(all(path.is_relative_to(support_root) for path in owned_paths))
        record, validated_hash = PROTOCOL.validate_verdict_file(path)
        self.assertEqual(record["verdict"], "PASS")
        self.assertEqual(validated_hash, digest_file(path))
        result = run_command(
            ["python3", str(PROTOCOL_PATH), "validate-verdict", "--verdict", str(path)]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"verdict_sha256={digest_file(path)}", result.stdout)

    def test_historical_validation_does_not_require_snapshot_or_live_tool_path(self) -> None:
        path, _ = self.make_run("component-historical", "lineage")
        record, _ = PROTOCOL.validate_verdict_file(path)
        manifest_path = Path(str(record["integrity_manifest"]["path"]))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertFalse(Path(manifest["snapshot_path"]).exists())
        self.assertNotIn("path", manifest["create"]["tools"]["protocol_helper"])

    def test_extra_run_file_rejected(self) -> None:
        path, _ = self.make_run("component-extra", "schema")
        (path.parent / "extra.log").write_text("extra\n", encoding="utf-8")
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "exactly"):
            PROTOCOL.validate_verdict_file(path)

    def test_unhashed_observation_rejected(self) -> None:
        path, record = self.make_run("component-observation", "schema")
        record["evidence"] = [{"description": "claim", "observation": "self report"}]
        self.rewrite(path, record)
        with self.assertRaises(PROTOCOL.ProtocolError):
            PROTOCOL.validate_verdict_file(path)

    def test_tampered_command_output_rejected(self) -> None:
        path, record = self.make_run("component-output", "schema")
        commands = record["commands"]
        assert isinstance(commands, list) and isinstance(commands[0], dict)
        Path(str(commands[0]["stdout_path"])).write_text("tampered\n", encoding="utf-8")
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "stdout_sha256 mismatch"):
            PROTOCOL.validate_verdict_file(path)

    def test_supporting_evidence_outside_checkpoint_rejected(self) -> None:
        path, record = self.make_run("component-outside", "schema")
        outside = self.base / "outside.log"
        outside.write_text("outside\n", encoding="utf-8")
        commands = record["commands"]
        assert isinstance(commands, list) and isinstance(commands[0], dict)
        commands[0]["stdout_path"] = str(outside)
        commands[0]["stdout_sha256"] = digest_file(outside)
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "support root"):
            PROTOCOL.validate_verdict_file(path)

    def test_external_artifact_and_input_rejected(self) -> None:
        outside_artifact = self.base / "external-artifact.bin"
        outside_artifact.write_bytes(b"external artifact")
        path, record = self.make_run("component-external-artifact", "schema")
        artifact = record["artifact"]
        assert isinstance(artifact, dict)
        artifact["path"] = str(outside_artifact)
        artifact["sha256"] = digest_file(outside_artifact)
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "support root"):
            PROTOCOL.validate_verdict_file(path)

        outside_input = self.base / "external-input.bin"
        outside_input.write_bytes(b"external input")
        path2, record2 = self.make_run("component-external-input", "schema")
        inputs = record2["inputs"]
        assert isinstance(inputs, dict) and isinstance(inputs["items"], list)
        item = inputs["items"][0]
        assert isinstance(item, dict)
        item["path"] = str(outside_input)
        item["sha256"] = digest_file(outside_input)
        self.rewrite(path2, record2)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "support root"):
            PROTOCOL.validate_verdict_file(path2)

    def test_sibling_run_support_file_rejected(self) -> None:
        path, record = self.make_run("component-owner-a", "schema")
        _, sibling = self.make_run("component-owner-b", "lineage")
        sibling_artifact = sibling["artifact"]
        artifact = record["artifact"]
        assert isinstance(sibling_artifact, dict) and isinstance(artifact, dict)
        artifact["path"] = sibling_artifact["path"]
        artifact["sha256"] = sibling_artifact["sha256"]
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "this Critic run's support root"):
            PROTOCOL.validate_verdict_file(path)

    def test_symlinked_support_file_rejected(self) -> None:
        path, record = self.make_run("component-symlink-file", "schema")
        artifact = record["artifact"]
        assert isinstance(artifact, dict)
        original = Path(str(artifact["path"]))
        link = original.parent / "artifact-link.log"
        os.symlink(original, link)
        artifact["path"] = str(link)
        artifact["sha256"] = digest_file(original)
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "symlink"):
            PROTOCOL.validate_verdict_file(path)

    def test_cross_run_hard_links_rejected_for_all_file_backed_roles(self) -> None:
        owner_path, owner = self.make_run("component-hardlink-owner", "schema")
        _, donor = self.make_run("component-hardlink-donor", "lineage")
        owner_artifact = owner["artifact"]
        owner_inputs = owner["inputs"]
        owner_commands = owner["commands"]
        owner_evidence = owner["evidence"]
        donor_artifact = donor["artifact"]
        donor_inputs = donor["inputs"]
        donor_commands = donor["commands"]
        donor_evidence = donor["evidence"]
        assert isinstance(owner_artifact, dict) and isinstance(donor_artifact, dict)
        assert isinstance(owner_inputs, dict) and isinstance(owner_inputs["items"], list)
        assert isinstance(donor_inputs, dict) and isinstance(donor_inputs["items"], list)
        assert isinstance(owner_commands, list) and isinstance(owner_commands[0], dict)
        assert isinstance(donor_commands, list) and isinstance(donor_commands[0], dict)
        assert isinstance(owner_evidence, list) and isinstance(owner_evidence[0], dict)
        assert isinstance(donor_evidence, list) and isinstance(donor_evidence[0], dict)

        owner_support = Path(str(owner_artifact["path"])).parent
        donor_roles = {
            "artifact": (
                str(donor_artifact["path"]),
                str(donor_artifact["sha256"]),
            ),
            "input": (
                str(donor_inputs["items"][0]["path"]),
                str(donor_inputs["items"][0]["sha256"]),
            ),
            "command": (
                str(donor_commands[0]["stdout_path"]),
                str(donor_commands[0]["stdout_sha256"]),
            ),
            "evidence": (
                str(donor_evidence[0]["path"]),
                str(donor_evidence[0]["sha256"]),
            ),
        }
        links: dict[str, tuple[Path, str]] = {}
        for role, (donor_path, donor_hash) in donor_roles.items():
            link = owner_support / f"hardlink-{role}.bin"
            os.link(donor_path, link)
            links[role] = (link, donor_hash)

        for role in ("artifact", "input", "command", "evidence"):
            with self.subTest(role=role):
                mutated = copy.deepcopy(owner)
                link, linked_hash = links[role]
                if role == "artifact":
                    target = mutated["artifact"]
                    assert isinstance(target, dict)
                    target["path"] = str(link)
                    target["sha256"] = linked_hash
                elif role == "input":
                    target = mutated["inputs"]
                    assert isinstance(target, dict) and isinstance(target["items"], list)
                    target["items"][0]["path"] = str(link)
                    target["items"][0]["sha256"] = linked_hash
                elif role == "command":
                    target = mutated["commands"]
                    assert isinstance(target, list) and isinstance(target[0], dict)
                    target[0]["stdout_path"] = str(link)
                    target[0]["stdout_sha256"] = linked_hash
                else:
                    target = mutated["evidence"]
                    assert isinstance(target, list) and isinstance(target[0], dict)
                    target[0]["path"] = str(link)
                    target[0]["sha256"] = linked_hash
                self.rewrite(owner_path, mutated)
                with self.assertRaisesRegex(PROTOCOL.ProtocolError, "hard-linked"):
                    PROTOCOL.validate_verdict_file(owner_path)

    def test_hard_linked_verdict_and_manifest_json_rejected(self) -> None:
        path, record = self.make_run("component-json-hardlink", "schema")
        verdict_alias = self.base / "verdict-alias.json"
        os.link(path, verdict_alias)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "hard-linked JSON"):
            PROTOCOL.validate_verdict_file(path)
        verdict_alias.unlink()

        manifest = record["integrity_manifest"]
        assert isinstance(manifest, dict)
        manifest_path = Path(str(manifest["path"]))
        manifest_alias = self.base / "manifest-alias.json"
        os.link(manifest_path, manifest_alias)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "hard-linked JSON"):
            PROTOCOL.validate_verdict_file(path)

    def test_plan_blob_hash_excerpt_and_safe_path_are_enforced(self) -> None:
        nested_path, _ = self.make_run(
            "component-nested-plan",
            "schema",
            plan_filename="plans/nested-capstone.md",
        )
        PROTOCOL.validate_verdict_file(nested_path)

        bad_hash_path, bad_hash = self.make_run("component-plan-hash", "schema")
        plan = bad_hash["plan"]
        assert isinstance(plan, dict)
        plan["sha256"] = "0" * 64
        self.rewrite(bad_hash_path, bad_hash)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "plan SHA-256 mismatch"):
            PROTOCOL.validate_verdict_file(bad_hash_path)

        excerpt_path, excerpt_record = self.make_run(
            "component-plan-excerpt", "schema"
        )
        excerpt_plan = excerpt_record["plan"]
        assert isinstance(excerpt_plan, dict)
        excerpt_plan["bar_excerpt"] = "text absent from committed plan"
        self.rewrite(excerpt_path, excerpt_record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "occur verbatim"):
            PROTOCOL.validate_verdict_file(excerpt_path)

        unsafe_path, unsafe_record = self.make_run("component-plan-path", "schema")
        unsafe_plan = unsafe_record["plan"]
        assert isinstance(unsafe_plan, dict)
        unsafe_plan["filename"] = "../capstone_V6_4.md"
        self.rewrite(unsafe_path, unsafe_record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "safe repo-relative"):
            PROTOCOL.validate_verdict_file(unsafe_path)

    def test_candidate_tree_mismatch_rejected(self) -> None:
        path, record = self.make_run("component-tree", "schema")
        candidate = record["candidate"]
        assert isinstance(candidate, dict)
        candidate["tree_sha"] = "f" * 40
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "does not match"):
            PROTOCOL.validate_verdict_file(path)

    def test_missing_or_wrong_evidence_ref_rejected(self) -> None:
        path, record = self.make_run("component-ref", "schema")
        candidate = record["candidate"]
        assert isinstance(candidate, dict)
        candidate["evidence_ref"] = "refs/gauntlet-evidence/CP-1/wrong/schema"
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "must be exactly"):
            PROTOCOL.validate_verdict_file(path)

    def test_committed_schema_hash_rejected(self) -> None:
        path, record = self.make_run("component-schema-hash", "schema")
        schema = record["verdict_schema"]
        assert isinstance(schema, dict)
        schema["sha256"] = "0" * 64
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "schema SHA-256 mismatch"):
            PROTOCOL.validate_verdict_file(path)

    def test_manifest_hash_and_backdated_verdict_rejected(self) -> None:
        path, record = self.make_run("component-manifest-hash", "schema")
        binding = record["integrity_manifest"]
        assert isinstance(binding, dict)
        binding["sha256"] = "0" * 64
        self.rewrite(path, record)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "manifest SHA-256 mismatch"):
            PROTOCOL.validate_verdict_file(path)

        path2, record2 = self.make_run(
            "component-backdated", "schema", recorded_at=self.CREATE_TIME
        )
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "precedes"):
            PROTOCOL.validate_verdict_file(path2)

    def test_integration_accepts_current_exact_candidate_components(self) -> None:
        component_path, component = self.make_run("component-current", "temporal")
        binding = self.component_binding(component_path, component)
        integration_path, _ = self.make_run(
            "integration-current",
            "integration",
            record_type="integration_critic_verdict",
            components=[binding],
        )
        record, _ = PROTOCOL.validate_verdict_file(integration_path)
        self.assertEqual(record["record_type"], "integration_critic_verdict")

    def test_integration_rejects_stale_candidate(self) -> None:
        component_path, component = self.make_run("component-stale", "temporal")
        (self.repo / "candidate.txt").write_text("repaired candidate\n", encoding="utf-8")
        self.git("add", "candidate.txt")
        self.git("commit", "-q", "-m", "repair candidate")
        final_sha = self.git("rev-parse", "HEAD")
        final_tree = self.git("rev-parse", "HEAD^{tree}")
        binding = self.component_binding(component_path, component)
        binding["candidate_sha"] = final_sha
        binding["candidate_tree"] = final_tree
        integration_path, _ = self.make_run(
            "integration-stale",
            "integration",
            record_type="integration_critic_verdict",
            candidate_sha=final_sha,
            tree_sha=final_tree,
            components=[binding],
        )
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "stale candidate"):
            PROTOCOL.validate_verdict_file(integration_path)

    def test_integration_rejects_plan_and_piece_relabel(self) -> None:
        component_path, component = self.make_run("component-plan", "temporal")
        binding = self.component_binding(component_path, component)
        integration_path, _ = self.make_run(
            "integration-plan",
            "integration",
            record_type="integration_critic_verdict",
            plan_version="6.5",
            components=[binding],
        )
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "different plan"):
            PROTOCOL.validate_verdict_file(integration_path)

        component_path2, component2 = self.make_run("component-piece", "temporal")
        relabeled = self.component_binding(component_path2, component2, piece="schema")
        integration_path2, _ = self.make_run(
            "integration-piece",
            "integration",
            record_type="integration_critic_verdict",
            components=[relabeled],
        )
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "verdict piece"):
            PROTOCOL.validate_verdict_file(integration_path2)


class SchemaParityTests(unittest.TestCase):
    def test_documented_schema_required_fields_match_authoritative_validator(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertIn("validator is authoritative", schema["description"])
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(
            set(schema["required"]), set(PROTOCOL.VERDICT_BASE_REQUIRED_FIELDS)
        )
        self.assertEqual(
            set(schema["properties"]["candidate"]["required"]),
            set(PROTOCOL.CANDIDATE_REQUIRED_FIELDS),
        )
        self.assertEqual(
            set(schema["properties"]["commands"]["items"]["required"]),
            set(PROTOCOL.COMMAND_REQUIRED_FIELDS),
        )
        self.assertEqual(
            set(schema["properties"]["evidence"]["items"]["required"]),
            set(PROTOCOL.EVIDENCE_REQUIRED_FIELDS),
        )
        self.assertEqual(
            set(schema["properties"]["plan"]["required"]),
            set(PROTOCOL.PLAN_REQUIRED_FIELDS),
        )
        self.assertEqual(
            set(schema["properties"]["component_verdicts"]["items"]["required"]),
            set(PROTOCOL.COMPONENT_BINDING_REQUIRED_FIELDS),
        )
        self.assertEqual(
            schema["properties"]["verdict_schema"]["properties"][
                "repo_relative_path"
            ]["const"],
            PROTOCOL.VERDICT_SCHEMA_RELATIVE_PATH,
        )
        integration_rule = schema["allOf"][0]
        self.assertEqual(
            integration_rule["then"]["required"], ["component_verdicts"]
        )
        self.assertEqual(
            integration_rule["else"]["not"]["required"], ["component_verdicts"]
        )

    def test_documented_schema_enums_types_patterns_and_closed_objects_match(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        properties = schema["properties"]
        definitions = schema["$defs"]
        self.assertEqual(
            set(properties["record_type"]["enum"]),
            {PROTOCOL.COMPONENT_RECORD_TYPE, PROTOCOL.INTEGRATION_RECORD_TYPE},
        )
        self.assertEqual(set(properties["verdict"]["enum"]), {"PASS", "FAIL"})
        self.assertEqual(properties["schema_version"]["const"], PROTOCOL.SCHEMA_VERSION)
        self.assertEqual(definitions["identifier"]["pattern"], PROTOCOL.IDENTIFIER_RE.pattern)
        self.assertEqual(definitions["gitSHA"]["pattern"], PROTOCOL.GIT_SHA_RE.pattern)
        self.assertEqual(definitions["sha256"]["pattern"], PROTOCOL.SHA256_RE.pattern)
        self.assertEqual(definitions["utcTimestamp"]["pattern"], PROTOCOL.UTC_RE.pattern)
        self.assertEqual(
            definitions["repoRelativeMarkdownPath"]["pattern"],
            PROTOCOL.REPO_RELATIVE_MARKDOWN_RE.pattern,
        )
        self.assertEqual(properties["commands"]["items"]["properties"]["exit_code"]["type"], "integer")
        for closed_object in (
            properties["candidate"],
            properties["verdict_schema"],
            properties["plan"],
            properties["commands"]["items"],
            properties["evidence"]["items"],
            properties["component_verdicts"]["items"],
        ):
            self.assertIs(closed_object["additionalProperties"], False)
        self.assertEqual(
            {variant["properties"]["status"]["const"] for variant in definitions["hashOrNA"]["oneOf"]},
            {"HASHED", "N/A"},
        )
        self.assertEqual(
            {variant["properties"]["status"]["const"] for variant in properties["inputs"]["oneOf"]},
            {"HASHED", "N/A"},
        )

    def test_repo_relative_markdown_path_samples_match_schema_pattern(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        schema_pattern = schema["$defs"]["repoRelativeMarkdownPath"]["pattern"]
        valid = (
            "capstone_V6_4.md",
            "docs/plans/capstone v6.4.md",
            ".plans/capstone.md",
        )
        invalid = (
            "/absolute.md",
            "../escape.md",
            "docs/../escape.md",
            "docs//double.md",
            "docs\\windows.md",
            "not-markdown.txt",
        )
        for value in valid:
            with self.subTest(value=value):
                self.assertIsNotNone(PROTOCOL.REPO_RELATIVE_MARKDOWN_RE.fullmatch(value))
                self.assertIsNotNone(re.fullmatch(schema_pattern, value))
        for value in invalid:
            with self.subTest(value=value):
                self.assertIsNone(PROTOCOL.REPO_RELATIVE_MARKDOWN_RE.fullmatch(value))
                self.assertIsNone(re.fullmatch(schema_pattern, value))


if __name__ == "__main__":
    unittest.main()
