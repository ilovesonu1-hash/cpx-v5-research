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
| Effective pilot semantic checkpoint | `33cca3781b301c29af965430c3caaf32378c28ff` |
| Checkpoint parent | `a1bc72238acc05b25d25f251c7d8b4a53dd8e506` |
| Checkpoint role | accepted G2.1b P25 oracle clarification |
| Governance bootstrap | **ACCEPTED / MERGED / EFFECTIVE** |

The governance bootstrap that introduced `CLAUDE.md`, `AGENTS.md`, and this file
is accepted and effective on `main`. Its governance checkpoint is recorded
separately from the pilot semantic checkpoint above.

| Governance field | Value |
|---|---|
| Accepted governance proposal | `ce254e5bb26906e1a6dd4dfe57d96e6cc8398bd8` |
| Original proposal | `e9f7200bb14f08ea325ec378a50489f0b7c62dd7` |
| Accepted merge commit | `43704a8e670d16fdd101d28a988acf8b96ec0089` |
| Independent bootstrap audit | `PASS_AFTER_MINOR_PATCH`, 0 blockers |
| Delta audit of the correction | `PASS`, 0 blockers, 0 major findings |
| Human acceptance | `RECORDED` |
| Accepted treatment | `docs/governance/context-bootstrap-audit-disposition.md` |

The governance acceptance itself changed no pilot semantics and authorized no
G2 execution. The later accepted G2.1b semantic checkpoint is recorded
separately above.

G2.1b acceptance record:

| Field | Value |
|---|---|
| Accepted proposal | `33cca3781b301c29af965430c3caaf32378c28ff` |
| Acceptance merge | `e734964521041a281c51c6bf6a1984c7ec4c013d` |
| Independent delta audit | ChatGPT GPT-5.6 Pro: `PASS`, 0 blockers, 0 major findings |
| Human acceptance | `RECORDED` |

## Current phase and gate state

| Gate | State |
|---|---|
| `G1_RESEARCH_EXPANSION` | `PAUSED` |
| `G1_PRODUCT_BASELINE` | `REACHED` |
| `G2_CONTRACTS` | `EXECUTABLE_AS_PROVISIONAL_GOLD` |
| `G2_1A_LANGUAGE_ORACLE_PATCH` | `COMPLETE` |
| `G2_1A_DELTA_AUDIT` | `REVISION_REQUIRED / HISTORICAL / CORRECTED_BY_G2_1B` |
| `G2_1B_ORACLE_CLARIFICATION` | `ACCEPTED / MERGED / EFFECTIVE` |
| `G2_PROMPT_V0_1` | `FROZEN_UNCHANGED` |
| `G2_SMALL_PROBE` | `COMPLETE_WITH_ERRATUM` |
| `G2_STRUCTURAL_PRE_BATCH_AUDIT` | `REVISION_REQUIRED / 1 BLOCKER / 6 MAJOR / 10 MINOR` |
| `G2_EXECUTION_ENVELOPE_V1` | `PROPOSED / NOT YET ACCEPTED` |
| `G2_EXECUTION_ENVELOPE_V1_DELTA_AUDIT` | `PASS_AFTER_MINOR_PATCH / 0 BLOCKERS / 0 MAJOR / 3 MINOR` |
| `G2_EXECUTION_ENVELOPE_V1_CORRECTION` | `PROPOSED / NOT YET ACCEPTED` |
| `G2_FIXTURE_RUNNER_IMPLEMENTATION` | `BLOCKED_PENDING_ENVELOPE_ACCEPTANCE` |
| `G2_FULL_COVERAGE` | `NOT_EXECUTED / UNAUTHORIZED` |
| `SESSION_ISOLATION_BASELINE` | `NOT_ESTABLISHED` |
| `ARCHITECTURE_ESCALATION` | `NOT_JUSTIFIED` |
| `PRODUCTION_IMPLEMENTATION_AUTHORIZED` | `NO` |

No clinician or SP-educator acceptance has occurred. "Provisional gold" means
executable as a test oracle, not accepted by a domain expert.

The structural pre-batch audit is complete and its verdict is recorded. Its
findings are treated in `docs/pilot/g2-structural-prebatch-disposition.md`,
which is `PROPOSED / NOT YET ACCEPTED`. The audited envelope was a chat-issued
specification with no repository SHA; the first repository-pinned
execution-envelope candidate is
`docs/pilot/g2.7a-isolated-full-coverage-envelope-v1.md`. Neither the
disposition nor the envelope is accepted, so no fixture, payload snapshot,
runner, or execution is eligible.

An independent GitHub-connected read-only delta audit by ChatGPT GPT-5.6 Pro of
`c02ab75a..1c831494` returned `PASS_AFTER_MINOR_PATCH` with 0 blockers, 0
major findings, and 3 minor findings. The substantive envelope was found
structurally acceptable, and the architecture direction remains
`KEEP_MINIMAL_EXECUTION_DESIGN`.

The exact authorized minor corrections are now **proposed** on the review
branch: the section-3 concept count, removal of one duplicated
retry-accounting paragraph, an added non-executable preflight-input-freezing
requirement, and the recorded auditor-identity provenance disposition.

No full re-audit is required if deterministic verification confirms that no
other semantic content changed. Human acceptance and merge remain required.
Fixture and runner implementation remains blocked, and full execution remains
unauthorized.

## Active artifact owners

Pilot and research semantic artifacts below are effective at the recorded pilot
semantic checkpoint unless separately identified. Governance records belong to
the separately recorded governance checkpoint. Only the system prompt carries a
separately pinned byte identity, because it is frozen against a completed probe.

| Path | Role | Class |
|---|---|---|
| `docs/pilot/sp-system-prompt-v0.1.md` | generic SP behavioral prompt, frozen | active normative |
| `docs/pilot/jaundice-behavior-contract.md` | jaundice case truth, knowledge, disclosure eligibility, forbidden set | active normative |
| `docs/pilot/palpitations-behavior-contract.md` | palpitations case truth, knowledge, disclosure eligibility, forbidden set | active normative |
| `docs/pilot/jaundice-trajectories.md` | jaundice gold trajectory oracle | active normative |
| `docs/pilot/palpitations-trajectories.md` | palpitations gold trajectory oracle | active normative |
| `docs/pilot/g2-evaluation-spec.md` | metrics, scoring rules, provisional thresholds | active normative |
| `docs/pilot/g2.1a-language-oracle-disposition.md` | accepted treatment of the language and oracle audit | disposition record |
| `docs/pilot/g2.1a-language-oracle-delta-audit.md` | independent final-state/delta audit of G2.1a | historical audit evidence |
| `docs/pilot/g2.1b-oracle-clarification-disposition.md` | accepted treatment of the G2.1a delta-audit findings | disposition record |
| `docs/pilot/g2.1b-oracle-clarification-delta-audit.md` | independent pre-merge delta audit of G2.1b | historical audit evidence |
| `docs/pilot/g2-structural-prebatch-audit.md` | independent structural pre-batch audit of the chat-issued execution envelope | historical audit evidence |
| `docs/pilot/g2-structural-prebatch-disposition.md` | proposed treatment of the structural pre-batch audit findings | disposition record |
| `docs/pilot/g2.7a-isolated-full-coverage-envelope-v1.md` | proposed isolated 58-unit full-coverage execution envelope, not yet accepted | proposed normative candidate |
| `docs/pilot/g2.7a-execution-envelope-v1-delta-audit.md` | independent delta audit of the v1 execution-envelope candidate | historical audit evidence |
| `docs/pilot/g2.1-contract-review.md` | contract executability review and open expert questions | historical evidence |
| `docs/pilot/g2.2-probe-plan.md` | historical small-probe execution plan and as-run limitation record | historical evidence |
| `docs/pilot/g2.2-probe-results.md` | historical small-probe scored dispositions, aggregate results, and erratum; the complete P25 response is preserved, but a complete immutable raw-response corpus was not retained for all 12 calls | historical evidence |
| `docs/pilot/g2-plan.md` | G2 phase sequence and architecture restraint | active normative |
| `docs/governance/context-bootstrap-audit-disposition.md` | accepted treatment of the independent context-bootstrap audit | disposition record |
| `docs/research/g1-product-baseline.md` | product-evidence baseline and research-expansion policy | active normative |
| `docs/research/g1-status.md` | historical publication-style G1 record, expansion paused | historical evidence |

Frozen system-prompt identity:

- source commit: `997e5200370ee5f5823af4c24b86c5d62f4625ee`
- SHA-256: `373351AAA9D254E42A88C0DAF209124FEFB3FF59FC59571095345E28EA451D72`

Both were verified against the working file at the effective checkpoint.

Prompt-commentary supersession: the exact generic prompt remains frozen and
unchanged. **Known limitations** item 6 in the prompt document is non-prompt
historical commentary from before the G2.1a alcohol correction; it does not
govern current J-T11 behavior. The active jaundice behavior contract and the
accepted G2.1a disposition require the reproducible approximate value and no
discretionary under-reporting. The accepted G2.1b disposition records this
clarification without changing the prompt file.

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

Historical provenance limitation: the 12-call exploratory probe predates the
official raw-output preservation rule. It is executability evidence, not a
provenance-complete official baseline. Every future official execution must
freeze complete final responses before scoring. This limits provenance claims
only; it does not retract the probe's useful conclusions — 11 PASS, 0 FAIL,
1 `ORACLE_AMBIGUOUS`, 0 `EXECUTION_ERROR`, no numerical pulse invention in P25,
and minimal architecture still justified.

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

The independent delta audit of the proposed v1 envelope is **complete**. The
next permitted task is **explicit human acceptance and merge of the corrected
v1 envelope**, or a bounded deterministic re-verification of the correction
diff.

1. Deterministic verification that the correction commit changed only the
   authorized minor content.
2. Explicit human acceptance of the structural pre-batch disposition and the
   corrected v1 envelope, recorded here, followed by merge.
3. Only after that acceptance do frozen pilot payloads and fixtures become
   eligible.
4. Only after payloads, fixtures, and a runner exist under an accepted envelope
   may the isolated 58-unit coverage run begin.

Fixture creation, runner creation, and execution are **not** eligible. The
58-unit execution remains unauthorized.

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
