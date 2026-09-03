# G2.7a fixture and runner candidate v1 audit

Status: **IMMUTABLE HISTORICAL AUDIT EVIDENCE**

## Audit identity

| Field | Value |
|---|---|
| Base | `1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6` |
| Target | `f11df66df7fc12a860cc1beac76bcd53685f22f7` |
| Auditor | ChatGPT GPT-5.6 Pro |
| Access mode | GitHub-connected independent read-only static/delta review |
| Verdict | `REVISION_REQUIRED` |
| Blockers | 1 |
| Major findings | 4 |
| Minor findings | 2 |
| Local test execution by auditor | not performed |
| Model calls | 0 |

The audited implementation report recorded 157 deterministic checks, 23
in-memory tests, a reproducible second build, and a plan count of 58 scored
units / 64 calls / 48 sessions. Those were implementation-session results, not
results independently rerun by the auditor.

## Blocker B1 — self-expiring main validation

`build_bundle.py` named `1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6`
as `GOVERNING_MAIN`, and `validate_bundle.py` required live `origin/main` to
equal that exact commit. That condition passes on the review branch but
necessarily fails after an ordinary accepted merge advances `origin/main`.
The immutable review base must remain provenance, not a permanent condition on
the current remote tip.

## Major M1 — incomplete behavioral payload and weak provenance

The 25/30 case-truth inventories are present, and static review found no
obvious new medical fact. The transmitted payloads nevertheless omitted
case-specific response-scope behavior from accepted sources: leading
true-premise behavior, leading false-premise behavior for a known absence,
examination consent without reporting a finding, and the accepted local P29
no-prompt behavior. Payload provenance hardcoded empty missing and duplicate
arrays, proving ID coverage rather than semantic equivalence.

## Major M2 — session-creation lifecycle outside retry

`transport.create_session()` was outside the protected attempt block, so a
session-creation failure was neither retried nor preserved. A pre-call session
failure must be recorded as an execution-unit attempt event without fabricating
a patient-model raw-call row. Session-close failure also requires explicit,
safe treatment.

## Major M3 — no post-run record/session validator

The validator checked the planned manifest but not a future completed raw
record corpus for session-ID uniqueness across units, one session per
execution-unit attempt, a new session per retry, preflight/official session
disjointness, exactly one authoritative complete attempt, or planned-versus-
actual call correspondence.

## Major M4 — multi-turn score evidence not frozen

The manifest did not predeclare the exact ordered response evidence required
by each scorecard row. For example, J14 requires J07 and J14; J15 requires J07,
J14, and J15; P14 requires the setup response and P14; P15 requires setup,
P14, and P15; and P29 requires all six constituent responses.

## Minor findings

1. The inspected Claude CLI was not the target Gemini transport path. Target
   harness capability therefore remained unverified.
2. Future run records must bind execution-control provenance, including the
   accepted runner/adapter identity, execution authorization, and passing
   preflight evidence.

## Advancement

Candidate merge is not yet appropriate. A bounded correction is required; no
patient-model reprobe and no architecture escalation are required. Isolation
preflight and official execution remain unauthorized.
