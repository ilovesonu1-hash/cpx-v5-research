# CPX v5 current state

## Scope

This file owns only the present phase, the effective checkpoint, current
gate/readiness state, blockers, active artifact identities, and the next
permitted action.

It does not own detailed behavior, oracle definitions, evidence extraction,
audit prose, or historical narrative. Use `AGENTS.md` to route a task to its
active normative owner.

## Canonical checkpoint

| Field | Current value |
|---|---|
| Repository | `ilovesonu1-hash/cpx-v5-research` |
| Default branch | `main` |
| Effective pilot semantic checkpoint | `e1db18d0ef9e7cec931837389875b719e9250da4` |
| Checkpoint parent | `9d88c9d4c364960b5fa12c9c9ee8c278cdedcc0e` |
| Checkpoint role | G2.1a language and oracle correction |
| Governance bootstrap | **PROPOSED / NOT YET ACCEPTED** on branch `governance/claude-context-bootstrap` |

The governance bootstrap that introduced `CLAUDE.md`, `AGENTS.md`, and this file
is a review candidate. It becomes effective only after independent review and an
accepted merge to `main`.

## Current phase and gate state

| Gate | State |
|---|---|
| `G1_RESEARCH_EXPANSION` | `PAUSED` |
| `G1_PRODUCT_BASELINE` | `REACHED` |
| `G2_CONTRACTS` | `EXECUTABLE_AS_PROVISIONAL_GOLD` |
| `G2_1A_LANGUAGE_ORACLE_PATCH` | `COMPLETE` |
| `G2_PROMPT_V0_1` | `FROZEN_UNCHANGED` |
| `G2_SMALL_PROBE` | `COMPLETE_WITH_ERRATUM` |
| `G2_FULL_COVERAGE` | `NOT_EXECUTED` |
| `SESSION_ISOLATION_BASELINE` | `NOT_ESTABLISHED` |
| `ARCHITECTURE_ESCALATION` | `NOT_JUSTIFIED` |
| `PRODUCTION_IMPLEMENTATION_AUTHORIZED` | `NO` |

No clinician or SP-educator acceptance has occurred. "Provisional gold" means
executable as a test oracle, not accepted by a domain expert.

## Active artifact owners

All paths below are at the effective semantic checkpoint above. Only the system
prompt carries a separately pinned byte identity, because it is frozen against a
completed probe.

| Path | Role | Class |
|---|---|---|
| `docs/pilot/sp-system-prompt-v0.1.md` | generic SP behavioral prompt, frozen | active normative |
| `docs/pilot/jaundice-behavior-contract.md` | jaundice case truth, knowledge, disclosure eligibility, forbidden set | active normative |
| `docs/pilot/palpitations-behavior-contract.md` | palpitations case truth, knowledge, disclosure eligibility, forbidden set | active normative |
| `docs/pilot/jaundice-trajectories.md` | jaundice gold trajectory oracle | active normative |
| `docs/pilot/palpitations-trajectories.md` | palpitations gold trajectory oracle | active normative |
| `docs/pilot/g2-evaluation-spec.md` | metrics, scoring rules, provisional thresholds | active normative |
| `docs/pilot/g2.1a-language-oracle-disposition.md` | accepted treatment of the language and oracle audit | disposition record |
| `docs/pilot/g2.1-contract-review.md` | contract executability review and open expert questions | historical evidence |
| `docs/pilot/g2.2-probe-results.md` | small-probe raw evidence, aggregate, and erratum | historical evidence |
| `docs/pilot/g2-plan.md` | G2 phase sequence and architecture restraint | active normative |
| `docs/research/g1-product-baseline.md` | product-evidence baseline and research-expansion policy | active normative |
| `docs/research/g1-status.md` | historical publication-style G1 record, expansion paused | historical evidence |

Frozen system-prompt identity:

- source commit: `997e5200370ee5f5823af4c24b86c5d62f4625ee`
- SHA-256: `373351AAA9D254E42A88C0DAF209124FEFB3FF59FC59571095345E28EA451D72`

Both were verified against the working file at the effective checkpoint.

## Current evidence and result summary

| Quantity | Value |
|---|---:|
| Evidence-matrix candidate records | 54 |
| Pilot cases | 2 |
| Jaundice case facts | 25 |
| Palpitations case facts | 30 |
| Jaundice trajectories | 28 |
| Palpitations trajectories | 30 |
| Total trajectories | 58 |
| Historical official small-probe calls | 12 |

Corrected small-probe disposition:

| Disposition | Count |
|---|---:|
| PASS | 11 |
| FAIL | 0 |
| ORACLE_AMBIGUOUS | 1 |
| EXECUTION_ERROR | 0 |

P25 is the single `ORACLE_AMBIGUOUS` result. The response invented no numerical
pulse rate, so the exact-rate safety boundary held. Patient-perceived rhythm
regularity remains unauthored, so the responsible layer is the contract and
oracle, not the prompt and not the architecture.

## Current unresolved human questions

Carried forward from `docs/pilot/g2.1a-language-oracle-disposition.md` and still
open:

1. Patient-perceived rhythm regularity.
2. Patient-originated hedged cancer fear.
3. Whether `황달` is always acceptable as lay symptom language.
4. Final age and register guidance for both synthetic patients.
5. Whether alcohol minimisation should later be a separately authored
   deterministic trajectory.
6. Whether voluntary herbal disclosure under a generic medication question needs
   a standardized rule in a future high-stakes station.

Any future output whose scoring depends on one of these must be recorded
`ORACLE_AMBIGUOUS` rather than forced into PASS or FAIL until it is adjudicated.

Broader clinician and SP-methodology questions remain listed in
`docs/pilot/g2.1-contract-review.md`.

## Next permitted sequence

Each step is *eligible*, not authorized. Completing one does not start the next.

1. Independent read-only final-state or delta audit of the G2.1a correction.
2. If that audit is accepted, an independent structural pre-batch audit.
3. If that audit accepts an exact isolated execution envelope, prepare frozen
   pilot payloads and fixtures.
4. Only after explicit acceptance of that envelope may the isolated
   58-trajectory coverage run begin.

The governance bootstrap itself requires independent review before merging.

## Explicitly unauthorized

- Modifying SP system prompt v0.1.
- Full-suite execution before an accepted structural audit and execution
  envelope.
- Production schema design or disclosure enum freeze.
- Any change to cpx-v4.
- Any change to `CPX_SOURCE_ROOT`.
- Production scenario dataset migration.
- SP2D import.
- Model adjudication of pending SP2D.6 labels.
- Model or provider comparison, or automatic substitution.
- Broad G1 literature expansion.
- Architecture escalation.
- Merging `design/frontend-v5`.
- Production deployment.

## Concurrent-work boundary

`design/frontend-v5` is concurrent independent work. Its commits must not be
mixed into pilot or governance commits, and integrating it requires an explicit
later task.
