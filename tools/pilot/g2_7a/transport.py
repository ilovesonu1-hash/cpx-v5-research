"""Minimal transport contract and in-memory fake for the G2.7a pilot.

PILOT_ONLY / NON_PRODUCTION.  No real transport adapter is implemented here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Protocol, Sequence


@dataclass(frozen=True)
class TransportResponse:
    """Only transport metadata and the learner-visible final field."""

    safe_session_id: str
    final_response: str
    completion_status: str
    separate_reasoning_field_present: bool


class TransportError(RuntimeError):
    """A safe, retryable transport/harness failure with no completed output."""

    def __init__(self, error_class: str, safe_message: str) -> None:
        super().__init__(safe_message)
        self.error_class = error_class
        self.safe_message = safe_message


class Session(Protocol):
    @property
    def safe_session_id(self) -> str:
        ...

    def send(self, user_message: str) -> TransportResponse:
        ...

    def close(self) -> None:
        ...


class Transport(Protocol):
    def create_session(self, system_message: str, runtime: str) -> Session:
        """Create one physically new session with exactly one system message."""
        ...


@dataclass
class FakeCall:
    safe_session_id: str
    turn_index: int
    user_message: str


@dataclass
class FakeSessionState:
    safe_session_id: str
    system_message: str
    runtime: str
    turns: list[str] = field(default_factory=list)
    remembered_nonce: str | None = None
    closed: bool = False


FakeOutcome = str | TransportResponse | TransportError | Exception
LifecycleOutcome = TransportError | Exception | None
ResponseFactory = Callable[[FakeSessionState, str], FakeOutcome]


class FakeSession:
    def __init__(self, owner: "FakeTransport", state: FakeSessionState) -> None:
        self._owner = owner
        self._state = state

    @property
    def safe_session_id(self) -> str:
        return self._state.safe_session_id

    def send(self, user_message: str) -> TransportResponse:
        if self._state.closed:
            raise TransportError("SESSION_CLOSED", "fake session is already closed")
        self._state.turns.append(user_message)
        self._owner.calls.append(
            FakeCall(
                safe_session_id=self.safe_session_id,
                turn_index=len(self._state.turns),
                user_message=user_message,
            )
        )
        outcome = self._owner.next_outcome(self._state, user_message)
        if isinstance(outcome, TransportError):
            raise outcome
        if isinstance(outcome, Exception):
            raise outcome
        if isinstance(outcome, TransportResponse):
            if outcome.safe_session_id != self.safe_session_id:
                raise TransportError("SESSION_ID_MISMATCH", "fake response used another session identifier")
            return outcome
        return TransportResponse(
            safe_session_id=self.safe_session_id,
            final_response=outcome,
            completion_status="completed",
            separate_reasoning_field_present=False,
        )

    def close(self) -> None:
        if not self._state.closed:
            self._owner.close_attempted_session_ids.append(self.safe_session_id)
            outcome = self._owner.next_close_outcome()
            if isinstance(outcome, Exception):
                raise outcome
            self._state.closed = True
            self._owner.closed_session_ids.append(self.safe_session_id)


class FakeTransport:
    """Deterministic process-local fake; it never touches network or subprocesses."""

    def __init__(
        self,
        scripted_outcomes: Sequence[FakeOutcome] | None = None,
        response_factory: ResponseFactory | None = None,
        create_session_outcomes: Sequence[LifecycleOutcome] | None = None,
        close_outcomes: Sequence[LifecycleOutcome] | None = None,
    ) -> None:
        self._scripted_outcomes = list(scripted_outcomes or ())
        self._response_factory = response_factory
        self._create_session_outcomes = list(create_session_outcomes or ())
        self._close_outcomes = list(close_outcomes or ())
        self._session_counter = 0
        self.create_session_attempts = 0
        self.sessions: dict[str, FakeSessionState] = {}
        self.created_session_ids: list[str] = []
        self.close_attempted_session_ids: list[str] = []
        self.closed_session_ids: list[str] = []
        self.calls: list[FakeCall] = []

    def create_session(self, system_message: str, runtime: str) -> FakeSession:
        self.create_session_attempts += 1
        if self._create_session_outcomes:
            outcome = self._create_session_outcomes.pop(0)
            if isinstance(outcome, Exception):
                raise outcome
        self._session_counter += 1
        safe_session_id = f"fake-session-{self._session_counter:03d}"
        state = FakeSessionState(
            safe_session_id=safe_session_id,
            system_message=system_message,
            runtime=runtime,
        )
        self.sessions[safe_session_id] = state
        self.created_session_ids.append(safe_session_id)
        return FakeSession(self, state)

    def next_outcome(self, state: FakeSessionState, user_message: str) -> FakeOutcome:
        if self._scripted_outcomes:
            return self._scripted_outcomes.pop(0)
        if self._response_factory is not None:
            return self._response_factory(state, user_message)
        return self._neutral_memory_response(state, user_message)

    def next_close_outcome(self) -> LifecycleOutcome:
        if self._close_outcomes:
            return self._close_outcomes.pop(0)
        return None

    @staticmethod
    def _neutral_memory_response(state: FakeSessionState, user_message: str) -> str:
        nonce_match = re.search(r"CPX-G2-ISO-[0-9a-f]{32}", user_message)
        if nonce_match:
            state.remembered_nonce = nonce_match.group(0)
            return "기억했습니다."
        if "직전 메시지" in user_message and state.remembered_nonce is not None:
            return state.remembered_nonce
        if "별도 세션" in user_message:
            return "모름"
        return "FAKE_RESPONSE"


__all__ = [
    "FakeCall",
    "FakeSessionState",
    "FakeTransport",
    "Session",
    "Transport",
    "TransportError",
    "TransportResponse",
]
