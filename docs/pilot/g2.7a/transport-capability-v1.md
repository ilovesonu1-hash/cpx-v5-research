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

## Target-path capability disposition

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
