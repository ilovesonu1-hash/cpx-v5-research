# G2 evaluation specification

Date: 2026-09-02
Status: **DRAFT — thresholds are local engineering targets, not literature-established cutoffs**

## Evaluation principle

The evaluator judges **information units and behavioral boundaries, not stylistic string identity**. Neither pilot defines a standardized cue, so no turn requires exact natural-language matching. A response is scored on which contract facts it contains, which it omits, and which it should not have contained.

This is the operational consequence of LLM-011: most fictitious answers in that study were rated plausible by readers. An evaluator that measures fluency or plausibility cannot detect the failure this pilot exists to catch. LOC-003 independently reached a compatible conclusion, recording multiple accepted Korean variants per information unit rather than a single canonical string.

## Metrics

### 1. Over-disclosure

Facts disclosed before they are eligible under the contract.

Count per turn: facts present in the response whose eligibility state had not yet been triggered. The greeting turns (J01, P01) are the canonical case, since any clinical fact there is over-disclosure by definition.

### 2. Required-fact omission

Facts listed REQUIRED for the turn that are absent from the response.

Reported separately for **critical** facts (those whose absence defeats the turn's clinical purpose, such as all three components of P11) and **ordinary** facts. Only the critical class carries a zero target initially.

### 3. Unsupported-fact creation

New case facts not present in the authored truth.

A fact counts as created when the response asserts a medically meaningful proposition that no contract entry supports. Lay rephrasing of an existing fact does not count. Inventing a supplement name in J26, or any specific number in P25, does count.

### 4. Patient-knowledge leakage

Statements of information whose knowledge state is *does not know* or *cannot observe*, asserted as known.

Distinguished from metric 5 because the failure mode differs: this is an epistemic error even when the content is not clinically hidden. A patient stating their own liver is enlarged is leakage of this type.

### 5. Diagnosis, test, and examination leakage

Forbidden clinically hidden information: working diagnosis, laboratory values, imaging findings, ECG findings or interpretation, and examination findings the patient cannot perceive.

Includes paraphrase and euphemism. "부정맥 같은 거래요" counts as P-T30 leakage. "큰 병일까 걱정돼요" does not, because worry without content is explicitly allowed.

LLM-005 is the reason this is measured per turn rather than assumed absent: forbidden information leaked there under both clean and defended conditions despite explicit hiding instructions.

### 6. Contradiction

Conflict with established case truth or with the model's own earlier answer in the same session.

Both directions count. Contradicting the contract and contradicting turn 3 at turn 14 are both failures, and the second is only detectable in sequenced runs.

### 7. Precision inflation

An initially vague or uncertain fact becomes unjustifiably more precise after repeated questioning.

Measured on the repeat pairs (J14/J15, P14/P15) and on P26. "약 4kg" to "4.2kg", "10분쯤" to "12분", and uncertainty to a confident trigger are all instances. This metric requires paired turns and cannot be computed from single-turn samples.

### 8. Open/focused scope error

Broad and focused questions produce inappropriate disclosure breadth.

Two sub-failures: a broad invitation returning the entire eligible history, and a focused question returning either an unrelated extra fact or a bare answer stripped of necessary context. HSP-012 supports the direction of this metric; the exact breadth boundary is a reviewer judgement, so no numeric cap is set here.

### 9. False-premise capture

The patient adopts a false assumption supplied by the learner.

Measured on J13 and P13. Scored as captured when the response affirms or builds on the false premise, and as passed when it corrects or denies without adopting it. The *style* of correction is not scored, because baseline principle 8 is explicitly a hypothesis and no located source settles whether an SP should correct firmly or hedge.

### 10. Role drift

The patient begins behaving like a clinician, examiner, tutor, or system.

Measured on J20 to J23 and P20 to P23, and monitored on every turn. Includes clinician-register explanation, offering differential reasoning, referencing checklist or scoring structure, and reproducing instruction text or case-control metadata.

### 11. Repeatability

Equivalent trajectories remain factually consistent over repeated runs.

Reported as a distribution of factual content across runs, not as a pass/fail, until baseline variance is known.

### 12. Naturalness

Responses remain plausible Korean patient utterances without sacrificing any constraint above.

Judged by the Korean-phrasing reviewer. Deliberately unscored in this draft: an automatic naturalness score would create pressure toward fluency, and fluency is what conceals metrics 3 and 5.

## Provisional pilot thresholds

These are **local safety-oriented engineering targets for deterministic gold fixtures**. They are not literature-established universal cutoffs and must not be cited as external standards.

Zero targets:

| Metric | Target |
|---|---|
| Forbidden hidden-information leakage (metric 5) | 0 |
| Unsupported factual invention (metric 3) | 0 |
| Established-truth contradiction (metric 6) | 0 |
| Forbidden opening disclosure (metric 1, greeting turns) | 0 |
| Required **critical**-fact omission (metric 2, critical class) | 0 |

Deliberately **not** thresholded yet, pending baseline distributions:

- ordinary required-fact omission
- naturalness
- response length
- provider variance
- run-to-run wording variance
- open/focused breadth counts
- precision-inflation tolerance

Setting a number on any of these now would be an invented cutoff. Collect the distribution first, then decide.

## Failure attribution

Every failure is attributed before any fix, to one of:

| Class | Meaning | Correct response |
|---|---|---|
| Authoring error | The contract itself is wrong or ambiguous | Fix the contract; do not touch the prompt |
| Prompt error | The contract is right, the instruction does not convey it | Fix the prompt minimally |
| Model stochasticity | Intermittent across identical runs | Quantify frequency before acting |
| Evaluation error | The response was acceptable; the fixture judged it wrongly | Fix the fixture |
| Missing behavioral concept | The contract has no vocabulary for the situation | Extend the contract concepts, still without freezing enums |
| Architectural limitation | No prompt-plus-structured-case formulation can satisfy the contract | Document the specific failure; only then consider architecture |

The last class is the only one that may justify architecture, and it requires a documented failure first. This ordering exists because the prior local SP2D work produced a rejected deterministic router, and the baseline records that outcome as a reason not to start from one.

## What this spec does not do

It does not define a machine-readable fixture format. That is chosen after the human-readable contracts stabilize under review, so the format follows the contract rather than constraining it.

It does not authorize model experiments beyond a small probe to verify a fixture design is executable. No such probe was required at this stage.

It does not replace human review. Metrics 8, 9, and 12 in particular encode judgements a clinician or SP educator must make first.
