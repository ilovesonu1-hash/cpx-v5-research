# G2.7a fixture and runner candidate v1

Date: 2026-09-03
Status: **PROPOSED / NOT YET ACCEPTED**
Classification: **PILOT_ONLY / NON_PRODUCTION**

## Purpose and boundary

This candidate reconstructs frozen patient-model inputs, represents all 58
scored units, plans 64 official calls in 48 isolated execution units, preserves
P29 as one six-call station-level unit, freezes neutral isolation-preflight
inputs, and exercises retry/session/raw-record behavior with an in-memory fake.

It performs no preflight, patient-model call, evaluator-model call, semantic
scoring, official batch execution, production integration, or architecture
escalation. It modifies no prompt, contract, trajectory, evaluation
specification, accepted envelope, or historical record.

Accepted execution envelope:

- commit: `77b17f9a5716e67b7ccaf2c589572cc4b0ea23c4`
- merge: `f5f2ac2675caa270444b5b0e8223d8cb7fe2f7fd`
- file SHA-256: `2b69b1d1fbf0c1a5fcc0ab8177362e998a198860d763e4a65552e90e797f4fc5`
- working file byte-identical to the accepted commit: yes

## Artifact inventory

The bounded candidate consists of:

- exact prompt, two payload, two assembled system-message, and four preflight
  text fixtures under `docs/pilot/g2.7a/fixtures/`;
- payload-provenance, preflight, execution, ambiguity, criticality, and
  aggregate input-bundle manifests under `docs/pilot/g2.7a/manifests/`;
- raw-response and scorecard specifications under
  `docs/pilot/g2.7a/specs/`;
- one unscored 58-row scorecard CSV under
  `docs/pilot/g2.7a/templates/`;
- this report and the no-call transport capability record; and
- the builder, validator, execution-disabled runner, minimal transport
  interface, in-memory fake, and standard-library tests under
  `tools/pilot/g2_7a/`.

No listed file is a production package, API, schema, database, router, model
judge, retrieval component, or orchestration framework.

## Canonicalization and construction

Canonical text fixtures are UTF-8 without BOM, LF-only, without trailing
spaces, and without a terminal LF. JSON is UTF-8 without BOM, two-space
indented with sorted keys, LF-only, and has one terminal LF. CSV is RFC
4180-compatible, UTF-8 without BOM, fixed-column, LF-only, and has one terminal
LF.

The builder reads prompt, contract, trajectory, evaluation, and envelope bytes
from exact Git objects. It extracts only the fenced `text` block following
`## Exact prompt`, constructs each system message as
`prompt + "\n\n[환자 정보]\n" + payload`, and renders all generated artifacts
deterministically. The committed nonce is reused after its one-time generation.

## Frozen source identities

| Source | Git blob SHA | SHA-256 |
|---|---|---|
| Prompt document at `997e5200370ee5f5823af4c24b86c5d62f4625ee` | `fa11f52c22a4a8fe6d07e31d58baa504709a6cc1` | `373351aaa9d254e42a88c0daf209124fefb3ff59fc59571095345e28ea451d72` |
| Transmitted prompt block | n/a | `f4df500f622633480cd9525fa2f61e57c94921af12fa51b0842b506d8f9040b8` |
| Jaundice contract at `33cca3781b301c29af965430c3caaf32378c28ff` | `d574c1740501061b20c2a32505aed9caf2abcea3` | `a22e976baf1051fef2b8e3d997cdc0cffc5b8f6533414733af3989d35e1272df` |
| Palpitations contract at `33cca3781b301c29af965430c3caaf32378c28ff` | `09bf2c36d153d970c93971ca82ad8ee039487bc4` | `36124a164c1325da072a879697762ce6356b25f1495677f7ddd070ae581ae0a9` |
| Jaundice trajectories at `33cca3781b301c29af965430c3caaf32378c28ff` | `767912271f90a516d9ec59cbc533f751e004bfc6` | `267a645877cae27839e0a82dca019cdfb00c7d722e10175fb4b4abe9fc95fd7b` |
| Palpitations trajectories at `33cca3781b301c29af965430c3caaf32378c28ff` | `ad0067d14f6d3dad894eb0eac28e7bca208b2a3c` | `becab7ac4df836a72f3d5f902c3cba3f6190fa37eed99ee4542f9704526eae75` |
| Evaluation specification at `33cca3781b301c29af965430c3caaf32378c28ff` | `d9b911cadf45572986f926186746951c14234744` | `defffb1e40d3da49d67ca0fda7db9212c4e05f0458f7969cab872dab798794ad` |

## Payloads and assembled messages

| Case | Station frame | Facts | Forbidden facts retained | Payload SHA-256 | System-message SHA-256 |
|---|---|---:|---|---|---|
| Jaundice | 김영수; 58; male; outpatient first visit; 12 minutes; opening after reason-for-visit question | 25 | J-T19 through J-T24 | `848476d74902fcf4fa1e024145dbd7ac031acaa5961d285ff3d2f636925a4935` | `4eb9f01ecd8a21eeb5b18d48c51855be5ba0562ad46bd1c6408124aaa109eada` |
| Palpitations | 박지현; 34; female; outpatient; 12 minutes; opening after reason-for-visit question | 30 | P-T25 through P-T30 | `54440b644bd568e7f88600922d0e07d8ad3c9f694fc3213a5f190ccbb957c1a7` | `15ac92444408efd1262654eb34e3144d59a8d971324aa755fd8474a20c3a9637` |

Each source fact ID occurs once in its inventory. The payloads preserve authored
meaning, approximation, absence/presence, knowledge, disclosure eligibility,
focused/prerequisite behavior, uncertainty, cannot-observe behavior, and
never-disclose constraints. They exclude case-selection rationale, literature,
open review questions, evaluator/audit text, and historical implementation
commentary. No new clinical case fact was added and no `REVIEW_PENDING` item
was resolved.

## Execution plan

| Quantity | Planned count |
|---|---:|
| Scored units / scorecard rows | 58 |
| Individually scored response calls | 57 |
| Official unscored calls | 7 |
| Official calls | 64 |
| Independent single-turn execution units/sessions | 38 |
| Ordinary sequence execution units/sessions | 9 |
| P29 station execution units/sessions | 1 |
| Total execution units/sessions | 48 |

The nine ordinary sequences are J-SEQ-01 through J-SEQ-05 and P-SEQ-01
through P-SEQ-04 exactly as accepted. P-SEQ-02 begins with the one unscored
`P-SETUP-DURATION-01` call. P29 is one scored row linked to six ordered,
unscored constituent calls P29-U01 through P29-U06 in one session.

Execution-manifest SHA-256:
`184da7a421b248f15dd867a38692ea1022c81383380661297a17b554704214f8`.

## Preflight inputs

Committed public-safe nonce:
`CPX-G2-ISO-012fb514aefc248b0e058f8f98c0e43e`.

| Input | SHA-256 |
|---|---|
| Neutral system instruction | `25049a3ca382bbda5df20dcf99f651173187a2c60ed108a6f2de8a2b0d3ca72d` |
| Session A turn 1 | `9aa9f605ceb5621de11ee5d3b7694355591fef7c462f5f752fd203d680105fd5` |
| Session A turn 2 | `2b5dfc3b8fe2eee09c247617587ac298cba934e8b891e4f1c5470e881943723d` |
| Session B turn 1 | `958ad26637372fb4d67f4ac20a970d1cb4002da6ef46bb916c83ecc365aff263` |

The manifest plans three calls in two sessions using the same future runtime,
session creation, history, and final-output extraction mechanisms as the
official run. It records `executed=false`, `execution_authorized=false`, and
fail-closed result `HARNESS_ISOLATION_BLOCKED`.

Preflight status: **NOT_EXECUTED**.

## Aggregate input bundle

`input_bundle_id`:
`sha256:9c15bb52b494008eadcf7919fba6a51c2227081c745f4663873ecffdba7b423b`.

It is the SHA-256 of canonical compact JSON containing only the sorted logical
component-name to component-SHA-256 mapping. The aggregate identifier is not
included in its own calculation. The execution manifest has no aggregate-ID
back-reference, avoiding a circular hash.

## Runner and transport

| Command | Current behavior |
|---|---|
| `plan` | Loads frozen manifests and prints 58 scored units / 64 calls / 48 ordered execution units; no call |
| `validate` | Runs deterministic validation only; no call |
| `preflight` | Refuses with `PREFLIGHT_EXECUTION_NOT_AUTHORIZED` |
| `execute` | Refuses with `PATIENT_MODEL_EXECUTION_NOT_AUTHORIZED` |

Retry logic is capped at three complete execution-unit attempts, uses a new
physical session per retry, preserves partial records, and restarts an entire
sequence or P29. Successful empty or poor outputs are valid outputs and are not
retried. Only the explicitly designated learner-visible final field is copied;
no stripping or repair occurs.

The process-local fake covers same-session memory, cross-session isolation,
sequence restart, P29's six calls, raw-record creation, retry accounting,
successful empty output, poor valid output, and exact final-field preservation.

Real transport status:
`REAL_TRANSPORT_INTERFACE_PARTIALLY_VERIFIED`. Claude Code 2.1.259 help was
inspected without a prompt. The exact required runtime and all physical-session
and final/reasoning-channel guarantees remain unverified, so no real adapter is
implemented and execution remains disabled.

## Validation record

Portable command notation is used so no private machine path is committed.

| Command | Result |
|---|---|
| `python tools/pilot/g2_7a/build_bundle.py` | PASS; deterministic bundle rendered |
| same builder command a second time | PASS; no byte change |
| `python tools/pilot/g2_7a/build_bundle.py --check` | PASS; temporary regeneration byte-identical |
| `python tools/pilot/g2_7a/build_bundle.py --print-summary` | PASS; 58 / 64 / 48 and bundle ID reported without writes |
| `python tools/pilot/g2_7a/validate_bundle.py` | PASS; 157 deterministic checks |
| `python tools/pilot/g2_7a/runner.py plan` | PASS; 58 scored units / 64 calls / 48 sessions |
| `python tools/pilot/g2_7a/runner.py validate` | PASS; deterministic validation only |
| `python -m unittest discover -s tools/pilot/g2_7a/tests -v` | PASS; 23 tests |
| JSON and CSV parsing | PASS through validator and tests |
| aggregate ID recomputation | PASS through validator and tests |
| `git diff --check` | PASS |

No unit test imports a network client or invokes a subprocess. No preflight,
provider probe, model call, evaluator call, semantic score, raw run output, or
authorization artifact was created.

## Known limitations

- The required real transport interface is only partially verified and has no
  adapter.
- Session isolation is not established; only fake behavior is tested.
- Future output is `INPUT_REPRODUCIBLE / OUTPUT_NOT_DETERMINISTIC` if generation
  controls remain unexposed.
- Criticality uses the required explicit-source-only provisional policy and
  awaits audit and human acceptance.
- The canonical scorecard template leaves its aggregate bundle field blank.
  A future accepted scoring copy binds that field before scoring because the
  template hash itself participates in the bundle identity.
- Semantic scoring remains human-only; `MODEL_JUDGE = NONE`.

## Explicit nonauthorization

Candidate completion does not authorize preflight, patient-model execution,
scoring, the official 58-unit run, prompt/contract/trajectory/evaluation
changes, architecture escalation, production integration, or a real transport
adapter. The next permitted task is an independent read-only audit of this
candidate.
