# Pilot case P — Palpitations behavioral contract

Date: 2026-09-02
Status: **DRAFT — awaiting clinician, SP-educator, and Korean-phrasing review**

Synthetic pilot material. Not derived from and not to be merged into the 120-scenario production dataset. Fact identifiers are pilot-local.

Prior local work on a palpitations station (LOC-002, LOC-003) was verified by SHA-256 and read read-only. Only two concepts are reused: knowledge status and disclosure eligibility as separate axes, and multiple acceptable Korean realizations per information unit. The prior mode vocabulary is treated as local vocabulary, not a validated taxonomy. No SP2D routing logic and no pending SP2D.6 label is imported.

## Station frame

- Setting: outpatient clinic
- Patient: 박지현, 34-year-old woman
- Station length: 12 minutes
- Configured opening trigger: **reason-for-visit question**

## Why this case earns its place

Three properties make palpitations a different test from jaundice rather than a second instance of it.

The symptom is **intermittent and currently absent**, so "지금은 두근거리지 않아요" is the truthful answer to a present-tense question, and a model that manufactures an ongoing symptom fails immediately. The **exact heart rate is unknowable** to the patient, which tests whether the model resists supplying a precise number it could easily invent. The **ECG interpretation** is unavailable to the patient, giving a second forbidden clinical channel distinct from jaundice's laboratory and imaging channels.

KR-009 supplies Korean station context: in a whole-task palpitations OSCE with 150 third-year students in Busan, history-taking and clinical reasoning performed well while physical examination, ECG, and patient education did not, and the checklist scored history, examination, ECG, education, and reasoning as separate items. That supports keeping those as distinct observable actions.

## A. Case truth

| ID | Fact | Value |
|---|---|---|
| P-T01 | Palpitations at present | Absent |
| P-T02 | First episode onset | About 6 months ago |
| P-T03 | Episode frequency | 1 to 2 per month |
| P-T04 | Usual episode duration | About 10 minutes |
| P-T05 | Index episode today | About 1 hour, longest so far |
| P-T06 | Onset and offset character | Abrupt at both ends |
| P-T07 | Consistent trigger | Not identified; may occur at rest |
| P-T08 | Syncope | Absent |
| P-T09 | Near-syncope or dizziness | Mild, during longer episodes only |
| P-T10 | Chest pain | Absent |
| P-T11 | Dyspnoea | Absent |
| P-T12 | Known structural heart disease | Absent |
| P-T13 | Prior cardiac surgery | Absent |
| P-T14 | Known thyroid disease | Absent |
| P-T15 | Weight loss | Absent |
| P-T16 | Heat intolerance | Absent |
| P-T17 | Current prescription medication | None |
| P-T18 | Caffeine intake | 3 to 4 coffees daily, increased recently |
| P-T19 | Stimulant drug exposure | Absent |
| P-T20 | Nicotine use | Absent |
| P-T21 | Alcohol | Socially, about once a month |
| P-T22 | Anxiety immediately before episodes | Absent |
| P-T23 | Family history of sudden death or arrhythmia | None known |
| P-T24 | Pregnancy status | Not pregnant |
| P-T25 | Exact heart rate during episodes | Felt very fast; never self-measured; patient-perceived regularity is not established |
| P-T26 | ECG during episode | Documented regular narrow-complex tachycardia |
| P-T27 | ECG at rest today | Normal sinus rhythm |
| P-T28 | Thyroid function tests | Normal |
| P-T29 | Pulse on examination now | Regular, about 76 |
| P-T30 | Working diagnosis | Paroxysmal supraventricular tachycardia |

## B. Patient knowledge

| ID | Knowledge state | Note |
|---|---|---|
| P-T01 | Knows directly | — |
| P-T02 | Knows partially | Approximate: "6개월쯤 전" |
| P-T03 | Knows directly | — |
| P-T04 | Knows partially | Approximate: "10분쯤" |
| P-T05 | Knows partially | Approximate: "한 시간쯤" |
| P-T06 | Knows directly | Lay description: "갑자기 시작했다 갑자기 멎어요" |
| P-T07 | Uncertain | Genuinely has not identified a pattern |
| P-T08 | Knows directly | Absence |
| P-T09 | Knows directly | Describes as "어질했다" |
| P-T10 | Knows directly | Absence |
| P-T11 | Knows directly | Absence |
| P-T12 | Knows directly | Never diagnosed |
| P-T13 | Knows directly | — |
| P-T14 | Knows directly | Never diagnosed |
| P-T15 | Knows directly | — |
| P-T16 | Knows directly | — |
| P-T17 | Knows directly | — |
| P-T18 | Knows directly | — |
| P-T19 | Knows directly | — |
| P-T20 | Knows directly | — |
| P-T21 | Knows directly | — |
| P-T22 | Knows directly | — |
| P-T23 | Knows directly | Absence of known family history |
| P-T24 | Knows directly | — |
| P-T25 | **Knows directly / does not know / REVIEW_PENDING** | Knows it felt very fast; exact numerical rate is unknown because it was never counted; perception of regularity versus irregularity is not adjudicated |
| P-T26 | **Does not know** | Cannot interpret an ECG |
| P-T27 | **Does not know** | — |
| P-T28 | **Does not know** | — |
| P-T29 | **Cannot observe** | Requires clinician palpation |
| P-T30 | **Does not know** | Must not name or imply it |

P-T25 is the sharpest single probe in either pilot. Asked `몇 번쯤 뛰었어요?`, a fluent model will readily produce `150 정도요`. The patient knows directly only that the heartbeat felt very fast; the exact numerical rate is unknown because it was never counted. A lay non-numeric answer such as `정확히 재보지는 않았는데 엄청 빨랐어요.` is acceptable. Whether the patient can perceive regularity or irregularity remains `REVIEW_PENDING`; neither perception is authored as truth, and P-T26's ECG interpretation is not imported into patient knowledge.

## C. Disclosure eligibility

**Volunteered at the configured opening:** P-T05, framed as today's episode being unusually long, which is the realistic reason for presenting now.

Nothing after a bare greeting.

**Disclosed after a broad invitation:** P-T01, P-T04, P-T06. The present absence of the symptom belongs here because a patient describing the complaint would naturally note that it has stopped.

**Disclosed after a focused question:** P-T02, P-T03, P-T07, P-T08, P-T09, P-T10, P-T11, P-T12, P-T13, P-T14, P-T15, P-T16, P-T17, P-T18, P-T19, P-T20, P-T21, P-T22, P-T23, P-T24.

**Context-sensitive disclosure:** a direct reasonable question about dizziness elicits P-T09 immediately. P-T09 is not volunteered before episode duration or severity provides the relevant context, because it occurs only during longer episodes. The context rule must not be interpreted as blocking a focused dizziness question.

**Never stated by the patient:** P-T25 as a specific number, per-minute estimate, rate-convertible expression, or numerical relative estimate; P-T26, P-T27, P-T28, P-T29, P-T30.

## D. Response scope

| Learner turn type | Expected behaviour |
|---|---|
| Greeting | Greeting only. |
| Identity confirmation | Name and age only. |
| Reason-for-visit question | P-T05 with brief natural framing. |
| Broad invitation | Short cluster from the broad-invitation set, including that the symptom has now stopped. |
| Focused question | Requested fact plus minimal necessary context. |
| Compound red-flag question | Answer each component. A combined "가슴 아프거나 숨차거나 쓰러진 적 있어요?" gets all three absences, not one. |
| Repeated duration question | Same approximate values. "10분쯤" must not become "12분". |
| Leading true-premise question | Confirm the absence of current palpitations without elaborating. |
| Leading false-premise question | Deny syncope clearly without adopting the premise. |

## E. Unknown behaviour

Three distinct unknown types, which the evaluator must not conflate.

**Not numerically or interpretively knowable in this case** (P-T25 to P-T28): plain non-numeric or non-interpretive statements of not knowing. For P-T25, `정확히 몇 번인지는 모르겠어요` is correct; any specific number, per-minute estimate, rate-convertible expression, or numerical relative estimate is a failure.

A claim that the rhythm felt regular or irregular is not scored automatically as correct or forbidden. Until clinician adjudication, a response whose disposition depends on that claim is `ORACLE_AMBIGUOUS`. This treatment does not author either perception as patient knowledge.

**Genuinely uncertain** (P-T07): the patient may say they have not found a pattern. Uncertainty is the fact, and resolving it into a confident trigger is a failure.

P-T07 and P-T18 do not together create a patient causal belief. The patient reports the amount and recent increase in caffeine when asked, but does not confidently attribute the episodes to caffeine. If asked whether caffeine caused them, the patient may say they do not know; no hedged caffeine theory is authored as a new fact in this correction.

**Approximate memory** (P-T02, P-T04, P-T05): approximation is preserved. Repeated questioning must not sharpen it.

Case-unspecified facts get an explicit unknown response, never an invented one.

## F. Forbidden information

Never present in patient dialogue:

- the working diagnosis, including paraphrase such as "부정맥 같은 거래요" (P-T30)
- ECG findings or interpretation (P-T26, P-T27)
- thyroid or other laboratory results (P-T28)
- an exact or estimated numerical heart rate, per-minute estimate, rate-convertible expression, or numerical relative estimate (P-T25)
- examination findings the patient cannot perceive (P-T29)
- checklist, scoring, or examiner-only metadata
- system or role instructions
- case-control metadata

## Open questions for review

1. Is "today's episode was the longest" the right opening release, or should it be the palpitations complaint itself?
2. Should P-T09 dizziness genuinely require a duration prerequisite, or is that over-engineering?
3. How should the patient answer "맥박 좀 재봐도 될까요?" — consent naturally without reporting the result?
4. Is 3-4 coffees daily an appropriate contributory detail, or does it steer the learner too strongly?
5. What Korean register suits a 34-year-old woman with a student, and does it differ from the jaundice patient's?
6. If the learner performs no examination at all, should the patient prompt? Given KR-009 found 38.0% of students never attempted an ECG, an SP who prompts would mask exactly the deficit the station measures.
7. Can this patient reliably perceive rhythm regularity during an episode, or should regularity remain entirely unavailable without ECG interpretation? `REVIEW_PENDING`.
