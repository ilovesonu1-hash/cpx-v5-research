# G-1 seed evidence synthesis

Status: evidence map v0.1 / G-1 not yet complete
Search date: 2026-09-02

## 1. Evidence-map inventory

The evidence matrix contains 53 candidate evidence records: 50 from the seed
pass and 3 added by the G1.2 Korean-search and citation-chasing pass. Inclusion
does not imply completed full-text appraisal or final review eligibility.
The reproducible PubMed pass returned 58 query records (57 unique because one
record appeared in both queries); all 58 received a title-level decision:

| Stream | Records | Main use |
|---|---:|---|
| Human SP / OSCE standards, guidance, and studies | 14 | Case construction, prompting boundaries, repeatability |
| Classical virtual patients | 6 | Educational design and evaluation context |
| LLM virtual/standardized patients | 18 | Modern failure modes, prompting, fidelity metrics |
| Korean CPX/SP evidence | 10 | Local educational and linguistic context |
| Read-only local `CPX_source` evidence | 5 | Prior accepted work and invalidated parser branch |

Eight obviously out-of-scope or unsuitable source classes were also recorded.
This is a seed map, not a PRISMA-complete review.

## 2. Findings that are already well supported

### 2.1 Disclosure behavior is part of the case, not an incidental prompt detail

ASPE treats situation, backstory, history, affect, signs, symptoms, and cues as
case components. Human-SP case-development literature also treats disclosure
guidance as part of the script. CPX v5 should therefore store disclosure policy
as a first-class, versioned, reviewable case artifact rather than a single
generic sentence appended to a provider prompt.

Evidence: HSP-001, HSP-005, HSP-007, HSP-008.

### 2.2 There is no universal rule that every encounter begins with greeting only

OSCE guidance allows or requires a short opening statement in many cases and
may specify its exact timing. Conversely, an LLM feasibility study classified
the patient taking the conversational lead after a bare greeting as an
authenticity failure in that study's case.

The evidence supports a **case-configurable opening trigger**, not a universal
`greeting_only` constant. A Korean CPX case may validly specify that the chief
complaint appears only after “어떻게 오셨어요?”, while another station may
require an immediate safety-critical or emotionally salient opening.

Evidence: HSP-006 and HSP-008 are provisional pending authorized full-text
appraisal; LLM-006 supplies public case-specific failure evidence.

### 2.3 Prompted-only information and bounded sufficiency are established SP practices

Public SP guidance explicitly distinguishes information that should not be
offered until asked. It also warns against being so sparse that a reasonable
question fails to elicit pertinent information. Empirical unannounced-SP work
measured facts as prompted and disclosed, prompted and omitted, unprompted and
volunteered, or unprompted and withheld.

This supports both an over-disclosure metric and an under-disclosure metric.
Avoiding all volunteered detail by making the patient maximally terse would not
be faithful either.

Evidence: HSP-009, HSP-012.

### 2.4 Open and focused questions should not have identical disclosure scope

Human SPs have been trained to follow the clinician's lead and disclose an
appropriate amount according to open versus closed questioning. LLM-VP reviews
also describe dialogue-history and few-shot methods intended to produce gradual
disclosure.

The policy needs at least a notion of an open invitation versus a focused fact
request. The literature does not yet establish the exact CPX v5 labels or
algorithm.

Evidence: HSP-012, LLM-004.

### 2.5 Patient knowledge is a separate boundary from medical truth

An SP may truthfully experience a symptom without knowing a diagnosis,
examination sign, ECG interpretation, or laboratory result. Recent LLM-patient
studies identify patient answers about examination-only findings as explicit
authenticity failures. The local SP2B pilot likewise separated truth from
patient epistemic access and withheld the target diagnosis.

Evidence: HSP-009, LLM-005, LLM-006, LOC-002.

### 2.6 Unknown is safer than invention

Human-SP operational guidance recommends “I don't know” or “I can't remember”
rather than ad-libbing facts absent from the script. For an LLM patient this
must be an explicit, testable behavior because fluent invention can appear
plausible.

One prospective GPT simulated-patient study makes the risk concrete: when the
learner asked 195 questions not covered by the illness script, 56.4% of answers
used fictitious information even though most answers were rated plausible.

Evidence: HSP-009, LLM-004, LLM-005, LLM-011.

### 2.7 Repeatability requires training, dry-runs, and measured fidelity

SP standards and high-stakes OSCE literature consistently require advance
training, rehearsal, calibration, and pilot revision. A prompt that produces
one plausible transcript is not sufficient evidence of standardization.

Evidence: HSP-001, HSP-010, HSP-011, HSP-014, KR-001, LLM-018.

### 2.8 Prompt rules alone do not establish safe disclosure

The recent Japanese robustness benchmark used explicit rules to disclose only
naturally elicited facts and to hide diagnosis and test results, yet forbidden
information leakage persisted in clean and defended conditions. Prompt hygiene
is necessary but not sufficient; turn-level regression tests and independent
output evaluation are required.

Evidence: LLM-005, LLM-006, LLM-007.

## 3. Findings that remain hypotheses or evidence gaps

### 3.1 The seven proposed disclosure modes are not an external standard

`greeting_only`, `reason_for_visit_prompted`, `open_elaboration`, `ask_only`,
`conditional`, `exam_only`, and `not_disclosable` are useful candidate concepts,
but no located source validates this exact taxonomy. SP2B provides local support
for a related vocabulary in one palpitations case only.

Decision: do not freeze enum names during G-1.

### 3.2 A deterministic semantic question router is not justified

The local SP2D experiments found over-disclosure in candidate routers and near-
total abstention in the conservative alternative. Thirty-one adjudications
remain pending.

Decision: do not import SP2D or begin SP2E. Start with a structured policy
compiled into provider prompts and evaluate failures before proposing a new
router.

Evidence: LOC-004, LOC-005.

### 3.3 Korean turn-level disclosure evidence is sparse

The seed Korean literature supports the importance of scenario training,
standardization, history-taking, and CPX domains. It has not yet yielded a
validated Korean taxonomy for greeting, open-question expansion, focused
answers, and withholding.

Decision: Korean SP educators or clinicians must review the two pilot response
tables. Literature evidence alone will not settle natural Korean disclosure
length or honorific style.

### 3.4 Educational benefit does not prove patient-role fidelity

Some virtual-patient studies report improved learner performance or positive
experience. Those outcomes do not prove that the patient revealed the right
fact at the right time.

Decision: measure educational outcomes and patient fidelity separately.

Evidence: VP-001, VP-003, VP-004, LLM-002, LLM-009.

### 3.5 Gemini/OpenAI equivalence is unproven

The located literature does not establish that two frontier providers will
implement the same disclosure contract with equivalent reliability.

Decision: treat a common policy source as an architecture hypothesis, and test
and report provider-specific behavior rather than claiming equivalence.

## 4. Evidence-derived product direction

The following is a candidate implementation direction, not an
evidence-established disclosure requirement:

```text
server-only medical truth
        +
server-only patient epistemic model
        +
server-only disclosure and cue policy
        +
Korean realization constraints
        ↓
provider-neutral patient contract compiler
        ↓
Gemini prompt / OpenAI prompt
        ↓
turn-level fidelity and leakage evaluation
```

The policy should remain separate from the existing scenario JSON during the
pilot. This preserves the current dataset and allows evidence-derived revisions
without a schema migration.

## 5. Initial evaluation dimensions

At minimum, the pilot must measure:

1. unprompted information units;
2. requested but omitted information units;
3. unsupported or invented facts;
4. diagnosis, test, examiner-only, or examination-only leakage;
5. disclosure breadth after open versus focused questions;
6. truth preservation under leading or false-premise questions;
7. repeat-answer consistency;
8. role drift and clinician-style explanation;
9. sensitivity to prompt injection or indirect instruction contamination;
10. provider and repeated-run variance.

## 6. Provisional conclusion

The current user-observed behavior—volunteering the chief complaint immediately
after “안녕하세요”—can be a defect **for a case whose opening trigger is the
reason-for-visit question**, but it is not universally invalid for every OSCE
case. The case author must declare the opening trigger, and the evaluator must
judge the model against that declared behavior.

This is the central correction to the earlier all-cases `greeting_only` plan.

## 7. Work remaining before G-1 approval

- Run the documented searches in Korean databases and at least one
  education/engineering index. The two PubMed searches are complete and title
  screened.
  G1.2 completed the Korean database-native family across KoreaMed, KCI, RISS,
  and a DBpia scale reference; no education or computing index has been searched.
- Deduplicate records and create a countable PRISMA flow.
- Retrieve and appraise full texts for the high-directness sources.
- Perform backward/forward citation chasing.
- G1.2 screened the two audit-identified records: Peters 2026 was included as
  HSP-015, and the described Davies 2021 scoping review could not be retrieved
  in PubMed and remains unverified pending a DOI or PMID.
- Obtain independent screening and extraction review.
- Have Korean clinicians/SP educators review the two pilot trajectory tables.
- Freeze evidence-backed requirements only after adjudication.
