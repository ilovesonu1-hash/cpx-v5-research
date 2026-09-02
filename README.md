# CPX v5 research workspace

## Repository authority

- [`CLAUDE.md`](CLAUDE.md): the Claude Code adapter; it imports the router.
- [`AGENTS.md`](AGENTS.md): the repository task router, authority precedence,
  and invariants.
- [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md): the current phase, gate,
  blocker, and next-permitted-action authority.

This README is a human entry point, not an operational authority.

This repository contains the G1 product-evidence baseline and the isolated G2
behavioral-contract pilot documentation. It is not an application scaffold and
contains no production CPX implementation.

Preservation boundaries:

- `CPX_V4_ROOT` is the protected current application baseline and is outside
  this research/pilot repository's write authority.
- `CPX_SOURCE_ROOT` is a read-only research reference.
- No proprietary, recalled, leaked, or access-controlled examination script is
  copied into this workspace.
- Source texts are represented by citations, short evidence extractions, and
  rights notes. Case scripts are not reproduced.

Pilot documents are in [`docs/pilot`](docs/pilot): the SP system prompt, the
two case behavior contracts, their trajectory specifications, the evaluation
specification, and the small-probe records.

Research documents are in [`docs/research`](docs/research):

- `protocol.md`: review scope and G-1 exit criteria
- `search-log.csv`: executed and planned searches
- `pubmed-title-screen.csv`: all 58 PubMed query records and decisions
- `screening-log.csv`: included seed evidence and exclusions
- `evidence-matrix.csv`: extracted design evidence
- `evidence-synthesis.md`: current synthesis and evidence gaps
- `disclosure-requirements.md`: evidence-linked candidate requirements
- `source-rights-register.csv`: access and reuse boundaries
- `local-source-manifest.csv`: SHA-256 anchors for the read-only local evidence
- `g1-status.md`: current gate decision and remaining blockers
- `g1.1-audit-disposition.md`: disposition of the independent seed-evidence audit
- `g1.2-search-completeness.md`: Korean database-native search remediation
- `g1-product-baseline.md`: product-evidence baseline milestone and paused research expansion

Local source aliases are intentionally machine-independent:

- `CPX_V4_ROOT`: the local checkout of CPX v4
- `CPX_SOURCE_ROOT`: the canonical `phase_sp0_source_discovery` research root
