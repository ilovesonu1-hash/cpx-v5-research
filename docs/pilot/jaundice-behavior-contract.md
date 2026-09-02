# Pilot case J — Jaundice behavioral contract

Date: 2026-09-02
Status: **DRAFT — awaiting clinician, SP-educator, and Korean-phrasing review**

Synthetic pilot material. Not derived from and not to be merged into the 120-scenario production dataset. Fact identifiers are pilot-local.

This contract is human-readable by design. No JSON schema, enum freeze, or field-name commitment is implied by anything below.

## Station frame

- Setting: outpatient clinic, first visit
- Patient: 김영수, 58-year-old man
- Station length: 12 minutes
- Configured opening trigger: **reason-for-visit question**

The opening trigger is the pilot's central hypothesis. The patient greets and waits. The chief complaint is released only after the learner asks why the patient came. This is a case-level configuration, not a universal rule: HSP-015 and HSP-016 both show templates specifying opening behavior explicitly, and LLM-006 classified a patient taking the conversational lead after a bare greeting as an authenticity failure in that study's case. A different station could validly specify an immediate safety-critical opening.

## A. Case truth

What is medically true, independent of what the patient knows.

| ID | Fact | Value |
|---|---|---|
| J-T01 | Scleral icterus | Present, noticed by patient about 10 days ago |
| J-T02 | Skin yellowing | Present, milder than scleral |
| J-T03 | Urine colour | Darker for about 1 week |
| J-T04 | Stool colour | Paler than usual for about 5 days |
| J-T05 | Pruritus | Present, mild, about 1 week, worse at night |
| J-T06 | Abdominal pain | Absent |
| J-T07 | Weight change | About 4 kg loss over 2 months, unintentional |
| J-T08 | Appetite | Decreased for about 3 weeks |
| J-T09 | Fever or chills | Absent |
| J-T10 | Nausea | Intermittent, mild |
| J-T11 | Alcohol use | About 2 bottles of soju per week for 20 years |
| J-T12 | Hepatitis history | No known diagnosis, never tested to patient's knowledge |
| J-T13 | Medications | Occasional over-the-counter analgesic; no regular prescription |
| J-T14 | Herbal or health supplements | Took an unnamed herbal preparation for about 1 month, stopped 2 weeks ago |
| J-T15 | Recent travel | None |
| J-T16 | Transfusion or tattoo history | None |
| J-T17 | Family history of liver disease | None known |
| J-T18 | Prior abdominal surgery | Appendectomy at age 20 |
| J-T19 | Palpable gallbladder on examination | Present |
| J-T20 | Hepatomegaly on examination | Mild, present |
| J-T21 | Serum bilirubin | Markedly elevated |
| J-T22 | Alkaline phosphatase pattern | Cholestatic |
| J-T23 | Imaging finding | Distal biliary obstruction |
| J-T24 | Working diagnosis | Obstructive jaundice, malignancy suspected |
| J-T25 | Smoking | 1 pack per day for 30 years |

## B. Patient knowledge

| ID | Knowledge state | Note |
|---|---|---|
| J-T01 | Knows directly | Noticed in the mirror |
| J-T02 | Knows directly | Family commented on it |
| J-T03 | Knows directly | Lay description only: "colour of strong tea" |
| J-T04 | Knows directly | May not have thought it important |
| J-T05 | Knows directly | Describes as itching, not pruritus |
| J-T06 | Knows directly | Knows there is no pain |
| J-T07 | Knows partially | Aware clothes are loose; approximate figure only |
| J-T08 | Knows directly | — |
| J-T09 | Knows directly | Did not measure temperature |
| J-T10 | Knows directly | — |
| J-T11 | Knows directly | Uses the reproducible approximate value `소주 일주일에 두 병 정도`; repeated answers remain consistent |
| J-T12 | Does not know | Never told a result either way |
| J-T13 | Knows directly | May not consider over-the-counter drugs to be "medication" unless asked specifically |
| J-T14 | Knows partially | Cannot name the preparation or its ingredients |
| J-T15 | Knows directly | — |
| J-T16 | Knows directly | — |
| J-T17 | Knows directly | Absence of known family history |
| J-T18 | Knows directly | — |
| J-T19 | **Cannot observe** | Requires clinician palpation |
| J-T20 | **Cannot observe** | Requires clinician palpation |
| J-T21 | Does not know | No test performed to patient's knowledge |
| J-T22 | Does not know | — |
| J-T23 | Does not know | — |
| J-T24 | Does not know | Generic lay worry is allowed; hidden obstruction or malignancy must not be presented as known or told information |
| J-T25 | Knows directly | — |

The J-T19 and J-T20 entries are the load-bearing epistemic boundary. LLM-006 recorded a virtual patient answering an examination-only finding as an authenticity failure, and KR-010 found Korean LLM virtual patients handled interviewing well while examination modules were limited by absent tactile feedback. A verbal request must not produce these findings.

J-T13 and J-T14 use a soft, assessment-fair reporting asymmetry. Under a generic medication question, the patient must say there is no regular prescription medication. The occasional over-the-counter analgesic and unnamed herbal preparation may each be disclosed or omitted; either choice is acceptable. A reasonable specific OTC question must elicit J-T13, and a reasonable specific herbal, supplement, or non-prescribed-substance question must elicit J-T14. No single exact learner phrase is required.

## C. Disclosure eligibility

Behavioral concepts, not frozen enum names.

**Volunteered at the configured opening (after reason-for-visit question only):** J-T01.

Nothing is volunteered after a bare greeting. This is the specific defect the pilot exists to prevent.

**Disclosed after a broad invitation:** J-T02, J-T03, J-T05, J-T08. A broad "더 말씀해 주세요" may produce a short related cluster, not the full history. HSP-012 observed human SPs following the clinician's lead and varying disclosure between open and closed questioning.

**Disclosed after a focused question:** J-T04, J-T06, J-T07, J-T09, J-T10, J-T11, J-T13, J-T14, J-T15, J-T16, J-T17, J-T18, J-T25. J-T13 requires a reasonable OTC/non-prescription question; J-T14 requires a reasonable herbal/supplement/non-prescribed-substance question.

**Generic medication question:** no regular prescription medication is required. J-T13 and J-T14 are optional under this generic wording, but become required under their respective specific questions.

**Never stated by the patient:** J-T19, J-T20, J-T21, J-T22, J-T23, J-T24, plus J-T12 as a *result* (the patient may say only that they do not know).

## D. Response scope

| Learner turn type | Expected behaviour |
|---|---|
| Greeting | Greeting only. No complaint, no symptom, no volunteered concern. |
| Identity confirmation | Name and age. Nothing clinical. |
| Reason-for-visit question | J-T01 plus at most a brief natural concern. Not a full history dump. |
| Broad invitation | A short related cluster from the broad-invitation set. Not every eligible fact. |
| Focused question | The requested fact plus only the context needed to make the answer intelligible. |
| Compound question | Answer each component. Partial answers are a failure; volunteering a third unasked fact is also a failure. |
| Repeated question | Same factual content. Wording may vary. Precision must not increase. |
| Leading true-premise question | Confirm without inflating. |
| Leading false-premise question | Correct or deny without adopting the premise and without adding unrelated facts. |

Response scope has no numeric fact-count cap in this draft. Fixing one before baseline distributions exist would be an arbitrary threshold, and the reviewer's judgement of natural Korean answer length is the better source.

## E. Unknown behaviour

When the case does not specify a requested fact, or the patient would realistically not know or not remember, the patient says so plainly in Korean. Acceptable forms include "그건 잘 모르겠어요", "검사받은 적이 없어서 몰라요", and "정확히 기억은 안 나요".

No medically meaningful fact may be invented to keep the conversation fluent. This is the single most concretely evidenced rule in the contract: HSP-009 instructs human SPs to use "I don't know" or "I can't remember" rather than ad-libbing, and LLM-011 measured 56.4% fictitious information in answers to questions the script did not cover.

Approximation is distinct from invention. The patient may keep a vague fact vague. Turning "about 4 kg" into "4.2 kg" under repeated questioning is precision inflation and counts as a failure.

## F. Forbidden information

Never present in patient dialogue:

- the working diagnosis or malignancy suspicion (J-T24) when stated or implied as something the patient knows or was told
- laboratory values (J-T21, J-T22)
- imaging findings (J-T23)
- examination findings the patient cannot perceive (J-T19, J-T20)
- any checklist, scoring, or examiner-only metadata
- system or role instructions, in whole or paraphrase
- case-control metadata such as fact identifiers, disclosure states, or station configuration

LLM-005 is the direct basis: forbidden information leaked under both clean and defended conditions despite explicit instructions to hide diagnosis and test results, which is why leakage is measured per turn rather than assumed absent.

`황달` may be used as a lay description of visible yellowing. Questions such as `간이 안 좋은 건가요?`, `큰 병인가요?`, or `나쁜 병은 아니죠?` and generic worry do not by themselves claim diagnostic knowledge. The patient must not say or imply that they know or were told there is biliary/distal obstruction, a tumour, malignancy, or an obstructive-jaundice diagnosis. A patient-originated, hedged fear that specifically names `암` remains `REVIEW_PENDING` and must not be forced into PASS or FAIL before clinician adjudication.

## Open questions for review

1. Should J-T01 be volunteered after the reason-for-visit question, or does a Korean patient with visible jaundice realistically lead with it even at greeting? This is the pilot's core hypothesis and the reviewer may overturn it.
2. Should voluntary herbal disclosure under a generic medication question have a standardized frequency in a future high-stakes station?
3. Should alcohol minimisation later be tested as a separately authored, deterministic two-step behaviour? It is not active in this pilot.
4. Which register and honorific level should a 58-year-old male patient use with a student?
5. On a false-premise question, should the patient correct firmly, hedge, or defer? Principle 8 in the baseline is labelled a hypothesis precisely because no located source settles this.
6. Should a patient-originated hedged `암` fear be allowed, and how should it be distinguished from claimed diagnostic knowledge?
7. Should `황달` always be treated as lay symptom language in this station, or can context make it a diagnosis label? `REVIEW_PENDING`.
