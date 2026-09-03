# G2.7a transport capability inspection v1

Date: 2026-09-03
Classification: **PILOT_ONLY / NON_PRODUCTION**
Status: **REAL_TRANSPORT_INTERFACE_PARTIALLY_VERIFIED**

This is a no-call capability inspection. It is not preflight evidence, session
isolation evidence, execution authorization, or proof that the required
patient-model runtime is available.

## Inspected surface

Commands run without a prompt:

```text
claude --version
claude --help
```

Observed public CLI version: `2.1.259 (Claude Code)`.

No settings file, environment variable value, credential, token, authentication
header, keychain entry, or provider configuration was read. No prompt was sent
and no model/provider call occurred.

## Capability disposition

| Required capability | No-call observation | Status |
|---|---|---|
| Explicit new physical session per execution unit | Help exposes `--session-id` and `--fork-session`, but physical isolation for the required runtime was not demonstrated. | partial |
| History continuity within one execution unit | Help exposes `--resume`, `--continue`, and session identifiers. Continuity was not exercised. | partial |
| Stable safe session identifier | A caller-supplied UUID is supported, but a stable returned safe identifier was not verified. | partial |
| Machine-readable final assistant response | Help advertises `--output-format json` and `stream-json`; the exact returned schema was not inspected through a call. | partial |
| Final response separated from reasoning/tool traces | Help distinguishes output formats and reasoning-related streaming options, but final-field separation was not verified. | unverified |
| Exact runtime `google-vertex/gemini-3.7-flash` | The inspected CLI's model option documents Claude aliases/full names. The required runtime was not verifiable from help. | unverified |

Because all six requirements are not verified, no real adapter is implemented.
The runner contains only a process-local fake used by unit tests and refuses
both `preflight` and `execute`. A later task must independently verify the
actual authorized harness before any execution-capable adapter is considered.
