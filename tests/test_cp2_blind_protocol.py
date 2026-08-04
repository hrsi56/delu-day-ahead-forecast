from __future__ import annotations

import copy
from decimal import Decimal, localcontext
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
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = REPO_ROOT / "scripts" / "gauntlet_protocol.py"
SNAPSHOT_PATH = REPO_ROOT / "scripts" / "gauntlet_critic_snapshot.sh"
VERDICT_SCHEMA_PATH = (
    REPO_ROOT / "docs" / "track-b" / "schemas" / "critic-verdict.schema.json"
)
BLIND_SCHEMA_PATH = (
    REPO_ROOT
    / "docs"
    / "track-b"
    / "schemas"
    / "cp2-blind-four-catalog.schema.json"
)
PLAN_EXCERPT = "CP-2 exact four-catalog acceptance rule."

SPEC = importlib.util.spec_from_file_location("cp2_gauntlet_protocol", PROTOCOL_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot import gauntlet_protocol.py")
PROTOCOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROTOCOL)


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class CP2RepoCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("symbolic-ref", "HEAD", "refs/heads/main")
        self.git("config", "user.name", "CP2 Test")
        self.git("config", "user.email", "cp2@example.invalid")
        (self.repo / "scripts").mkdir()
        schema_root = self.repo / "docs" / "track-b" / "schemas"
        schema_root.mkdir(parents=True)
        shutil.copyfile(PROTOCOL_PATH, self.repo / "scripts" / PROTOCOL_PATH.name)
        shutil.copyfile(SNAPSHOT_PATH, self.repo / "scripts" / SNAPSHOT_PATH.name)
        shutil.copyfile(VERDICT_SCHEMA_PATH, schema_root / VERDICT_SCHEMA_PATH.name)
        shutil.copyfile(BLIND_SCHEMA_PATH, schema_root / BLIND_SCHEMA_PATH.name)
        (self.repo / ".gitignore").write_text("/.gauntlet/\n", encoding="utf-8")
        self.plan_path = self.repo / "capstone_V6_4.md"
        self.plan_path.write_text(f"# Test plan\n\n{PLAN_EXCERPT}\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repo), *arguments],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode:
            self.fail(
                f"git {' '.join(arguments)} failed\n{result.stdout}\n{result.stderr}"
            )
        return result.stdout.strip()

    def source_csv(self, prediction: str, *, crossing: bool = False) -> bytes:
        rows: list[dict[str, str]] = []
        for fold in PROTOCOL.CP2_FOLDS:
            values = {name: prediction for name, _ in PROTOCOL.CP2_QUANTILES}
            if crossing:
                values["q10"] = "1"
                values["q90"] = "-1"
            rows.append(
                {
                    "fold_id": str(fold),
                    "row_id": f"r{fold:06d}",
                    "y": "0",
                    **values,
                }
            )
        return PROTOCOL._cp2_csv_bytes(PROTOCOL.CP2_SOURCE_HEADER, rows)

    def install_candidate(self, *, declared_winner: str = "residual_arm") -> None:
        prediction_values = {
            "strict_base": "100",
            "residual_arm": "98",
            "scarcity_arm": "99",
            "both_arms": "98.05",
        }
        prediction_root = self.repo / "artifacts" / "cp2" / "predictions"
        blind_root = self.repo / "artifacts" / "cp2" / "blind"
        prediction_root.mkdir(parents=True)
        blind_root.mkdir(parents=True)
        rows_by_role: dict[str, list[dict[str, str]]] = {}
        catalogs: list[dict[str, object]] = []
        for role in PROTOCOL.CP2_SEMANTIC_ROLES:
            raw = self.source_csv(prediction_values[role])
            relative = f"artifacts/cp2/predictions/{role}.csv"
            (self.repo / relative).write_bytes(raw)
            rows = PROTOCOL._cp2_parse_csv(
                raw, anonymous=False, field=f"test source {role}"
            )
            rows_by_role[role] = rows
            catalogs.append(
                {
                    "role": role,
                    "prediction_path": relative,
                    "sha256": digest(raw),
                    "feature_count": PROTOCOL.CP2_FEATURE_COUNTS[role],
                }
            )
        semantic_rows = [
            {"role": role, **row}
            for role in PROTOCOL.CP2_SEMANTIC_ROLES
            for row in rows_by_role[role]
        ]
        metrics = PROTOCOL._cp2_metrics(semantic_rows, identity_field="role")
        declaration = {
            "record_type": "cp2_blind_selection_declaration",
            "schema_version": "1.0",
            "checkpoint": "CP-2",
            "source_manifest_repo_relative_path": (
                "artifacts/cp2/blind/source-manifest.json"
            ),
            "rule_version": PROTOCOL.CP2_RULE_VERSION,
            "selected_role": declared_winner,
            "metrics_by_role": metrics,
            "recorded_at_utc": "2026-01-01T00:00:00Z",
        }
        declaration_raw = canonical_json(declaration)
        declaration_path = blind_root / "selection-declaration.json"
        declaration_path.write_bytes(declaration_raw)
        plan_raw = self.plan_path.read_bytes()
        manifest = {
            "record_type": "cp2_blind_source_manifest",
            "schema_version": "1.0",
            "checkpoint": "CP-2",
            "catalogs": catalogs,
            "csv_contract": {
                "header": list(PROTOCOL.CP2_SOURCE_HEADER),
                "folds": list(PROTOCOL.CP2_FOLDS),
                "quantiles": [name for name, _ in PROTOCOL.CP2_QUANTILES],
                "canonical_sort": ["fold_id_numeric", "row_id_utf8_bytes"],
            },
            "data_snapshot": {
                "snapshot_id": "test-snapshot",
                "cutoff_utc": "2026-01-01T00:00:00Z",
                "sha256": "1" * 64,
            },
            "rule": {
                "version": PROTOCOL.CP2_RULE_VERSION,
                "plan_filename": "capstone_V6_4.md",
                "plan_sha256": digest(plan_raw),
                "bar_citation": "§4.1 exact rule",
                "bar_excerpt": PLAN_EXCERPT,
                "canonicalization_version": PROTOCOL.CP2_CANONICALIZATION_VERSION,
            },
            "selection_declaration": {
                "repo_relative_path": (
                    "artifacts/cp2/blind/selection-declaration.json"
                ),
                "sha256": digest(declaration_raw),
            },
        }
        (blind_root / "source-manifest.json").write_bytes(canonical_json(manifest))
        self.git("add", ".")
        self.git("commit", "-q", "-m", "CP-2 candidate")
        self.git("checkout", "-q", "-b", "gauntlet/CP-2")
        self.candidate_sha = self.git("rev-parse", "HEAD")
        self.candidate_tree = self.git("rev-parse", "HEAD^{tree}")

    def allocate_run(self, run_id: str, piece: str) -> tuple[Path, Path, str]:
        ref, _, _ = PROTOCOL.create_evidence_ref(
            str(self.repo), "CP-2", run_id, piece, self.candidate_sha
        )
        run_root, support = PROTOCOL.initialize_evidence_root(
            str(self.repo), "CP-2", run_id
        )
        return run_root, support, ref

    def prepare_component(
        self, blind_id: str = "blind-001", run_id: str = "blind-run"
    ) -> tuple[Path, Path, dict[str, object], str]:
        run_root, support, ref = self.allocate_run(run_id, "blind-metrics")
        PROTOCOL.cp2_blind_prepare(
            str(self.repo), self.candidate_sha, blind_id, run_id
        )
        PROTOCOL.cp2_blind_recompute(str(support), blind_id)
        metrics = json.loads(
            (support / PROTOCOL.CP2_METRICS_FILENAME).read_text(encoding="utf-8")
        )
        manifest_path = run_root / "integrity-manifest.json"
        manifest_path.write_bytes(canonical_json({"test": "manifest"}))
        verdict_path = run_root / "critic-verdict.json"
        verdict_path.write_bytes(canonical_json({"test": "verdict"}))
        schema_hash = digest(
            (self.repo / PROTOCOL.CP2_BLIND_SCHEMA_RELATIVE_PATH).read_bytes()
        )
        record: dict[str, object] = {
            "record_type": PROTOCOL.COMPONENT_RECORD_TYPE,
            "checkpoint": "CP-2",
            "run_id": run_id,
            "piece": "blind-metrics",
            "verdict": "PASS",
            "candidate": {
                "commit_sha": self.candidate_sha,
                "tree_sha": self.candidate_tree,
                "evidence_ref": ref,
            },
            "integrity_manifest": {
                "path": str(manifest_path),
                "sha256": digest(manifest_path.read_bytes()),
            },
            "recorded_at_utc": PROTOCOL._timestamp_after(metrics["recorded_at_utc"]),
            "blind_review": {
                "blind_review_id": blind_id,
                "public_manifest": PROTOCOL._cp2_binding(
                    support / PROTOCOL.CP2_PUBLIC_MANIFEST_FILENAME
                ),
                "commitment": PROTOCOL._cp2_binding(
                    support / PROTOCOL.CP2_COMMITMENT_FILENAME
                ),
                "preparation_receipt": PROTOCOL._cp2_binding(
                    support / PROTOCOL.CP2_PREPARATION_RECEIPT_FILENAME
                ),
                "metrics": PROTOCOL._cp2_binding(
                    support / PROTOCOL.CP2_METRICS_FILENAME
                ),
                "protocol_schema": {
                    "repo_relative_path": PROTOCOL.CP2_BLIND_SCHEMA_RELATIVE_PATH,
                    "sha256": schema_hash,
                },
                "recompute_command": metrics["recompute_command"],
                "identity_decision": "NOT_PERFORMED",
            },
        }
        return verdict_path, support, record, digest(verdict_path.read_bytes())

    def build_frozen_chain(
        self, *, declared_winner: str = "residual_arm", blind_id: str = "blind-001"
    ) -> tuple[Path, Path, dict[str, object]]:
        self.install_candidate(declared_winner=declared_winner)
        component_path, component_support, component_record, component_hash = (
            self.prepare_component(blind_id)
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, component_hash),
        ):
            frozen = PROTOCOL.cp2_blind_freeze(
                str(self.repo),
                blind_id,
                str(component_path),
                "integration-run",
                "integration",
            )
            integration_support = Path(frozen["integration_support_root"])
        return integration_support, component_support, component_record

    def build_chain(
        self, *, declared_winner: str = "residual_arm", blind_id: str = "blind-001"
    ) -> tuple[Path, Path, dict[str, object]]:
        integration_support, component_support, component_record = (
            self.build_frozen_chain(
                declared_winner=declared_winner, blind_id=blind_id
            )
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(
                component_record,
                digest(
                    (
                        self.repo
                        / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
                    ).read_bytes()
                ),
            ),
        ):
            PROTOCOL.cp2_blind_reveal(
                str(self.repo), blind_id, "integration-run"
            )
        return integration_support, component_support, component_record


class CP2PrimitiveTests(unittest.TestCase):
    def metric(
        self, role: str, loss: str, hits: int, fold_losses: list[str]
    ) -> dict[str, object]:
        return {
            "role": role,
            "loss_sum": loss,
            "loss_denominator": 450,
            "coverage_hits": hits,
            "coverage_total": 50,
            "folds": [
                {
                    "fold_id": index + 1,
                    "loss_sum": value,
                    "loss_denominator": 90,
                    "row_count": 10,
                }
                for index, value in enumerate(fold_losses)
            ],
        }

    def test_fisher_yates_known_answer(self) -> None:
        seed = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
        self.assertEqual(
            PROTOCOL.cp2_permutation(seed),
            ("strict_base", "scarcity_arm", "both_arms", "residual_arm"),
        )

    def test_raw_quantile_crossing_is_accepted(self) -> None:
        case = object.__new__(CP2RepoCase)
        raw = CP2RepoCase.source_csv(case, "2", crossing=True)
        rows = PROTOCOL._cp2_parse_csv(raw, anonymous=False, field="crossing")
        self.assertGreater(Decimal(rows[0]["q10"]), Decimal(rows[0]["q90"]))

    def test_binary_or_filename_identity_leak_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            support = Path(directory).resolve()
            hidden = support / "opaque.bin"
            hidden.write_bytes(b"\xffstrict_base")
            with self.assertRaisesRegex(PROTOCOL.ProtocolError, "Identity token"):
                PROTOCOL._cp2_assert_public_sanitized(support)
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "Identity token"):
            PROTOCOL._cp2_assert_identity_free_value(
                {"expected_output": "winner is residual arm"}, "Blind verdict"
            )
        with tempfile.TemporaryDirectory() as directory:
            support = Path(directory).resolve()
            named = support / "strict_base.bin"
            named.write_bytes(b"\x00\xff")
            with self.assertRaisesRegex(PROTOCOL.ProtocolError, "Identity token"):
                PROTOCOL._cp2_assert_public_sanitized(support)

    def test_exact_boundaries_and_dynamic_precision(self) -> None:
        huge = "9" * 140
        with localcontext() as context:
            context.prec = 300
            base = Decimal(huge)
            arm = base * Decimal("0.99")
            fold_base = base / 5
            fold_arm = arm / 5
            metrics = [
                self.metric("strict_base", str(base), 45, [str(fold_base)] * 5),
                self.metric("residual_arm", str(arm), 44, [str(fold_arm)] * 5),
                self.metric("scarcity_arm", str(base), 45, [str(fold_base)] * 5),
                self.metric("both_arms", str(base), 45, [str(fold_base)] * 5),
            ]
        winner, trace = PROTOCOL._cp2_adjudicate_exact(metrics)
        self.assertEqual(winner, "residual_arm")
        residual = trace["candidates"][0]
        self.assertTrue(residual["relative_loss"]["pass"])
        self.assertTrue(residual["coverage"]["pass"])
        self.assertEqual(residual["improving_folds"], 5)
        self.assertGreater(
            PROTOCOL._cp2_precision([huge, "0." + "0" * 130 + "1"]), 270
        )

    def test_metric_recompute_preserves_huge_integer_and_tiny_fraction(self) -> None:
        huge = "8" * 135
        tiny = "0." + "0" * 125 + "1"
        rows: list[dict[str, str]] = []
        for label in PROTOCOL.CP2_LABELS:
            for fold in PROTOCOL.CP2_FOLDS:
                rows.append(
                    {
                        "label": label,
                        "fold_id": str(fold),
                        "row_id": f"r{fold:06d}",
                        "y": huge,
                        **{name: tiny for name, _ in PROTOCOL.CP2_QUANTILES},
                    }
                )
        metrics = PROTOCOL._cp2_metrics(rows, identity_field="label")
        with localcontext() as context:
            context.prec = 400
            per_row = sum(
                (
                    max(
                        tau * (Decimal(huge) - Decimal(tiny)),
                        (tau - Decimal(1)) * (Decimal(huge) - Decimal(tiny)),
                    )
                    for _, tau in PROTOCOL.CP2_QUANTILES
                ),
                Decimal(0),
            )
            expected = PROTOCOL._cp2_decimal_string(per_row * 5)
        self.assertEqual(metrics[0]["loss_sum"], expected)

    def test_metric_validator_rejects_boolean_and_integral_float_integers(self) -> None:
        metrics = [
            self.metric(role, "50", 40, ["10"] * 5)
            for role in PROTOCOL.CP2_SEMANTIC_ROLES
        ]
        for path, invalid in (
            ((0, "coverage_hits"), True),
            ((0, "folds", 0, "fold_id"), True),
            ((0, "folds", 0, "loss_denominator"), 90.0),
        ):
            with self.subTest(path=path, invalid=invalid):
                malformed = copy.deepcopy(metrics)
                target: object = malformed
                for key in path[:-1]:
                    target = target[key]  # type: ignore[index]
                target[path[-1]] = invalid  # type: ignore[index]
                with self.assertRaisesRegex(
                    PROTOCOL.ProtocolError, "non-Boolean JSON integer"
                ):
                    PROTOCOL._cp2_validate_metric_entries(
                        malformed,
                        identity_field="role",
                        field="strict metrics",
                    )


class CP2ProtocolFlowTests(CP2RepoCase):
    def test_prepare_requires_empty_support_and_runtime_tool_identity(self) -> None:
        self.install_candidate()
        _, support, _ = self.allocate_run("blind-nonempty", "blind-metrics")
        (support / "identity-bearing.txt").write_text(
            "strict_base", encoding="utf-8"
        )
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "completely empty"):
            PROTOCOL.cp2_blind_prepare(
                str(self.repo), self.candidate_sha, "blind-nonempty", "blind-nonempty"
            )
        _, clean_support, _ = self.allocate_run("blind-runtime", "blind-metrics")
        with mock.patch.object(
            PROTOCOL,
            "_cp2_require_runtime_tool_hash",
            side_effect=PROTOCOL.ProtocolError("runtime mismatch"),
        ):
            with self.assertRaisesRegex(PROTOCOL.ProtocolError, "runtime mismatch"):
                PROTOCOL.cp2_blind_prepare(
                    str(self.repo), self.candidate_sha, "blind-runtime", "blind-runtime"
                )
        self.assertTrue(
            (self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-runtime").is_dir()
        )
        self.assertFalse((clean_support / PROTOCOL.CP2_PUBLIC_INPUT_FILENAME).exists())

        _, drift_support, _ = self.allocate_run("blind-runtime-real", "blind-metrics")
        runtime_copy = self.repo / "scripts" / "gauntlet_protocol.py"
        runtime_copy.write_bytes(runtime_copy.read_bytes() + b"\n# runtime drift\n")
        result = subprocess.run(
            [
                "python3",
                str(runtime_copy),
                "blind-prepare",
                "--repo-root",
                str(self.repo),
                "--candidate-sha",
                self.candidate_sha,
                "--blind-review-id",
                "blind-runtime-real",
                "--component-run-id",
                "blind-runtime-real",
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("strict_base", result.stderr)
        self.assertFalse((drift_support / PROTOCOL.CP2_PUBLIC_INPUT_FILENAME).exists())

    def test_end_to_end_uses_only_integration_owned_copies(self) -> None:
        integration_support, component_support, _ = self.build_chain()
        freeze = json.loads(
            (integration_support / PROTOCOL.CP2_FREEZE_FILENAME).read_text(
                encoding="utf-8"
            )
        )
        for name in (
            "anonymous_csv",
            "public_manifest",
            "commitment",
            "preparation_receipt",
            "metrics",
        ):
            path = Path(freeze[name]["path"])
            self.assertEqual(path.parent, integration_support)
            self.assertEqual(path.stat().st_nlink, 1)
        hidden_component = self.base / "hidden-component-support"
        hidden_custody = self.base / "hidden-custody"
        component_support.rename(hidden_component)
        custody = self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
        custody.rename(hidden_custody)
        result, matched = PROTOCOL.cp2_blind_adjudicate(
            str(integration_support), "blind-001"
        )
        self.assertTrue(matched)
        self.assertEqual(result["computed_winner"], "residual_arm")
        self.assertEqual(result["reason"], "match")

    def test_freeze_refuses_preallocated_integration_identity(self) -> None:
        self.install_candidate()
        component_path, _, component_record, component_hash = self.prepare_component()
        _, preallocated_support, _ = self.allocate_run(
            "integration-preallocated", "integration"
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, component_hash),
        ):
            with self.assertRaisesRegex(PROTOCOL.ProtocolError, "Refusing to reuse"):
                PROTOCOL.cp2_blind_freeze(
                    str(self.repo),
                    "blind-001",
                    str(component_path),
                    "integration-preallocated",
                    "integration",
                )
        self.assertEqual(list(preallocated_support.iterdir()), [])

    def test_prepare_receipt_binds_immutable_custody_record(self) -> None:
        self.install_candidate()
        _, support, _ = self.allocate_run("blind-run", "blind-metrics")
        PROTOCOL.cp2_blind_prepare(
            str(self.repo), self.candidate_sha, "blind-001", "blind-run"
        )
        receipt = json.loads(
            (support / PROTOCOL.CP2_PREPARATION_RECEIPT_FILENAME).read_text(
                encoding="utf-8"
            )
        )
        custody_record = (
            self.repo
            / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
            / PROTOCOL.CP2_CUSTODY_RECORD_FILENAME
        )
        self.assertEqual(
            receipt["custody_record_sha256"], digest(custody_record.read_bytes())
        )

    def test_blind_verdict_rejects_paired_custody_receipt_rewrite(self) -> None:
        self.install_candidate()
        _, support, component_record, _ = self.prepare_component()
        custody_root = (
            self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
        )
        custody_path = custody_root / PROTOCOL.CP2_CUSTODY_RECORD_FILENAME
        custody = json.loads(custody_path.read_text(encoding="utf-8"))
        custody["sources"][0]["repo_relative_path"] = "false/source.csv"
        custody_path.write_bytes(canonical_json(custody))
        receipt_path = support / PROTOCOL.CP2_PREPARATION_RECEIPT_FILENAME
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["custody_record_sha256"] = digest(custody_path.read_bytes())
        receipt_path.write_bytes(canonical_json(receipt))
        with self.assertRaisesRegex(
            PROTOCOL.ProtocolError, "preparation_receipt.sha256 mismatch"
        ):
            PROTOCOL._validate_cp2_blind_review(
                component_record["blind_review"],
                support_root=support,
                repo_root=self.repo,
                candidate_sha=self.candidate_sha,
                candidate_tree=self.candidate_tree,
                checkpoint="CP-2",
                recorded_at_utc=component_record["recorded_at_utc"],
            )

    def test_prepare_rejects_boolean_feature_counts(self) -> None:
        self.install_candidate()
        manifest_path = (
            self.repo / "artifacts/cp2/blind/source-manifest.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["catalogs"][0]["feature_count"] = False
        manifest["catalogs"][1]["feature_count"] = True
        manifest["catalogs"][2]["feature_count"] = True
        manifest_path.write_bytes(canonical_json(manifest))
        self.git("add", str(manifest_path.relative_to(self.repo)))
        self.git("commit", "-q", "-m", "malformed boolean feature counts")
        self.candidate_sha = self.git("rev-parse", "HEAD")
        self.candidate_tree = self.git("rev-parse", "HEAD^{tree}")
        self.allocate_run("blind-run", "blind-metrics")
        with self.assertRaisesRegex(
            PROTOCOL.ProtocolError, "non-Boolean JSON integer"
        ):
            PROTOCOL.cp2_blind_prepare(
                str(self.repo), self.candidate_sha, "blind-001", "blind-run"
            )

    def test_source_folds_and_commitment_seed_bits_are_type_strict(self) -> None:
        self.install_candidate()
        manifest_path = self.repo / "artifacts/cp2/blind/source-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for invalid in (True, 1.0):
            with self.subTest(source_fold=invalid):
                malformed = copy.deepcopy(manifest)
                malformed["csv_contract"]["folds"][0] = invalid
                with self.assertRaisesRegex(PROTOCOL.ProtocolError, "folds"):
                    PROTOCOL._cp2_validate_source_manifest(
                        malformed,
                        source_manifest_sha256="a" * 64,
                        selection_declaration_sha256=manifest[
                            "selection_declaration"
                        ]["sha256"],
                    )

        _, support, _ = self.allocate_run("blind-run", "blind-metrics")
        PROTOCOL.cp2_blind_prepare(
            str(self.repo), self.candidate_sha, "blind-001", "blind-run"
        )
        public_path = support / PROTOCOL.CP2_PUBLIC_MANIFEST_FILENAME
        public, public_raw = PROTOCOL._load_json(public_path)
        commitment_path = support / PROTOCOL.CP2_COMMITMENT_FILENAME
        commitment, _ = PROTOCOL._load_json(commitment_path)
        for invalid in (True, 256.0):
            with self.subTest(seed_bits=invalid):
                malformed = copy.deepcopy(commitment)
                malformed["seed_bits"] = invalid
                with self.assertRaisesRegex(
                    PROTOCOL.ProtocolError, "non-Boolean JSON integer"
                ):
                    PROTOCOL._cp2_validate_commitment(
                        malformed,
                        support_root=support,
                        blind_review_id="blind-001",
                        public_manifest_path=public_path,
                        public_manifest_hash=digest(public_raw),
                    )

    def test_reveal_rejects_rewritten_preparation_invocation(self) -> None:
        integration_support, _, component_record = self.build_frozen_chain()
        custody = self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
        invocation_path = custody / PROTOCOL.CP2_PREPARATION_INVOCATION_FILENAME
        invocation = json.loads(invocation_path.read_text(encoding="utf-8"))
        invocation["argv"][0] = "python-rewritten"
        invocation_path.write_bytes(canonical_json(invocation))
        custody_record_path = custody / PROTOCOL.CP2_CUSTODY_RECORD_FILENAME
        custody_record = json.loads(custody_record_path.read_text(encoding="utf-8"))
        custody_record["preparation_invocation"]["sha256"] = digest(
            invocation_path.read_bytes()
        )
        custody_record_path.write_bytes(canonical_json(custody_record))
        component_path = (
            self.repo / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "custody-record hash mismatch"
            ):
                PROTOCOL.cp2_blind_reveal(
                    str(self.repo), "blind-001", "integration-run"
                )

    def test_reveal_rejects_external_custody_source_path(self) -> None:
        integration_support, _, component_record = self.build_frozen_chain()
        custody = self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
        canonical_source = custody / PROTOCOL.CP2_CUSTODY_SOURCE_MANIFEST_FILENAME
        external_source = self.base / "external-source-manifest.json"
        shutil.copyfile(canonical_source, external_source)
        custody_record_path = custody / PROTOCOL.CP2_CUSTODY_RECORD_FILENAME
        custody_record = json.loads(custody_record_path.read_text(encoding="utf-8"))
        custody_record["source_manifest"]["custody_path"] = str(external_source)
        custody_record_path.write_bytes(canonical_json(custody_record))
        component_path = (
            self.repo / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "custody-record hash mismatch"
            ):
                PROTOCOL.cp2_blind_reveal(
                    str(self.repo), "blind-001", "integration-run"
                )
        self.assertFalse(
            (integration_support / PROTOCOL.CP2_REVEAL_FILENAME).exists()
        )

    def test_reveal_rejects_false_custody_source_identity_even_if_rebound(self) -> None:
        integration_support, _, component_record = self.build_frozen_chain()
        custody_root = (
            self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
        )
        custody_path = custody_root / PROTOCOL.CP2_CUSTODY_RECORD_FILENAME
        custody = json.loads(custody_path.read_text(encoding="utf-8"))
        custody["sources"][0]["repo_relative_path"] = "false/source.csv"
        custody_path.write_bytes(canonical_json(custody))

        receipt_path = integration_support / PROTOCOL.CP2_FROZEN_RECEIPT_FILENAME
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["custody_record_sha256"] = digest(custody_path.read_bytes())
        receipt_path.write_bytes(canonical_json(receipt))
        freeze_path = integration_support / PROTOCOL.CP2_FREEZE_FILENAME
        freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
        freeze["preparation_receipt"]["sha256"] = digest(receipt_path.read_bytes())
        freeze_path.write_bytes(canonical_json(freeze))

        component_path = (
            self.repo / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "source manifest and mapping preimage"
            ):
                PROTOCOL.cp2_blind_reveal(
                    str(self.repo), "blind-001", "integration-run"
                )

    def test_reveal_rejects_invalid_custody_timestamp(self) -> None:
        _, _, component_record = self.build_frozen_chain()
        custody = self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
        custody_record_path = custody / PROTOCOL.CP2_CUSTODY_RECORD_FILENAME
        custody_record = json.loads(custody_record_path.read_text(encoding="utf-8"))
        custody_record["recorded_at_utc"] = "tampered"
        custody_record_path.write_bytes(canonical_json(custody_record))
        component_path = (
            self.repo / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            with self.assertRaisesRegex(PROTOCOL.ProtocolError, "UTC timestamp"):
                PROTOCOL.cp2_blind_reveal(
                    str(self.repo), "blind-001", "integration-run"
                )

    def test_reveal_rejects_valid_rewritten_custody_timestamp(self) -> None:
        _, _, component_record = self.build_frozen_chain()
        custody = self.repo / ".gauntlet/evidence/CP-2/_blind-custody/blind-001"
        custody_record_path = custody / PROTOCOL.CP2_CUSTODY_RECORD_FILENAME
        custody_record = json.loads(custody_record_path.read_text(encoding="utf-8"))
        custody_record["recorded_at_utc"] = "2026-01-01T00:00:00Z"
        custody_record_path.write_bytes(canonical_json(custody_record))
        component_path = (
            self.repo / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "custody-record hash mismatch"
            ):
                PROTOCOL.cp2_blind_reveal(
                    str(self.repo), "blind-001", "integration-run"
                )

    def test_reveal_rejects_freeze_integrity_manifest_substitution(self) -> None:
        integration_support, _, component_record = self.build_frozen_chain()
        freeze_path = integration_support / PROTOCOL.CP2_FREEZE_FILENAME
        freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
        component_path = (
            self.repo / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        freeze["blind_component"]["integrity_manifest"] = {
            "path": str(component_path),
            "sha256": digest(component_path.read_bytes()),
        }
        freeze_path.write_bytes(canonical_json(freeze))
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "exactly reproduce"
            ):
                PROTOCOL.cp2_blind_reveal(
                    str(self.repo), "blind-001", "integration-run"
                )

    def test_terminal_binding_requires_exactly_one_blind_component(self) -> None:
        integration_support, _, component_record = self.build_chain()
        adjudication, matched = PROTOCOL.cp2_blind_adjudicate(
            str(integration_support), "blind-001"
        )
        self.assertTrue(matched)
        component_path = (
            self.repo
            / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        component_hash = digest(component_path.read_bytes())
        binding = {
            "path": str(component_path),
            "piece": "blind-metrics",
            "sha256": component_hash,
            "candidate_sha": self.candidate_sha,
            "candidate_tree": self.candidate_tree,
        }
        selection_raw = subprocess.run(
            [
                "git",
                "-C",
                str(self.repo),
                "show",
                f"{self.candidate_sha}:{PROTOCOL.CP2_SELECTION_DECLARATION_RELATIVE_PATH}",
            ],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        value = {
            "blind_review_id": "blind-001",
            "freeze": PROTOCOL._cp2_binding(
                integration_support / PROTOCOL.CP2_FREEZE_FILENAME
            ),
            "reveal": PROTOCOL._cp2_binding(
                integration_support / PROTOCOL.CP2_REVEAL_FILENAME
            ),
            "adjudication": PROTOCOL._cp2_binding(
                integration_support / PROTOCOL.CP2_ADJUDICATION_FILENAME
            ),
            "selected_role": adjudication["computed_winner"],
            "selection_declaration": {
                "repo_relative_path": PROTOCOL.CP2_SELECTION_DECLARATION_RELATIVE_PATH,
                "sha256": digest(selection_raw),
            },
        }
        components = [(binding, component_record, component_hash)]
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, component_hash),
        ):
            PROTOCOL._validate_cp2_integration_adjudication(
                value,
                support_root=integration_support,
                repo_root=self.repo,
                candidate_sha=self.candidate_sha,
                candidate_tree=self.candidate_tree,
                integration_verdict="PASS",
                integration_recorded_at=PROTOCOL._timestamp_after(
                    adjudication["recorded_at_utc"]
                ),
                component_records=components,
            )
            with self.assertRaisesRegex(PROTOCOL.ProtocolError, "exactly one"):
                PROTOCOL._validate_cp2_integration_adjudication(
                    value,
                    support_root=integration_support,
                    repo_root=self.repo,
                    candidate_sha=self.candidate_sha,
                    candidate_tree=self.candidate_tree,
                    integration_verdict="PASS",
                    integration_recorded_at=PROTOCOL._timestamp_after(
                        adjudication["recorded_at_utc"]
                    ),
                    component_records=[*components, *components],
                )

    def test_mismatch_creates_valid_record_and_nonzero_cli(self) -> None:
        integration_support, _, component_record = self.build_chain(
            declared_winner="scarcity_arm"
        )
        command = subprocess.run(
            [
                "python3",
                str(PROTOCOL_PATH),
                "blind-adjudicate",
                "--integration-support-root",
                str(integration_support),
                "--blind-review-id",
                "blind-001",
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(command.returncode, 2, command.stderr)
        record = json.loads(
            (integration_support / PROTOCOL.CP2_ADJUDICATION_FILENAME).read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(record["match"])
        self.assertIn("winner_mismatch", record["reason"])
        component_path = (
            self.repo
            / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            validated, _, _ = PROTOCOL._cp2_validate_adjudication_record(
                integration_support,
                "blind-001",
                repo_root=self.repo,
            )
        self.assertFalse(validated["match"])
        adjudication_path = integration_support / PROTOCOL.CP2_ADJUDICATION_FILENAME
        backdated = json.loads(adjudication_path.read_text(encoding="utf-8"))
        reveal = json.loads(
            (integration_support / PROTOCOL.CP2_REVEAL_FILENAME).read_text(
                encoding="utf-8"
            )
        )
        backdated["recorded_at_utc"] = reveal["recorded_at_utc"]
        adjudication_path.write_bytes(canonical_json(backdated))
        with mock.patch.object(
            PROTOCOL,
            "validate_verdict_file",
            return_value=(component_record, digest(component_path.read_bytes())),
        ):
            with self.assertRaisesRegex(PROTOCOL.ProtocolError, "chronology"):
                PROTOCOL._cp2_validate_adjudication_record(
                    integration_support,
                    "blind-001",
                    repo_root=self.repo,
                )

    def test_terminal_adjudication_rejects_boolean_integer_substitution(self) -> None:
        integration_support, _, component_record = self.build_chain()
        PROTOCOL.cp2_blind_adjudicate(str(integration_support), "blind-001")
        adjudication_path = integration_support / PROTOCOL.CP2_ADJUDICATION_FILENAME
        original = json.loads(adjudication_path.read_text(encoding="utf-8"))
        component_path = (
            self.repo / ".gauntlet/evidence/CP-2/blind-run/critic-verdict.json"
        )
        for field, invalid, expected_error in (
            ("decision.base_loss_zero", 0, "decision trace mismatch"),
            ("declaration_metrics_match", 1, "declaration_metrics_match mismatch"),
        ):
            with self.subTest(field=field):
                malformed = copy.deepcopy(original)
                if field.startswith("decision."):
                    malformed["decision"][field.split(".", 1)[1]] = invalid
                else:
                    malformed[field] = invalid
                adjudication_path.write_bytes(canonical_json(malformed))
                with mock.patch.object(
                    PROTOCOL,
                    "validate_verdict_file",
                    return_value=(
                        component_record,
                        digest(component_path.read_bytes()),
                    ),
                ):
                    with self.assertRaisesRegex(
                        PROTOCOL.ProtocolError, expected_error
                    ):
                        PROTOCOL._cp2_validate_adjudication_record(
                            integration_support,
                            "blind-001",
                            repo_root=self.repo,
                        )
        adjudication_path.write_bytes(canonical_json(original))

    def test_future_reveal_burns_adjudication_without_record(self) -> None:
        integration_support, _, _ = self.build_chain()
        reveal_path = integration_support / PROTOCOL.CP2_REVEAL_FILENAME
        reveal = json.loads(reveal_path.read_text(encoding="utf-8"))
        reveal["recorded_at_utc"] = "2999-01-01T00:00:00Z"
        reveal_path.write_bytes(canonical_json(reveal))
        with self.assertRaisesRegex(PROTOCOL.ProtocolError, "strictly after"):
            PROTOCOL.cp2_blind_adjudicate(str(integration_support), "blind-001")
        self.assertTrue(
            (integration_support / PROTOCOL.CP2_ADJUDICATE_ATTEMPT_FILENAME).is_file()
        )
        self.assertFalse(
            (integration_support / PROTOCOL.CP2_ADJUDICATION_FILENAME).exists()
        )


class CP2SchemaParityTests(unittest.TestCase):
    def test_schema_ids_and_verdict_extension_required_fields(self) -> None:
        blind = json.loads(BLIND_SCHEMA_PATH.read_text(encoding="utf-8"))
        verdict = json.loads(VERDICT_SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(blind["$id"], PROTOCOL.CP2_BLIND_SCHEMA_ID)
        self.assertEqual(blind["x-validator"], "scripts/gauntlet_protocol.py@1.0")
        self.assertEqual(
            set(verdict["properties"]["blind_review"]["required"]),
            set(PROTOCOL.CP2_BLIND_REVIEW_REQUIRED_FIELDS),
        )
        self.assertEqual(
            set(verdict["properties"]["blind_adjudication"]["required"]),
            set(PROTOCOL.CP2_BLIND_ADJUDICATION_REQUIRED_FIELDS),
        )
        self.assertEqual(
            verdict["properties"]["blind_review"]["properties"][
                "identity_decision"
            ]["const"],
            "NOT_PERFORMED",
        )
        self.assertIn(
            "allocated_at_utc",
            blind["$defs"]["integrationIdentity"]["required"],
        )
        self.assertIn(
            "preparation_invocation_sha256",
            blind["$defs"]["mappingPreimage"]["required"],
        )
        self.assertIn(
            "custody_record_sha256",
            blind["$defs"]["preparationReceipt"]["required"],
        )
        self.assertNotIn(
            "preparation_receipt",
            blind["$defs"]["custody"]["required"],
        )
        self.assertIn("non-Boolean Python int", blind["x-runtime-integer-policy"])
        self.assertIn("non-Boolean Python int", verdict["x-runtime-integer-policy"])
        conditional_text = json.dumps(verdict["allOf"], sort_keys=True)
        self.assertIn('"checkpoint": {"const": "CP-2"}', conditional_text)

    def test_blind_schema_closes_nested_objects_and_matches_canonical_decimal(self) -> None:
        schema = json.loads(BLIND_SCHEMA_PATH.read_text(encoding="utf-8"))
        open_objects: list[str] = []

        def visit(value: object, path: str = "$") -> None:
            if isinstance(value, dict):
                if value.get("type") == "object" and value.get(
                    "additionalProperties"
                ) is not False:
                    open_objects.append(path)
                for name, child in value.items():
                    visit(child, f"{path}/{name}")
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    visit(child, f"{path}/{index}")

        visit(schema)
        self.assertEqual(open_objects, [])
        pattern = schema["$defs"]["decimal"]["pattern"]
        accepted = ("0", "1", "-1", "10.01", "0.0001", "-0.0001")
        rejected = ("-0", "0.0", "1.20", "01", "+1", "1e2", "NaN")
        for value in accepted:
            self.assertIsNotNone(re.fullmatch(pattern, value), value)
            PROTOCOL._cp2_decimal(value, "sample")
        for value in rejected:
            self.assertIsNone(re.fullmatch(pattern, value), value)
            with self.assertRaises(PROTOCOL.ProtocolError):
                PROTOCOL._cp2_decimal(value, "sample")


if __name__ == "__main__":
    unittest.main()
