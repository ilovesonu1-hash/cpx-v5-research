# G2.7a offline review checkpoint

PILOT_ONLY / NON_PRODUCTION

Status: PROPOSED / REVIEW_READY / NOT ACCEPTED.
This is the single implementation-session report, not an independent audit,
semantic score, acceptance record or execution authorization.

## Scope and provenance

- Actual base: `456c31af6b8fc0325de6adae510da2a0f3348528`.
- Base parent / immutable F1-F3 audit: `3e56e8a47ed3274f76548fc92c6daf5490d8ef39`.
- Reference main at refreshed bootstrap:
  `1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6`.
- Review branch: `pilot/g2.7a-offline-review-v1`.
- Head identity is the commit containing this report; the final handoff supplies
  its full SHA without putting a self-referential commit hash into this file.
- Refreshed Git refs showed no newer descendants of the base. Existing dirty
  frontend paths and all concurrent worktrees were preserved.
- The named `cpx_validator_proposed.patch` and `reproduce_review.py` were not
  accessible in the provided workspace/attachment resources or bounded named-file
  search. They were not applied or claimed reviewed. Reproductions were derived
  directly from the owner's two explicit defect descriptions and existing tests.

## Demonstrated findings and decisions

| Finding | Reproduction at base | Bounded decision / outcome |
|---|---|---|
| Exhausted retry history rejected | Replace J01's successful call with three coherent create-failure events. Validator rejected the corpus for missing authority/completion/evidence. | Accept coherent exactly-three-attempt exhaustion as a valid execution-error record, not an invalid corpus. Keep all existing session, prefix and event checks. |
| Final scorecard ID inventory unchecked | A valid 58-row scorecard plus a duplicate or unexpected ID passed. Missing IDs failed only indirectly at evidence lookup. | Validate string IDs, exact set equality and uniqueness before dictionary conversion. Duplicate/missing/unexpected IDs now fail with RUN_SCORECARD_ID_INVENTORY_INVALID. |
| Candidate-only checks mixed with reusable integrity | Presence of future run artifacts was a bundle failure; source keywords were counted as safety proof. | Move candidate artifact/type inventory checks to the offline entrypoint. Keep reusable source/hash/coverage/accounting validation separate. Test gates behaviorally, not by finding refusal text. |
| Unused and redundant helpers | Scoped references found no consumer of _payload_fact_ids; _source_imports only served the removed import-keyword safety checks. | Remove these helpers and the unused Iterable import from validate_bundle.py. Do not rewrite the builder or remove essential evidence checks. |
| Repeated verification and state narrative | Separate entrypoints encouraged rerunning the same full suite for documentation edits. | One offline entrypoint; compact CURRENT_STATE to current identities, blockers and owner links. Existing audits/dispositions remain byte-identical. |

### Record-result meaning

`RunRecordValidationResult.ok` means the record corpus is structurally valid,
not that the experiment passed or even completed successfully.

For coherent exhaustion, `exhausted_execution_unit_ids` and
`execution_error_scored_unit_ids` identify transport/harness outcomes. No success
response or authoritative run ID is fabricated. The affected scored IDs have no
entry in `authoritative_run_ids_by_scored_unit`. The CLI reports exhaustion
metadata separately from its record-validation PASS/FAIL.

Exactly three failed attempts are required for this terminal outcome. An
incomplete history, a fourth attempt, contradictory terminal event, session reuse,
malformed prefix or retry after success remains invalid. Every failed call/event
is retained. A successful empty, poor, refused or truncated output is still an
output and is never retried on content grounds.

If a final scorecard is supplied, exhausted rows must say EXECUTION_ERROR and
have either blank authoritative_run_ids or a JSON empty array. Successful units
still require their exact ordered evidence mapping. This is deterministic record
consistency, not model judging or automatic semantic scoring.

## Verification actually performed

One bounded repair/recheck cycle completed; no second repair was needed.

```text
python -B tools/pilot/g2_7a/verify_offline.py
python -B tools/pilot/g2_7a/runner.py plan
git diff --check
```

The single entrypoint invoked the existing builder --check, reusable bundle
validator, candidate snapshot checks and unittest discovery once. It does not
invoke runner preflight/execute, a model, an agent, or a provider.

| Check | Actual result |
|---|---|
| Builder --check | PASS; all 19 generated artifacts reproduce the committed bytes |
| Reusable bundle integrity | 175 checks, 0 errors |
| Candidate snapshot | 3 checks, 0 errors |
| Existing suite plus focused regressions | 74 tests passed: all 60 existing plus 14 new methods |
| Completed-corpus exhaustion reproduction | PASS, 26 structural checks; J01 marked execution-error eligible, no fabricated authority |
| Final scorecard duplicate / missing / unexpected reproductions | All rejected before dictionary conversion |
| Plan | 58 scored units / 64 calls / 48 sessions; execution_authorized=false |
| Protected bytes | 26 source/fixture/manifest/spec/template files identical to review base |
| Historical audit/disposition bytes | Unchanged |

Tests exercise single, sequence and P29 exhaustion; creation/call/close failures;
mixed failures; correct third-attempt success; invalid counts; exhausted scorecard
mapping; F1-F3 mutations; and a genuinely exhausted in-memory fake runner result.
No official JSONL output or authorization artifact was created in the repository.

The test phase blocks socket/process launch entrypoints with unittest mocks.
Git source reads occur before that guard. The candidate transport class inventory
is a review-scope check, not proof of no possible external calls or of physical
isolation. Source-text keyword matches are not used as such proof. Runner refusal
and default-plan behavior are covered by executable regression tests; permission
gates and the actual runner/transport implementation remain unchanged.

The two original malformed-record repros and all earlier F1-F3 regressions remain
in the existing suite. The builder's byte-idempotence test remains. No generated
input changes were made, so redundant builder writes and full reruns after
documentation-only changes were omitted. Final documentation changes receive
only diff, owner-link, scope, protected-byte and bounded secret/private-path checks.

## Frozen identity and accounting

Unchanged input_bundle_id:

`sha256:991159fc06f2f135f97422995da029442d79584269c2fc2d10cf33011feed317`

The unchanged `manifests/input-bundle-v1.json` owns all component SHA-256 values,
including contracts, trajectories, evaluation, payloads and assembled messages.
Its canonical compact component-map digest was recomputed successfully.

- Semantic checkpoint: `33cca3781b301c29af965430c3caaf32378c28ff`.
- Envelope: `77b17f9a5716e67b7ccaf2c589572cc4b0ea23c4`.
- Prompt document: `373351aaa9d254e42a88c0daf209124fefb3ff59fc59571095345e28ea451d72`.
- Prompt block: `f4df500f622633480cd9525fa2f61e57c94921af12fa51b0842b506d8f9040b8`.
- Nonce: `CPX-G2-ISO-012fb514aefc248b0e058f8f98c0e43e`.
- Fact inventories: 25 jaundice, 30 palpitations; no new medical fact.
- 58 scored units and scorecard rows; 57 individually scored calls plus 7
  official unscored calls (one duration setup, six P29 calls) = 64.
- 38 single sessions + 9 sequence sessions + 1 P29 session = 48.
- Retries increase attempted records/sessions, not these planned totals.

## No-call target transport inspection

The Paseo skill was used only to route read-only provider metadata inspection.
Observed path: Paseo -> OpenCode -> Vertex namespace. The draft selectedModel
was exactly `google-vertex/gemini-3.7-flash`; this does not verify serving access.
OpenCode 1.18.28 session/run help was inspected with no message. Initial sandbox
help attempts failed during configuration-directory access; only version/help
was retried with scoped permission. No configuration/credential values were read.

The smallest missing capability is a documented fresh physical-session
initialization contract carrying exactly the supplied patient system message on
that path. Final-only response extraction and safe close semantics are also
unverified. Generic JSON/continue flags do not establish these properties.
Detailed safe observations belong to `transport-capability-v1.md`.

HARNESS_CAPABILITY_UNVERIFIED remains; no adapter is implemented, no runtime is
changed, no session is created, and no prompt is sent.

## Review boundary

Only the review branch may be pushed. No main merge or acceptance is authorized
by this task. No independent-review verdict is claimed; static-only external
review must be labelled STATIC_REVIEW_ONLY and cannot satisfy an independent
execution-verification gate. No reviewer agent was spawned.

SESSION_ISOLATION_BASELINE=NOT_ESTABLISHED; ISOLATION_PREFLIGHT_EXECUTED=NO;
PATIENT_MODEL_CALLS=0; MODEL_JUDGE=NONE; HUMAN remains the semantic scorer;
G2_FULL_COVERAGE=NOT_EXECUTED/UNAUTHORIZED; PROMPT_V0_1_MODIFIED=NO;
ARCHITECTURE_ESCALATION=NOT_JUSTIFIED;
PRODUCTION_IMPLEMENTATION_AUTHORIZED=NO.
