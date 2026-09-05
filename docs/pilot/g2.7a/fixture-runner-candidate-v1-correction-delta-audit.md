# G2.7a corrected fixture/runner candidate final-state and delta audit

Date: 2026-09-05
Status: **IMMUTABLE HISTORICAL AUDIT EVIDENCE**
Classification: **PILOT_ONLY / NON_PRODUCTION**
Verdict: **REVISION_REQUIRED / 0 BLOCKERS / 3 MAJOR / 0 MINOR**

## Identity and authority

- Repository: `ilovesonu1-hash/cpx-v5-research`.
- Fetched main: `1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6`.
- Exact candidate: `710e6b4b4e7030e25cce1b106401b915a301eb20` on
  `pilot/g2.7a-fixture-runner-v1`.
- Audited correction delta:
  `f11df66df7fc12a860cc1beac76bcd53685f22f7..710e6b4b4e7030e25cce1b106401b915a301eb20`.
- Candidate parent: `f11df66df7fc12a860cc1beac76bcd53685f22f7`, whose sole
  parent is the fetched main above.
- Semantic checkpoint: `33cca3781b301c29af965430c3caaf32378c28ff`.
- Accepted envelope: `77b17f9a5716e67b7ccaf2c589572cc4b0ea23c4`, reachable
  through merge `f5f2ac2675caa270444b5b0e8223d8cb7fe2f7fd`.
- Auditor: Codex audit session; exact model revision is not separately attested
  by repository evidence. This is a new local final-state/delta audit, not the
  earlier ChatGPT GPT-5.6 Pro GitHub-connected static review.
- Access: source/delta inspection and independently rerun offline checks in a
  clean isolated worktree on `audit/g2.7a-fixture-runner-final-v1`.
- No additional model reviewer, patient model, evaluator, or provider probe was
  invoked. Synthetic record mutations below create no official raw outputs.

The user's conditional acceptance requires final PASS with no required
findings. That condition is not met. No acceptance, main merge, main sync,
execution authorization, or Stage 3 transport inspection follows this audit.
The existing candidate implementation is left unchanged.

## Treatment of the earlier correction scope

| Earlier finding | Final-state observation |
|---|---|
| B1, self-expiring main validation | Corrected: immutable candidate-base existence/HEAD ancestry and pinned semantic/envelope ancestry replace live remote-tip equality. Validation runs without fetching; the existing simulated descendant/detached-state test passes. No actual main merge is claimed. |
| M1, payload behavior/provenance | Required true-premise, known-absence false-premise, examination-consent, and local P29 no-prompt rules are present. Case-truth and patient-knowledge IDs are parsed from source tables. Missing, duplicate, and unexpected IDs are computed. |
| M2, session lifecycle outside retry | Creation and close failures participate in the three-attempt whole-unit lifecycle. Creation failures generate events, not fabricated call rows. Close failure makes that attempt nonauthoritative; its records are retained. Fake lifecycle and exception-sanitization tests pass. |
| M3, completed-record validation | Implemented but not sufficient: F1-F3 below demonstrate malformed complete corpora passing the validator. |
| M4, score evidence dependencies | All 58 rows have the correct ordered execution-unit prefix; setup and all six P29 calls are linked correctly. |
| Minor, target transport path | Correctly remains `HARNESS_CAPABILITY_UNVERIFIED`; no real adapter. This audit does not repeat or expand the historical CLI inspection. |
| Minor, execution-control provenance | Future accepted runner/adapter, authorization, preflight evidence, and bundle bindings are required in the specifications; none is fabricated or accepted now. |

The station frames and all 25 jaundice / 30 palpitations facts were compared
against the pinned contract truth and knowledge rows. No new medical truth was
identified in the payloads or behavioral additions. Hidden/forbidden facts and
pending human questions remain retained. This is a source/paraphrase audit
judgment, not a claim that ID-count checks prove semantic equivalence. No
clinical judgment or pending question was adjudicated.

## Required findings

### F1 — MAJOR: missing physical-session identities pass validation

Location: `tools/pilot/g2_7a/validate_run_records.py:174`, especially the null
skip at line 180 and the safe-ID check at line 184.

Replacing every raw-call and terminal-event `safe_session_id` with null in an
otherwise valid 64-call/48-unit corpus returns PASS: 23 checks, no errors, and
58 derived score-evidence rows. Null values are skipped when collecting
sessions, and no later requirement demands a non-null safe identifier for an
attempt that actually sent calls. The corpus can therefore assert verified
physical isolation without any auditable session identity.

This violates envelope sections 7 and 10 and the raw-call specification's
mandatory stable session identity. Require a valid non-null identifier on
every call and every post-creation terminal event, consistent throughout the
attempt. Null is appropriate only for a genuine pre-call creation-failure
event with no calls. Add full-corpus missing/null identity rejection tests.

### F2 — MAJOR: an execution-error call can become authoritative evidence

Location: `tools/pilot/g2_7a/validate_run_records.py:286` and the authoritative
completion checks beginning at line 311.

Starting with the same valid full corpus, replace CALL-J01's response with
null, set its error class/message to `TIMEOUT` / `safe timeout`, and set
completion status to `execution_error`. Leave its authoritative flag and
`ATTEMPT_COMPLETED` event intact. The validator again returns PASS: 23 checks,
no errors, 58 derived evidence rows.

The raw error row is individually well formed, but the validator never links
that failure to the authoritative attempt's completeness. It derives a
scorecard evidence ID for a call with no completed output. Require every
authoritative call to be a successful completed output, including a valid
empty string, with null error fields and a coherent successful terminal event.
An error row must invalidate that attempt. Add error/event contradiction tests;
do not reject successful empty or poor patient outputs.

### F3 — MAJOR: failed-attempt call order and retry termination are unchecked

Location: `tools/pilot/g2_7a/validate_run_records.py:233` (attempt-index
continuity) and line 313 onward (call inventory/order restricted to the
selected authoritative attempt).

Three independently constructed invalid variants pass with 23 checks and no
errors:

1. A nonauthoritative failed retry is appended after a fully successful first
   authoritative attempt.
2. In a failed P-SEQ-02 attempt before a valid complete second attempt, calls
   are ordered P14, setup, P15 instead of setup, P14, P15.
3. That failed first attempt instead contains the setup call twice, using
   distinct run IDs, before P14 and the failed P15 call.

Known call fields are checked individually, but there is no exact-prefix or
one-occurrence rule for failed attempts, and contiguous attempt numbers do not
enforce stopping after the first safely completed attempt. This allows extra
calls and invalid history to disappear into preserved nonauthoritative data.
Validate every attempt against an ordered, duplicate-free planned prefix, with
coherent failure/close events; allow retries only after an invalid attempt and
none after authoritative success. Add failed-prefix, duplicate-call, and
post-success retry rejection tests. These are record-integrity corrections,
not an invitation to add an orchestration framework or semantic state machine.

## Offline validation actually rerun

Portable commands below use the installed Python interpreter with `-B` to
avoid generating bytecode. No dependencies were installed.

| Check / command | Observed result |
|---|---|
| `git fetch origin` and exact ref/parent/ancestry/worktree checks | PASS; expected main and candidate match; concurrent dirty frontend paths preserved |
| `python -B tools/pilot/g2_7a/build_bundle.py` twice | PASS both times; 19 generated artifacts; `git diff --exit-code` empty after each build |
| `python -B tools/pilot/g2_7a/build_bundle.py --check` | PASS, byte-identical regeneration |
| `python -B tools/pilot/g2_7a/validate_bundle.py` | PASS, 184 deterministic checks |
| `python -B tools/pilot/g2_7a/runner.py plan` | 58 scored units / 64 calls / 48 sessions; execution unauthorized |
| `python -B tools/pilot/g2_7a/runner.py validate` | PASS, 184 deterministic checks |
| `python -B -m unittest discover -s tools/pilot/g2_7a/tests -v` | PASS, 40 tests |
| Same 40 tests under a Python audit hook rejecting network/process actions | PASS, 40 tests, zero errors/failures; not 40 additional distinct tests |
| Independent parsed-source, evidence-prefix, JSON/CSV, hash, scope, and safety assertions | PASS, 94 assertions; 32 candidate changed paths scanned; no bounded secret/private-path pattern findings |
| Independent full-corpus record validator scenarios | 8 scenarios: valid control passes; session-reuse negative control rejects; 6 malformed variants incorrectly pass, establishing F1-F3 |
| `git diff --check` | PASS |

The independent integrity script initially encountered a shell/stdin encoding
issue in its Korean assembly delimiter. Using the delimiter's Unicode escapes
resolved that audit-script issue; the candidate fixture bytes were unchanged.

The 184-check bundle result does not override the failed adversarial corpus
checks. The existing 40 tests do not exercise these missing rejection cases.
The bounded security scan inspects only candidate-changed text for private
machine paths, key/header/credential-value patterns, and personal email
patterns. It does not inspect credentials, configuration secrets, or unrelated
application/evidence content, and is not an exhaustive secret-detection claim.

## Reproduction of the two core failures

Run this Python snippet from the exact audited candidate checkout with
`python -B`. It builds synthetic records only in memory, using the committed
test helper; it neither invokes a transport nor writes JSONL.

```python
import copy
import sys

sys.path[:0] = ['tools/pilot/g2_7a', 'tools/pilot/g2_7a/tests']
from test_run_records import RunRecordValidatorTests
from validate_run_records import validate_records

RunRecordValidatorTests.setUpClass()
helper = RunRecordValidatorTests()
calls, events = [], []
for unit in helper.manifest['execution_units']:
    unit_calls, unit_events = helper.completed_attempt(unit['execution_unit_id'])
    calls.extend(unit_calls)
    events.extend(unit_events)

def report(label, rows, terminal_events):
    result = validate_records(helper.manifest, helper.bundle, rows, terminal_events)
    print(label, result.ok, result.checks_passed, result.errors)

report('valid', calls, events)
null_calls, null_events = copy.deepcopy(calls), copy.deepcopy(events)
for row in null_calls + null_events:
    row['safe_session_id'] = None
report('F1_null_sessions', null_calls, null_events)
error_calls = copy.deepcopy(calls)
error_calls[0].update(
    final_patient_response=None,
    execution_error_class='TIMEOUT',
    execution_error_message_safe='safe timeout',
    provider_completion_status='execution_error',
)
report('F2_authoritative_error', error_calls, events)
```

All three print `True 23 []` at the audited target; the last two must instead
be rejected by a corrected validator. F3 uses the same helper with P-SEQ-02
attempt 2 as the authoritative unit, plus a nonauthoritative attempt-1 prefix
mutated as described above, or an extra failed attempt following success.

## Preserved bundle and accounting

- Audited, **not accepted**, input bundle:
  `sha256:991159fc06f2f135f97422995da029442d79584269c2fc2d10cf33011feed317`.
- Prompt document SHA-256:
  `373351aaa9d254e42a88c0daf209124fefb3ff59fc59571095345e28ea451d72`.
- Transmitted prompt block SHA-256:
  `f4df500f622633480cd9525fa2f61e57c94921af12fa51b0842b506d8f9040b8`.
- Accepted envelope SHA-256:
  `2b69b1d1fbf0c1a5fcc0ab8177362e998a198860d763e4a65552e90e797f4fc5`.
- Contract, trajectory, and evaluation Git-object bytes match the exact
  semantic checkpoint; all protected source files match the candidate base.
- Nonce unchanged: `CPX-G2-ISO-012fb514aefc248b0e058f8f98c0e43e`.
- 58 scored units / 58 unscored-template rows; 57 individually scored calls
  plus one unscored setup plus six P29 constituents = 64 planned official calls.
- 38 single-turn + 9 ordinary sequence + 1 P29 station = 48 planned sessions.
- Setup is shared by P14/P15 evidence. P29 remains one scored row linked to six
  ordered constituent calls. The three neutral preflight calls / two sessions
  remain outside official totals and were not executed.
- No payload, system message, generated manifest/spec/template, runner, or
  validator bytes were patched by this audit. Their candidate identities stay
  as recorded at `710e6b4`.

## Advancement and stop

Required next work is a separately authorized bounded disposition/correction
of F1-F3, followed by independent offline final-state/delta audit. This audit
does not itself authorize those substantive patches. Candidate acceptance and
main merge are withheld. The conditional post-merge static transport stage is
not entered, and no adapter is authored or auto-merged.

`SESSION_ISOLATION_BASELINE=NOT_ESTABLISHED`
`ISOLATION_PREFLIGHT_EXECUTED=NO`
`PATIENT_MODEL_CALLS=0`
`EVALUATOR_MODEL_CALLS=0`
`REAL_PROVIDER_CALLS=0`
`G2_FULL_COVERAGE=NOT_EXECUTED/UNAUTHORIZED`
`MODEL_JUDGE=NONE`
`PROMPT_V0_1_MODIFIED=NO`
`PATIENT_SEMANTIC_SOURCES_MODIFIED=NO`
`REAL_TRANSPORT_ADAPTER=ABSENT`
`HARNESS_CAPABILITY=UNVERIFIED`
`FIXTURE_RUNNER_ACCEPTED=NO`
`ARCHITECTURE_ESCALATION=NOT_JUSTIFIED`
`PRODUCTION_IMPLEMENTATION_AUTHORIZED=NO`
