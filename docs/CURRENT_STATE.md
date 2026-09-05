# CPX v5 current state

Mutable owner of phase, accepted identities, gates, blockers and next action.
AGENTS.md routes detailed behavior to its owners. Superseded state is preserved
at review base 456c31af6b8fc0325de6adae510da2a0f3348528 and in the existing
immutable evidence below; historical audit bytes are not rewritten.

## Identities

| Field | Current value |
|---|---|
| Repository | ilovesonu1-hash/cpx-v5-research |
| Reference main at review fetch | 1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6; unchanged by this task |
| Review base / prior F1-F3 correction | 456c31af6b8fc0325de6adae510da2a0f3348528 |
| Review branch | pilot/g2.7a-offline-review-v1 |
| Accepted governance proposal / merge | ce254e5bb26906e1a6dd4dfe57d96e6cc8398bd8 / 43704a8e670d16fdd101d28a988acf8b96ec0089 |
| Effective patient semantic checkpoint | 33cca3781b301c29af965430c3caaf32378c28ff |
| Accepted G2.1b merge | e734964521041a281c51c6bf6a1984c7ec4c013d |
| Accepted execution envelope / merge | 77b17f9a5716e67b7ccaf2c589572cc4b0ea23c4 / f5f2ac2675caa270444b5b0e8223d8cb7fe2f7fd |
| Frozen prompt source | 997e5200370ee5f5823af4c24b86c5d62f4625ee |
| Prompt document SHA-256 | 373351aaa9d254e42a88c0daf209124fefb3ff59fc59571095345e28ea451d72 |
| Transmitted prompt SHA-256 | f4df500f622633480cd9525fa2f61e57c94921af12fa51b0842b506d8f9040b8 |

The accepted envelope retains its historical proposal heading; the accepted
checkpoint above governs. It does not authorize execution. Patient semantic
sources, prompt and frozen input bytes are unchanged by this review.

Proposed input_bundle_id:

`sha256:991159fc06f2f135f97422995da029442d79584269c2fc2d10cf33011feed317`

The bundle component map owns individual source/fixture/spec hashes. Tooling
acceptance is separate, not a self-referential hash. Plan: 25/30 facts; 58 scored
units/score rows; 64 calls; 48 sessions (38 single + 9 sequence + 1 P29).
P29 has six calls; preflight remains outside official totals.

## Gates and blockers

| Gate | State |
|---|---|
| G1_RESEARCH_EXPANSION | PAUSED; product baseline reached |
| G2_CONTRACTS | EXECUTABLE_AS_PROVISIONAL_GOLD; no clinician/SP-educator acceptance |
| G2_1B_ORACLE_CLARIFICATION | ACCEPTED / MERGED / EFFECTIVE |
| G2_EXECUTION_ENVELOPE_V1 | ACCEPTED / MERGED / EFFECTIVE |
| G2_FIXTURE_RUNNER_IMPLEMENTATION | PROPOSED / REVIEW_READY / NOT YET ACCEPTED |
| G2_INPUT_BUNDLE_V1 / G2_PAYLOAD_SNAPSHOTS_V1 / G2_EXECUTION_MANIFEST_V1 | PROPOSED / UNCHANGED / NOT YET ACCEPTED |
| G2_PREFLIGHT_MANIFEST_V1 | PROPOSED / NOT_EXECUTED / UNAUTHORIZED |
| G2_RUNNER_V1 | PROPOSED / HARNESS_CAPABILITY_UNVERIFIED / EXECUTION_DISABLED |
| SESSION_ISOLATION_BASELINE | NOT_ESTABLISHED |
| ISOLATION_PREFLIGHT_EXECUTED | NO |
| G2_FULL_COVERAGE | NOT_EXECUTED / UNAUTHORIZED |
| MODEL_JUDGE | NONE; semantic scorer HUMAN |
| PROMPT_V0_1_MODIFIED | NO |
| ARCHITECTURE_ESCALATION | NOT_JUSTIFIED |
| PRODUCTION_IMPLEMENTATION_AUTHORIZED | NO |

The demonstrated exhaustion and final scorecard-ID defects are corrected in
this review diff, with F1-F3 protections retained. The single offline checkpoint
report owns findings, decisions and actual verification; this is implementation
self-verification, not independent acceptance.

Execution blockers remain: no accepted real adapter/control bundle, no passing
authorized preflight, no execution authorization. The actual Paseo/OpenCode path
still lacks verified fresh physical-session initialization with the exact patient
system message. Final-output extraction and close semantics also remain unverified.

Human review questions remain unadjudicated under the accepted G2.1b disposition
and ambiguity map. Prompt-document limitation 6 is historical commentary:
accepted reproducible J-T11 alcohol quantity, not discretionary minimisation,
remains active. The historical 12-call probe is not a provenance-complete
session-isolation baseline; its corrected results remain in the existing owner.

## Owner links

All unaccepted tooling, fixtures, manifests and specifications remain pilot-only.

| Owner | Role / class |
|---|---|
| docs/pilot/g2.7a/offline-review-checkpoint-v1.md | current implementation report; proposed, not independent audit |
| tools/pilot/g2_7a/verify_offline.py | one offline entrypoint; candidate-only checks, no authority to execute |
| tools/pilot/g2_7a/validate_bundle.py | reusable source/bundle integrity |
| tools/pilot/g2_7a/validate_run_records.py | raw/event integrity and coherent exhaustion |
| tools/pilot/g2_7a/tests/ | existing standard-library regression suite |
| tools/pilot/g2_7a/build_bundle.py | unchanged deterministic builder |
| tools/pilot/g2_7a/runner.py; tools/pilot/g2_7a/transport.py | unchanged disabled runner and fake-only transport |
| docs/pilot/g2.7a/fixtures/ | proposed frozen prompt/payload/system/preflight bytes |
| docs/pilot/g2.7a/manifests/input-bundle-v1.json | identity and component-hash owner |
| docs/pilot/g2.7a/manifests/ | provenance, preflight, execution, ambiguity, criticality |
| docs/pilot/g2.7a/specs/; docs/pilot/g2.7a/templates/scorecard-v1.csv | proposed raw/event/score specs and unscored template |
| docs/pilot/g2.7a/transport-capability-v1.md | no-call observations; capability unverified |
| docs/pilot/sp-system-prompt-v0.1.md | frozen generic prompt |
| docs/pilot/jaundice-behavior-contract.md; docs/pilot/palpitations-behavior-contract.md | active case truth/knowledge/disclosure |
| docs/pilot/jaundice-trajectories.md; docs/pilot/palpitations-trajectories.md | active trajectory oracles |
| docs/pilot/g2-evaluation-spec.md | active scoring/metrics |
| docs/pilot/g2.7a-isolated-full-coverage-envelope-v1.md | accepted control envelope, not execution authorization |
| docs/pilot/g2.7a/fixture-runner-candidate-v1.md | original implementation evidence |
| docs/pilot/g2.7a/fixture-runner-candidate-v1-audit.md; docs/pilot/g2.7a/fixture-runner-candidate-v1-audit-disposition.md | preserved first audit/treatment |
| docs/pilot/g2.7a/fixture-runner-candidate-v1-correction-delta-audit.md | immutable F1-F3 audit, REVISION_REQUIRED at its target |
| docs/pilot/g2.7a/record-integrity-correction-v1-disposition.md | preserved F1-F3 correction; independent review pending |
| docs/pilot/g2.7a-execution-envelope-v1-correction-delta-audit.md | accepted envelope audit |
| docs/pilot/g2-structural-prebatch-disposition.md | accepted pre-batch treatment |
| docs/pilot/g2.1b-oracle-clarification-disposition.md | accepted semantic treatment and pending human questions |
| docs/pilot/g2.2-probe-results.md | historical probe and erratum, provenance limitation retained |
| docs/governance/context-bootstrap-audit-disposition.md | accepted governance treatment |
| docs/research/g1-product-baseline.md | active research-expansion policy |

## Next permitted action

External read-only review of this one checkpoint. Use
`python -B tools/pilot/g2_7a/verify_offline.py` after code/input changes.
Documentation-only edits need bounded diff, owner-link and secret/path checks,
not repeated full validation. STATIC_REVIEW_ONLY cannot satisfy the independent
execution-verification gate.

This task authorizes publishing only the review branch: no main merge, adapter,
runtime substitution, model/provider prompt, preflight, scoring, official run,
production integration or architecture expansion. Do not infer acceptance from
passing tests or spawn an unapproved reviewer. Concurrent frontend work, cpx-v4,
external evidence, production data and schemas remain untouched and outside scope.
