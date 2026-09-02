# Context-bootstrap audit disposition

PILOT_ONLY / NON_PRODUCTION

This is a disposition record: the project's explicit treatment of the
independent audit findings on the governance context bootstrap. It is not a new
normative governance owner. `AGENTS.md` remains the router and repository-wide
contract, and `docs/CURRENT_STATE.md` remains the only mutable authority for
phase, gates, blockers, and next permitted action.

## Audit identity

| Field | Value |
|---|---|
| Target commit | `e9f7200bb14f08ea325ec378a50489f0b7c62dd7` |
| Base commit | `e1db18d0ef9e7cec931837389875b719e9250da4` |
| Branch | `governance/claude-context-bootstrap` |
| Auditor model | Claude Opus 5 |
| Provider / harness | Codex provider |
| Independent session | yes |
| Cross-harness review | yes |
| Cross-model review | no |
| Fable audit | no |
| Audit mode | independent read-only |
| Verdict | `PASS_AFTER_MINOR_PATCH` |
| Blockers | 0 |
| Merge unchanged | not recommended |

This was a cross-harness review by the same model family under a different
provider/harness. It is explicitly **not** a Fable audit and **not** a
cross-model audit. Fable auditing is deferred by user decision; that deferral
does not convert this review into an independent-model verdict.

## Accepted findings

1. **Probe provenance overstated.** The historical 12-call small probe did not
   preserve a complete immutable raw-response corpus for all 12 calls. The
   complete P25 response is preserved; the remaining rows carry scored
   dispositions and concise response evidence. `docs/CURRENT_STATE.md` is
   corrected to describe the record accurately and to record the historical
   provenance limitation.
2. **README scope stale.** The README claimed the repository contained only G1
   evidence work. It is corrected to describe both the G1 product-evidence
   baseline and the isolated G2 behavioral-contract pilot documentation.
3. **Mutable state in stable routing.** `AGENTS.md` carried a current
   `PAUSED` research value and prompt-version-specific wording. The research
   invariant is generalized to a problem-driven rule, the prompt invariant is
   generalized to a frozen-artifact rule, and the Korean-SP audit router row now
   names the current SP system prompt through `docs/CURRENT_STATE.md` instead of
   a hardcoded version path. The current `PAUSED` value remains only in
   `docs/CURRENT_STATE.md`.
4. **Probe plan unclassified.** `docs/pilot/g2.2-probe-plan.md` is classified in
   the active-artifact-owner table as historical evidence, with the role
   "historical small-probe execution plan and as-run limitation record".
5. **Post-merge synchronization required.** `docs/CURRENT_STATE.md` now records
   the explicit remaining merge lifecycle and the required content of the
   post-merge synchronization commit.

The raw-output invariant in `AGENTS.md` is additionally clarified to bind every
**future** official execution. Historical probe records are not rewritten to
pretend they already met that standard.

## Deferred finding

- Re-enumeration of the six unresolved human questions inside
  `docs/CURRENT_STATE.md` duplicates
  `docs/pilot/g2.1a-language-oracle-disposition.md`. This duplication is
  retained for now because those questions are operationally active and gate
  scoring dispositions. It must not be expanded further; new or adjudicated
  questions belong to the owning disposition record, referenced from current
  state.

## Scope of this disposition and its patch

Explicitly excluded:

- no pilot semantic change;
- no system prompt change;
- no model execution or probe;
- no schema, fixture, payload, or runner;
- no architecture escalation;
- no merge authorization;
- no full-suite authorization.

The patch changes only `AGENTS.md`, `README.md`, `docs/CURRENT_STATE.md`, and
this record. The SP system prompt, both behavior contracts, both trajectory
specifications, the evaluation specification, the probe records, and all G1
research evidence are byte-unchanged.

## Consequence

The verdict `PASS_AFTER_MINOR_PATCH` with the corrections above does not
authorize merge. Per the audit/disposition lifecycle in `AGENTS.md`, the
corrected proposal still requires a delta audit and explicit human acceptance
before an accepted merge to `main`, followed immediately by the post-merge
current-state synchronization.

`DELTA_AUDIT_REQUIRED = YES`

`MERGE_TO_MAIN_AUTHORIZED = NO`

`G2_FULL_BATCH_AUTHORIZED = NO`

`PRODUCTION_IMPLEMENTATION_AUTHORIZED = NO`
