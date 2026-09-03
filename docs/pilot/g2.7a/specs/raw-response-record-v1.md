# G2.7a raw-response record v1

Classification: **PILOT_ONLY / NON_PRODUCTION**

One JSONL object represents one attempted patient-model call. No official raw
response row is created by this candidate task.

## Required fields

| Field | Type / rule |
|---|---|
| `run_id` | public-safe unique call-attempt identifier |
| `planned_call_id` | exact planned-call identity from the execution manifest |
| `execution_unit_id` | manifest execution unit |
| `unit_attempt_index` | integer 1 through 3 |
| `scored_unit_id` | scored-unit linkage; null only for the P14/P15 setup call |
| `source_trajectory_id` | trajectory linkage when applicable; null for setup and P29 constituent calls |
| `constituent_or_setup_id` | setup or P29 constituent identifier when applicable |
| `turn_index` | one-based order within the execution unit |
| `scored_turn` | boolean |
| `authoritative_attempt` | true only for calls in the first complete unit attempt |
| `case` | `jaundice` or `palpitations` |
| `safe_session_id` | stable safe identifier; never a URL, credential, or token |
| `physical_isolation_verified` | boolean |
| `model` | reported model name |
| `runtime` | exact runtime name |
| `exposed_generation_settings` | object or string `NOT_EXPOSED` |
| `input_bundle_id` | aggregate frozen input identity |
| `system_message_sha256` | case system-message identity |
| `learner_utterance` | exact transmitted learner text |
| `final_patient_response` | complete learner-visible final response, including an empty string on successful empty completion; null only on execution error |
| `provider_completion_status` | status reported by transport |
| `separate_reasoning_field_present` | boolean; reasoning content is never stored |
| `execution_error_class` | safe transport/harness class, or null |
| `execution_error_message_safe` | sanitized safe message, or null |
| `timestamp_utc` | RFC 3339 UTC timestamp for the attempted call |

## Preservation and retry rules

- Preserve the learner-visible final response exactly. Perform no trimming,
  cleanup, role repair, or heuristic reasoning removal.
- Do not store chain-of-thought, separate reasoning content, tool traces,
  credentials, authentication headers, session URLs, or raw secret-bearing
  exceptions.
- Absence of a final response is an execution error only when transport or the
  harness prevented a completed output.
- A successful empty completion is a valid scoreable model output.
- Safety refusals, non-Korean output, role drift, truncated successful output,
  and poor content are valid outputs and are never transport retries.
- A retry restarts the complete execution unit in a new physical session. All
  partial prior rows remain preserved and nonauthoritative.

Session-creation and session-close failures are preserved separately as
execution-attempt events; a failure before a model call must not fabricate a
raw-call row. A close failure makes every completed call in that attempt
nonauthoritative because physical isolation was not safely closed.

## Mandatory future execution-control provenance

Before any real preflight or official execution, records must bind directly or
through a separately accepted execution-control bundle to the accepted
fixture/runner checkpoint, runner file or accepted runner commit identity, real
transport-adapter identity, execution-authorization ID, passing
preflight-evidence ID, and `input_bundle_id`. These future accepted identities
do not exist in this candidate and are not included in its self-hashed bundle.
