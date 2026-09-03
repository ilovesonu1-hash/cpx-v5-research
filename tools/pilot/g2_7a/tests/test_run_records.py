from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MODULE_DIR = ROOT / "tools/pilot/g2_7a"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import build_bundle as builder
import validate_run_records as run_validator


class RunRecordValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / builder.EXECUTION_MANIFEST).read_text(encoding="utf-8"))
        cls.bundle = json.loads((ROOT / builder.INPUT_BUNDLE).read_text(encoding="utf-8"))
        cls.unit_by_id = {unit["execution_unit_id"]: unit for unit in cls.manifest["execution_units"]}
        cls.call_by_id = {call["planned_call_id"]: call for call in cls.manifest["planned_calls"]}

    def completed_attempt(
        self,
        unit_id: str,
        *,
        attempt: int = 1,
        session_id: str | None = None,
    ) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
        session_id = session_id or f"session-{unit_id.lower()}-{attempt}"
        rows: list[dict[str, object]] = []
        for call_id in self.unit_by_id[unit_id]["planned_call_ids"]:
            planned = self.call_by_id[call_id]
            system_hashes = self.bundle["identities"]["system_messages"]
            suffix = f"/{planned['case']}-system-message-v1.txt"
            system_hash = next(value for path, value in system_hashes.items() if path.endswith(suffix))
            rows.append(
                {
                    "authoritative_attempt": True,
                    "case": planned["case"],
                    "constituent_or_setup_id": planned["constituent_or_setup_id"],
                    "execution_error_class": None,
                    "execution_error_message_safe": None,
                    "execution_unit_id": unit_id,
                    "exposed_generation_settings": "NOT_EXPOSED",
                    "final_patient_response": "",
                    "input_bundle_id": self.bundle["input_bundle_id"],
                    "learner_utterance": planned["learner_utterance"],
                    "model": "gemini-3.7-flash",
                    "planned_call_id": call_id,
                    "physical_isolation_verified": True,
                    "provider_completion_status": "completed",
                    "run_id": f"run-{unit_id.lower()}-{attempt}-{planned['turn_index']}",
                    "safe_session_id": session_id,
                    "scored_turn": planned["scored_turn"],
                    "scored_unit_id": planned["scored_unit_id"],
                    "separate_reasoning_field_present": False,
                    "source_trajectory_id": planned["source_trajectory_id"],
                    "system_message_sha256": system_hash,
                    "timestamp_utc": "2026-09-03T00:00:00Z",
                    "turn_index": planned["turn_index"],
                    "unit_attempt_index": attempt,
                    "runtime": self.manifest["runtime"],
                }
            )
        events = [
            {
                "authoritative_attempt": True,
                "event_type": "ATTEMPT_COMPLETED",
                "execution_error_class": None,
                "execution_error_message_safe": None,
                "execution_unit_id": unit_id,
                "input_bundle_id": self.bundle["input_bundle_id"],
                "model_call_created": True,
                "safe_session_id": session_id,
                "timestamp_utc": "2026-09-03T00:00:00Z",
                "unit_attempt_index": attempt,
            }
        ]
        return rows, events

    def test_correct_multiturn_unit_passes_and_derives_ordered_score_ids(self) -> None:
        calls, events = self.completed_attempt("P-SEQ-02")
        result = run_validator.validate_records(
            self.manifest,
            self.bundle,
            calls,
            events,
            required_execution_unit_ids={"P-SEQ-02"},
        )
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(
            [calls[0]["run_id"], calls[1]["run_id"]],
            result.authoritative_run_ids_by_scored_unit["P14"],
        )
        self.assertEqual(
            [calls[0]["run_id"], calls[1]["run_id"], calls[2]["run_id"]],
            result.authoritative_run_ids_by_scored_unit["P15"],
        )

    def test_correct_p29_unit_passes_with_six_evidence_calls(self) -> None:
        calls, events = self.completed_attempt("P29-STATION-01")
        result = run_validator.validate_records(
            self.manifest,
            self.bundle,
            calls,
            events,
            required_execution_unit_ids={"P29-STATION-01"},
        )
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(6, len(result.authoritative_run_ids_by_scored_unit["P29"]))

    def test_cross_unit_session_reuse_fails(self) -> None:
        calls_a, events_a = self.completed_attempt("J01-SINGLE", session_id="shared-session")
        calls_b, events_b = self.completed_attempt("J02-SINGLE", session_id="shared-session")
        result = run_validator.validate_records(
            self.manifest,
            self.bundle,
            calls_a + calls_b,
            events_a + events_b,
            required_execution_unit_ids={"J01-SINGLE", "J02-SINGLE"},
        )
        self.assertIn("RUN_SESSION_REUSED_ACROSS_ATTEMPTS", result.errors)

    def test_retry_session_reuse_fails(self) -> None:
        calls, events = self.completed_attempt("J01-SINGLE", attempt=2, session_id="reused-session")
        failed = copy.deepcopy(calls[0])
        failed.update(
            {
                "authoritative_attempt": False,
                "execution_error_class": "TIMEOUT",
                "execution_error_message_safe": "safe timeout",
                "final_patient_response": None,
                "provider_completion_status": "execution_error",
                "run_id": "run-j01-failed",
                "unit_attempt_index": 1,
            }
        )
        failed_event = {
            "authoritative_attempt": False,
            "event_type": "ATTEMPT_FAILED",
            "execution_error_class": "TIMEOUT",
            "execution_error_message_safe": "safe timeout",
            "execution_unit_id": "J01-SINGLE",
            "input_bundle_id": self.bundle["input_bundle_id"],
            "model_call_created": True,
            "safe_session_id": "reused-session",
            "timestamp_utc": "2026-09-03T00:00:00Z",
            "unit_attempt_index": 1,
        }
        result = run_validator.validate_records(
            self.manifest,
            self.bundle,
            [failed, *calls],
            [failed_event, *events],
            required_execution_unit_ids={"J01-SINGLE"},
        )
        self.assertIn("RUN_SESSION_REUSED_ACROSS_ATTEMPTS", result.errors)

    def test_preflight_and_official_session_overlap_fails(self) -> None:
        calls, events = self.completed_attempt("J01-SINGLE", session_id="preflight-session-a")
        result = run_validator.validate_records(
            self.manifest,
            self.bundle,
            calls,
            events,
            preflight_session_ids={"preflight-session-a"},
            required_execution_unit_ids={"J01-SINGLE"},
        )
        self.assertIn("RUN_PREFLIGHT_SESSION_OVERLAP", result.errors)

    def test_multiple_authoritative_attempts_fail(self) -> None:
        calls_a, events_a = self.completed_attempt("J01-SINGLE", attempt=1)
        calls_b, events_b = self.completed_attempt("J01-SINGLE", attempt=2)
        result = run_validator.validate_records(
            self.manifest,
            self.bundle,
            calls_a + calls_b,
            events_a + events_b,
            required_execution_unit_ids={"J01-SINGLE"},
        )
        self.assertIn("RUN_AUTHORITATIVE_ATTEMPT_COUNT", result.errors)

    def test_missing_extra_and_out_of_order_calls_fail(self) -> None:
        calls, events = self.completed_attempt("P-SEQ-02")
        missing = run_validator.validate_records(
            self.manifest,
            self.bundle,
            calls[:-1],
            events,
            required_execution_unit_ids={"P-SEQ-02"},
        )
        self.assertIn("RUN_AUTHORITATIVE_ATTEMPT_INCOMPLETE", missing.errors)

        extra_calls = copy.deepcopy(calls)
        extra_calls.append(copy.deepcopy(calls[-1]))
        extra_calls[-1]["run_id"] = "run-extra"
        extra = run_validator.validate_records(
            self.manifest,
            self.bundle,
            extra_calls,
            events,
            required_execution_unit_ids={"P-SEQ-02"},
        )
        self.assertIn("RUN_AUTHORITATIVE_ATTEMPT_INCOMPLETE", extra.errors)

        out_of_order = run_validator.validate_records(
            self.manifest,
            self.bundle,
            list(reversed(calls)),
            events,
            required_execution_unit_ids={"P-SEQ-02"},
        )
        self.assertIn("RUN_AUTHORITATIVE_ATTEMPT_INCOMPLETE", out_of_order.errors)

    def test_scorecard_run_id_mapping_is_exact_and_ordered(self) -> None:
        calls, events = self.completed_attempt("J-SEQ-02")
        expected = {
            "J07": [calls[0]["run_id"]],
            "J14": [calls[0]["run_id"], calls[1]["run_id"]],
            "J15": [calls[0]["run_id"], calls[1]["run_id"], calls[2]["run_id"]],
        }
        scorecard = [
            {
                "scored_unit_id": scored_id,
                "authoritative_run_ids": json.dumps(run_ids, separators=(",", ":")),
            }
            for scored_id, run_ids in expected.items()
        ]
        result = run_validator.validate_records(
            self.manifest,
            self.bundle,
            calls,
            events,
            required_execution_unit_ids={"J-SEQ-02"},
            scorecard_rows=scorecard,
        )
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(expected, result.authoritative_run_ids_by_scored_unit)


if __name__ == "__main__":
    unittest.main()
