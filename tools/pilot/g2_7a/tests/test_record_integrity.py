from __future__ import annotations

import copy
import unittest

import test_run_records as fixtures
import runner
import validate_run_records as validator
from transport import FakeTransport, TransportError


class RecordIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixtures.RunRecordValidatorTests.setUpClass()
        cls.helper = fixtures.RunRecordValidatorTests()

    def corpus(self, retry_unit: str | None = None):
        calls, events = [], []
        for unit in self.helper.manifest["execution_units"]:
            unit_id = unit["execution_unit_id"]
            rows, terminal = self.helper.completed_attempt(
                unit_id, attempt=2 if unit_id == retry_unit else 1
            )
            calls.extend(rows)
            events.extend(terminal)
        return calls, events

    def failed_prefix(self, count: int = 2):
        calls, events = self.helper.completed_attempt("P-SEQ-02")
        calls = calls[:count]
        for row in calls:
            row["authoritative_attempt"] = False
        calls[-1].update(
            final_patient_response=None,
            execution_error_class="TIMEOUT",
            execution_error_message_safe="safe timeout",
            provider_completion_status="execution_error",
        )
        events[0].update(
            authoritative_attempt=False,
            event_type="ATTEMPT_FAILED",
            execution_error_class="TIMEOUT",
            execution_error_message_safe="safe timeout",
        )
        return calls, events

    def validate(self, calls, events):
        return validator.validate_records(
            self.helper.manifest, self.helper.bundle, calls, events
        )

    def assert_rejected(self, calls, events, code):
        result = self.validate(calls, events)
        self.assertFalse(result.ok)
        self.assertIn(code, result.errors)
        self.assertEqual({}, result.authoritative_run_ids_by_scored_unit)

    def test_full_corpus_and_empty_success_pass(self):
        calls, events = self.corpus()
        self.assertTrue(all(row["final_patient_response"] == "" for row in calls))
        result = self.validate(calls, events)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(58, len(result.authoritative_run_ids_by_scored_unit))
        self.assertEqual(6, len(result.authoritative_run_ids_by_scored_unit["P29"]))

    def test_exact_prior_audit_f1_null_sessions_rejected(self):
        calls, events = self.corpus()
        for row in calls + events:
            row["safe_session_id"] = None
        self.assert_rejected(calls, events, "RUN_SAFE_SESSION_ID_INVALID")

    def test_missing_null_or_unsafe_call_and_event_ids_rejected(self):
        for collection in ("calls", "events"):
            for mutation in ("missing", None, "", "https://invalid.example/session", [], {}):
                with self.subTest(collection=collection, mutation=mutation):
                    calls, events = self.corpus()
                    row = (calls if collection == "calls" else events)[0]
                    if mutation == "missing":
                        row.pop("safe_session_id")
                    else:
                        row["safe_session_id"] = mutation
                    self.assert_rejected(calls, events, "RUN_SAFE_SESSION_ID_INVALID")

    def test_mismatched_session_id_rejected(self):
        calls, events = self.corpus()
        events[0]["safe_session_id"] = "different-session"
        self.assert_rejected(calls, events, "RUN_MULTIPLE_SESSIONS_IN_ATTEMPT")

    def test_genuine_creation_failure_then_success_passes(self):
        calls, events = self.corpus("P-SEQ-02")
        _, creation = self.failed_prefix()
        creation[0].update(
            event_type="SESSION_CREATION_FAILED", safe_session_id=None,
            model_call_created=False,
        )
        result = self.validate(calls, creation + events)
        self.assertTrue(result.ok, result.errors)
        for mutation in ("missing", "existing-session"):
            corrupted = copy.deepcopy(creation)
            if mutation == "missing":
                corrupted[0].pop("safe_session_id")
            else:
                corrupted[0]["safe_session_id"] = mutation
            self.assert_rejected(calls, corrupted + events, "RUN_SAFE_SESSION_ID_INVALID")

    def test_creation_failure_with_calls_rejected(self):
        calls, events = self.corpus("P-SEQ-02")
        failed, terminal = self.failed_prefix()
        terminal[0].update(event_type="SESSION_CREATION_FAILED", safe_session_id=None)
        self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_EVENT_INVALID")

    def test_exact_prior_audit_f2_authoritative_error_rejected(self):
        calls, events = self.corpus()
        calls[0].update(
            final_patient_response=None, execution_error_class="TIMEOUT",
            execution_error_message_safe="safe timeout",
            provider_completion_status="execution_error",
        )
        self.assert_rejected(calls, events, "RUN_AUTHORITATIVE_ATTEMPT_INCOMPLETE")

    def test_success_error_field_and_completion_contradictions_rejected(self):
        for patch in (
            {"execution_error_class": "TIMEOUT"},
            {"execution_error_message_safe": "safe timeout"},
            {"provider_completion_status": "execution_error"},
            {"provider_completion_status": None},
            {"provider_completion_status": ""},
            {"provider_completion_status": False},
            {"final_patient_response": None},
        ):
            with self.subTest(patch=patch):
                calls, events = self.corpus()
                calls[0].update(patch)
                self.assert_rejected(calls, events, "RUN_AUTHORITATIVE_ATTEMPT_INCOMPLETE")

    def test_success_terminal_event_contradictions_rejected(self):
        for patch in (
            {"execution_error_class": "TIMEOUT"},
            {"execution_error_message_safe": "safe timeout"},
            {"authoritative_attempt": False},
            {"event_type": "ATTEMPT_FAILED"},
            {"event_type": "SESSION_CLOSE_FAILED"},
            {"model_call_created": False},
        ):
            with self.subTest(patch=patch):
                calls, events = self.corpus()
                events[0].update(patch)
                self.assert_rejected(calls, events, "RUN_ATTEMPT_EVENT_INVALID")

    def test_valid_partial_failed_prefix_then_success_passes(self):
        calls, events = self.corpus("P-SEQ-02")
        failed, terminal = self.failed_prefix()
        before = copy.deepcopy(failed)
        result = self.validate(failed + calls, terminal + events)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(before, failed)
        self.assertTrue(all("-2-" in run_id for run_id in result.authoritative_run_ids_by_scored_unit["P15"]))

    def test_failed_attempt_reversed_prefix_rejected(self):
        calls, events = self.corpus("P-SEQ-02")
        failed, terminal = self.failed_prefix(3)
        failed[0], failed[1] = failed[1], failed[0]
        self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_CALL_PREFIX_INVALID")

    def test_failed_attempt_duplicate_call_rejected(self):
        calls, events = self.corpus("P-SEQ-02")
        failed, terminal = self.failed_prefix(3)
        failed.insert(1, dict(failed[0], run_id="run-duplicate-setup"))
        self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_CALL_PREFIX_INVALID")

    def test_failed_attempt_skipped_call_rejected(self):
        calls, events = self.corpus("P-SEQ-02")
        failed, terminal = self.failed_prefix(3)
        failed.pop(1)
        self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_CALL_PREFIX_INVALID")

    def test_failed_attempt_unknown_or_extra_call_rejected(self):
        for call_id in ("CALL-NOT-PLANNED", "CALL-J01"):
            with self.subTest(call_id=call_id):
                calls, events = self.corpus("P-SEQ-02")
                failed, terminal = self.failed_prefix()
                extra = dict(failed[0], planned_call_id=call_id, run_id="run-extra-call")
                failed.insert(1, extra)
                self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_CALL_PREFIX_INVALID")

    def test_retry_after_success_rejected(self):
        calls, events = self.corpus()
        failed, terminal = self.failed_prefix()
        for row in failed + terminal:
            row.update(unit_attempt_index=2, safe_session_id="session-extra-retry")
        for row in failed:
            row["run_id"] += "-extra"
        self.assert_rejected(calls + failed, events + terminal, "RUN_RETRY_AFTER_COMPLETION")

    def test_failed_event_without_failed_call_rejected(self):
        calls, events = self.corpus("P-SEQ-02")
        failed, terminal = self.failed_prefix()
        failed[-1].update(
            execution_error_class=None, execution_error_message_safe=None,
            final_patient_response="", provider_completion_status="completed",
        )
        self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_TERMINAL_CALL_CONTRADICTION")

    def test_failed_call_before_last_or_mismatched_error_event_rejected(self):
        for mutation in ("earlier_error", "event_error"):
            with self.subTest(mutation=mutation):
                calls, events = self.corpus("P-SEQ-02")
                failed, terminal = self.failed_prefix(3)
                if mutation == "earlier_error":
                    for field in ("execution_error_class", "execution_error_message_safe", "final_patient_response", "provider_completion_status"):
                        failed[0][field] = failed[-1][field]
                else:
                    terminal[0]["execution_error_class"] = "DIFFERENT_FAILURE"
                self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_TERMINAL_CALL_CONTRADICTION")

    def test_close_failure_does_not_certify_isolation(self):
        calls, events = self.corpus("P-SEQ-02")
        failed, terminal = self.helper.completed_attempt("P-SEQ-02")
        for row in failed:
            row.update(authoritative_attempt=False, physical_isolation_verified=False)
        terminal[0].update(
            authoritative_attempt=False, event_type="SESSION_CLOSE_FAILED",
            execution_error_class="CLOSE_FAILED", execution_error_message_safe="safe close failure",
        )
        result = self.validate(failed + calls, terminal + events)
        self.assertTrue(result.ok, result.errors)
        failed[0]["physical_isolation_verified"] = True
        self.assert_rejected(failed + calls, terminal + events, "RUN_ATTEMPT_TERMINAL_CALL_CONTRADICTION")

    def test_partial_success_cannot_be_claimed_as_close_failure(self):
        calls, events = self.corpus("P-SEQ-02")
        partial, terminal = self.helper.completed_attempt("P-SEQ-02")
        partial = partial[:1]
        partial[0].update(authoritative_attempt=False, physical_isolation_verified=False)
        terminal[0].update(
            authoritative_attempt=False, event_type="SESSION_CLOSE_FAILED",
            execution_error_class="CLOSE_FAILED", execution_error_message_safe="safe close failure",
        )
        self.assert_rejected(partial + calls, terminal + events, "RUN_ATTEMPT_TERMINAL_CALL_CONTRADICTION")

    def test_fake_runner_lifecycle_outputs_validate(self):
        variants = (
            {"create_session_outcomes": [TransportError("CREATE_FAILED", "safe create failure")]},
            {"close_outcomes": [TransportError("CLOSE_FAILED", "safe close failure")]},
            {"scripted_outcomes": ["first", TransportError("TIMEOUT", "safe timeout")]},
            {"scripted_outcomes": ["", "refusal or poor content", "  final preserved  "]},
        )
        for options in variants:
            with self.subTest(options=tuple(options)):
                calls, events = self.corpus()
                calls = [row for row in calls if row["execution_unit_id"] != "P-SEQ-02"]
                events = [row for row in events if row["execution_unit_id"] != "P-SEQ-02"]
                unit = self.helper.unit_by_id["P-SEQ-02"]
                planned = [self.helper.call_by_id[call_id] for call_id in unit["planned_call_ids"]]
                system = (fixtures.ROOT / "docs/pilot/g2.7a/fixtures/palpitations-system-message-v1.txt").read_text(encoding="utf-8")
                result = runner.run_execution_unit(
                    unit, planned, system, FakeTransport(**options), self.helper.bundle["input_bundle_id"],
                    physical_isolation_verified=True,
                    run_id_factory=lambda unit_id, attempt, turn: f"audit-{unit_id}-{attempt}-{turn}",
                    timestamp_factory=lambda: "2026-09-05T00:00:00Z",
                )
                validated = self.validate(calls + result.attempted_call_records, events + result.attempt_events)
                self.assertTrue(validated.ok, validated.errors)


if __name__ == "__main__":
    unittest.main()
