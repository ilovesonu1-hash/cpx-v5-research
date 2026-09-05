#!/usr/bin/env python3
"""Offline validator for future G2.7a raw-call and attempt-event JSONL.

PILOT_ONLY / NON_PRODUCTION. This module performs no network, provider, or
model call and does not score patient responses.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
TERMINAL_EVENT_TYPES = {
    "SESSION_CREATION_FAILED",
    "ATTEMPT_FAILED",
    "SESSION_CLOSE_FAILED",
    "ATTEMPT_COMPLETED",
}
REQUIRED_CALL_FIELDS = {
    "authoritative_attempt",
    "case",
    "constituent_or_setup_id",
    "execution_error_class",
    "execution_error_message_safe",
    "execution_unit_id",
    "exposed_generation_settings",
    "final_patient_response",
    "input_bundle_id",
    "learner_utterance",
    "model",
    "physical_isolation_verified",
    "planned_call_id",
    "provider_completion_status",
    "run_id",
    "runtime",
    "safe_session_id",
    "scored_turn",
    "scored_unit_id",
    "separate_reasoning_field_present",
    "source_trajectory_id",
    "system_message_sha256",
    "timestamp_utc",
    "turn_index",
    "unit_attempt_index",
}
REQUIRED_EVENT_FIELDS = {
    "authoritative_attempt",
    "event_type",
    "execution_error_class",
    "execution_error_message_safe",
    "execution_unit_id",
    "input_bundle_id",
    "model_call_created",
    "safe_session_id",
    "timestamp_utc",
    "unit_attempt_index",
}


@dataclass
class RunRecordValidationResult:
    checks_passed: int = 0
    errors: list[str] = field(default_factory=list)
    authoritative_run_ids_by_scored_unit: dict[str, list[str]] = field(default_factory=dict)

    def check(self, condition: bool, code: str) -> None:
        if condition:
            self.checks_passed += 1
        else:
            self.errors.append(code)

    @property
    def ok(self) -> bool:
        return not self.errors


def _safe_identifier(value: object) -> bool:
    return isinstance(value, str) and SAFE_IDENTIFIER.fullmatch(value) is not None


def _attempt_key(row: Mapping[str, Any]) -> tuple[str, int] | None:
    unit = row.get("execution_unit_id")
    attempt = row.get("unit_attempt_index")
    if not isinstance(unit, str) or type(attempt) is not int:
        return None
    return unit, attempt


def _system_hash_for_case(bundle: Mapping[str, Any], case: str) -> str | None:
    suffix = f"/{case}-system-message-v1.txt"
    messages = bundle.get("identities", {}).get("system_messages", {})
    return next((value for path, value in messages.items() if path.endswith(suffix)), None)


def _successful_call(record: Mapping[str, Any]) -> bool:
    status = record.get("provider_completion_status")
    return (
        record.get("execution_error_class") is None
        and record.get("execution_error_message_safe") is None
        and isinstance(record.get("final_patient_response"), str)
        and isinstance(status, str)
        and bool(status)
        and status != "execution_error"
    )


def _failed_call(record: Mapping[str, Any]) -> bool:
    return (
        isinstance(record.get("execution_error_class"), str)
        and bool(record.get("execution_error_class"))
        and isinstance(record.get("execution_error_message_safe"), str)
        and record.get("final_patient_response") is None
        and record.get("provider_completion_status") == "execution_error"
    )


def validate_records(
    manifest: Mapping[str, Any],
    bundle: Mapping[str, Any],
    call_records: Sequence[Mapping[str, Any]],
    attempt_events: Sequence[Mapping[str, Any]],
    *,
    preflight_session_ids: Iterable[str] = (),
    required_execution_unit_ids: Iterable[str] | None = None,
    scorecard_rows: Sequence[Mapping[str, str]] | None = None,
) -> RunRecordValidationResult:
    """Validate record/session topology and derive ordered score evidence IDs."""

    result = RunRecordValidationResult()
    unit_by_id = {
        unit["execution_unit_id"]: unit for unit in manifest.get("execution_units", [])
    }
    call_by_id = {
        call["planned_call_id"]: call for call in manifest.get("planned_calls", [])
    }
    scored_by_id = {
        scored["scored_unit_id"]: scored for scored in manifest.get("scored_units", [])
    }
    required_units = (
        set(unit_by_id)
        if required_execution_unit_ids is None
        else set(required_execution_unit_ids)
    )
    result.check(required_units <= set(unit_by_id), "RUN_REQUIRED_UNIT_UNKNOWN")
    input_bundle_id = bundle.get("input_bundle_id")

    all_rows: list[Mapping[str, Any]] = [*call_records, *attempt_events]
    keys = [_attempt_key(row) for row in all_rows]
    result.check(all(key is not None for key in keys), "RUN_ATTEMPT_KEY_INVALID")
    concrete_keys = [key for key in keys if key is not None]
    result.check(
        all(unit in unit_by_id for unit, _ in concrete_keys),
        "RUN_EXECUTION_UNIT_UNKNOWN",
    )
    result.check(
        all(1 <= attempt <= 3 for _, attempt in concrete_keys),
        "RUN_ATTEMPT_INDEX_INVALID",
    )
    result.check(
        all(row.get("input_bundle_id") == input_bundle_id for row in all_rows),
        "RUN_INPUT_BUNDLE_ID_MISMATCH",
    )
    if not result.ok:
        return result

    events_by_attempt: dict[tuple[str, int], list[Mapping[str, Any]]] = {}
    calls_by_attempt: dict[tuple[str, int], list[Mapping[str, Any]]] = {}
    for event in attempt_events:
        key = _attempt_key(event)
        if key is not None:
            events_by_attempt.setdefault(key, []).append(event)
    for record in call_records:
        key = _attempt_key(record)
        if key is not None:
            calls_by_attempt.setdefault(key, []).append(record)

    attempt_keys = set(events_by_attempt) | set(calls_by_attempt)
    result.check(
        all(len(events_by_attempt.get(key, [])) == 1 for key in attempt_keys),
        "RUN_ATTEMPT_TERMINAL_EVENT_COUNT",
    )
    result.check(
        all(
            isinstance(events[0].get("event_type"), str)
            and events[0]["event_type"] in TERMINAL_EVENT_TYPES
            for events in events_by_attempt.values()
            if len(events) == 1
        ),
        "RUN_ATTEMPT_EVENT_TYPE_INVALID",
    )

    sessions_by_attempt: dict[tuple[str, int], set[str]] = {}
    safe_ids_valid = all(_safe_identifier(row.get("safe_session_id")) for row in call_records)
    for event in attempt_events:
        if event.get("event_type") == "SESSION_CREATION_FAILED":
            valid = "safe_session_id" in event and event["safe_session_id"] is None
        else:
            valid = _safe_identifier(event.get("safe_session_id"))
        safe_ids_valid = safe_ids_valid and valid
    for row in all_rows:
        key = _attempt_key(row)
        session_id = row.get("safe_session_id")
        if not _safe_identifier(session_id) or key is None:
            continue
        sessions_by_attempt.setdefault(key, set()).add(session_id)
    result.check(safe_ids_valid, "RUN_SAFE_SESSION_ID_INVALID")
    result.check(
        all(len(session_ids) <= 1 for session_ids in sessions_by_attempt.values()),
        "RUN_MULTIPLE_SESSIONS_IN_ATTEMPT",
    )
    session_owner: dict[str, tuple[str, int]] = {}
    session_reuse = False
    for key, session_ids in sessions_by_attempt.items():
        for session_id in session_ids:
            previous = session_owner.setdefault(session_id, key)
            if previous != key:
                session_reuse = True
    result.check(not session_reuse, "RUN_SESSION_REUSED_ACROSS_ATTEMPTS")
    result.check(
        set(session_owner).isdisjoint(set(preflight_session_ids)),
        "RUN_PREFLIGHT_SESSION_OVERLAP",
    )

    events_well_formed = True
    for key, events in events_by_attempt.items():
        if len(events) != 1:
            continue
        event = events[0]
        events_well_formed = events_well_formed and REQUIRED_EVENT_FIELDS <= set(event)
        event_type = event.get("event_type")
        attempt_calls = calls_by_attempt.get(key, [])
        events_well_formed = events_well_formed and (
            event.get("model_call_created") is bool(attempt_calls)
        )
        if event_type == "SESSION_CREATION_FAILED":
            events_well_formed = events_well_formed and not attempt_calls
            events_well_formed = events_well_formed and event.get("safe_session_id") is None
        if event_type == "ATTEMPT_COMPLETED":
            events_well_formed = events_well_formed and event.get("authoritative_attempt") is True
            events_well_formed = events_well_formed and event.get("execution_error_class") is None
            events_well_formed = events_well_formed and event.get("execution_error_message_safe") is None
        else:
            events_well_formed = events_well_formed and event.get("authoritative_attempt") is False
            events_well_formed = events_well_formed and isinstance(
                event.get("execution_error_class"), str
            )
            events_well_formed = events_well_formed and isinstance(
                event.get("execution_error_message_safe"), str
            )
    result.check(events_well_formed, "RUN_ATTEMPT_EVENT_INVALID")

    attempt_indices_by_unit: dict[str, set[int]] = {}
    for unit, attempt in attempt_keys:
        attempt_indices_by_unit.setdefault(unit, set()).add(attempt)
    result.check(
        all(
            sorted(indices) == list(range(1, max(indices) + 1))
            for indices in attempt_indices_by_unit.values()
            if indices
        ),
        "RUN_ATTEMPT_SEQUENCE_INVALID",
    )

    record_shape_valid = True
    seen_run_ids: set[str] = set()
    duplicate_run_id = False
    unknown_call = False
    plan_mismatch = False
    nullability_invalid = False
    for record in call_records:
        record_shape_valid = record_shape_valid and REQUIRED_CALL_FIELDS <= set(record)
        record_shape_valid = record_shape_valid and record.get("runtime") == manifest.get("runtime")
        record_shape_valid = record_shape_valid and isinstance(record.get("model"), str)
        record_shape_valid = record_shape_valid and isinstance(
            record.get("separate_reasoning_field_present"), bool
        )
        run_id = record.get("run_id")
        record_shape_valid = record_shape_valid and _safe_identifier(run_id)
        if isinstance(run_id, str):
            if run_id in seen_run_ids:
                duplicate_run_id = True
            seen_run_ids.add(run_id)
        planned_id = record.get("planned_call_id")
        planned = call_by_id.get(planned_id) if isinstance(planned_id, str) else None
        if planned is None:
            unknown_call = True
            continue
        for field in (
            "execution_unit_id",
            "turn_index",
            "case",
            "learner_utterance",
            "scored_turn",
            "scored_unit_id",
            "source_trajectory_id",
            "constituent_or_setup_id",
        ):
            if record.get(field) != planned.get(field):
                plan_mismatch = True
        if record.get("system_message_sha256") != _system_hash_for_case(
            bundle, str(record.get("case"))
        ):
            plan_mismatch = True
        if not (_successful_call(record) or _failed_call(record)):
            nullability_invalid = True
    result.check(record_shape_valid and not duplicate_run_id, "RUN_ID_INVALID_OR_DUPLICATE")
    result.check(not unknown_call, "RUN_PLANNED_CALL_UNKNOWN")
    result.check(not plan_mismatch, "RUN_PLANNED_CALL_MISMATCH")
    result.check(not nullability_invalid, "RUN_RECORD_NULLABILITY_INVALID")

    prefixes_valid = True
    terminal_calls_coherent = True
    retry_termination_valid = True
    for key in attempt_keys:
        unit_id, attempt_index = key
        attempt_calls = calls_by_attempt.get(key, [])
        planned_ids = unit_by_id[unit_id]["planned_call_ids"]
        actual_ids = [record.get("planned_call_id") for record in attempt_calls]
        prefixes_valid = prefixes_valid and (
            len(actual_ids) <= len(planned_ids)
            and actual_ids == planned_ids[:len(actual_ids)]
        )
        events = events_by_attempt.get(key, [])
        if len(events) != 1:
            terminal_calls_coherent = False
            continue
        event = events[0]
        event_type = event.get("event_type")
        valid = all(_successful_call(record) for record in attempt_calls[:-1])
        if event_type == "ATTEMPT_COMPLETED":
            valid = valid and actual_ids == planned_ids and all(
                _successful_call(record)
                and record.get("authoritative_attempt") is True
                and record.get("physical_isolation_verified") is True
                for record in attempt_calls
            )
            retry_termination_valid = retry_termination_valid and (
                attempt_index == max(attempt_indices_by_unit[unit_id])
            )
        else:
            valid = valid and all(
                record.get("authoritative_attempt") is False for record in attempt_calls
            )
            if event_type == "SESSION_CREATION_FAILED":
                valid = valid and not attempt_calls
            elif event_type == "ATTEMPT_FAILED":
                valid = valid and bool(attempt_calls) and _failed_call(attempt_calls[-1])
                if attempt_calls:
                    valid = valid and all(
                        event.get(field) == attempt_calls[-1].get(field)
                        for field in ("execution_error_class", "execution_error_message_safe")
                    )
            elif event_type == "SESSION_CLOSE_FAILED":
                valid = valid and all(
                    record.get("physical_isolation_verified") is False
                    for record in attempt_calls
                )
                if attempt_calls:
                    valid = valid and (
                        _successful_call(attempt_calls[-1]) or _failed_call(attempt_calls[-1])
                    )
                if len(attempt_calls) < len(planned_ids):
                    valid = valid and bool(attempt_calls) and _failed_call(attempt_calls[-1])
            else:
                valid = False
        terminal_calls_coherent = terminal_calls_coherent and valid
    result.check(prefixes_valid, "RUN_ATTEMPT_CALL_PREFIX_INVALID")
    result.check(terminal_calls_coherent, "RUN_ATTEMPT_TERMINAL_CALL_CONTRADICTION")
    result.check(retry_termination_valid, "RUN_RETRY_AFTER_COMPLETION")

    authoritative_event_by_unit: dict[str, list[tuple[int, Mapping[str, Any]]]] = {}
    for (unit, attempt), events in events_by_attempt.items():
        if len(events) == 1 and events[0].get("authoritative_attempt") is True:
            authoritative_event_by_unit.setdefault(unit, []).append((attempt, events[0]))
    result.check(
        all(len(authoritative_event_by_unit.get(unit, [])) == 1 for unit in required_units),
        "RUN_AUTHORITATIVE_ATTEMPT_COUNT",
    )

    authoritative_call_by_unit_and_plan: dict[tuple[str, str], Mapping[str, Any]] = {}
    authoritative_complete = True
    partial_nonauthoritative = True
    for unit_id in required_units:
        authoritative_events = authoritative_event_by_unit.get(unit_id, [])
        if len(authoritative_events) != 1:
            authoritative_complete = False
            continue
        attempt_index, event = authoritative_events[0]
        if event.get("event_type") != "ATTEMPT_COMPLETED":
            authoritative_complete = False
        attempt_calls = calls_by_attempt.get((unit_id, attempt_index), [])
        expected_call_ids = unit_by_id[unit_id]["planned_call_ids"]
        actual_call_ids = [record.get("planned_call_id") for record in attempt_calls]
        if actual_call_ids != expected_call_ids:
            authoritative_complete = False
        if not all(record.get("authoritative_attempt") is True for record in attempt_calls):
            authoritative_complete = False
        if not all(record.get("physical_isolation_verified") is True for record in attempt_calls):
            authoritative_complete = False
        if not all(_successful_call(record) for record in attempt_calls):
            authoritative_complete = False
        for record in attempt_calls:
            planned_id = record.get("planned_call_id")
            if isinstance(planned_id, str):
                authoritative_call_by_unit_and_plan[(unit_id, planned_id)] = record
        for (other_unit, other_attempt), other_calls in calls_by_attempt.items():
            if other_unit == unit_id and other_attempt != attempt_index:
                partial_nonauthoritative = partial_nonauthoritative and all(
                    record.get("authoritative_attempt") is False for record in other_calls
                )
    result.check(authoritative_complete, "RUN_AUTHORITATIVE_ATTEMPT_INCOMPLETE")
    result.check(partial_nonauthoritative, "RUN_PARTIAL_ATTEMPT_MARKED_AUTHORITATIVE")

    for scored_id, scored in scored_by_id.items():
        unit_id = scored["execution_unit_id"]
        if unit_id not in required_units:
            continue
        run_ids: list[str] = []
        derivable = True
        for planned_id in scored["planned_evidence_call_ids"]:
            record = authoritative_call_by_unit_and_plan.get((unit_id, planned_id))
            if record is None or not isinstance(record.get("run_id"), str):
                derivable = False
                break
            run_ids.append(record["run_id"])
        if derivable:
            result.authoritative_run_ids_by_scored_unit[scored_id] = run_ids
    expected_scored = {
        scored_id
        for scored_id, scored in scored_by_id.items()
        if scored["execution_unit_id"] in required_units
    }
    result.check(
        set(result.authoritative_run_ids_by_scored_unit) == expected_scored,
        "RUN_SCORECARD_EVIDENCE_NOT_DERIVABLE",
    )
    if scorecard_rows is not None:
        row_by_id = {row.get("scored_unit_id", ""): row for row in scorecard_rows}
        mapping_matches = True
        for scored_id in expected_scored:
            encoded = row_by_id.get(scored_id, {}).get("authoritative_run_ids", "")
            try:
                mapping_matches = mapping_matches and json.loads(encoded) == result.authoritative_run_ids_by_scored_unit.get(scored_id)
            except (json.JSONDecodeError, TypeError):
                mapping_matches = False
        result.check(mapping_matches, "RUN_SCORECARD_EVIDENCE_MAPPING_MISMATCH")

    p29 = result.authoritative_run_ids_by_scored_unit.get("P29")
    if "P29-STATION-01" in required_units:
        result.check(p29 is not None and len(p29) == 6, "RUN_P29_EVIDENCE_COUNT")
    if "P-SEQ-02" in required_units:
        p14_calls = scored_by_id["P14"]["planned_evidence_call_ids"]
        p15_calls = scored_by_id["P15"]["planned_evidence_call_ids"]
        result.check(
            p14_calls == ["CALL-P-SETUP-DURATION-01", "CALL-P14"]
            and p15_calls == ["CALL-P-SETUP-DURATION-01", "CALL-P14", "CALL-P15"]
            and call_by_id["CALL-P-SETUP-DURATION-01"]["scored_turn"] is False,
            "RUN_P14_P15_SETUP_INVALID",
        )
    if not result.ok:
        result.authoritative_run_ids_by_scored_unit.clear()
    return result


def _load_jsonl(path: Path) -> list[Mapping[str, Any]]:
    rows: list[Mapping[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"JSONL line {number} is not an object")
        rows.append(value)
    return rows


def _load_scorecard(path: Path) -> list[Mapping[str, str]]:
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call-records", type=Path, required=True)
    parser.add_argument("--attempt-events", type=Path, required=True)
    parser.add_argument("--preflight-evidence", type=Path)
    parser.add_argument("--scorecard", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[3])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.repository_root.resolve()
    manifest = json.loads(
        (root / "docs/pilot/g2.7a/manifests/execution-manifest-v1.json").read_text(encoding="utf-8")
    )
    bundle = json.loads(
        (root / "docs/pilot/g2.7a/manifests/input-bundle-v1.json").read_text(encoding="utf-8")
    )
    preflight_ids: list[str] = []
    if args.preflight_evidence:
        evidence = json.loads(args.preflight_evidence.read_text(encoding="utf-8"))
        preflight_ids = list(evidence.get("safe_session_ids", []))
    scorecard = _load_scorecard(args.scorecard) if args.scorecard else None
    result = validate_records(
        manifest,
        bundle,
        _load_jsonl(args.call_records),
        _load_jsonl(args.attempt_events),
        preflight_session_ids=preflight_ids,
        scorecard_rows=scorecard,
    )
    summary = {
        "checks_passed": result.checks_passed,
        "errors": result.errors,
        "status": "PASS" if result.ok else "FAIL",
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    print(
        f"RUN RECORD VALIDATION {'PASS' if result.ok else 'FAIL'}: "
        f"{result.checks_passed} deterministic checks"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
