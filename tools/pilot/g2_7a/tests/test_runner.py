from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MODULE_DIR = ROOT / "tools/pilot/g2_7a"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import runner
from transport import FakeTransport, TransportError


def planned_call(call_id: str, turn_index: int, utterance: str) -> dict[str, object]:
    return {
        "case": "jaundice",
        "constituent_or_setup_id": None,
        "execution_unit_id": "TEST-SEQ",
        "learner_utterance": utterance,
        "planned_call_id": call_id,
        "scored_turn": True,
        "scored_unit_id": f"J{turn_index:02d}",
        "source_trajectory_id": f"J{turn_index:02d}",
        "turn_index": turn_index,
    }


def execution_unit(call_ids: list[str]) -> dict[str, object]:
    return {
        "execution_unit_id": "TEST-SEQ",
        "planned_call_ids": call_ids,
    }


def deterministic_run_id(unit: str, attempt: int, turn: int) -> str:
    return f"run-{unit}-{attempt}-{turn}"


class FakeTransportTests(unittest.TestCase):
    def test_same_session_memory(self) -> None:
        nonce = "CPX-G2-ISO-0123456789abcdef0123456789abcdef"
        transport = FakeTransport()
        session = transport.create_session("neutral", runner.RUNTIME)
        first = session.send(f"식별 문자열: {nonce}")
        second = session.send("직전 메시지 식별 문자열을 말하세요")
        session.close()
        self.assertEqual("기억했습니다.", first.final_response)
        self.assertEqual(nonce, second.final_response)

    def test_cross_session_isolation(self) -> None:
        nonce = "CPX-G2-ISO-fedcba9876543210fedcba9876543210"
        transport = FakeTransport()
        session_a = transport.create_session("neutral", runner.RUNTIME)
        session_a.send(f"식별 문자열: {nonce}")
        session_a.close()
        session_b = transport.create_session("neutral", runner.RUNTIME)
        response = session_b.send("별도 세션 식별 문자열을 말하세요")
        session_b.close()
        self.assertNotIn(nonce, response.final_response)
        self.assertEqual("모름", response.final_response)

    def test_full_unit_retry_restarts_sequence(self) -> None:
        calls = [planned_call("CALL-1", 1, "turn one"), planned_call("CALL-2", 2, "turn two")]
        transport = FakeTransport(
            scripted_outcomes=[
                "first partial",
                TransportError("TIMEOUT", "safe timeout"),
                "retry first",
                "retry second",
            ]
        )
        records = runner.run_execution_unit(
            execution_unit(["CALL-1", "CALL-2"]),
            calls,
            "system",
            transport,
            "sha256:test",
            physical_isolation_verified=True,
            run_id_factory=deterministic_run_id,
            timestamp_factory=lambda: "2026-09-03T00:00:00Z",
        )
        self.assertEqual(4, len(records))
        self.assertEqual(2, len(transport.created_session_ids))
        self.assertEqual(["turn one", "turn two", "turn one", "turn two"], [call.user_message for call in transport.calls])
        self.assertFalse(records[0]["authoritative_attempt"])
        self.assertFalse(records[1]["authoritative_attempt"])
        self.assertTrue(records[2]["authoritative_attempt"])
        self.assertTrue(records[3]["authoritative_attempt"])

    def test_three_attempt_cap(self) -> None:
        calls = [planned_call("CALL-1", 1, "turn one")]
        transport = FakeTransport(
            scripted_outcomes=[
                TransportError("TIMEOUT", "one"),
                TransportError("TIMEOUT", "two"),
                TransportError("TIMEOUT", "three"),
                "must not be consumed",
            ]
        )
        records = runner.run_execution_unit(
            execution_unit(["CALL-1"]),
            calls,
            "system",
            transport,
            "sha256:test",
            physical_isolation_verified=True,
            run_id_factory=deterministic_run_id,
            timestamp_factory=lambda: "2026-09-03T00:00:00Z",
        )
        self.assertEqual(3, len(records))
        self.assertEqual(3, len(transport.created_session_ids))
        self.assertTrue(all(not record["authoritative_attempt"] for record in records))

    def test_valid_poor_response_is_not_retried(self) -> None:
        calls = [planned_call("CALL-1", 1, "turn one")]
        transport = FakeTransport(scripted_outcomes=["I AM A DOCTOR", "unused"])
        records = runner.run_execution_unit(
            execution_unit(["CALL-1"]),
            calls,
            "system",
            transport,
            "sha256:test",
            physical_isolation_verified=True,
            run_id_factory=deterministic_run_id,
            timestamp_factory=lambda: "2026-09-03T00:00:00Z",
        )
        self.assertEqual(1, len(records))
        self.assertEqual(1, len(transport.created_session_ids))
        self.assertEqual("I AM A DOCTOR", records[0]["final_patient_response"])
        self.assertTrue(records[0]["authoritative_attempt"])

    def test_successful_empty_response_is_valid_output(self) -> None:
        calls = [planned_call("CALL-1", 1, "turn one")]
        transport = FakeTransport(scripted_outcomes=[""])
        records = runner.run_execution_unit(
            execution_unit(["CALL-1"]),
            calls,
            "system",
            transport,
            "sha256:test",
            physical_isolation_verified=True,
            run_id_factory=deterministic_run_id,
            timestamp_factory=lambda: "2026-09-03T00:00:00Z",
        )
        self.assertEqual("", records[0]["final_patient_response"])
        self.assertIsNone(records[0]["execution_error_class"])
        self.assertTrue(records[0]["authoritative_attempt"])

    def test_final_response_preserved_without_stripping(self) -> None:
        raw = "  analysis-like text\nFINAL: patient words  \n"
        calls = [planned_call("CALL-1", 1, "turn one")]
        transport = FakeTransport(scripted_outcomes=[raw])
        records = runner.run_execution_unit(
            execution_unit(["CALL-1"]),
            calls,
            "system",
            transport,
            "sha256:test",
            physical_isolation_verified=True,
            run_id_factory=deterministic_run_id,
            timestamp_factory=lambda: "2026-09-03T00:00:00Z",
        )
        self.assertEqual(raw, records[0]["final_patient_response"])

    def test_raw_record_contains_required_fields(self) -> None:
        calls = [planned_call("CALL-1", 1, "turn one")]
        transport = FakeTransport(scripted_outcomes=["patient response"])
        records = runner.run_execution_unit(
            execution_unit(["CALL-1"]),
            calls,
            "system",
            transport,
            "sha256:test",
            physical_isolation_verified=True,
            run_id_factory=deterministic_run_id,
            timestamp_factory=lambda: "2026-09-03T00:00:00Z",
        )
        required = {
            "run_id", "execution_unit_id", "unit_attempt_index", "scored_unit_id",
            "source_trajectory_id", "constituent_or_setup_id", "turn_index",
            "scored_turn", "authoritative_attempt", "case", "safe_session_id",
            "physical_isolation_verified", "model", "runtime",
            "exposed_generation_settings", "input_bundle_id", "system_message_sha256",
            "learner_utterance", "final_patient_response", "provider_completion_status",
            "separate_reasoning_field_present", "execution_error_class",
            "execution_error_message_safe", "timestamp_utc",
        }
        self.assertEqual(required, set(records[0]))

    def test_p29_six_calls_in_one_fake_session(self) -> None:
        calls = [planned_call(f"CALL-P29-U{i:02d}", i, f"turn {i}") for i in range(1, 7)]
        transport = FakeTransport(scripted_outcomes=[f"response {i}" for i in range(1, 7)])
        records = runner.run_execution_unit(
            execution_unit([call["planned_call_id"] for call in calls]),
            calls,
            "system",
            transport,
            "sha256:test",
            physical_isolation_verified=True,
            run_id_factory=deterministic_run_id,
            timestamp_factory=lambda: "2026-09-03T00:00:00Z",
        )
        self.assertEqual(6, len(records))
        self.assertEqual(1, len(transport.created_session_ids))
        self.assertEqual(1, len({record["safe_session_id"] for record in records}))


class AuthorizationTests(unittest.TestCase):
    def test_preflight_refusal(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = runner.main(["preflight"])
        self.assertEqual(3, result)
        self.assertEqual(runner.PREFLIGHT_REFUSAL, stream.getvalue().strip())

    def test_execute_refusal(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = runner.main(["execute"])
        self.assertEqual(3, result)
        self.assertEqual(runner.EXECUTION_REFUSAL, stream.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
