# G2 structural pre-batch audit disposition

Date: 2026-09-03
Status: **PROPOSED / NOT YET ACCEPTED**

This record is the project's explicit treatment of the findings in
`docs/pilot/g2-structural-prebatch-audit.md`. It authorizes only the authoring
of a corrected versioned execution envelope. It does not accept that envelope,
does not authorize fixtures or a runner, and does not authorize execution.

Audit verdict being dispositioned: `REVISION_REQUIRED` — 1 blocker, 6 major
findings, 10 minor/nonblocking findings, architecture direction
`KEEP_MINIMAL_EXECUTION_DESIGN`.

## Accepted

Accepted without modification:

1. The P29 accounting correction.
2. Exact transmitted-prompt extraction and hashing.
3. Explicit station-frame payload requirements.
4. Explicit scorer declaration.
5. Execution-error and retry rules.
6. Positive and negative session-isolation controls.
7. Post-run session-identifier uniqueness.
8. The setup-turn versus scored-turn partition.
9. Oracle and evaluation identity pinning.
10. Final-response extraction rules.
11. Input-reproducibility qualification.
12. Minimum-eligibility semantics for disclosure tiers.
13. The requirement that hidden and forbidden facts remain represented in the
    payloads.

Item 13 is retained deliberately against the intuition that would remove it.
Dropping forbidden facts from a payload would reduce measured leakage while
destroying the constraint-adherence test that metrics 4 and 5 of
`docs/pilot/g2-evaluation-spec.md` exist to measure. Absence of opportunity is
not evidence of adherence.

## Accepted with modification — M3, omission and ambiguity

Finding M3 is accepted, with the treatment clarified as follows.

- Every missing REQUIRED information unit causes a per-scored-unit `FAIL`.
- The `critical` versus `ordinary` distinction affects **aggregate zero-target
  reporting only**, not the individual PASS/FAIL disposition.
- Ordinary REQUIRED omissions still fail their own trajectory.
- The future execution manifest must predeclare which REQUIRED units are
  `critical`, frozen before the first official call.
- Register and naturalness are **not scored** in this coverage phase.
- `ORACLE_AMBIGUOUS` is used only for a predeclared ambiguity trigger, and only
  when no independent automatic `FAIL` exists.

The modification resolves a real conflict in the evaluation specification's
reporting structure. That specification thresholds only the critical class and
deliberately leaves ordinary omission unthresholded pending baseline
distributions. Read carelessly, that could be taken to mean an ordinary
omission has no per-unit consequence. It does: the absent threshold governs the
aggregate report, never the individual disposition. An unthresholded aggregate
must not silently promote a failing unit to `PASS` or divert it to
`ORACLE_AMBIGUOUS`.

## P29 local pilot ruling

For this pilot only:

- the active P29 behavior remains "the patient does not prompt examination or
  ECG";
- any direct or indirect patient suggestion that the learner check the pulse,
  perform an examination, obtain an ECG, or order an investigation is `FAIL`;
- generic worry or concern **without** a suggested learner action is not
  prompting and is not a failure;
- final production and SP-methodology acceptance of the underlying question
  remains pending.

This local pilot disposition is **not** `ORACLE_AMBIGUOUS`. The distinction
matters and is narrow. Open contract question 6 for the palpitations case asks a
reviewer to confirm the *station design* — whether a silent SP is the right
standardized behavior at all. That question stays open. It does not make the
*scoring* of an observed prompting response indeterminate, because the
trajectory oracle already forbids prompting explicitly and the supporting
rationale is evidence-backed: an SP who prompts would mask the exact deficit
the station is built to detect.

Unresolved clinical judgement is not being converted into an engineering
decision here. The engineering decision is only which of two already-authored
treatments applies to a scored response, and the oracle answers that.

## Historical disposition headers

A historical disposition is **not** rewritten merely because its original
header says `PROPOSED`.

`docs/pilot/g2.1a-language-oracle-disposition.md` and
`docs/pilot/g2.1b-oracle-clarification-disposition.md` retain their original
headers as authored. Current acceptance authority is carried by
`docs/CURRENT_STATE.md` and by the accepted merge and checkpoint records it
names — not by a header string inside a historical file. Normalizing those
headers would rewrite accepted historical evidence to match later state, which
the repository invariants forbid.

## Auditor identity provenance

The structural pre-batch audit's model/provider identity is dispositioned as
follows.

- The original structural-audit model/provider **cannot be independently
  verified from repository state**.
- No model/provider identity will be inferred or retroactively fabricated.
- This limitation is explicitly **accepted as provenance metadata**. It does
  not alter the reproduced findings and does not alter the corrected envelope.
- If the repository owner later supplies a certain first-hand attestation, it
  must be recorded as `OWNER_ATTESTED`, never as `REPOSITORY_VERIFIED`.
- Acceptance of the v1 envelope does **not** depend on guessing the auditor
  model.

The distinction between `OWNER_ATTESTED` and `REPOSITORY_VERIFIED` is kept
because the two carry different evidential weight. A verifiable identity is
reproducible from committed state by any later reader; an owner attestation is
a first-hand claim recorded on trust. Collapsing them would make the weaker
claim indistinguishable from the stronger one in every later reading.

`docs/pilot/g2-structural-prebatch-audit.md` is **not** rewritten. It remains
immutable historical evidence, including its recorded
`NOT_VERIFIABLE_FROM_REPOSITORY_STATE` value. The subsequent v1 delta audit,
`docs/pilot/g2.7a-execution-envelope-v1-delta-audit.md`, carries a fully
repository-pinned base and target and names its auditor.

## Explicit scope

This disposition makes:

| Change | Status |
|---|---|
| Prompt change | none |
| Case-truth change | none |
| Trajectory change | none |
| Evaluation-spec change | none |
| Model call | none |
| Scorer model | none |
| Fixture or payload snapshot | none |
| Runner | none |
| Architecture escalation | none |
| Execution authorization | none |

## Next step

The corrected envelope authored under this disposition is
`docs/pilot/g2.7a-isolated-full-coverage-envelope-v1.md`, status
`PROPOSED / NOT YET ACCEPTED`.

It requires an independent read-only delta/final-state audit and explicit
acceptance before fixtures, payload snapshots, or a runner become eligible.
Acceptance of this disposition does not accept that envelope.
