# G1-PRODUCT-BASELINE

Date: 2026-09-02

Status: **REACHED**

Scope of this milestone: the evidence set is sufficient to begin bounded behavioral prototyping of a CPX standardized-patient contract. This is a product-development milestone, not a research-completeness milestone.

## What this milestone is not

- It is **not** systematic-review or scoping-review completion.
- It does **not** claim publication readiness or publication-grade search completeness.
- It does **not** replace later clinician or SP-methodology review.
- It does **not** authorize production deployment, dataset migration, or schema freeze.
- It does **not** convert any CPX v5 implementation vocabulary into an external standard.

What it does authorize: a bounded two-case behavioral prototype using synthetic or explicitly approved pilot material, evaluated against expert-authored trajectories.

## Why the gate model changed

The original G-1 exit criteria were written like publication criteria: database-native completeness across every planned index, an independent second reviewer adjudicating all 50-plus records, and full-text appraisal of high-directness sources. Those are the right criteria for an academic review and the wrong criteria for deciding whether a standardized-patient contract behaves correctly.

The immediate product question is not answerable by more literature. Whether a Korean CPX patient reveals the right fact at the right conversational moment is an empirical property of a specific case policy plus a specific model, and the current evidence already says so directly: LLM-005 shows forbidden information leaking despite clean instructions, and LLM-011 shows 56.4% of answers to script-uncovered questions using fictitious information. Neither finding is refined by additional searching.

The historical publication-style G-1 criteria remain documented in `protocol.md` section 10 and `g1-status.md`. They are hereby marked **RESEARCH-COMPLETENESS NOT PURSUED AT THIS STAGE** rather than deleted or restated as satisfied.

## Milestone criteria assessment

| # | Criterion | Status | Basis |
|---|---|---|---|
| 1 | Major human-SP case/disclosure principles have credible sources | MET | ASPE Standards of Best Practice (HSP-001), public SP program guidance on prompted-only disclosure and no ad-libbing (HSP-009), unannounced-SP fidelity coding of prompted/volunteered/omitted/withheld facts (HSP-012), AMEE Guide 81 Part II (HSP-010), and two role-template sources (HSP-015, HSP-016) |
| 2 | Known LLM-SP leakage, hallucination, and fidelity failure modes are represented | MET | Persistent forbidden-information leakage under clean and defended conditions (LLM-005), greeting over-disclosure and clinically unknowable answers (LLM-006), 56.4% fictitious answers to uncovered questions (LLM-011), transcript-level expert appropriateness rating (HSP-014), evaluation-metric work (LLM-007) |
| 3 | Korean CPX context is represented | MET | 10 Korean records including national clinical skill test implementation (KR-006), consortium case development and SP training (KR-007), a Korean AI standardized-patient system (KR-004), a Korean palpitations OSCE station with separated checklist domains (KR-009), and Korean LLM virtual-patient feasibility with examination-channel limits (KR-010) |
| 4 | Candidate behavioral requirements are explicitly labelled by epistemic type | MET | `disclosure-requirements.md` labels each of 13 requirements as High, Moderate-high, Moderate inference, or Hypothesis, and relocates DR-012 as an architecture hypothesis and DR-013 as a project preservation rule |
| 5 | No known restricted or recalled examination content is used | MET | `source-rights-register.csv` records access and reuse boundaries per source class; no examination case is reproduced. Two provenance limitations remain open and are stated below |
| 6 | No major known factual evidence error remains uncorrected | MET | G1.1 corrected stream counts, the HSP-005 year, and requirement misclassification. G1.2a corrected the Davies false negative and added HSP-016 |
| 7 | Evidence is sufficient to author two supervised pilot cases | MET | The twelve provisional behavioral principles below are each traceable to at least one credible source, which is enough to author jaundice and palpitations contracts for supervised testing |

## Provisional behavioral principles adopted for pilot testing

These are **product-level provisional principles**, not external standards and not frozen implementation vocabulary.

| # | Principle | Primary support | Epistemic type |
|---|---|---|---|
| 1 | Opening behavior is case-specific rather than universally greeting-only | HSP-015, HSP-016, LLM-006 | Evidence-informed, case-specific validation required |
| 2 | Information may be designated spontaneous versus question-contingent | HSP-009, HSP-012, HSP-005 | Evidence-derived |
| 3 | Open and focused questions may legitimately produce different amounts of information | HSP-012, HSP-009 | Evidence-derived for direction; exact breadth is inference |
| 4 | Reasonable in-scope questions should not be answered misleadingly sparsely | HSP-009, HSP-012 | Evidence-derived |
| 5 | Facts absent from the authored case should not be invented | HSP-009, LLM-011 | Evidence-derived |
| 6 | Patient-accessible knowledge must be distinguished from medical truth | LLM-006, LLM-005, KR-010 | Evidence-derived boundary; storage design is inference |
| 7 | Diagnosis, hidden test information, examiner-only information, and examination-only findings must not leak simply because the model can infer them | LLM-005, LLM-006 | Evidence-derived |
| 8 | Leading or false-premise questions must not overwrite established case truth | HSP-001 | Hypothesis requiring pilot validation |
| 9 | Repeated equivalent questions should remain factually consistent | HSP-001, HSP-010, HSP-011 | Evidence-derived |
| 10 | Human-SP standardization requires explicit case authoring, review, rehearsal, and revision rather than trusting a generic prompt | HSP-001, HSP-007, HSP-010, HSP-011, HSP-015, HSP-016, KR-001 | Evidence-derived |
| 11 | LLM prompt instructions alone do not prove behavioral fidelity | LLM-005 | Evidence-derived |
| 12 | Fidelity therefore requires trajectory-level testing for leakage, hallucination, omission, contradiction, and role drift | LLM-005, LLM-006, LLM-007, LLM-011, HSP-014 | Evidence-derived |

Principle 8 is the weakest. No located source directly validates false-premise correction behavior in an SP, so the pilot must treat it as a measured open question rather than a known rule.

Principle 1 deserves a specific caution. HSP-016 found that the 17 located SP templates "differed in structure, length, and depth." That supports having an explicit template while explicitly refusing to claim that any particular structure, including ours, is standardized.

## Limitations explicitly preserved

These are carried forward unresolved and must not be described as closed:

1. **No education or computing index has been searched natively.** ERIC, Scopus or Web of Science, ACM Digital Library, and IEEE Xplore remain unrun. Paused deliberately, not completed.
2. **Single-reviewer screening throughout.** Every inclusion and extraction decision in this repository carries one reviewer. No independent human second review has occurred.
3. **HSP-006 and HSP-008 provenance is unresolved.** Detailed findings rest on secondary-hosted copies; authorized originals are not obtained.
4. **Full-text appraisal is outstanding** for HSP-015, HSP-016, KR-004, KR-009, KR-010, KR-011, and KR-012, plus most medium- and low-directness sources.
5. **DBpia's 1,981-record corpus is unscreened** and KoreaMed's 53-record case-authoring family was sampled rather than fully screened.
6. **No Korean source establishes a validated turn-level disclosure taxonomy.** Nine targeted Korean queries returned zero. Given KoreaMed's lack of Korean indexing and the unscreened DBpia corpus, this is a bounded finding and not proof of absence.
7. **The proposed zero-error thresholds are local engineering targets**, not literature-established universal cutoffs.
8. **No clinician or SP-educator review has occurred** for any requirement or pilot trajectory.

## Research expansion policy from this point

Broad literature expansion is **PAUSED**. New evidence is sought problem-driven only, when all three of the following hold:

1. an observed behavioral failure cannot be resolved from the current baseline;
2. the correct human-SP behavior is genuinely uncertain, Korean-specific behavior is disputed, or the decision has material safety or assessment implications;
3. the question is specific enough to answer with a targeted search rather than a corpus sweep.

Relevance to standardized patients is **not** by itself a reason to add a source.

If an academic publication is later prepared from this review, the stricter research-completeness track reopens separately and does not block product work in the meantime.

## Authorization boundary

Authorized: bounded two-case behavioral prototyping (jaundice, palpitations) with human-readable contracts, gold trajectories, an evaluation spec, and a minimal system prompt, using synthetic or explicitly approved pilot material.

Not authorized: production deployment, dataset migration, production schema design, disclosure enum freeze, SP2D import, semantic-router construction, application implementation, or generalization from two cases to the full corpus.
