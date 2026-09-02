# CPX v5 research repository — agent router

- **Purpose:** state the small repository-wide contract and route each task to
  its minimum controlling documents.
- **Ownership domain:** authority interpretation, repository-wide invariants,
  session bootstrap, task classification and routing, documentation ownership,
  and the audit/disposition lifecycle.
- **Does not own:** current phase or gates, detailed SP behavior, exact
  trajectory oracles, evidence extraction, or run outputs. Those belong to
  `docs/CURRENT_STATE.md` and to the active normative documents named below.
- **Governs:** every human or automated contribution to this repository.

## Canonical repository

`ilovesonu1-hash/cpx-v5-research` is the canonical Git memory for this isolated
research and pilot workspace. Before changing it, verify that the checkout,
remote, branch, and base commit are the intended ones.

Boundaries this repository does **not** extend over:

- `CPX_V4_ROOT` (cpx-v4) is a separate protected application baseline.
- `CPX_SOURCE_ROOT` is external, read-only research evidence.
- Production scenario data, production schemas, and SP2D artifacts are outside
  this repository's authority.

Copying, transcribing, linking, or referencing content does not transfer
authority over it. A path or filename is not semantic identity.

## Authority precedence

Use this order when interpreting repository text:

1. Explicitly accepted decisions, dispositions, authorizations, and accepted
   checkpoint records govern their bounded domain.
2. This `AGENTS.md` owns repository-wide interpretation, invariants, and task
   routing.
3. `docs/CURRENT_STATE.md` owns only current phase, effective checkpoint,
   gate/readiness state, blockers, active artifact identities, and the next
   permitted action. It cannot redefine a contract.
4. The active normative document named by the router owns the detailed behavior
   or contract in its domain and must faithfully incorporate accepted
   dispositions.
5. Immutable audits, reviews, probe results, run reports, manifests, and
   historical checkpoints preserve evidence and provenance. They do not describe
   current state unless `docs/CURRENT_STATE.md` or an active normative document
   incorporates them.
6. `README.md` is a human entry point, not operational authority.
7. Chat history, resumed-session memory, auto memory, filenames, and directory
   names are never authority.

If these cannot be reconciled from already accepted text, stop and report
`GOVERNANCE_DECISION_REQUIRED`. Preserve the competing text; do not silently
adopt whichever document appears newest.

## Repository-wide invariants

- Verified repository state overrides chat history and session memory.
- Completing, testing, committing, or auditing one step never authorizes the
  next step automatically.
- An audit finding is not an active decision until an explicit disposition
  accepts, modifies, defers, or rejects it.
- Current state must not duplicate detailed normative content; it references the
  owner instead.
- Accepted historical records are not rewritten to match later state.
- Research expansion must be problem-driven and governed by the active research
  policy and current state. Topical relevance alone is not a reason to expand
  the evidence corpus.
- An artifact marked frozen by `docs/CURRENT_STATE.md` must not be modified
  outside an explicitly accepted change envelope. Prompt revision additionally
  requires preserved failure evidence and the routed normative context.
- No architecture escalation — router, classifier, state machine, output filter,
  orchestration, retrieval — without a documented repeated structural failure
  that the smallest responsible layer cannot absorb.
- For every future official execution, complete final model outputs must be
  frozen before scoring or interpretation.
- No model or provider comparison, substitution, or migration unless the user
  explicitly requests it.
- No restricted or recalled examination content, PHI, secrets, credentials,
  private absolute machine paths, or unauthorized source bytes are committed.
- No production integration unless `docs/CURRENT_STATE.md` names an accepted
  envelope for it.
- Concurrent branches and worktrees are preserved. Unrelated work is never
  reset, cleaned, stashed, or folded into another task's commit.
- cpx-v4, `CPX_SOURCE_ROOT`, production scenario data, production schemas, and
  SP2D artifacts do not change implicitly.

Current commit identities are **not** recorded here. They belong in
`docs/CURRENT_STATE.md`.

## Active versus historical text

- **Active normative document** — the current bounded contract or specification
  for its domain: behavior contracts, trajectory specifications, the evaluation
  specification, the system prompt.
- **Current-state record** — `docs/CURRENT_STATE.md`, the only mutable authority
  for phase, gates, blockers, and next permitted action.
- **Immutable historical record** — audits, reviews, probe results, run reports,
  manifests, and accepted checkpoints. Evidence and provenance, not status.
- **Disposition / decision record** — the project's explicit treatment of audit
  findings: accepted, accepted with modification, deferred, or not adopted.

A search hit inside a historical document does not regain normative authority
because its text is relevant. Never normalize an accepted historical record to
match later state; record the later fact in current state, in the active
normative owner, or in a new evidence record.

## Session bootstrap

Every substantive task in this repository begins by:

1. verifying repository identity, remote, branch, HEAD, worktree list, and
   working-tree dirty state;
2. reading `AGENTS.md`;
3. reading `docs/CURRENT_STATE.md`;
4. classifying the task mode and domain;
5. loading only the documents routed for that mode;
6. determining read scope, write scope, protected paths, required validation,
   and the stopping boundary before editing anything.

Do not begin with a broad repository crawl, and do not load the audit history by
default.

## Task modes

Exactly one primary mode per task:

`ORIENTATION`, `DESIGN`, `IMPLEMENTATION`, `AUDIT`, `EXECUTION`,
`DOCUMENTATION`, `INVESTIGATION`.

A domain refines a mode; it never creates a parallel governance system. Korean
language realism, clinical truth, and structural batch readiness are **domains
routed by this one system**, for example:

- `AUDIT / KOREAN_SP_REALISM`
- `AUDIT / CLINICAL_TRUTH`
- `AUDIT / BATCH_STRUCTURE`
- `IMPLEMENTATION / CONTRACT_ORACLE`
- `IMPLEMENTATION / SYSTEM_PROMPT`
- `EXECUTION / BEHAVIORAL_SUITE`
- `DOCUMENTATION / CURRENT_STATE`

## Minimum-context task router

`AGENTS.md` and `docs/CURRENT_STATE.md` are implicit in every row. Add
historical evidence only when exact provenance or a named envelope requires it.

| Task | Minimum additional context | Default write scope |
|---|---|---|
| Project orientation or present status | `README.md`, only when human-facing orientation is needed | read-only |
| G1 evidence or literature question | `docs/research/protocol.md`; the active research status or synthesis document for the exact question | read-only |
| Korean SP language, realism, or assessment-fairness audit | the current SP system prompt named by `docs/CURRENT_STATE.md`; both behavior contracts; both trajectory specifications; the latest accepted language/oracle disposition named by current state | read-only |
| Clinical-truth or patient-knowledge audit | the target case contract; the affected trajectory rows; only the clinical source the task explicitly names | read-only |
| Contract or oracle correction | the exact audit evidence; the accepted disposition; only the affected contracts and trajectories; the relevant evaluation rule | bounded write, only when explicitly authorized |
| System-prompt revision | the current prompt; frozen failure evidence; affected contracts and oracles; `docs/pilot/g2-evaluation-spec.md` | unauthorized unless current state or the user names an accepted prompt-revision envelope |
| Structural pre-batch audit | current prompt identity; `docs/pilot/g2-evaluation-spec.md`; the proposed execution envelope; fixture and payload snapshots; runner and session-isolation design; raw-output and scorecard provenance design | read-only |
| Behavioral execution | the exact accepted execution envelope named by current state; frozen prompt; frozen payloads; frozen trajectory manifest; runtime configuration; validation and stop rules | forbidden when no exact envelope is accepted |
| Scoring or result interpretation | frozen raw outputs; the frozen trajectory oracle; `docs/pilot/g2-evaluation-spec.md`; the accepted scoring envelope | bounded write to the scoring record only |
| Frontend or design work | its own owning documents, in its own branch or worktree | isolated; never merged implicitly into pilot or governance work |
| Production integration | — | forbidden unless current state records an explicit accepted authorization |

Additional routing rules:

- Do not load the full evidence matrix unless the exact question requires it.
- Broad G1 literature expansion is unauthorized unless current state or the user
  explicitly reopens it.
- Do not convert an unresolved clinical judgement into an engineering decision.
- Do not run a model probe as part of a contract or oracle correction; probes
  require separate authorization.
- Do not reopen Korean language realism during a structural audit unless a
  structural result depends on a specific unresolved oracle.
- Raw output must predate scoring, and no oracle may be changed after an
  official response has been read.

## Audit, disposition, patch, state lifecycle

```text
AUDIT
-> DISPOSITION
-> AUTHORIZED NORMATIVE PATCH
-> VALIDATION
-> ACCEPTANCE
-> CURRENT STATE UPDATE
-> NEXT PERMITTED ACTION
```

- Audit is read-only unless the user explicitly authorizes a later correction
  task. Auditors do not silently patch what they find.
- Auditor recommendations are not automatically adopted. Accepted, modified,
  deferred, and rejected findings all remain traceable in the disposition
  record.
- The resulting normative artifacts, not the raw audit report, are the
  executable contract afterwards.
- An audit PASS does not authorize execution, merge, or the next phase.

## Execution discipline

For any exact execution:

- reverify all live inputs, artifact identities, and hashes before starting;
- freeze prompt, payload, oracle, and scoring rules before the first official
  call, and change none of them mid-run;
- distinguish trajectories, calls, sessions, setup turns, retries, and errors,
  and exclude non-official turns from scoring;
- preserve complete final outputs before scoring;
- never store or expose private model reasoning as patient dialogue;
- stop fail-closed when session isolation or input identity cannot be verified.

## Documentation maintenance

Ownership:

- `docs/CURRENT_STATE.md` — current mutable state only.
- Active contracts and specifications — stable detailed behavior.
- Audits, reviews, probe and run records — immutable historical evidence.
- Disposition and decision records — the project's treatment of findings.
- `README.md` — human entry point.

Rules:

1. Update the existing owner rather than creating a parallel document.
2. Do not create Markdown for every minor debugging event; summarize such events
   in the eventual checkpoint or evidence record.
3. Do not let `docs/CURRENT_STATE.md` become a chronological log; compact
   superseded state into referenced immutable records.
4. Do not duplicate one fact across multiple active authorities.
5. Add every new normative document to the router above.
6. When a change alters behavior or a contract owned elsewhere, update that
   owner in the same change.
