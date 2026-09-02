# CPX v5 research workspace

This directory currently contains only the G-1 evidence work for staged
standardized-patient disclosure. It is not an application scaffold and has no
runnable CPX code yet.

Preservation boundaries:

- `CPX_V4_ROOT` is the current application baseline and must not be
  modified by G-1.
- `CPX_SOURCE_ROOT` is a read-only research reference.
- No proprietary, recalled, leaked, or access-controlled examination script is
  copied into this workspace.
- Source texts are represented by citations, short evidence extractions, and
  rights notes. Case scripts are not reproduced.

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

Local source aliases are intentionally machine-independent:

- `CPX_V4_ROOT`: the local checkout of CPX v4
- `CPX_SOURCE_ROOT`: the canonical `phase_sp0_source_discovery` research root
