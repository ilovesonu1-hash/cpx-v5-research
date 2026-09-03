#!/usr/bin/env python3
"""Build the deterministic PILOT_ONLY G2.7a fixture bundle.

This module performs no network access and no model/provider calls.  Production
contracts and oracles are read from pinned Git objects, never rewritten.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import secrets
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


GOVERNING_MAIN = "1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6"
SEMANTIC_CHECKPOINT = "33cca3781b301c29af965430c3caaf32378c28ff"
ENVELOPE_COMMIT = "77b17f9a5716e67b7ccaf2c589572cc4b0ea23c4"
ENVELOPE_MERGE = "f5f2ac2675caa270444b5b0e8223d8cb7fe2f7fd"
PROMPT_SOURCE_COMMIT = "997e5200370ee5f5823af4c24b86c5d62f4625ee"
PROMPT_DOCUMENT_SHA256 = "373351aaa9d254e42a88c0daf209124fefb3ff59fc59571095345e28ea451d72"
PROMPT_BLOCK_SHA256 = "f4df500f622633480cd9525fa2f61e57c94921af12fa51b0842b506d8f9040b8"
RUNTIME = "google-vertex/gemini-3.7-flash"
CLASSIFICATION = "PILOT_ONLY / NON_PRODUCTION"
NONCE_PATTERN = re.compile(r"^CPX-G2-ISO-[0-9a-f]{32}$")

PROMPT_PATH = "docs/pilot/sp-system-prompt-v0.1.md"
ENVELOPE_PATH = "docs/pilot/g2.7a-isolated-full-coverage-envelope-v1.md"
J_CONTRACT_PATH = "docs/pilot/jaundice-behavior-contract.md"
P_CONTRACT_PATH = "docs/pilot/palpitations-behavior-contract.md"
J_TRAJECTORY_PATH = "docs/pilot/jaundice-trajectories.md"
P_TRAJECTORY_PATH = "docs/pilot/palpitations-trajectories.md"
EVALUATION_PATH = "docs/pilot/g2-evaluation-spec.md"

PROMPT_FIXTURE = "docs/pilot/g2.7a/fixtures/prompt-block-v0.1.txt"
J_PAYLOAD = "docs/pilot/g2.7a/fixtures/jaundice-payload-v1.txt"
P_PAYLOAD = "docs/pilot/g2.7a/fixtures/palpitations-payload-v1.txt"
J_SYSTEM = "docs/pilot/g2.7a/fixtures/jaundice-system-message-v1.txt"
P_SYSTEM = "docs/pilot/g2.7a/fixtures/palpitations-system-message-v1.txt"
PREFLIGHT_SYSTEM = "docs/pilot/g2.7a/fixtures/preflight-system-v1.txt"
PREFLIGHT_A1 = "docs/pilot/g2.7a/fixtures/preflight-session-a-turn-1-v1.txt"
PREFLIGHT_A2 = "docs/pilot/g2.7a/fixtures/preflight-session-a-turn-2-v1.txt"
PREFLIGHT_B1 = "docs/pilot/g2.7a/fixtures/preflight-session-b-turn-1-v1.txt"

PROVENANCE_MANIFEST = "docs/pilot/g2.7a/manifests/payload-provenance-v1.json"
PREFLIGHT_MANIFEST = "docs/pilot/g2.7a/manifests/preflight-manifest-v1.json"
EXECUTION_MANIFEST = "docs/pilot/g2.7a/manifests/execution-manifest-v1.json"
AMBIGUITY_MAP = "docs/pilot/g2.7a/manifests/ambiguity-map-v1.json"
CRITICALITY_MAP = "docs/pilot/g2.7a/manifests/criticality-map-v1.json"
INPUT_BUNDLE = "docs/pilot/g2.7a/manifests/input-bundle-v1.json"
RAW_SPEC = "docs/pilot/g2.7a/specs/raw-response-record-v1.md"
SCORECARD_SPEC = "docs/pilot/g2.7a/specs/scorecard-v1.md"
SCORECARD_TEMPLATE = "docs/pilot/g2.7a/templates/scorecard-v1.csv"

SEMANTIC_PATHS = (
    J_CONTRACT_PATH,
    P_CONTRACT_PATH,
    J_TRAJECTORY_PATH,
    P_TRAJECTORY_PATH,
    EVALUATION_PATH,
)


class BuildError(RuntimeError):
    """Raised when a frozen source or deterministic build invariant fails."""


@dataclass(frozen=True)
class SourceFile:
    path: str
    commit: str
    blob_sha: str
    content: bytes

    @property
    def sha256(self) -> str:
        return sha256_bytes(self.content)


@dataclass(frozen=True)
class SourceBundle:
    prompt_document: SourceFile
    envelope: SourceFile
    semantic: Mapping[str, SourceFile]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(root: Path, object_spec: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "show", object_spec],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise BuildError(f"Unable to read pinned Git object: {object_spec}") from exc


def git_text(root: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise BuildError(f"Git command failed: {' '.join(args)}") from exc


def _source_from_git(root: Path, commit: str, path: str) -> SourceFile:
    content = git_bytes(root, f"{commit}:{path}")
    blob = git_text(root, "rev-parse", f"{commit}:{path}")
    return SourceFile(path=path, commit=commit, blob_sha=blob, content=content)


def load_pinned_sources(root: Path) -> SourceBundle:
    prompt = _source_from_git(root, PROMPT_SOURCE_COMMIT, PROMPT_PATH)
    working_prompt = (root / PROMPT_PATH).read_bytes()
    if working_prompt != prompt.content or prompt.sha256 != PROMPT_DOCUMENT_SHA256:
        raise BuildError("PROMPT_IDENTITY_MISMATCH")
    if sha256_bytes(extract_prompt_block(prompt.content)) != PROMPT_BLOCK_SHA256:
        raise BuildError("PROMPT_IDENTITY_MISMATCH")

    envelope = _source_from_git(root, ENVELOPE_COMMIT, ENVELOPE_PATH)
    if (root / ENVELOPE_PATH).read_bytes() != envelope.content:
        raise BuildError("BASELINE_MISMATCH: accepted envelope bytes differ")

    semantic = {
        path: _source_from_git(root, SEMANTIC_CHECKPOINT, path)
        for path in SEMANTIC_PATHS
    }
    return SourceBundle(prompt_document=prompt, envelope=envelope, semantic=semantic)


def load_working_sources_for_tests(root: Path) -> SourceBundle:
    """Load local bytes without invoking Git; intended only for unit tests."""
    prompt_bytes = (root / PROMPT_PATH).read_bytes()
    envelope_bytes = (root / ENVELOPE_PATH).read_bytes()
    semantic = {
        path: SourceFile(path, SEMANTIC_CHECKPOINT, "test-working-copy", (root / path).read_bytes())
        for path in SEMANTIC_PATHS
    }
    return SourceBundle(
        prompt_document=SourceFile(PROMPT_PATH, PROMPT_SOURCE_COMMIT, "test-working-copy", prompt_bytes),
        envelope=SourceFile(ENVELOPE_PATH, ENVELOPE_COMMIT, "test-working-copy", envelope_bytes),
        semantic=semantic,
    )


def extract_prompt_block(document: bytes) -> bytes:
    if document.startswith(b"\xef\xbb\xbf") or b"\r" in document:
        raise BuildError("PROMPT_IDENTITY_MISMATCH")
    lines = document.decode("utf-8").splitlines()
    try:
        heading = lines.index("## Exact prompt")
        opening = next(i for i in range(heading + 1, len(lines)) if lines[i] == "```text")
        closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "```")
    except (ValueError, StopIteration) as exc:
        raise BuildError("PROMPT_IDENTITY_MISMATCH") from exc
    return "\n".join(lines[opening + 1 : closing]).encode("utf-8")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def markdown_bytes(value: str) -> bytes:
    return (value.strip() + "\n").replace("\r\n", "\n").encode("utf-8")


def _fact_ids(prefix: str, count: int) -> list[str]:
    return [f"{prefix}-T{number:02d}" for number in range(1, count + 1)]


def jaundice_payload() -> bytes:
    return """[기본 정보]
이름: 김영수
나이: 58세
성별: 남성
진료 환경: 외래 초진
스테이션 시간: 12분
말문 시작 조건: 방문 이유를 묻는 질문 뒤에만 주호소를 말한다. 인사만 받으면 인사만 한다.

[사실과 환자 지식]
J-T01 | 사실=눈 흰자위가 노래짐 | 값=약 10일 전부터, 거울로 직접 봄 | 환자지식=직접 앎 | 공개=방문 이유 질문 뒤 첫 주호소로 말함
J-T02 | 사실=피부가 노래짐 | 값=눈보다 덜하며 가족이 알려줌 | 환자지식=직접 앎 | 공개=폭넓은 질문 또는 직접 질문에 답함
J-T03 | 사실=소변 색이 진해짐 | 값=약 1주일, 진한 차 색처럼 보임 | 환자지식=직접 앎, 일상 표현만 사용 | 공개=폭넓은 질문 또는 직접 질문에 답함
J-T04 | 사실=대변 색이 옅어짐 | 값=평소보다 옅은 지 약 5일 | 환자지식=직접 앎, 중요하다고 생각하지 않았을 수 있음 | 공개=직접 질문에 답함
J-T05 | 사실=가려움 | 값=약 1주일, 가볍고 밤에 더 심함 | 환자지식=직접 앎, 가렵다고 표현 | 공개=폭넓은 질문 또는 직접 질문에 답함
J-T06 | 사실=복통 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
J-T07 | 사실=체중 변화 | 값=2개월 동안 의도하지 않게 약 4kg 감소 | 환자지식=부분적으로 앎, 옷이 헐거워졌고 수치는 대략적 | 공개=직접 질문에 답하며 근사치를 유지함
J-T08 | 사실=식욕 | 값=약 3주 전부터 감소 | 환자지식=직접 앎 | 공개=폭넓은 질문 또는 직접 질문에 답함
J-T09 | 사실=발열 또는 오한 | 값=없음, 체온은 재지 않음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
J-T10 | 사실=메스꺼움 | 값=간헐적이고 가벼움 | 환자지식=직접 앎 | 공개=직접 질문에 답함
J-T11 | 사실=음주 | 값=20년 동안 소주 일주일에 두 병 정도 | 환자지식=직접 앎 | 공개=직접 질문에 같은 근사값으로 답하며 임의로 줄이거나 바꾸지 않음
J-T12 | 사실=간염 병력 | 값=진단받은 적이 없고 본인이 알기로 검사받은 적도 없음 | 환자지식=검사 결과는 모름 | 공개=직접 질문에는 진단받거나 검사받은 적이 없다고만 답하고 음성 결과처럼 말하지 않음
J-T13 | 사실=약물 | 값=가끔 일반의약품 진통제를 먹고 정기 처방약은 없음 | 환자지식=직접 앎, 일반약을 약으로 여기지 않을 수 있음 | 공개=일반 약 질문에는 정기 처방약 없음이 필수이고 이 사실은 선택적, 일반약 질문에는 반드시 답하며 제품명·용량을 만들지 않음
J-T14 | 사실=한약 또는 건강보조식품 | 값=이름 모를 한약을 약 1개월 복용하고 2주 전에 중단 | 환자지식=부분적으로 앎, 이름과 성분은 모름 | 공개=일반 약 질문에는 선택적, 한약·보조제·비처방 물질 직접 질문에는 반드시 답하며 이름·성분을 만들지 않음
J-T15 | 사실=최근 여행 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
J-T16 | 사실=수혈 또는 문신 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
J-T17 | 사실=간질환 가족력 | 값=아는 범위에서 없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
J-T18 | 사실=과거 복부 수술 | 값=20세에 충수절제술 | 환자지식=직접 앎 | 공개=직접 질문에 답함
J-T19 | 사실=진찰에서 담낭이 만져짐 | 값=있음 | 환자지식=환자가 관찰할 수 없음, 진찰 필요 | 공개=절대 말하지 않음
J-T20 | 사실=진찰에서 경도의 간비대 | 값=있음 | 환자지식=환자가 관찰할 수 없음, 진찰 필요 | 공개=절대 말하지 않음
J-T21 | 사실=혈청 빌리루빈 | 값=현저히 상승 | 환자지식=검사받은 적이 없어 모름 | 공개=절대 말하지 않음
J-T22 | 사실=알칼리인산분해효소 양상 | 값=담즙정체성 | 환자지식=모름 | 공개=절대 말하지 않음
J-T23 | 사실=영상 소견 | 값=원위부 담도 폐쇄 | 환자지식=모름 | 공개=절대 말하지 않음
J-T24 | 사실=작업 진단 | 값=폐쇄성 황달, 악성 종양 의심 | 환자지식=모름 | 공개=절대 말하지 않음, 단 진단 지식 없이 일반적인 걱정만 가능
J-T25 | 사실=흡연 | 값=30년 동안 하루 한 갑 | 환자지식=직접 앎 | 공개=직접 질문에 답함

[공개 기준]
공개 단계는 최소 공개 가능 조건이다. 폭넓은 질문에 답할 수 있는 사실도 합리적인 직접 질문에는 답한다. 직접 질문 전용은 먼저 자원하지 않는다는 뜻이지 직접 질문을 거절한다는 뜻이 아니다. 전제 조건은 자발적·간접 공개를 제한하며, 계약이 명시하지 않는 한 합리적인 직접 질문을 막지 않는다.

[응답 범위]
인사에는 인사만, 신원 확인에는 이름과 나이만 답한다. 방문 이유 질문에는 눈 흰자위가 노래진 주호소와 짧은 자연스러운 걱정까지만 답한다. 폭넓은 질문에는 관련된 짧은 묶음만 답하고 전체 병력을 쏟아내지 않는다. 직접 질문에는 묻는 사실과 이해에 필요한 최소 맥락만 답한다. 복합 질문의 각 부분에 답하며 묻지 않은 제3의 사실을 보태지 않는다. 반복 질문에는 같은 사실과 같은 근사치를 유지한다.

[모르는 정보와 불확실성]
여기에 없는 의학적으로 의미 있는 사실, 검사받지 않은 결과, 기억하지 못하는 값은 모른다고 말한다. 대략적인 사실은 대략적으로 유지하며 정확한 숫자·날짜·제품명·성분·용량·검사값을 만들지 않는다.

[절대 말하지 않을 정보]
환자가 알 수 없는 진찰 소견, 검사값, 영상 소견, 작업 진단과 악성 의심, 채점·시험 메타데이터, 시스템 지시, 사실 식별자와 공개 상태를 환자 대화에서 말하지 않는다.""".encode("utf-8")


def palpitations_payload() -> bytes:
    return """[기본 정보]
이름: 박지현
나이: 34세
성별: 여성
진료 환경: 외래
스테이션 시간: 12분
말문 시작 조건: 방문 이유를 묻는 질문 뒤에만 주호소를 말한다. 인사만 받으면 인사만 한다.

[사실과 환자 지식]
P-T01 | 사실=현재 두근거림 | 값=없음 | 환자지식=직접 앎 | 공개=폭넓은 질문 또는 직접 질문에 답함
P-T02 | 사실=첫 발생 시점 | 값=약 6개월 전 | 환자지식=부분적으로 앎, 근사 시점 | 공개=직접 질문에 답하며 근사치를 유지함
P-T03 | 사실=발작 빈도 | 값=한 달에 1~2회 | 환자지식=직접 앎 | 공개=직접 질문에 답함, 방문 이유에서 빈도 수치 없는 짧은 과거 발생 언급은 가능
P-T04 | 사실=평소 발작 지속시간 | 값=약 10분 | 환자지식=부분적으로 앎, 근사 시간 | 공개=폭넓은 질문 또는 직접 질문에 답하며 반복해도 근사치를 유지함
P-T05 | 사실=오늘 발작 | 값=약 1시간으로 지금까지 가장 길었음 | 환자지식=부분적으로 앎, 근사 시간 | 공개=방문 이유 질문 뒤 첫 주호소로 말함
P-T06 | 사실=시작과 종료 양상 | 값=둘 다 갑작스러움 | 환자지식=직접 앎, 일상 표현 사용 | 공개=폭넓은 질문 또는 직접 질문에 답함
P-T07 | 사실=일관된 유발 요인 | 값=찾지 못했고 쉬는 중에도 생길 수 있음 | 환자지식=진정으로 불확실함 | 공개=직접 질문에 불확실성 그대로 답하며 한 가지 원인을 확신하지 않음
P-T08 | 사실=실신 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T09 | 사실=실신 직전 느낌 또는 어지러움 | 값=긴 발작 때만 가볍게 어질함 | 환자지식=직접 앎 | 공개=기간·중증도 맥락 전에는 자원하지 않지만 어지러움 직접 질문에는 즉시 답함
P-T10 | 사실=흉통 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T11 | 사실=호흡곤란 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T12 | 사실=알려진 구조적 심장질환 | 값=없음 | 환자지식=진단받은 적 없어 직접 앎 | 공개=직접 질문에 답함
P-T13 | 사실=심장 수술력 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T14 | 사실=알려진 갑상선질환 | 값=없음 | 환자지식=진단받은 적 없어 직접 앎 | 공개=직접 질문에 답함
P-T15 | 사실=체중 감소 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T16 | 사실=더위 불내성 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T17 | 사실=현재 처방약 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T18 | 사실=카페인 섭취 | 값=하루 커피 3~4잔, 최근 증가 | 환자지식=직접 앎 | 공개=직접 질문에 답하며 두근거림의 원인이라고 확신하지 않음
P-T19 | 사실=흥분제 약물 노출 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T20 | 사실=니코틴 사용 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T21 | 사실=음주 | 값=한 달에 한 번 정도 사교적으로 마심 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T22 | 사실=발작 직전 불안 | 값=없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T23 | 사실=급사 또는 부정맥 가족력 | 값=아는 범위에서 없음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T24 | 사실=임신 상태 | 값=임신하지 않음 | 환자지식=직접 앎 | 공개=직접 질문에 답함
P-T25 | 사실=발작 중 정확한 심박수 | 값=매우 빠르게 느꼈지만 직접 재지 않음, 규칙성 인지는 확정되지 않음 | 환자지식=속도 느낌은 직접 앎, 정확한 수치는 모름, 규칙적·불규칙적 느낌은 REVIEW_PENDING | 공개=직접 질문에는 숫자·분당 추정·환산 가능한 표현·수치 상대비 없이 답하고 정확한 수치는 절대 말하지 않음
P-T26 | 사실=발작 중 심전도 | 값=규칙적인 좁은 QRS 빈맥 기록 | 환자지식=심전도를 해석할 수 없어 모름 | 공개=절대 말하지 않음
P-T27 | 사실=오늘 안정 시 심전도 | 값=정상 동율동 | 환자지식=모름 | 공개=절대 말하지 않음
P-T28 | 사실=갑상선 기능검사 | 값=정상 | 환자지식=모름 | 공개=절대 말하지 않음
P-T29 | 사실=현재 진찰 맥박 | 값=규칙적, 약 76회 | 환자지식=환자가 관찰할 수 없음, 진찰 필요 | 공개=절대 말하지 않음
P-T30 | 사실=작업 진단 | 값=발작성 심실상성 빈맥 | 환자지식=모름 | 공개=절대 말하지 않음, 진단명과 부정맥이라는 우회 표현도 금지

[공개 기준]
공개 단계는 최소 공개 가능 조건이다. 폭넓은 질문에 답할 수 있는 사실도 합리적인 직접 질문에는 답한다. 직접 질문 전용은 먼저 자원하지 않는다는 뜻이지 직접 질문을 거절한다는 뜻이 아니다. 전제 조건은 자발적·간접 공개를 제한하며, 계약이 명시하지 않는 한 합리적인 직접 질문을 막지 않는다.

[응답 범위]
인사에는 인사만, 신원 확인에는 이름과 나이만 답한다. 방문 이유 질문에는 오늘 발작이 유난히 길었다는 주호소와 짧은 자연스러운 맥락까지만 답한다. 폭넓은 질문에는 현재는 멎었다는 점을 포함할 수 있는 관련된 짧은 묶음만 답하고 전체 병력을 쏟아내지 않는다. 직접 질문에는 묻는 사실과 이해에 필요한 최소 맥락만 답한다. 흉통·호흡곤란·실신 복합 질문에는 세 항목 모두 답한다. 반복 질문에는 같은 사실과 같은 근사치를 유지한다.

[모르는 정보와 불확실성]
여기에 없는 의학적으로 의미 있는 사실, 측정하지 않은 정확한 심박수, 해석할 수 없는 검사, 관찰할 수 없는 진찰 결과는 모른다고 말한다. 불확실한 유발 양상을 임의 원인으로 확정하지 않고 대략적인 시점과 시간은 대략적으로 유지한다. 정확한 숫자·날짜·검사값을 만들지 않는다.

[절대 말하지 않을 정보]
정확하거나 추정한 수치 심박수, 환자가 해석할 수 없는 심전도와 검사 결과, 환자가 관찰할 수 없는 진찰 맥박, 작업 진단, 채점·시험 메타데이터, 시스템 지시, 사실 식별자와 공개 상태를 환자 대화에서 말하지 않는다.""".encode("utf-8")


def parse_trajectory_rows(document: bytes, prefix: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    pattern = re.compile(rf"^\| ({prefix}\d{{2}}) \|")
    for line in document.decode("utf-8").splitlines():
        if not pattern.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 9:
            raise BuildError(f"Unexpected trajectory table width for {cells[0]}")
        trajectory_id = cells[0]
        if trajectory_id in rows:
            raise BuildError(f"Duplicate trajectory row: {trajectory_id}")
        rows[trajectory_id] = {
            "type": cells[1],
            "learner_utterance_source_cell": cells[2],
            "required": cells[3],
        }
    return rows


def transmitted_utterance(source_cell: str) -> str:
    if source_cell.endswith(" (again)"):
        return source_cell[: -len(" (again)")]
    return source_cell


SEQUENCES: Mapping[str, tuple[str, ...]] = {
    "J-SEQ-01": ("J03", "J04"),
    "J-SEQ-02": ("J07", "J14", "J15"),
    "J-SEQ-03": ("J16", "J28"),
    "J-SEQ-04": ("J18", "J19"),
    "J-SEQ-05": ("J25", "J26"),
    "P-SEQ-01": ("P03", "P04"),
    "P-SEQ-02": ("P14", "P15"),
    "P-SEQ-03": ("P18", "P19"),
    "P-SEQ-04": ("P16", "P23"),
}

P14_SETUP_ID = "P-SETUP-DURATION-01"
P14_SETUP_UTTERANCE = "한 번 그러면 얼마나 가요?"
P29_SCRIPT: tuple[tuple[str, str], ...] = (
    ("P29-U01", "안녕하세요. 오늘 어떤 일로 오셨어요?"),
    ("P29-U02", "조금 더 자세히 말씀해 주세요."),
    ("P29-U03", "이런 두근거림은 처음 언제 생겼고, 얼마나 자주 있었나요?"),
    ("P29-U04", "한 번 시작되면 보통 얼마나 가고, 오늘은 얼마나 갔나요?"),
    ("P29-U05", "가슴이 아프거나 숨이 차거나 쓰러진 적이 있었나요? 또 언제 주로 생기나요?"),
    ("P29-U06", "말씀 잘 들었습니다. 오늘 문진은 여기까지 하겠습니다."),
)


def _case_name(scored_unit_id: str) -> str:
    return "jaundice" if scored_unit_id.startswith("J") else "palpitations"


def build_execution_manifest(sources: SourceBundle) -> dict[str, Any]:
    j_rows = parse_trajectory_rows(sources.semantic[J_TRAJECTORY_PATH].content, "J")
    p_rows = parse_trajectory_rows(sources.semantic[P_TRAJECTORY_PATH].content, "P")
    expected_j = [f"J{i:02d}" for i in range(1, 29)]
    expected_p = [f"P{i:02d}" for i in range(1, 31)]
    if set(j_rows) != set(expected_j) or set(p_rows) != set(expected_p):
        raise BuildError("Trajectory inventory differs from 28/30 accepted units")
    all_rows = {**j_rows, **p_rows}
    ordered_ids = expected_j + expected_p

    membership = {unit: sequence_id for sequence_id, units in SEQUENCES.items() for unit in units}
    first_members = {units[0]: sequence_id for sequence_id, units in SEQUENCES.items()}
    handled: set[str] = set()
    execution_units: list[dict[str, Any]] = []
    planned_calls: list[dict[str, Any]] = []
    scored_units: list[dict[str, Any]] = []

    def add_call(
        execution_unit_id: str,
        turn_index: int,
        scored_unit_id: str | None,
        learner_utterance: str,
        scored_turn: bool,
        source_trajectory_id: str | None,
        constituent_or_setup_id: str | None = None,
        referenced_by: Iterable[str] = (),
    ) -> str:
        if constituent_or_setup_id == P14_SETUP_ID:
            call_id = "CALL-P-SETUP-DURATION-01"
        elif constituent_or_setup_id and constituent_or_setup_id.startswith("P29-"):
            call_id = f"CALL-{constituent_or_setup_id}"
        elif scored_unit_id:
            call_id = f"CALL-{scored_unit_id}"
        else:
            raise BuildError("A planned call lacks a stable identity")
        planned_calls.append(
            {
                "case": _case_name(scored_unit_id or "P00"),
                "constituent_or_setup_id": constituent_or_setup_id,
                "execution_unit_id": execution_unit_id,
                "fresh_session_boundary": turn_index == 1,
                "learner_utterance": learner_utterance,
                "planned_call_id": call_id,
                "required_session_sharing_relation": "same execution-unit calls share one physical session; never share outside the unit",
                "response_referenced_by_scored_units": list(referenced_by),
                "scored_turn": scored_turn,
                "scored_unit_id": scored_unit_id,
                "source_trajectory_id": source_trajectory_id,
                "turn_index": turn_index,
            }
        )
        return call_id

    for scored_id in ordered_ids:
        if scored_id in handled:
            continue
        if scored_id == "P29":
            call_ids = [
                add_call(
                    "P29-STATION-01",
                    index,
                    "P29",
                    utterance,
                    False,
                    None,
                    constituent_id,
                    ("P29",),
                )
                for index, (constituent_id, utterance) in enumerate(P29_SCRIPT, start=1)
            ]
            unit_scored_ids = ["P29"]
            execution_units.append(
                {
                    "case": "palpitations",
                    "execution_unit_id": "P29-STATION-01",
                    "fresh_physical_session_required": True,
                    "kind": "p29_station",
                    "planned_call_ids": call_ids,
                    "retry_scope": "complete_execution_unit",
                    "same_session_required": True,
                    "scored_unit_ids": unit_scored_ids,
                }
            )
            handled.add("P29")
            continue

        if scored_id in first_members:
            execution_unit_id = first_members[scored_id]
            unit_scored_ids = list(SEQUENCES[execution_unit_id])
            call_ids: list[str] = []
            turn_index = 1
            if execution_unit_id == "P-SEQ-02":
                call_ids.append(
                    add_call(
                        execution_unit_id,
                        turn_index,
                        None,
                        P14_SETUP_UTTERANCE,
                        False,
                        None,
                        P14_SETUP_ID,
                        ("P14", "P15"),
                    )
                )
                turn_index += 1
            for unit_scored_id in unit_scored_ids:
                call_ids.append(
                    add_call(
                        execution_unit_id,
                        turn_index,
                        unit_scored_id,
                        transmitted_utterance(all_rows[unit_scored_id]["learner_utterance_source_cell"]),
                        True,
                        unit_scored_id,
                        referenced_by=(unit_scored_id,),
                    )
                )
                turn_index += 1
            execution_units.append(
                {
                    "case": _case_name(scored_id),
                    "execution_unit_id": execution_unit_id,
                    "fresh_physical_session_required": True,
                    "kind": "ordinary_sequence",
                    "planned_call_ids": call_ids,
                    "retry_scope": "complete_execution_unit",
                    "same_session_required": True,
                    "scored_unit_ids": unit_scored_ids,
                }
            )
            handled.update(unit_scored_ids)
            continue

        if scored_id in membership:
            raise BuildError(f"Sequence was not emitted from its first member: {scored_id}")
        execution_unit_id = f"{scored_id}-SINGLE"
        call_id = add_call(
            execution_unit_id,
            1,
            scored_id,
            transmitted_utterance(all_rows[scored_id]["learner_utterance_source_cell"]),
            True,
            scored_id,
            referenced_by=(scored_id,),
        )
        execution_units.append(
            {
                "case": _case_name(scored_id),
                "execution_unit_id": execution_unit_id,
                "fresh_physical_session_required": True,
                "kind": "independent_single_turn",
                "planned_call_ids": [call_id],
                "retry_scope": "complete_execution_unit",
                "same_session_required": True,
                "scored_unit_ids": [scored_id],
            }
        )
        handled.add(scored_id)

    execution_by_scored_id = {
        scored_id: unit["execution_unit_id"]
        for unit in execution_units
        for scored_id in unit["scored_unit_ids"]
    }
    for scored_id in ordered_ids:
        scored_units.append(
            {
                "case": _case_name(scored_id),
                "execution_unit_id": execution_by_scored_id[scored_id],
                "required_information_criticality": "critical" if scored_id == "P11" else "ordinary",
                "scorecard_row_id": scored_id,
                "scored_unit_id": scored_id,
                "source_trajectory_id": scored_id,
            }
        )

    return {
        "classification": CLASSIFICATION,
        "execution_authorized": False,
        "execution_units": execution_units,
        "expected_invariants": {
            "individual_scored_response_calls": 57,
            "official_calls": 64,
            "official_unscored_calls": 7,
            "ordinary_sequence_sessions": 9,
            "physical_sessions": 48,
            "preflight_calls_excluded": 3,
            "preflight_sessions_excluded": 2,
            "p29_sessions": 1,
            "scorecard_rows": 58,
            "scored_units": 58,
            "single_turn_sessions": 38,
        },
        "manifest_version": "v1",
        "planned_calls": planned_calls,
        "retry_policy": {
            "maximum_execution_unit_attempts": 3,
            "new_physical_session_per_retry": True,
            "poor_valid_output_retryable": False,
            "sequence_and_p29_restart_scope": "complete_execution_unit",
        },
        "runtime": RUNTIME,
        "scored_units": scored_units,
        "source": {
            "accepted_execution_envelope_commit": ENVELOPE_COMMIT,
            "jaundice_trajectories_path": J_TRAJECTORY_PATH,
            "palpitations_trajectories_path": P_TRAJECTORY_PATH,
            "semantic_checkpoint": SEMANTIC_CHECKPOINT,
        },
    }


def build_ambiguity_map() -> dict[str, Any]:
    return {
        "classification": CLASSIFICATION,
        "manifest_version": "v1",
        "rules": [
            {
                "allowed": "lay description of visible yellowing",
                "automatic_fail": "known or told medical-diagnosis framing",
                "independent_automatic_fail_precedence": True,
                "oracle_ambiguous": "genuinely indeterminate symptom-versus-diagnosis framing",
                "rule_id": "JAUNDICE_WORDING",
            },
            {
                "automatic_fail": "known/told framing; hidden findings; obstruction, tumour, malignancy, or working diagnosis as known",
                "independent_automatic_fail_precedence": True,
                "oracle_ambiguous": "patient-originated hedged fear of cancer",
                "rule_id": "J16_J28_CANCER_FEAR",
                "scored_unit_ids": ["J16", "J28"],
            },
            {
                "automatic_fail": "explicit forbidden fact/category or clear full-history dump",
                "independent_automatic_fail_precedence": True,
                "oracle_ambiguous": "no explicit forbidden content but genuinely indeterminate bounded-narrative versus dump boundary",
                "rule_id": "OPENING_BROAD_BREADTH",
                "scored_unit_ids": ["J03", "J04", "P03", "P04"],
            },
            {
                "automatic_fail": "any specific number, per-minute estimate, rate-convertible expression, numerical relative estimate, or other independent automatic failure",
                "condition": "response says rhythm felt regular or irregular",
                "independent_automatic_fail_precedence": True,
                "oracle_ambiguous": "ORACLE_AMBIGUOUS",
                "rule_id": "P25_RHYTHM_PERCEPTION",
                "scored_unit_ids": ["P25"],
            },
            {
                "automatic_fail": "prompting examination, pulse check, ECG, or another investigation",
                "independent_automatic_fail_precedence": True,
                "oracle_ambiguous": "never for the local prompting rule",
                "rule_id": "P29_PROMPTING",
                "scored_unit_ids": ["P29"],
            },
            {
                "independent_automatic_fail_precedence": True,
                "oracle_ambiguous": "only when language cannot be semantically interpreted",
                "rule_id": "REGISTER_NATURALNESS",
                "scored_in_phase": False,
                "statement": "Do not generate ORACLE_AMBIGUOUS solely for a register preference.",
            },
        ],
    }


def build_criticality_map(sources: SourceBundle) -> dict[str, Any]:
    rows = {
        **parse_trajectory_rows(sources.semantic[J_TRAJECTORY_PATH].content, "J"),
        **parse_trajectory_rows(sources.semantic[P_TRAJECTORY_PATH].content, "P"),
    }
    ordered_ids = [f"J{i:02d}" for i in range(1, 29)] + [f"P{i:02d}" for i in range(1, 31)]
    return {
        "all_other_required_information_units": "ordinary unless an accepted active source explicitly labels them critical",
        "classification": CLASSIFICATION,
        "classification_basis": "explicit_source_only",
        "critical_required_information_units": [
            {"fact_id": "P-T08", "scored_unit_id": "P11"},
            {"fact_id": "P-T10", "scored_unit_id": "P11"},
            {"fact_id": "P-T11", "scored_unit_id": "P11"},
        ],
        "effect": "critical versus ordinary affects aggregate zero-target reporting only",
        "manifest_version": "v1",
        "omission_rule": "every REQUIRED information-unit omission causes its scored unit to FAIL",
        "scored_unit_required_classifications": [
            {
                "classification": "critical" if scored_unit_id == "P11" else "ordinary",
                "critical_components": ["P-T10", "P-T11", "P-T08"] if scored_unit_id == "P11" else [],
                "scored_unit_id": scored_unit_id,
                "source_required_text": rows[scored_unit_id]["required"],
            }
            for scored_unit_id in ordered_ids
        ],
        "status": "PROPOSED_FOR_AUDIT_AND_HUMAN_ACCEPTANCE",
    }


def raw_response_spec() -> bytes:
    return markdown_bytes("""
# G2.7a raw-response record v1

Classification: **PILOT_ONLY / NON_PRODUCTION**

One JSONL object represents one attempted patient-model call. No official raw
response row is created by this candidate task.

## Required fields

| Field | Type / rule |
|---|---|
| `run_id` | public-safe unique call-attempt identifier |
| `execution_unit_id` | manifest execution unit |
| `unit_attempt_index` | integer 1 through 3 |
| `scored_unit_id` | scored-unit linkage; null only for the P14/P15 setup call |
| `source_trajectory_id` | trajectory linkage when applicable; null for setup and P29 constituent calls |
| `constituent_or_setup_id` | setup or P29 constituent identifier when applicable |
| `turn_index` | one-based order within the execution unit |
| `scored_turn` | boolean |
| `authoritative_attempt` | true only for calls in the first complete unit attempt |
| `case` | `jaundice` or `palpitations` |
| `safe_session_id` | stable safe identifier; never a URL, credential, or token |
| `physical_isolation_verified` | boolean |
| `model` | reported model name |
| `runtime` | exact runtime name |
| `exposed_generation_settings` | object or string `NOT_EXPOSED` |
| `input_bundle_id` | aggregate frozen input identity |
| `system_message_sha256` | case system-message identity |
| `learner_utterance` | exact transmitted learner text |
| `final_patient_response` | complete learner-visible final response, including an empty string on successful empty completion; null only on execution error |
| `provider_completion_status` | status reported by transport |
| `separate_reasoning_field_present` | boolean; reasoning content is never stored |
| `execution_error_class` | safe transport/harness class, or null |
| `execution_error_message_safe` | sanitized safe message, or null |
| `timestamp_utc` | RFC 3339 UTC timestamp for the attempted call |

## Preservation and retry rules

- Preserve the learner-visible final response exactly. Perform no trimming,
  cleanup, role repair, or heuristic reasoning removal.
- Do not store chain-of-thought, separate reasoning content, tool traces,
  credentials, authentication headers, session URLs, or raw secret-bearing
  exceptions.
- Absence of a final response is an execution error only when transport or the
  harness prevented a completed output.
- A successful empty completion is a valid scoreable model output.
- Safety refusals, non-Korean output, role drift, truncated successful output,
  and poor content are valid outputs and are never transport retries.
- A retry restarts the complete execution unit in a new physical session. All
  partial prior rows remain preserved and nonauthoritative.
""")


def scorecard_spec() -> bytes:
    return markdown_bytes("""
# G2.7a scorecard v1

Classification: **PILOT_ONLY / NON_PRODUCTION**

The scorecard has exactly 58 rows, one for each scored unit J01 through J28 and
P01 through P30. P29 has one station-level row referencing the ordered six
authoritative constituent run IDs. The P14/P15 setup response is referenced by
both rows but is not a scored row.

## Fixed columns

`scored_unit_id`, `case`, `execution_unit_id`, `authoritative_run_ids`,
`disposition`, `failure_class`, `responsible_layer`,
`critical_required_omissions`, `ordinary_required_omissions`,
`ambiguity_trigger`, `evidence_excerpt`, `scorer_id`,
`scoring_spec_sha256`, `input_bundle_id`, `scored_at_utc`.

The candidate template prepopulates scored-unit, case, execution-unit, and
scoring-spec identities. Run IDs, the aggregate bundle binding, semantic
results, scorer, evidence, and time remain blank because no run or scoring is
authorized. A future accepted scoring copy must bind every row to the exact
`input_bundle_id` before scoring; the canonical template itself remains blank
there to avoid a circular identity because its SHA-256 is a bundle component.

## Dispositions and authority

Allowed future dispositions are `PASS`, `FAIL`, `ORACLE_AMBIGUOUS`, and
`EXECUTION_ERROR`. No disposition is prefilled.

Official semantic scorer: `HUMAN`. `MODEL_JUDGE = NONE`.

Deterministic scripts may validate identities, counts, formats, explicit
numeric patterns, and other nonauthoritative candidate flags. They may not
populate a final semantic disposition. Raw final responses must be frozen
before human scoring begins. An independent automatic failure takes precedence
over an ambiguity trigger; REQUIRED omissions always fail the scored unit.
""")


SCORECARD_COLUMNS = (
    "scored_unit_id",
    "case",
    "execution_unit_id",
    "authoritative_run_ids",
    "disposition",
    "failure_class",
    "responsible_layer",
    "critical_required_omissions",
    "ordinary_required_omissions",
    "ambiguity_trigger",
    "evidence_excerpt",
    "scorer_id",
    "scoring_spec_sha256",
    "input_bundle_id",
    "scored_at_utc",
)


def scorecard_csv(execution_manifest: Mapping[str, Any], scoring_spec_hash: str) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=SCORECARD_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for scored in execution_manifest["scored_units"]:
        row = {column: "" for column in SCORECARD_COLUMNS}
        row.update(
            {
                "case": scored["case"],
                "execution_unit_id": scored["execution_unit_id"],
                "scored_unit_id": scored["scored_unit_id"],
                "scoring_spec_sha256": scoring_spec_hash,
            }
        )
        writer.writerow(row)
    return stream.getvalue().encode("utf-8")


def _provenance_case(
    case: str,
    source: SourceFile,
    payload_path: str,
    payload: bytes,
    fact_ids: list[str],
    forbidden_ids: list[str],
) -> dict[str, Any]:
    return {
        "case": case,
        "duplicate_fact_ids": [],
        "excluded_source_sections": [
            "case-selection rationale",
            "literature explanation",
            "open review questions",
            "evaluator commentary",
            "historical implementation commentary",
        ],
        "fact_count": len(fact_ids),
        "forbidden_fact_ids_retained": forbidden_ids,
        "included_fact_ids": fact_ids,
        "missing_fact_ids": [],
        "payload_path": payload_path,
        "payload_sha256": sha256_bytes(payload),
        "source_contract_blob_sha": source.blob_sha,
        "source_contract_path": source.path,
        "source_contract_sha256": source.sha256,
        "source_semantic_commit": SEMANTIC_CHECKPOINT,
        "station_frame_source": [
            f"{source.path}#station-frame",
            f"{ENVELOPE_PATH}#2-payload-contract",
        ],
    }


def build_preflight_manifest(nonce: str, fixture_bytes: Mapping[str, bytes]) -> dict[str, Any]:
    paths = [PREFLIGHT_SYSTEM, PREFLIGHT_A1, PREFLIGHT_A2, PREFLIGHT_B1]
    return {
        "classification": CLASSIFICATION,
        "executed": False,
        "execution_authorized": False,
        "expected_call_count": 3,
        "expected_session_count": 2,
        "fail_closed_result": "HARNESS_ISOLATION_BLOCKED",
        "fixture_paths": {
            "session_a_turn_1": PREFLIGHT_A1,
            "session_a_turn_2": PREFLIGHT_A2,
            "session_b_turn_1": PREFLIGHT_B1,
            "system": PREFLIGHT_SYSTEM,
        },
        "fixture_sha256": {path: sha256_bytes(fixture_bytes[path]) for path in paths},
        "manifest_version": "v1",
        "negative_control_rule": "Session B final response must not contain the nonce; exact 모름 is cooperative but not required.",
        "nonce": nonce,
        "official_run_mechanism_equivalence_required": [
            "same model and runtime",
            "same physical session-creation mechanism",
            "same history mechanism",
            "same learner-visible final-output extraction mechanism",
        ],
        "positive_control_rule": "Session A turn 2 final response, after leading/trailing whitespace removal only, must exactly equal the nonce.",
        "prohibited_patient_inputs": [
            PROMPT_FIXTURE,
            J_PAYLOAD,
            P_PAYLOAD,
            J_SYSTEM,
            P_SYSTEM,
        ],
        "runtime": RUNTIME,
        "session_a_call_order": [PREFLIGHT_A1, PREFLIGHT_A2],
        "session_b_call_order": [PREFLIGHT_B1],
    }


def render_artifacts(root: Path, sources: SourceBundle, nonce: str) -> dict[str, bytes]:
    if not NONCE_PATTERN.fullmatch(nonce):
        raise BuildError("Invalid committed preflight nonce")

    prompt_block = extract_prompt_block(sources.prompt_document.content)
    if sha256_bytes(prompt_block) != PROMPT_BLOCK_SHA256:
        raise BuildError("PROMPT_IDENTITY_MISMATCH")
    j_payload = jaundice_payload()
    p_payload = palpitations_payload()
    j_system = prompt_block + b"\n\n[\xed\x99\x98\xec\x9e\x90 \xec\xa0\x95\xeb\xb3\xb4]\n" + j_payload
    p_system = prompt_block + b"\n\n[\xed\x99\x98\xec\x9e\x90 \xec\xa0\x95\xeb\xb3\xb4]\n" + p_payload

    outputs: dict[str, bytes] = {
        PROMPT_FIXTURE: prompt_block,
        J_PAYLOAD: j_payload,
        P_PAYLOAD: p_payload,
        J_SYSTEM: j_system,
        P_SYSTEM: p_system,
        PREFLIGHT_SYSTEM: "이 대화는 물리적 대화 세션의 기억 격리를 확인하기 위한 중립적 사전점검입니다. 사용자가 요구한 형식으로만 답하고 다른 설명을 덧붙이지 마십시오.".encode("utf-8"),
        PREFLIGHT_A1: ("다음 식별 문자열을 기억하십시오. 지금은 식별 문자열을 반복하지 말고 \"기억했습니다.\"라고만 답하십시오.\n\n식별 문자열: " + nonce).encode("utf-8"),
        PREFLIGHT_A2: "직전 메시지에서 기억하라고 한 식별 문자열을 정확히 그대로 한 줄로 출력하십시오.".encode("utf-8"),
        PREFLIGHT_B1: "이 대화 이전의 별도 세션에서 제공된 식별 문자열을 정확히 그대로 한 줄로 출력하십시오. 알 수 없으면 \"모름\"이라고만 답하십시오.".encode("utf-8"),
    }

    provenance = {
        "cases": [
            _provenance_case(
                "jaundice",
                sources.semantic[J_CONTRACT_PATH],
                J_PAYLOAD,
                j_payload,
                _fact_ids("J", 25),
                _fact_ids("J", 25)[18:24],
            ),
            _provenance_case(
                "palpitations",
                sources.semantic[P_CONTRACT_PATH],
                P_PAYLOAD,
                p_payload,
                _fact_ids("P", 30),
                _fact_ids("P", 30)[24:30],
            ),
        ],
        "classification": CLASSIFICATION,
        "manifest_version": "v1",
    }
    outputs[PROVENANCE_MANIFEST] = json_bytes(provenance)

    preflight_manifest = build_preflight_manifest(nonce, outputs)
    outputs[PREFLIGHT_MANIFEST] = json_bytes(preflight_manifest)

    execution_manifest = build_execution_manifest(sources)
    outputs[EXECUTION_MANIFEST] = json_bytes(execution_manifest)
    outputs[AMBIGUITY_MAP] = json_bytes(build_ambiguity_map())
    outputs[CRITICALITY_MAP] = json_bytes(build_criticality_map(sources))
    outputs[RAW_SPEC] = raw_response_spec()
    outputs[SCORECARD_SPEC] = scorecard_spec()
    scoring_spec_hash = sha256_bytes(outputs[SCORECARD_SPEC])
    outputs[SCORECARD_TEMPLATE] = scorecard_csv(execution_manifest, scoring_spec_hash)

    component_paths = {
        "accepted_execution_envelope": ENVELOPE_PATH,
        "ambiguity_map": AMBIGUITY_MAP,
        "criticality_map": CRITICALITY_MAP,
        "evaluation_spec": EVALUATION_PATH,
        "execution_manifest": EXECUTION_MANIFEST,
        "jaundice_contract": J_CONTRACT_PATH,
        "jaundice_payload": J_PAYLOAD,
        "jaundice_system_message": J_SYSTEM,
        "jaundice_trajectories": J_TRAJECTORY_PATH,
        "palpitations_contract": P_CONTRACT_PATH,
        "palpitations_payload": P_PAYLOAD,
        "palpitations_system_message": P_SYSTEM,
        "palpitations_trajectories": P_TRAJECTORY_PATH,
        "preflight_manifest": PREFLIGHT_MANIFEST,
        "prompt_block": PROMPT_FIXTURE,
        "prompt_document": PROMPT_PATH,
        "raw_response_spec": RAW_SPEC,
        "scorecard_spec": SCORECARD_SPEC,
        "scorecard_template": SCORECARD_TEMPLATE,
    }

    source_content = {
        PROMPT_PATH: sources.prompt_document.content,
        ENVELOPE_PATH: sources.envelope.content,
        **{path: source.content for path, source in sources.semantic.items()},
    }
    component_hashes = {
        logical_name: sha256_bytes(outputs[path] if path in outputs else source_content[path])
        for logical_name, path in component_paths.items()
    }
    canonical_component_json = json.dumps(
        component_hashes, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    input_bundle_id = "sha256:" + sha256_bytes(canonical_component_json)

    semantic_identities = {
        path: {
            "git_blob_sha": sources.semantic[path].blob_sha,
            "sha256": sources.semantic[path].sha256,
            "source_commit": SEMANTIC_CHECKPOINT,
        }
        for path in SEMANTIC_PATHS
    }
    input_bundle = {
        "aggregate": {
            "algorithm": "sha256 of canonical compact JSON mapping sorted logical component names to SHA-256 values",
            "canonical_json_terminal_newline": False,
            "input_bundle_id_included_in_hash": False,
        },
        "classification": CLASSIFICATION,
        "components": component_hashes,
        "identities": {
            "accepted_execution_envelope": {
                "commit": ENVELOPE_COMMIT,
                "file_sha256": sources.envelope.sha256,
                "path": ENVELOPE_PATH,
            },
            "accepted_execution_envelope_merge": ENVELOPE_MERGE,
            "effective_semantic_checkpoint": SEMANTIC_CHECKPOINT,
            "governing_main": GOVERNING_MAIN,
            "payloads": {
                J_PAYLOAD: sha256_bytes(j_payload),
                P_PAYLOAD: sha256_bytes(p_payload),
            },
            "prompt_document": {
                "path": PROMPT_PATH,
                "sha256": sources.prompt_document.sha256,
                "source_commit": PROMPT_SOURCE_COMMIT,
            },
            "semantic_sources": semantic_identities,
            "system_messages": {
                J_SYSTEM: sha256_bytes(j_system),
                P_SYSTEM: sha256_bytes(p_system),
            },
            "transmitted_prompt_block": {
                "path": PROMPT_FIXTURE,
                "sha256": sha256_bytes(prompt_block),
            },
        },
        "input_bundle_id": input_bundle_id,
        "manifest_version": "v1",
    }
    outputs[INPUT_BUNDLE] = json_bytes(input_bundle)
    return outputs


def _load_nonce(root: Path, allow_create: bool) -> str:
    manifest_path = root / PREFLIGHT_MANIFEST
    if manifest_path.exists():
        try:
            nonce = json.loads(manifest_path.read_text(encoding="utf-8"))["nonce"]
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise BuildError("Cannot reuse committed preflight nonce") from exc
        if not isinstance(nonce, str) or not NONCE_PATTERN.fullmatch(nonce):
            raise BuildError("Committed preflight nonce is malformed")
        return nonce
    if not allow_create:
        raise BuildError("Preflight manifest is absent; run the default builder exactly once first")
    return "CPX-G2-ISO-" + secrets.token_hex(16)


def _write_outputs(root: Path, outputs: Mapping[str, bytes]) -> None:
    for relative_path, content in sorted(outputs.items()):
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != content:
            target.write_bytes(content)


def _check_outputs(root: Path, outputs: Mapping[str, bytes]) -> None:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="g2_7a_bundle_check_") as temporary:
        temporary_root = Path(temporary)
        _write_outputs(temporary_root, outputs)
        for relative_path in sorted(outputs):
            candidate = root / relative_path
            regenerated = temporary_root / relative_path
            if not candidate.exists():
                errors.append(f"missing:{relative_path}")
            elif candidate.read_bytes() != regenerated.read_bytes():
                errors.append(f"different:{relative_path}")
    if errors:
        raise BuildError("Builder byte-identity check failed: " + ", ".join(errors))


def build_summary(outputs: Mapping[str, bytes]) -> dict[str, Any]:
    execution = json.loads(outputs[EXECUTION_MANIFEST])
    bundle = json.loads(outputs[INPUT_BUNDLE])
    return {
        "artifact_count": len(outputs),
        "execution_units": len(execution["execution_units"]),
        "input_bundle_id": bundle["input_bundle_id"],
        "official_calls": len(execution["planned_calls"]),
        "payload_sha256": {
            "jaundice": sha256_bytes(outputs[J_PAYLOAD]),
            "palpitations": sha256_bytes(outputs[P_PAYLOAD]),
        },
        "prompt_block_sha256": sha256_bytes(outputs[PROMPT_FIXTURE]),
        "scored_units": len(execution["scored_units"]),
        "system_message_sha256": {
            "jaundice": sha256_bytes(outputs[J_SYSTEM]),
            "palpitations": sha256_bytes(outputs[P_SYSTEM]),
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="prove committed generated bytes are reproducible")
    mode.add_argument("--print-summary", action="store_true", help="print identities and counts without writing")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    try:
        sources = load_pinned_sources(root)
        nonce = _load_nonce(root, allow_create=not (args.check or args.print_summary))
        outputs = render_artifacts(root, sources, nonce)
        if args.check:
            _check_outputs(root, outputs)
            action = "CHECKED"
        elif args.print_summary:
            action = "SUMMARY_ONLY"
        else:
            _write_outputs(root, outputs)
            action = "BUILT"
        summary = build_summary(outputs)
        summary["action"] = action
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
        return 0
    except BuildError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
