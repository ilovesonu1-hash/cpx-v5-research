#!/usr/bin/env python3
"""Execution-disabled G2.7a runner candidate.

PILOT_ONLY / NON_PRODUCTION.  ``plan`` and ``validate`` are the only commands
allowed by the current repository state.  No real transport adapter exists.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from transport import Transport, TransportError, TransportResponse


RUNTIME = "google-vertex/gemini-3.7-flash"
MODEL = "gemini-3.7-flash"
MAX_EXECUTION_UNIT_ATTEMPTS = 3
DEFAULT_COMMAND = "plan"
PREFLIGHT_REFUSAL = "PREFLIGHT_EXECUTION_NOT_AUTHORIZED"
EXECUTION_REFUSAL = "PATIENT_MODEL_EXECUTION_NOT_AUTHORIZED"
PREFLIGHT_REQUIRED_GATES = (
    "future accepted external preflight-authorization artifact",
    "accepted fixture/runner checkpoint",
    "exact input_bundle_id",
    "exact runtime",
)
EXECUTION_REQUIRED_GATES = (
    "future accepted execution-authorization artifact",
    "accepted fixture/runner checkpoint",
    "exact input_bundle_id",
    "explicit runtime",
    "public-safe scorer ID",
    "preflight authorization",
    "recorded passing preflight evidence",
    "explicit official-execution authorization",
)

RunIdFactory = Callable[[str, int, int], str]
TimestampFactory = Callable[[], str]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_bundle(root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root or repo_root()
    bundle = load_json(root / "docs/pilot/g2.7a/manifests/input-bundle-v1.json")
    manifest = load_json(root / "docs/pilot/g2.7a/manifests/execution-manifest-v1.json")
    return bundle, manifest


def _default_run_id(execution_unit_id: str, attempt_index: int, turn_index: int) -> str:
    del execution_unit_id, attempt_index, turn_index
    return "run-" + uuid.uuid4().hex


def _default_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _base_record(
    call: Mapping[str, Any],
    execution_unit_id: str,
    attempt_index: int,
    run_id: str,
    timestamp_utc: str,
    safe_session_id: str,
    physical_isolation_verified: bool,
    input_bundle_id: str,
    system_message_sha256: str,
) -> dict[str, Any]:
    return {
        "authoritative_attempt": False,
        "case": call["case"],
        "constituent_or_setup_id": call["constituent_or_setup_id"],
        "execution_error_class": None,
        "execution_error_message_safe": None,
        "execution_unit_id": execution_unit_id,
        "exposed_generation_settings": "NOT_EXPOSED",
        "final_patient_response": None,
        "input_bundle_id": input_bundle_id,
        "learner_utterance": call["learner_utterance"],
        "model": MODEL,
        "physical_isolation_verified": physical_isolation_verified,
        "provider_completion_status": None,
        "run_id": run_id,
        "runtime": RUNTIME,
        "safe_session_id": safe_session_id,
        "scored_turn": call["scored_turn"],
        "scored_unit_id": call["scored_unit_id"],
        "separate_reasoning_field_present": False,
        "source_trajectory_id": call["source_trajectory_id"],
        "system_message_sha256": system_message_sha256,
        "timestamp_utc": timestamp_utc,
        "turn_index": call["turn_index"],
        "unit_attempt_index": attempt_index,
    }


def run_execution_unit(
    execution_unit: Mapping[str, Any],
    planned_calls: Sequence[Mapping[str, Any]],
    system_message: str,
    transport: Transport,
    input_bundle_id: str,
    *,
    physical_isolation_verified: bool,
    run_id_factory: RunIdFactory = _default_run_id,
    timestamp_factory: TimestampFactory = _default_timestamp,
) -> list[dict[str, Any]]:
    """Exercise one unit with full-unit restart semantics using an injected transport.

    This function is used only with ``FakeTransport`` in the current task.  A
    successful response, including an empty or poor response, is never retried.
    """

    execution_unit_id = str(execution_unit["execution_unit_id"])
    ordered_calls = sorted(planned_calls, key=lambda call: int(call["turn_index"]))
    expected_call_ids = list(execution_unit["planned_call_ids"])
    if [call["planned_call_id"] for call in ordered_calls] != expected_call_ids:
        raise ValueError("planned calls do not match the execution unit")

    system_message_sha256 = hashlib.sha256(system_message.encode("utf-8")).hexdigest()
    all_records: list[dict[str, Any]] = []
    for attempt_index in range(1, MAX_EXECUTION_UNIT_ATTEMPTS + 1):
        session = transport.create_session(system_message, RUNTIME)
        attempt_records: list[dict[str, Any]] = []
        attempt_complete = True
        try:
            for call in ordered_calls:
                run_id = run_id_factory(execution_unit_id, attempt_index, int(call["turn_index"]))
                record = _base_record(
                    call,
                    execution_unit_id,
                    attempt_index,
                    run_id,
                    timestamp_factory(),
                    session.safe_session_id,
                    physical_isolation_verified,
                    input_bundle_id,
                    system_message_sha256,
                )
                try:
                    response: TransportResponse = session.send(str(call["learner_utterance"]))
                    if response.safe_session_id != session.safe_session_id:
                        raise TransportError(
                            "SESSION_ID_MISMATCH",
                            "transport response session identifier did not match the active session",
                        )
                    if not isinstance(response.final_response, str):
                        raise TransportError(
                            "FINAL_RESPONSE_CHANNEL_MISSING",
                            "transport did not provide a learner-visible final response string",
                        )
                    record["final_patient_response"] = response.final_response
                    record["provider_completion_status"] = response.completion_status
                    record["separate_reasoning_field_present"] = response.separate_reasoning_field_present
                except TransportError as exc:
                    record["execution_error_class"] = exc.error_class
                    record["execution_error_message_safe"] = exc.safe_message
                    record["provider_completion_status"] = "execution_error"
                    attempt_complete = False
                except Exception:
                    record["execution_error_class"] = "HARNESS_UNEXPECTED_ERROR"
                    record["execution_error_message_safe"] = "unexpected harness failure; raw exception suppressed"
                    record["provider_completion_status"] = "execution_error"
                    attempt_complete = False
                attempt_records.append(record)
                all_records.append(record)
                if not attempt_complete:
                    break
        finally:
            session.close()

        if attempt_complete and len(attempt_records) == len(ordered_calls):
            for record in attempt_records:
                record["authoritative_attempt"] = True
            return all_records

    return all_records


def print_plan(root: Path | None = None) -> int:
    bundle, manifest = load_bundle(root)
    print(
        "G2.7a PLAN: "
        f"{len(manifest['scored_units'])} scored units / "
        f"{len(manifest['planned_calls'])} calls / "
        f"{len(manifest['execution_units'])} sessions"
    )
    print(f"input_bundle_id={bundle['input_bundle_id']}")
    for index, unit in enumerate(manifest["execution_units"], start=1):
        scored = ",".join(unit["scored_unit_ids"])
        print(
            f"{index:02d} {unit['execution_unit_id']} "
            f"kind={unit['kind']} scored={scored} calls={len(unit['planned_call_ids'])}"
        )
    print("execution_authorized=false")
    return 0


def validate(root: Path | None = None) -> int:
    root = root or repo_root()
    from validate_bundle import validate_repository

    return validate_repository(root)


def refuse_preflight() -> int:
    print(PREFLIGHT_REFUSAL)
    return 3


def refuse_execute() -> int:
    print(EXECUTION_REFUSAL)
    return 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("plan", help="print the frozen nonexecuting plan")
    subparsers.add_parser("validate", help="run deterministic bundle validation")
    subparsers.add_parser("preflight", help="refuse until a future accepted authorization exists")
    subparsers.add_parser("execute", help="refuse until every future execution gate exists")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = args.command or DEFAULT_COMMAND
    if command == "plan":
        return print_plan()
    if command == "validate":
        return validate()
    if command == "preflight":
        return refuse_preflight()
    if command == "execute":
        return refuse_execute()
    raise AssertionError(f"unhandled command: {command}")


if __name__ == "__main__":
    raise SystemExit(main())
