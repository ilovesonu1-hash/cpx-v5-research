# G2 structural pre-batch audit

Date: 2026-09-03
Status: **IMMUTABLE HISTORICAL AUDIT EVIDENCE**

This record preserves the findings of the completed independent structural
pre-batch audit. It is evidence and provenance, not current status and not an
authorization. It is not rewritten to match later state. Its findings become
active only through an explicit disposition and an authorized normative patch.

## Identity

| Field | Value |
|---|---|
| Audit target commit | `c02ab75aa30c6c68899f3db65a9391882bfa7258` |
| Effective pilot semantic checkpoint at audit time | `33cca3781b301c29af965430c3caaf32378c28ff` |
| Mode | independent read-only |
| Domain | batch structure |
| Model calls made by the audit | 0 |
| Verdict | `REVISION_REQUIRED` |
| Blockers | 1 |
| Major findings | 6 |
| Minor / nonblocking findings | 10 |
| Architecture direction | `KEEP_MINIMAL_EXECUTION_DESIGN` |
| Fable audit | deferred |

Fable auditing remains deferred by the standing user decision recorded in
`docs/governance/context-bootstrap-audit-disposition.md`. This audit was not a
Fable audit and not a cross-model audit.

### Auditor identity limitation

The auditing session's model and provider identity is **not verifiable from
repository state**. The audit was delivered as a chat/task-issued result rather
than as a session-attested artifact, and no session metadata for the auditing
run was committed at or before the target commit.

Recorded honestly rather than guessed:

| Field | Value |
|---|---|
| Auditing session model/provider | `NOT_VERIFIABLE_FROM_REPOSITORY_STATE` |
| This record authored by | Codex CLI session, model `claude-opus-5` |
| Authoring session model calls against the patient model | 0 |

Prior accepted audits in this repository name their auditor explicitly, for
example the G2.1b delta audit recorded in `docs/CURRENT_STATE.md`. The auditor
identity for **this** audit must be supplied by the repository owner before the
disposition is accepted. Until then the gap is a known provenance limitation of
this record, not an omission to be filled by inference.

## Envelope provenance limitation

This is the most consequential provenance fact in this record.

- The audited execution envelope was a **user/chat-issued pre-batch
  specification**.
- It was **not** previously committed as a versioned repository artifact.
- The audit target commit `c02ab75a` pinned the governing contracts,
  trajectory oracles, evaluation specification, frozen prompt, and current
  state, but it **did not by itself pin every byte of the audited envelope**.
- Therefore the audited envelope has **no repository SHA**, and no such SHA may
  be asserted or reconstructed for it later.
- The corrected v1 envelope authored under the accompanying disposition,
  `docs/pilot/g2.7a-isolated-full-coverage-envelope-v1.md`, becomes the
  **first repository-pinned execution-envelope candidate**.

A consequence follows directly: findings below are reproducible against the
pinned contracts and oracles at `c02ab75a`, but the audited envelope text
itself is reproducible only as quoted inside this record.

## Findings

### Blocker

**B1 — P29 accounting could not reconcile.**

P29 was specified as a station-level scored unit spanning one-to-`k` learner
turns while the surrounding accounting model assumed one scored response per
trajectory.

- `k` was undefined.
- The station script was undefined.
- Trajectory counts, model-call counts, unscored setup-turn counts, and
  scorecard row counts could not be reconciled against each other.

With an undefined `k`, the planned run had no determinate call total, no
determinate session total, and no determinate scorecard shape. That is
disqualifying for an execution envelope regardless of the quality of the rest
of the specification.

### Major findings

| ID | Finding |
|---|---|
| M1 | The transmitted prompt block was not separately pinned. Only the prompt **document** carried an identity, while the substring actually sent to the patient model did not. |
| M2 | Payload requirements did not explicitly include station-frame identity, although J02/P02 and the configured opening behavior depend on it. |
| M3 | Ambiguity and trajectory disposition rules were under-specified, including the interaction between REQUIRED-unit omission, the critical/ordinary distinction, and `ORACLE_AMBIGUOUS`. |
| M4 | The scorer was unnamed. Neither scorer type, scorer identity, nor the boundary between deterministic tooling and semantic judgement was declared. |
| M5 | Execution-error and retry rules were under-specified. The boundary between a transport/harness failure and a valid but poor model output was not drawn, and no retry cap existed. |
| M6 | Isolation testing had no positive control and no post-run session-uniqueness invariant. A negative result alone cannot distinguish real isolation from a harness that fails to recall anything. |

### Minor / nonblocking findings

Ten minor findings were recorded. They did not individually block advancement
and are carried as clarifications absorbed by the corrected envelope:

1. Scored unit, execution unit, model call, response record, and physical
   session were used interchangeably in places.
2. Sequence-group membership was described narratively rather than enumerated
   as frozen groups.
3. The P14/P15 duration setup utterance was referenced but not fixed verbatim.
4. Raw-record field requirements were incomplete for post-hoc verification.
5. The final-response extraction channel was not specified, leaving hidden
   reasoning concatenation possible.
6. Oracle and evaluation-specification identities were not listed among the
   inputs to be pinned.
7. Reproducibility language risked implying deterministic replayability.
8. Disclosure tiers risked being read as mutually exclusive response channels
   rather than minimum eligibility.
9. Forbidden and hidden facts risked being dropped from payloads as a
   leakage-reduction measure, which would remove the constraint-adherence test.
10. Preflight activity was not separated from official run totals.

## Advancement result

| Question | Result |
|---|---|
| Fixture and runner implementation eligible? | No |
| Official 58-unit execution authorized? | No |
| Architecture escalation justified? | No — `KEEP_MINIMAL_EXECUTION_DESIGN` |
| Path forward | A corrected versioned envelope, then an independent delta audit, then explicit acceptance |

The audit found no evidence that a router, classifier, state machine, output
filter, orchestration layer, or retrieval system was required. Every blocker
and major finding was a specification defect absorbable by the execution
envelope itself, which is the smallest responsible layer.

An audit verdict does not authorize the next phase. This record authorizes
nothing.
