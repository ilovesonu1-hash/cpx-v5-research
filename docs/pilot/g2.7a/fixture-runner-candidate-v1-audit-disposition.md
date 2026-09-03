# G2.7a fixture and runner candidate v1 audit disposition

Status: **PROPOSED / NOT YET ACCEPTED**

## Scope

This proposed disposition addresses the independent static/delta audit of base
`1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6` to target
`f11df66df7fc12a860cc1beac76bcd53685f22f7`. It accepts blocker B1 and major
findings M1 through M4 for bounded correction. It accepts both minor findings
as required pre-execution provenance clarifications.

## Accepted corrections

- Treat `1db27d6c91abf5d2bcc87a0e11bdb4dfb46fbee6` as the candidate base
  commit, not a permanent live `origin/main` requirement.
- Complete the payload response-scope behavior and compute structural
  provenance from parsed source and payload inventories while retaining human
  audit as the semantic-equivalence authority.
- Place session creation and close inside an explicit, safe whole-unit attempt
  lifecycle, with separate attempt events and no fabricated pre-call raw row.
- Add deterministic validation for future raw-call/session/event corpora.
- Freeze ordered planned evidence-call dependencies for all 58 score rows.
- Mark the target Gemini-serving harness unverified and require future
  execution-control provenance before preflight or execution.

## Boundaries

This disposition changes no accepted prompt, behavior contract, trajectory,
or evaluation rule and adds no clinical fact. It adjudicates no human-review
question. It implements no real transport, performs no model call or
preflight, creates no execution authorization, and makes no architecture
escalation. The corrected candidate remains **PILOT_ONLY / NON_PRODUCTION** and
**PROPOSED / NOT YET ACCEPTED** pending independent delta audit and later human
acceptance.
