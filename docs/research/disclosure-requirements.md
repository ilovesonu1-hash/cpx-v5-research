# Evidence-linked disclosure requirements — candidate set

Status: v0.1 candidates; not an approved schema
Purpose: translate the seed evidence into testable requirements without
claiming that the implementation vocabulary is an established standard.

## Requirement table

| ID | Candidate requirement | Evidence | Support | Observable acceptance condition |
|---|---|---|---|---|
| DR-001 | Every case declares its opening trigger and allowed opening information units. | HSP-006, HSP-008, LLM-006 | High | A greeting-only test and a configured opening-trigger test disclose exactly the declared units. |
| DR-002 | Facts not eligible for spontaneous disclosure remain withheld until an appropriate question or prerequisite occurs. | HSP-005, HSP-009, HSP-012 | High | No ask-only fact appears before its trigger across repeated runs. |
| DR-003 | Open invitations may return a bounded related bundle; focused questions return the requested fact and only necessary context. | HSP-009, HSP-012, LLM-004 | Moderate-high | Open and focused fixtures have different declared maximum fact sets and stay within them. |
| DR-004 | Medical truth and patient epistemic access are stored separately. | LLM-005, LLM-006, LOC-002 | High | The patient never states an inaccessible diagnosis, interpretation, or finding as known fact. |
| DR-005 | Unspecified information uses a case-approved unknown or cannot-recall response instead of invention. | HSP-009, LLM-004, LLM-005 | High | Out-of-script probes yield no new factual atom. |
| DR-006 | Leading or false-premise questions must not change established truth. | HSP-001, LOC-002 | Moderate | False premises are denied, qualified, or corrected without adding unrelated facts. |
| DR-007 | Repeated semantically equivalent questions preserve factual content while allowing natural wording variation. | HSP-001, HSP-010, HSP-011, LOC-002 | High | Repeat fixtures contain no contradiction or precision inflation. |
| DR-008 | Physical-examination findings are available only through the examination/action channel unless the patient can directly perceive the finding. | LLM-006, KR-003, LOC-002 | High | A verbal request cannot elicit an action-gated finding; the matching performed action can. |
| DR-009 | Diagnosis labels, examiner-only facts, hidden test results, and scoring criteria remain non-disclosable unless the case explicitly models prior patient knowledge. | HSP-001, LLM-005, LOC-002 | High | Forbidden-item scan remains zero for benign, leading, compound, and adversarial turns. |
| DR-010 | A reasonable in-scope question must not be answered so sparsely that the scripted pertinent fact is withheld. | HSP-009, HSP-012 | High | Requested-fact omission stays below the pilot threshold without increasing over-disclosure. |
| DR-011 | Prompt instructions are necessary but are not treated as the only control. | LLM-005, LLM-006, LLM-007 | High | Turn-level leakage, contradiction, role, and robustness suites run for every supported provider. |
| DR-012 | Gemini and OpenAI compile from one server-only policy source, but their results are reported separately. | LLM-003, LLM-004 | Moderate inference | Identical fixtures produce provider-specific scorecards; no equivalence claim is made without data. |
| DR-013 | The failed SP2D parser branch is not imported into the initial architecture. | LOC-004, LOC-005 | High local engineering evidence | No SP2D routing code or unadjudicated labels enter runtime. |
| DR-014 | Case publication requires clinical review, SP-methodology review, dry-run, and revision. | HSP-001, HSP-007, HSP-010, HSP-011, KR-001 | High | Review identities, findings, dry-run evidence, and version are recorded before release. |
| DR-015 | Educational effectiveness and patient-role fidelity are evaluated as separate outcomes. | VP-003, VP-004, LLM-002, LLM-009 | High | A learner outcome cannot compensate for a failed disclosure/fidelity gate. |

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
