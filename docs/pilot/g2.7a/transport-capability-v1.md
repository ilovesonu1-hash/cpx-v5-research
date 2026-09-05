# G2.7a transport capability inspection v1

Date: 2026-09-03
Classification: **PILOT_ONLY / NON_PRODUCTION**
Status: **HARNESS_CAPABILITY_UNVERIFIED**

This is a no-call capability inspection. It is not preflight evidence, session
isolation evidence, execution authorization, or proof that the required
patient-model runtime is available.

## Background observation only

Commands run without a prompt:

```text
claude --version
claude --help
```

Observed public CLI version: `2.1.259 (Claude Code)`.

No settings file, environment variable value, credential, token, authentication
header, keychain entry, or provider configuration was read. No prompt was sent
and no model/provider call occurred.

The observed surface was Claude Code CLI help. It is not the actual
Gemini-serving Paseo/provider path required for
`google-vertex/gemini-3.7-flash`; generic CLI features were only partially
observed and cannot verify the target harness.

## Prior generic-CLI assessment (not target-path proof)

| Required capability | No-call observation | Status |
|---|---|---|
| Explicit new physical session per execution unit | Help exposes `--session-id` and `--fork-session`, but physical isolation for the required runtime was not demonstrated. | partial |
| History continuity within one execution unit | Help exposes `--resume`, `--continue`, and session identifiers. Continuity was not exercised. | partial |
| Stable safe session identifier | A caller-supplied UUID is supported, but a stable returned safe identifier was not verified. | partial |
| Machine-readable final assistant response | Help advertises `--output-format json` and `stream-json`; the exact returned schema was not inspected through a call. | partial |
| Final response separated from reasoning/tool traces | Help distinguishes output formats and reasoning-related streaming options, but final-field separation was not verified. | unverified |
| Exact runtime `google-vertex/gemini-3.7-flash` | The inspected CLI's model option documents Claude aliases/full names. The required runtime was not verifiable from help. | unverified |

Because all six requirements are not verified for the actual target path,
target harness capability is `HARNESS_CAPABILITY_UNVERIFIED`. No real adapter
is implemented. The runner contains only a process-local fake used by unit
tests and refuses both `preflight` and `execute`.

This does not invalidate the deterministic fixture bundle. It does block real
preflight and execute enablement until a later authorized task independently
verifies the Gemini-serving Paseo/provider path without guessing.

## Current offline-review target-path inspection

The offline-review checkpoint inspected the actual available Paseo/OpenCode
metadata path, not a Claude model alias. No agent/session was created and no
prompt, authentication value or credential file was read or sent.

Public-safe observations:

- Paseo `list_providers`: OpenCode is enabled and available.
- Paseo `list_models(provider=opencode)`: the catalog exposes the Vertex
  provider namespace. No model was invoked.
- Paseo `inspect_provider` with draft model
  `google-vertex/gemini-3.7-flash`: returned that exact `selectedModel` and
  `auto_accept=false`. This is configuration metadata, not a serving test.
- Installed `opencode --version`: `1.18.28`.
- `opencode session --help`: lists session listing/deletion, not a separately
  documented physical-session create-and-system-message transaction.
- `opencode run --help`: advertises `--session`, `--continue`, `--fork`,
  provider/model selection, raw JSON events, and a thinking-display option.
  Help was requested without a positional message; run itself was not invoked.

| Required property | Target-path static result |
|---|---|
| Fresh physical session with the exact single patient system message | Not verified. Paseo agent creation requires an initial prompt, and the inspected help does not specify the needed separate initialization contract. |
| Same-session history | Session/continue flags observed; history semantics not exercised or fully specified. |
| Public-safe returned session ID | Session addressing observed; returned ID shape and lifetime not verified. |
| Designated learner-visible final response separate from reasoning/tools | Raw JSON events and thinking display observed; a final-only typed extraction field was not verified. |
| Exact runtime | Exact draft selection observed; provider availability and serving were not tested. |
| Close semantics | A delete command exists; safe closure/isolation guarantees were not verified and deletion was not run. |

The smallest missing adapter contract is **explicit fresh physical-session
initialization carrying exactly the supplied patient system message on this
Paseo/OpenCode target path**. Final-field extraction and close semantics also
need documentation before any adapter proposal. Generic flags or source-text
keyword checks are not isolation evidence.

Status remains `HARNESS_CAPABILITY_UNVERIFIED`; adapter remains absent, runtime
unchanged, preflight/execute disabled. No adapter is implemented by this review.
The single implementation report is `offline-review-checkpoint-v1.md`.
