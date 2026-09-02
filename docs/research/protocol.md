# G-1 rapid scoping review protocol

Status: protocol v0.1 / seed search in progress
Date: 2026-09-02
Review purpose: CPX v5 product-design evidence, not a completed publication-grade systematic review

## 1. Objective

Map the evidence needed to design a Korean LLM standardized patient that
reveals information in a clinically authentic, repeatable, and assessable way.
The review precedes application scaffolding and schema design.

The review does **not** assume that the provisional CPX disclosure modes are an
established taxonomy. It will derive candidate requirements from human-SP
standards, empirical SP fidelity research, virtual-patient research, LLM
virtual-patient research, Korean CPX literature, and the existing local SP
research corpus.

## 2. Preservation and rights boundaries

- `CPX_V4_ROOT` remains untouched.
- `CPX_SOURCE_ROOT` remains read-only.
- Public citations and paraphrased design principles may be recorded.
- Copyrighted case templates and scripts are not copied wholesale.
- Leaked, recalled, reconstructed, pirated, login-only, or otherwise
  unauthorized examination material is excluded.
- No current CPX server dataset or scoring criterion is changed during G-1.

## 3. Review method

This is a rapid scoping review using the JBI scoping-review method as the
methodological reference and PRISMA-ScR as the reporting checklist. The first
pass is a single-reviewer seed map. A second independent reviewer is required
before G-1 can be considered complete.

### PCC framework

- **Population:** human standardized/simulated patients and virtual or
  LLM-based standardized patients used with health-professions learners.
- **Concept:** case development, role fidelity, patient knowledge boundaries,
  staged disclosure, question-contingent disclosure, consistency, and
  evaluation of premature or unsupported disclosure.
- **Context:** history taking, clinical interviewing, OSCE, CPX, and related
  formative or summative simulation.

## 4. Research questions

1. Which information should a human SP volunteer, and which should be disclosed
   only after an appropriate learner question?
2. How should disclosure scope differ after greetings, reason-for-visit
   questions, open invitations, focused questions, compound questions, and
   leading questions?
3. How are patient-knowable history and symptoms separated from examination,
   investigation, diagnosis, and examiner-only information?
4. How are repeatability, truth preservation, role fidelity, and resistance to
   ad-libbing evaluated in human SPs?
5. Which failure modes and metrics are used for virtual and LLM patients?
6. Which controls beyond a system prompt are supported when a model leaks or
   invents information?
7. Which rules require Korean-language or Korean-CPX-specific validation?

## 5. Information sources

Planned sources:

- PubMed/MEDLINE
- ERIC
- Scopus or Web of Science, where available
- ACM Digital Library and IEEE Xplore
- KoreaMed, KCI, RISS, and DBpia
- ASPE, INACSL, SSH, and public university SP-program guidance
- Backward and forward citation chasing
- Read-only local `CPX_SOURCE_ROOT` accepted reports and invalidated experiments

The current seed pass used web discovery to identify primary and official
sources. Two PubMed searches were then executed through NCBI E-utilities on
2026-09-02 and returned 58 query records / 57 unique PMIDs. Korean and
education/engineering database-native searches and final deduplication remain
required.

## 6. Eligibility criteria

### Include

- Standards, consensus guidance, or empirical studies describing SP case
  development, training, or fidelity.
- Studies measuring what was elicited, omitted, volunteered, contradicted, or
  invented in a patient interview.
- Virtual-patient or LLM-patient systems used for clinical interviewing or
  history-taking education.
- Studies exposing implementation details, evaluation dimensions, test
  trajectories, or reproducible failure examples.
- Korean CPX/SP case-development, training, reliability, or AI-SP studies that
  inform local adaptation.

### Exclude

- Diagnostic-answer benchmarks with complete vignettes and no interactive
  patient role.
- Patient-facing advice chatbots acting as clinicians rather than patients.
- Marketing pages, informal exam-preparation advice, unsourced blogs, and
  social-media anecdotes as design evidence.
- Sources whose only available copy appears unauthorized.
- Materials that expose or reconstruct live examination content.

## 7. Search limits

- Human SP and classical virtual-patient literature: no initial date limit.
- LLM patient literature: 2020 onward, with citation chasing to older enabling
  work where needed.
- Languages: Korean and English.
- Publication status: peer-reviewed work, standards, official guidance, and
  clearly labelled preprints. Preprints must not be treated as equivalent to
  peer-reviewed evidence.

## 8. Screening and extraction

Each record receives:

- source type and review stream;
- inclusion status and exclusion reason;
- population, context, and intervention/system description;
- disclosure rule or fidelity principle;
- patient-knowledge boundary;
- open/closed/leading-question behavior;
- evaluation method and reported failure modes;
- directness to CPX v5;
- limitations and rights/reuse notes.

The evidence matrix uses `high`, `medium`, or `low` **directness**, not GRADE
certainty. These mixed normative, qualitative, engineering, and educational
sources do not support a single clinical-effect certainty score.

## 9. Synthesis method

Evidence will be synthesized into observable behavior requirements rather than
copied into a predetermined state machine. Each candidate requirement must
identify:

- supporting human-SP evidence;
- supporting or conflicting virtual/LLM-patient evidence;
- whether it is directly supported, inferred, or an engineering hypothesis;
- expected learner utterances and allowed patient information units;
- a measurable failure condition.

## 10. G-1 exit criteria

Status note added 2026-09-02: these are publication-style research-completeness
criteria. They are retained as the historical record and marked
**RESEARCH-COMPLETENESS NOT PURSUED AT THIS STAGE**. Product work now proceeds
under the separate `G1-PRODUCT-BASELINE` milestone documented in
`g1-product-baseline.md`, which does not claim systematic-review completeness.

G-1 is complete only when:

1. At least 30 relevant sources have been screened, including Korean evidence.
2. Database-native searches and citation chasing are logged reproducibly.
3. A second reviewer adjudicates inclusion and the high-impact extractions.
4. Every proposed disclosure requirement has traceable evidence and a stated
   limitation.
5. The jaundice and palpitations pilots have expert-reviewed expected-response
   tables for greeting, reason-for-visit, open, focused, leading, repeated,
   diagnosis, and examination requests.
6. Unsupported rules remain labelled as hypotheses rather than standards.
7. A rights review confirms that no restricted examination content is used.

## 11. Current limitations

- The seed search is not a complete systematic search.
- One reviewer performed the current screening and extraction.
- Web-discovery result counts are not suitable for a PRISMA flow diagram;
  PubMed counts and PMIDs are reproducible and recorded separately.
- Several recent LLM studies are preprints or early feasibility studies.
- Korean literature located so far emphasizes CPX implementation and
  assessment more than turn-level disclosure policy.
