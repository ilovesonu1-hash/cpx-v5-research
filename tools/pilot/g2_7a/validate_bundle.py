#!/usr/bin/env python3
"""Reusable deterministic integrity validator for the PILOT_ONLY G2.7a bundle.

Candidate-only artifact/adapter restrictions belong to verify_offline.py.
This integrity check neither grants execution permission nor proves isolation.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

import build_bundle as builder


@dataclass
class ValidationReport:
    checks_passed: int = 0
    errors: list[str] = field(default_factory=list)

    def check(self, condition: bool, code: str) -> None:
        if condition:
            self.checks_passed += 1
        else:
            self.errors.append(code)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _load_json(root: Path, path: str) -> Any:
    return json.loads((root / path).read_text(encoding="utf-8"))


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_canonical_text_fixture(data: bytes) -> bool:
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data or data.endswith(b"\n"):
        return False
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(not line.endswith((" ", "\t")) for line in text.split("\n"))


def _expected_ids(prefix: str, count: int) -> list[str]:
    return [f"{prefix}{number:02d}" for number in range(1, count + 1)]


def validate_source_lifetime(
    head: str,
    commit_exists: Callable[[str], bool],
    is_ancestor: Callable[[str, str], bool],
    report: ValidationReport,
) -> None:
    """Validate immutable ancestry without consulting a live remote-tracking ref."""

    report.check(commit_exists(builder.CANDIDATE_BASE_COMMIT), "SOURCE_CANDIDATE_BASE_MISSING")
    report.check(
        is_ancestor(builder.CANDIDATE_BASE_COMMIT, head),
        "SOURCE_CANDIDATE_BASE_NOT_ANCESTOR_OF_HEAD",
    )
    for commit, code in (
        (builder.SEMANTIC_CHECKPOINT, "SOURCE_SEMANTIC_CHECKPOINT_UNREACHABLE"),
        (builder.ENVELOPE_COMMIT, "SOURCE_ENVELOPE_COMMIT_UNREACHABLE"),
        (builder.ENVELOPE_MERGE, "SOURCE_ENVELOPE_MERGE_UNREACHABLE"),
    ):
        report.check(commit_exists(commit) and is_ancestor(commit, head), code)
    report.check(
        is_ancestor(builder.ENVELOPE_COMMIT, builder.ENVELOPE_MERGE),
        "SOURCE_ENVELOPE_NOT_REACHABLE_THROUGH_MERGE",
    )


def _validate_sources(root: Path, report: ValidationReport) -> builder.SourceBundle | None:
    head_result = _git(root, "rev-parse", "HEAD")
    report.check(head_result.returncode == 0, "SOURCE_HEAD_UNRESOLVED")
    if head_result.returncode == 0:
        head = head_result.stdout.decode("ascii").strip()

        def commit_exists(commit: str) -> bool:
            return _git(root, "cat-file", "-e", f"{commit}^{{commit}}").returncode == 0

        def is_ancestor(ancestor: str, descendant: str) -> bool:
            return _git(root, "merge-base", "--is-ancestor", ancestor, descendant).returncode == 0

        validate_source_lifetime(head, commit_exists, is_ancestor, report)

    try:
        sources = builder.load_pinned_sources(root)
    except (builder.BuildError, OSError) as exc:
        report.errors.append(f"SOURCE_LOAD_FAILED:{exc}")
        return None

    report.check(
        sources.prompt_document.sha256 == builder.PROMPT_DOCUMENT_SHA256,
        "SOURCE_PROMPT_DOCUMENT_HASH_MISMATCH",
    )
    report.check(
        _sha256(builder.extract_prompt_block(sources.prompt_document.content))
        == builder.PROMPT_BLOCK_SHA256,
        "SOURCE_PROMPT_BLOCK_HASH_MISMATCH",
    )
    report.check(
        (root / builder.ENVELOPE_PATH).read_bytes() == sources.envelope.content,
        "SOURCE_ENVELOPE_WORKING_BYTES_MISMATCH",
    )
    for path, source in sources.semantic.items():
        report.check((root / path).read_bytes() == source.content, f"SOURCE_WORKING_COPY_MISMATCH:{path}")
    report.check(
        (root / builder.STRUCTURAL_DISPOSITION_PATH).read_bytes()
        == sources.structural_disposition.content,
        "SOURCE_STRUCTURAL_DISPOSITION_WORKING_COPY_MISMATCH",
    )
    return sources


def _validate_generated_identity(
    root: Path,
    sources: builder.SourceBundle,
    report: ValidationReport,
) -> Mapping[str, bytes] | None:
    try:
        preflight = _load_json(root, builder.PREFLIGHT_MANIFEST)
        nonce = preflight["nonce"]
        expected = builder.render_artifacts(root, sources, nonce)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, builder.BuildError) as exc:
        report.errors.append(f"GENERATED_EXPECTATION_FAILED:{exc}")
        return None
    for path, expected_bytes in sorted(expected.items()):
        candidate = root / path
        report.check(candidate.is_file(), f"GENERATED_MISSING:{path}")
        if candidate.is_file():
            report.check(candidate.read_bytes() == expected_bytes, f"GENERATED_BYTES_DIFFER:{path}")
    return expected


def _validate_canonical_files(root: Path, report: ValidationReport) -> None:
    text_paths = (
        builder.PROMPT_FIXTURE,
        builder.J_PAYLOAD,
        builder.P_PAYLOAD,
        builder.J_SYSTEM,
        builder.P_SYSTEM,
        builder.PREFLIGHT_SYSTEM,
        builder.PREFLIGHT_A1,
        builder.PREFLIGHT_A2,
        builder.PREFLIGHT_B1,
    )
    for path in text_paths:
        data = (root / path).read_bytes()
        report.check(_is_canonical_text_fixture(data), f"CANONICAL_TEXT_INVALID:{path}")

    json_paths = (
        builder.PROVENANCE_MANIFEST,
        builder.PREFLIGHT_MANIFEST,
        builder.EXECUTION_MANIFEST,
        builder.AMBIGUITY_MAP,
        builder.CRITICALITY_MAP,
        builder.INPUT_BUNDLE,
    )
    for path in json_paths:
        data = (root / path).read_bytes()
        try:
            parsed = json.loads(data)
            report.check(data == builder.json_bytes(parsed), f"CANONICAL_JSON_INVALID:{path}")
        except (UnicodeError, json.JSONDecodeError):
            report.check(False, f"JSON_PARSE_FAILED:{path}")

    csv_data = (root / builder.SCORECARD_TEMPLATE).read_bytes()
    report.check(
        not csv_data.startswith(b"\xef\xbb\xbf")
        and b"\r" not in csv_data
        and csv_data.endswith(b"\n")
        and not csv_data.endswith(b"\n\n"),
        "CANONICAL_CSV_INVALID",
    )


def _validate_payloads(
    root: Path,
    sources: builder.SourceBundle,
    report: ValidationReport,
) -> None:
    cases = (
        (
            builder.J_PAYLOAD,
            "J",
            25,
            [f"J-T{i:02d}" for i in range(19, 25)],
            ("이름: 김영수", "나이: 58세", "성별: 남성", "진료 환경: 외래 초진", "스테이션 시간: 12분"),
        ),
        (
            builder.P_PAYLOAD,
            "P",
            30,
            [f"P-T{i:02d}" for i in range(25, 31)],
            ("이름: 박지현", "나이: 34세", "성별: 여성", "진료 환경: 외래", "스테이션 시간: 12분"),
        ),
    )
    case_analyses: dict[str, Mapping[str, list[str]]] = {}
    for path, prefix, count, forbidden, station_markers in cases:
        data = (root / path).read_bytes()
        text = data.decode("utf-8")
        contract_path = builder.J_CONTRACT_PATH if prefix == "J" else builder.P_CONTRACT_PATH
        analysis = builder.analyze_payload_provenance(
            sources.semantic[contract_path].content,
            data,
            prefix,
        )
        case_analyses["jaundice" if prefix == "J" else "palpitations"] = analysis
        fact_ids = analysis["payload_fact_ids"]
        expected = [f"{prefix}-T{i:02d}" for i in range(1, count + 1)]
        report.check(
            analysis["source_case_truth_fact_ids"] == expected
            and analysis["patient_knowledge_fact_ids"] == expected,
            f"PROVENANCE_SOURCE_INVENTORY:{prefix}",
        )
        report.check(len(fact_ids) == count, f"PAYLOAD_FACT_COUNT:{prefix}")
        report.check(len(set(fact_ids)) == count, f"PAYLOAD_FACT_DUPLICATE:{prefix}")
        report.check(fact_ids == expected, f"PAYLOAD_FACT_RANGE_OR_ORDER:{prefix}")
        report.check(all(fact_id in fact_ids for fact_id in forbidden), f"PAYLOAD_FORBIDDEN_FACT_MISSING:{prefix}")
        report.check(all(marker in text for marker in station_markers), f"PAYLOAD_STATION_FRAME_MISSING:{prefix}")
        report.check("방문 이유를 묻는 질문 뒤" in text, f"PAYLOAD_OPENING_TRIGGER_MISSING:{prefix}")
        report.check("[상황별 행동 규칙]" in text, f"PAYLOAD_BEHAVIOR_SECTION_MISSING:{prefix}")
        report.check(
            all(marker in text for marker in ("사실인 내용을 전제로", "분명히 부정하거나 바로잡는다", "진찰 결과를 대신 말하지 않는다")),
            f"PAYLOAD_RESPONSE_SCOPE_RULE_MISSING:{prefix}",
        )
        if prefix == "P":
            report.check(
                all(marker in text for marker in ("심전도 또는 다른 검사를 요청하지 않더라도", "제안하거나 상기시키거나 유도하지 않는다")),
                "PAYLOAD_P29_NO_PROMPT_RULE_MISSING",
            )
        report.check(
            re.search(r"\b(?:PASS|FAIL)\b", text) is None,
            f"PAYLOAD_EVALUATOR_TERM_PRESENT:{prefix}",
        )
        report.check(
            not any(
                heading in text
                for heading in ("[평가자", "[감사", "[공개 질문", "[문헌", "[사례 선택 이유")
            ),
            f"PAYLOAD_EXCLUDED_SECTION_PRESENT:{prefix}",
        )

    provenance = _load_json(root, builder.PROVENANCE_MANIFEST)
    by_case = {case["case"]: case for case in provenance["cases"]}
    report.check(by_case["jaundice"]["fact_count"] == 25, "PROVENANCE_J_FACT_COUNT")
    report.check(by_case["palpitations"]["fact_count"] == 30, "PROVENANCE_P_FACT_COUNT")
    report.check(
        all(
            not case["missing_fact_ids"]
            and not case["duplicate_fact_ids"]
            and not case["unexpected_fact_ids"]
            for case in provenance["cases"]
        ),
        "PROVENANCE_MISSING_DUPLICATE_OR_UNEXPECTED",
    )
    for case_name, analysis in case_analyses.items():
        recorded = by_case[case_name]
        report.check(
            recorded["included_fact_ids"] == analysis["included_fact_ids"]
            and recorded["missing_fact_ids"] == analysis["missing_fact_ids"]
            and recorded["duplicate_fact_ids"] == analysis["duplicate_fact_ids"]
            and recorded["unexpected_fact_ids"] == analysis["unexpected_fact_ids"],
            f"PROVENANCE_COMPUTATION_MISMATCH:{case_name}",
        )
        report.check(
            analysis["source_case_truth_fact_ids"] == analysis["patient_knowledge_fact_ids"],
            f"PROVENANCE_SOURCE_KNOWLEDGE_COVERAGE:{case_name}",
        )
        report.check(
            recorded["coverage_assurance"]["semantic_paraphrase_equivalence"]
            == "audit-reviewed; not proven by structural ID-count checks",
            f"PROVENANCE_SEMANTIC_ASSURANCE_OVERCLAIM:{case_name}",
        )


def _validate_system_messages(root: Path, report: ValidationReport) -> None:
    prompt = (root / builder.PROMPT_FIXTURE).read_bytes()
    for payload_path, system_path in (
        (builder.J_PAYLOAD, builder.J_SYSTEM),
        (builder.P_PAYLOAD, builder.P_SYSTEM),
    ):
        payload = (root / payload_path).read_bytes()
        system = (root / system_path).read_bytes()
        expected = prompt + "\n\n[환자 정보]\n".encode("utf-8") + payload
        text = system.decode("utf-8")
        report.check(system == expected, f"SYSTEM_ASSEMBLY_MISMATCH:{system_path}")
        report.check(
            sum(line == "[환자 정보]" for line in text.splitlines()) == 1,
            f"SYSTEM_PATIENT_HEADER_COUNT:{system_path}",
        )
        report.check("```" not in text, f"SYSTEM_MARKDOWN_FENCE_PRESENT:{system_path}")
        report.check(not system.endswith(b"\n"), f"SYSTEM_TERMINAL_LF_PRESENT:{system_path}")
        report.check(
            not re.search(r"(?<!-)[JP]\d{2}", text),
            f"SYSTEM_TRAJECTORY_ID_PRESENT:{system_path}",
        )
        report.check(
            "평가자 지시" not in text and "숨겨진 추론" not in text,
            f"SYSTEM_FORBIDDEN_INSTRUCTION_PRESENT:{system_path}",
        )


def _validate_preflight(root: Path, report: ValidationReport) -> None:
    manifest = _load_json(root, builder.PREFLIGHT_MANIFEST)
    report.check(builder.NONCE_PATTERN.fullmatch(manifest["nonce"]) is not None, "PREFLIGHT_NONCE_INVALID")
    report.check(manifest["expected_call_count"] == 3, "PREFLIGHT_CALL_COUNT")
    report.check(manifest["expected_session_count"] == 2, "PREFLIGHT_SESSION_COUNT")
    report.check(manifest["executed"] is False, "PREFLIGHT_EXECUTED_FLAG")
    report.check(manifest["execution_authorized"] is False, "PREFLIGHT_AUTHORIZED_FLAG")
    report.check(manifest["fail_closed_result"] == "HARNESS_ISOLATION_BLOCKED", "PREFLIGHT_FAIL_CLOSED")
    a1 = (root / builder.PREFLIGHT_A1).read_text(encoding="utf-8")
    report.check(a1.count(manifest["nonce"]) == 1, "PREFLIGHT_NONCE_NOT_FIXED_IN_A1")
    for path in (builder.PREFLIGHT_SYSTEM, builder.PREFLIGHT_A1, builder.PREFLIGHT_A2, builder.PREFLIGHT_B1):
        text = (root / path).read_text(encoding="utf-8")
        report.check("[환자 정보]" not in text, f"PREFLIGHT_PATIENT_HEADER_PRESENT:{path}")
        report.check("김영수" not in text and "박지현" not in text, f"PREFLIGHT_PAYLOAD_CONTENT_PRESENT:{path}")
        report.check("[역할]" not in text and "J-T" not in text and "P-T" not in text, f"PREFLIGHT_SP_CONTENT_PRESENT:{path}")


def _validate_execution_manifest(root: Path, report: ValidationReport) -> None:
    manifest = _load_json(root, builder.EXECUTION_MANIFEST)
    scored = manifest["scored_units"]
    units = manifest["execution_units"]
    calls = manifest["planned_calls"]
    scored_ids = [row["scored_unit_id"] for row in scored]
    expected_ids = _expected_ids("J", 28) + _expected_ids("P", 30)
    report.check(len(scored) == 58, "EXECUTION_SCORED_UNIT_COUNT")
    report.check(scored_ids == expected_ids and len(set(scored_ids)) == 58, "EXECUTION_SCORED_UNIT_IDENTITY")
    report.check(len(units) == 48, "EXECUTION_UNIT_COUNT")
    report.check(len(calls) == 64, "EXECUTION_CALL_COUNT")
    report.check(sum(bool(call["scored_turn"]) for call in calls) == 57, "EXECUTION_SCORED_CALL_COUNT")
    report.check(sum(not bool(call["scored_turn"]) for call in calls) == 7, "EXECUTION_UNSCORED_CALL_COUNT")
    kinds = [unit["kind"] for unit in units]
    report.check(kinds.count("independent_single_turn") == 38, "EXECUTION_SINGLE_COUNT")
    report.check(kinds.count("ordinary_sequence") == 9, "EXECUTION_SEQUENCE_COUNT")
    report.check(kinds.count("p29_station") == 1, "EXECUTION_P29_UNIT_COUNT")

    unit_by_id = {unit["execution_unit_id"]: unit for unit in units}
    report.check(len(unit_by_id) == len(units), "EXECUTION_DUPLICATE_UNIT_ID")
    report.check(
        all(unit_by_id[sequence_id]["scored_unit_ids"] == list(members) for sequence_id, members in builder.SEQUENCES.items()),
        "EXECUTION_SEQUENCE_MEMBERSHIP",
    )
    p29_unit = unit_by_id.get("P29-STATION-01", {})
    report.check(len(p29_unit.get("planned_call_ids", [])) == 6, "EXECUTION_P29_K")
    p29_calls = [call for call in calls if call["execution_unit_id"] == "P29-STATION-01"]
    report.check(
        len(p29_calls) == 6
        and all(not call["scored_turn"] and call["scored_unit_id"] == "P29" for call in p29_calls)
        and [call["constituent_or_setup_id"] for call in p29_calls] == [item[0] for item in builder.P29_SCRIPT]
        and all(call["source_trajectory_id"] is None for call in p29_calls),
        "EXECUTION_P29_LINKAGE",
    )
    setup = [call for call in calls if call["constituent_or_setup_id"] == builder.P14_SETUP_ID]
    report.check(
        len(setup) == 1
        and setup[0]["scored_turn"] is False
        and setup[0]["scored_unit_id"] is None
        and setup[0]["learner_utterance"] == builder.P14_SETUP_UTTERANCE
        and setup[0]["response_referenced_by_scored_units"] == ["P14", "P15"],
        "EXECUTION_P14_SETUP_LINKAGE",
    )
    call_ids = [call["planned_call_id"] for call in calls]
    report.check(len(call_ids) == len(set(call_ids)), "EXECUTION_DUPLICATE_CALL_ID")
    source_ids = [call["source_trajectory_id"] for call in calls if call["source_trajectory_id"] is not None]
    report.check(
        sorted(source_ids) == sorted(scored_id for scored_id in expected_ids if scored_id != "P29")
        and len(source_ids) == len(set(source_ids)),
        "EXECUTION_TRAJECTORY_COVERAGE",
    )
    calls_by_unit: dict[str, list[Mapping[str, Any]]] = {}
    for call in calls:
        calls_by_unit.setdefault(call["execution_unit_id"], []).append(call)
    coherent = True
    for unit in units:
        unit_calls = calls_by_unit.get(unit["execution_unit_id"], [])
        coherent = coherent and [call["turn_index"] for call in unit_calls] == list(range(1, len(unit_calls) + 1))
        coherent = coherent and bool(unit_calls) and unit_calls[0]["fresh_session_boundary"] is True
        coherent = coherent and all(call["fresh_session_boundary"] is False for call in unit_calls[1:])
        coherent = coherent and [call["planned_call_id"] for call in unit_calls] == unit["planned_call_ids"]
        coherent = coherent and unit["fresh_physical_session_required"] is True
        coherent = coherent and unit["same_session_required"] is True
    report.check(coherent, "EXECUTION_SESSION_BOUNDARIES_INCOHERENT")

    call_by_id = {call["planned_call_id"]: call for call in calls}
    evidence_coherent = True
    for scored_unit in scored:
        unit = unit_by_id[scored_unit["execution_unit_id"]]
        unit_call_ids = unit["planned_call_ids"]
        evidence_ids = scored_unit.get("planned_evidence_call_ids", [])
        evidence_coherent = evidence_coherent and bool(evidence_ids)
        evidence_coherent = evidence_coherent and all(call_id in call_by_id for call_id in evidence_ids)
        evidence_coherent = evidence_coherent and all(
            call_by_id[call_id]["execution_unit_id"] == unit["execution_unit_id"]
            for call_id in evidence_ids
            if call_id in call_by_id
        )
        if unit["kind"] == "p29_station":
            expected_evidence = unit_call_ids
        else:
            target_index = next(
                (
                    index
                    for index, call_id in enumerate(unit_call_ids)
                    if call_by_id[call_id]["scored_turn"]
                    and call_by_id[call_id]["scored_unit_id"] == scored_unit["scored_unit_id"]
                ),
                -1,
            )
            expected_evidence = unit_call_ids[: target_index + 1] if target_index >= 0 else []
        evidence_coherent = evidence_coherent and evidence_ids == expected_evidence
        if unit["kind"] == "independent_single_turn":
            evidence_coherent = evidence_coherent and len(evidence_ids) == 1
    report.check(evidence_coherent, "EXECUTION_PLANNED_EVIDENCE_INCOHERENT")
    scored_by_id = {item["scored_unit_id"]: item for item in scored}
    report.check(
        scored_by_id["P14"]["planned_evidence_call_ids"]
        == ["CALL-P-SETUP-DURATION-01", "CALL-P14"]
        and scored_by_id["P15"]["planned_evidence_call_ids"]
        == ["CALL-P-SETUP-DURATION-01", "CALL-P14", "CALL-P15"],
        "EXECUTION_P14_P15_EVIDENCE_LINKAGE",
    )
    report.check(
        scored_by_id["P29"]["planned_evidence_call_ids"]
        == [f"CALL-P29-U{index:02d}" for index in range(1, 7)],
        "EXECUTION_P29_EVIDENCE_LINKAGE",
    )
    report.check(manifest["execution_authorized"] is False, "EXECUTION_AUTHORIZED_FLAG")


def _validate_maps(root: Path, report: ValidationReport) -> None:
    ambiguity = _load_json(root, builder.AMBIGUITY_MAP)
    rules = {rule["rule_id"]: rule for rule in ambiguity["rules"]}
    expected_rules = {
        "P25_RHYTHM_PERCEPTION",
        "J16_J28_CANCER_FEAR",
        "JAUNDICE_WORDING",
        "OPENING_BROAD_BREADTH",
        "REGISTER_NATURALNESS",
        "P29_PROMPTING",
    }
    report.check(set(rules) == expected_rules, "AMBIGUITY_RULE_INVENTORY")
    report.check(
        all(rule["independent_automatic_fail_precedence"] is True for rule in rules.values()),
        "AMBIGUITY_FAIL_PRECEDENCE",
    )
    report.check(rules["REGISTER_NATURALNESS"]["scored_in_phase"] is False, "AMBIGUITY_REGISTER_SCORING")
    report.check("never" in rules["P29_PROMPTING"]["oracle_ambiguous"], "AMBIGUITY_P29_RULING")

    criticality = _load_json(root, builder.CRITICALITY_MAP)
    critical_pairs = {
        (item["scored_unit_id"], item["fact_id"])
        for item in criticality["critical_required_information_units"]
    }
    report.check(
        critical_pairs == {("P11", "P-T08"), ("P11", "P-T10"), ("P11", "P-T11")},
        "CRITICALITY_EXPLICIT_SET",
    )
    report.check(criticality["classification_basis"] == "explicit_source_only", "CRITICALITY_BASIS")
    report.check(
        criticality["status"] == "PROPOSED_FOR_AUDIT_AND_HUMAN_ACCEPTANCE",
        "CRITICALITY_STATUS",
    )
    classifications = criticality["scored_unit_required_classifications"]
    report.check(
        [item["scored_unit_id"] for item in classifications]
        == _expected_ids("J", 28) + _expected_ids("P", 30),
        "CRITICALITY_SCORED_UNIT_COVERAGE",
    )
    report.check(
        all(
            item["classification"] == ("critical" if item["scored_unit_id"] == "P11" else "ordinary")
            for item in classifications
        ),
        "CRITICALITY_SCORED_UNIT_POLICY",
    )


def _validate_scorecard(root: Path, report: ValidationReport) -> None:
    data = (root / builder.SCORECARD_TEMPLATE).read_text(encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))
    report.check(len(rows) == 58, "SCORECARD_ROW_COUNT")
    ids = [row["scored_unit_id"] for row in rows]
    report.check(ids == _expected_ids("J", 28) + _expected_ids("P", 30), "SCORECARD_UNIT_IDENTITY")
    report.check(ids.count("P29") == 1, "SCORECARD_P29_COUNT")
    result_fields = (
        "authoritative_run_ids",
        "disposition",
        "failure_class",
        "responsible_layer",
        "critical_required_omissions",
        "ordinary_required_omissions",
        "ambiguity_trigger",
        "evidence_excerpt",
        "scorer_id",
        "input_bundle_id",
        "scored_at_utc",
    )
    report.check(all(not row[field] for row in rows for field in result_fields), "SCORECARD_RESULT_PREFILLED")
    report.check(
        all(
            row["case"]
            and row["execution_unit_id"]
            and row["planned_evidence_call_ids"]
            and row["scoring_spec_sha256"]
            for row in rows
        ),
        "SCORECARD_STATIC_IDENTITY_MISSING",
    )
    manifest = _load_json(root, builder.EXECUTION_MANIFEST)
    scored_by_id = {item["scored_unit_id"]: item for item in manifest["scored_units"]}
    report.check(
        all(
            json.loads(row["planned_evidence_call_ids"])
            == scored_by_id[row["scored_unit_id"]]["planned_evidence_call_ids"]
            for row in rows
        ),
        "SCORECARD_PLANNED_EVIDENCE_MISMATCH",
    )


def _validate_input_bundle(root: Path, report: ValidationReport) -> None:
    bundle = _load_json(root, builder.INPUT_BUNDLE)
    components = bundle["components"]
    canonical = json.dumps(
        components, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    recomputed = "sha256:" + _sha256(canonical)
    report.check(bundle["input_bundle_id"] == recomputed, "INPUT_BUNDLE_ID_MISMATCH")
    report.check("input_bundle_id" not in components, "INPUT_BUNDLE_SELF_REFERENCE")
    report.check(
        bundle["identities"]["candidate_base_commit"] == builder.CANDIDATE_BASE_COMMIT,
        "INPUT_BUNDLE_CANDIDATE_BASE_IDENTITY",
    )
    report.check("governing_main" not in bundle["identities"], "INPUT_BUNDLE_STALE_MAIN_IDENTITY")
    report.check(
        bundle["identities"]["effective_semantic_checkpoint"] == builder.SEMANTIC_CHECKPOINT,
        "INPUT_BUNDLE_SEMANTIC_IDENTITY",
    )
    required_components = {
        "accepted_execution_envelope",
        "prompt_document",
        "prompt_block",
        "jaundice_contract",
        "palpitations_contract",
        "jaundice_trajectories",
        "palpitations_trajectories",
        "evaluation_spec",
        "execution_attempt_event_spec",
        "jaundice_payload",
        "palpitations_payload",
        "jaundice_system_message",
        "palpitations_system_message",
        "preflight_manifest",
        "execution_manifest",
        "ambiguity_map",
        "criticality_map",
        "raw_response_spec",
        "scorecard_spec",
        "scorecard_template",
        "structural_prebatch_disposition",
    }
    report.check(set(components) == required_components, "INPUT_BUNDLE_COMPONENT_INVENTORY")


def validate_repository(root: Path) -> int:
    report = ValidationReport()
    sources = _validate_sources(root, report)
    try:
        if sources is not None:
            _validate_generated_identity(root, sources, report)
            _validate_payloads(root, sources, report)
        _validate_canonical_files(root, report)
        _validate_system_messages(root, report)
        _validate_preflight(root, report)
        _validate_execution_manifest(root, report)
        _validate_maps(root, report)
        _validate_scorecard(root, report)
        _validate_input_bundle(root, report)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        report.errors.append(f"VALIDATOR_EXCEPTION:{type(exc).__name__}:{exc}")

    result = {
        "checks_passed": report.checks_passed,
        "errors": report.errors,
        "status": "PASS" if not report.errors else "FAIL",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if report.errors:
        print(f"VALIDATION FAIL: {len(report.errors)} error(s)")
        for error in report.errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION PASS: {report.checks_passed} deterministic checks")
    return 0


def main() -> int:
    return validate_repository(Path(__file__).resolve().parents[3])


if __name__ == "__main__":
    raise SystemExit(main())
