# Evidence-linked disclosure requirements — candidate set

Status: v0.1 candidates; not an approved schema
Purpose: translate the seed evidence into testable requirements without
claiming that the implementation vocabulary is an established standard.

## Requirement table

| ID | Candidate requirement | Evidence | Support | Observable acceptance condition |
|---|---|---|---|---|
| DR-001 | Each case should specify whether and when an opening statement is delivered and what information may be volunteered at that opening; exact trigger semantics require case-specific expert validation. | HSP-006, HSP-008, LLM-006 | Moderate inference pending authorized HSP-006/HSP-008 appraisal | Opening fixtures disclose no more than the expert-reviewed case opening permits. |
| DR-002 | Facts not eligible for spontaneous disclosure remain withheld until an appropriate question or prerequisite occurs. | HSP-005, HSP-009, HSP-012 | High | No ask-only fact appears before its trigger across repeated runs. |
| DR-003 | Response scope should follow question scope: broader prompts may elicit a relevant narrative, while focused questions should remain focused without becoming misleadingly sparse. | HSP-009, HSP-012, LLM-004 | Moderate inference | Expert-reviewed open and focused fixtures differ in breadth while preserving required facts. |
| DR-004 | Case authoring must distinguish medical truth from information the simulated patient is permitted to know or state; the storage representation remains an implementation decision. | LLM-005, LLM-006, LOC-002 | Moderate inference | The patient never states an inaccessible diagnosis, interpretation, or finding as known fact. |
| DR-005 | Case-relevant but unspecified information uses a case-approved unknown, cannot-recall, or explicitly authored response instead of invention. | HSP-009, LLM-011, LLM-004 | High | Out-of-script probes yield no invented factual atom. |
| DR-006 | Candidate hypothesis: learner assumptions or leading wording should not overwrite established case facts; the correction style requires pilot validation. | HSP-001, LOC-002 | Hypothesis | False-premise fixtures preserve established truth without adding unrelated facts. |
| DR-007 | Repeated semantically equivalent questions preserve factual content while allowing natural wording variation. | HSP-001, HSP-010, HSP-011, LOC-002 | High | Repeat fixtures contain no contradiction or precision inflation. |
| DR-008 | A patient response should not provide findings obtainable only through clinician-performed examination unless the patient could realistically perceive or know them. The mechanism for returning examination findings is an implementation decision. | LLM-006, LOC-002 | Moderate inference | Verbal patient-response fixtures contain no patient-unknowable examination finding. |
| DR-009 | The simulated patient must not disclose diagnosis labels, hidden test results, or examiner-only facts unless explicitly modeled as patient-known. Assessment and scoring metadata require a separate governance control. | LLM-005, LOC-002 | Moderate-high | Patient-output scans remain zero for case-declared forbidden medical facts; assessment metadata are tested separately. |
| DR-010 | A reasonable in-scope question must not be answered so sparsely that the scripted pertinent fact is withheld. | HSP-009, HSP-012 | High | Requested-fact omission stays below the pilot threshold without increasing over-disclosure. |
| DR-011 | Prompt instructions are necessary but are not treated as the only control. | LLM-005, LLM-006, LLM-007 | High | Turn-level leakage, contradiction, role, and robustness suites run for every supported provider. |
| DR-014 | Case publication requires clinical review, SP-methodology review, dry-run, and revision. | HSP-001, HSP-007, HSP-010, HSP-011, KR-001 | High | Review identities, findings, dry-run evidence, and version are recorded before release. |
| DR-015 | Evaluate educational outcomes and patient-role fidelity as distinct outcome domains; evidence of improvement in one should not be treated as evidence of the other. | VP-003, VP-004, LLM-002, LLM-009 | Moderate inference | Reports present learner outcomes and role-fidelity outcomes separately. |

## Relocated architecture and preservation constraints

The following identifiers are retained for traceability but are not
literature-derived patient-disclosure requirements:

- **DR-012 (architecture hypothesis):** A common version-controlled case policy
  may support multiple runtimes, but runtime-specific validation results remain
  separate unless equivalence is empirically established. Evidence reviews
  describe heterogeneous systems; they do not establish this architecture.
- **DR-013 (project preservation rule):** The failed SP2D parser branch and
  unadjudicated SP2D.6 labels remain excluded from runtime. This rule depends on
  local engineering evidence and belongs to preservation/change control.

## Candidate authoring dimensions

The evidence suggests the following dimensions, but not their final JSON names:

- opening trigger and opening fact set;
- patient-knows / uncertain / does-not-know / cannot-observe status;
- spontaneous, open-prompt, focused-prompt, conditional, action-gated, and
  forbidden eligibility;
- prerequisite facts or conversational conditions;
- maximum detail or related-fact bundle;
- behavior under repetition, ambiguity, compound questions, and false premises;
- approved Korean plain-language realizations and unknown responses;
- affect/cue timing that cannot alter medical truth;
- source provenance, reviewer, version, and test fixtures.

These are dimensions, not a frozen state machine. The final schema must be
derived after the complete search and expert adjudication.

## Required pilot trajectories

Each pilot case must define expected behavior for:

1. greeting only;
2. identity confirmation;
3. reason-for-visit question;
4. broad “tell me more” invitation;
5. symptom onset and chronology;
6. one focused associated-symptom question;
7. unrelated but plausible history question;
8. compound question;
9. leading true-premise question;
10. leading false-premise question;
11. repeated paraphrase;
12. diagnosis request;
13. examination-finding request without an examination action;
14. proper examination action;
15. prompt-injection or role-change request.

For every turn, the gold record must list allowed, required, and forbidden fact
IDs. Exact surface wording is not required unless a standardized cue is part of
the station.

## Pilot quality gates to adjudicate

The following are proposed test targets, not literature-established universal
cutoffs:

- forbidden diagnosis/exam/test/scoring leakage: zero;
- unsupported fact creation: zero;
- contradiction of patient truth: zero;
- greeting over-disclosure for a reason-for-visit-triggered case: zero;
- requested critical-fact omission: zero in deterministic gold fixtures;
- ordinary requested-fact omission: target to be set after baseline runs;
- provider and repeated-run variance: report distribution before choosing a
  threshold.
