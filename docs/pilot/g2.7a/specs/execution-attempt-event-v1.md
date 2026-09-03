# G2.7a execution-attempt event v1

Classification: **PILOT_ONLY / NON_PRODUCTION**

An execution-attempt event is a lifecycle record for one execution-unit
attempt. It is not a patient-model raw-call row and cannot be used as patient
response evidence.

## Required fields

| Field | Type / rule |
|---|---|
| `execution_unit_id` | manifest execution unit |
| `unit_attempt_index` | integer 1 through 3 |
| `event_type` | `SESSION_CREATION_FAILED`, `ATTEMPT_FAILED`, `SESSION_CLOSE_FAILED`, or `ATTEMPT_COMPLETED` |
| `safe_session_id` | stable public-safe identifier when a session exists; otherwise null |
| `execution_error_class` | safe error class, or null for a completed attempt |
| `execution_error_message_safe` | sanitized safe message, or null for a completed attempt |
| `timestamp_utc` | RFC 3339 UTC timestamp |
| `input_bundle_id` | aggregate frozen input identity |
| `authoritative_attempt` | true only for the safely completed selected attempt |
| `model_call_created` | whether at least one raw-call row exists for the attempt |

Session creation failure consumes an attempt and produces no raw-call row.
Session close failure makes the attempt nonauthoritative, preserves its
completed raw-call rows, and requires a complete-unit retry in a new physical
session when attempts remain. Unexpected exceptions are represented only by a
generic safe class and message; raw exceptions, credentials, URLs, and tokens
must never be recorded.
