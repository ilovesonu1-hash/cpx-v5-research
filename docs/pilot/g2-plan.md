# G2 — Behavioral Contract Pilot

Date: 2026-09-02

Predecessor: `G1-PRODUCT-BASELINE: REACHED` (`docs/research/g1-product-baseline.md`)

## Objective

Determine whether an evidence-informed CPX standardized-patient behavioral contract can reliably produce the right information, at the right conversational time, at the right level of detail, while withholding information the patient should not reveal.

From this point the primary evidence is **observed model behavior against expert-authored test trajectories**, not additional literature.

## Why a contract before a schema

Two findings in the baseline make prompt-only assurance untenable. LLM-005 observed forbidden information leaking under clean and defended prompting conditions, and LLM-011 observed 56.4% of answers to script-uncovered questions using fictitious information despite most answers being rated plausible. Plausibility does not detect either failure. A written contract is what makes the failure detectable, because it states in advance what the patient may say.

HSP-016's scoping review of 17 SP role templates found they "differed in structure, length, and depth." That is the reason this phase writes a human-readable contract and refuses to claim its structure is standardized. HSP-015's 13-category consensus template shows what a reviewed template looks like, but its own usability evaluation is explicitly future work.

## Scope

Exactly two pilot cases: **jaundice** and **palpitations**.

- The 120-scenario production dataset is not modified, migrated, or read into pilot authoring.
- Pilot cases are authored separately as synthetic pilot material.
- Local SP2B/SP2C artifacts are read-only reference for previously accepted *concepts* only.
- SP2D parser architecture is not imported. Pending SP2D.6 labels are not treated as ground truth.

### Local reference use, stated precisely

Two local artifacts were verified against `local-source-manifest.csv` by SHA-256 before reading and were not modified:

- LOC-002 (`sp2b_summary.md`, 1014 bytes) — confirms a prior one-station contract used patient-knowledge statuses and disclosure modes with counted truth-behavior conflicts. Reused concept: knowledge status and disclosure eligibility are separate axes.
- LOC-003 (`korean_utterance_review.md`, 9720 bytes) — confirms Korean utterance variants were reviewed per response intent. Reused concept: multiple acceptable Korean realizations per information unit, with exact wording not required.

Their vocabulary (`ask_only`, `spontaneous_if_open_prompted`, `not_disclosable`, and similar) is treated as **prior local vocabulary, not a validated taxonomy**, consistent with the standing decision not to freeze enum names during G-1.

## Phase sequence

| Step | Artifact | Status after this task |
|---|---|---|
| G2.1 | Human-readable behavioral contracts | Sanity-reviewed; executable as provisional gold, awaiting expert acceptance |
| G2.2 | Gold trajectory specifications | Sanity-reviewed; 58 provisional trajectories |
| G2.3 | Evaluation spec and provisional thresholds | Drafted |
| G2.4 | Clinician / SP-educator / Korean-phrasing review | **Not started — required before pilot acceptance, not before a supervised probe** |
| G2.5 | Minimal system prompt derivation | v0.1 created and frozen for the small probe |
| G2.6 | Machine-readable fixtures | Not started; inline pilot payload used without freezing a format |
| G2.7 | Baseline model runs and distribution collection | 12-run high-information probe complete; full distribution not started |

G2.4 remains required before either pilot is accepted. The supervised G2.2 probe is permitted before that review because ambiguous expert-dependent judgements remain `REVIEW_PENDING` and must be scored `ORACLE_AMBIGUOUS`, not forced into pass/fail. The probe therefore tests executability without converting provisional authoring choices into validated standards.

## Architecture restraint

Not built in G2, by decision rather than by omission: dataset migration, production schema, universal semantic router, SP2D revival, web application, provider abstraction beyond pilot need, multi-agent orchestration, retrieval systems, or generalization from two cases.

If the simplest prompt-plus-structured-case approach fails, the specific failure is documented first. Architecture is introduced in response to a measured failure mode, not in anticipation of one.

## Empirical iteration rule

Observed failure outranks additional generic literature searching.

On a pilot failure:

1. classify the failure;
2. attribute it to authoring error, prompt error, model stochasticity, evaluation error, a missing behavioral concept, or an actual architectural limitation;
3. patch the smallest responsible layer;
4. rerun the relevant trajectory suite;
5. add a regression fixture.

Literature is consulted only when correct human-SP behavior is genuinely uncertain, Korean-specific behavior is disputed, or a decision carries material safety or assessment implications not covered by the baseline.

## Case selection rationale

**Jaundice** is the case where the user originally observed the defect: the patient volunteered "눈이 노래져서 걱정돼서 왔어요" after a bare greeting. It also has a naturally visible sign, which makes it the sharper test of what a patient can and cannot perceive about their own body.

**Palpitations** has an intermittent symptom that may be absent at the time of the encounter, an unknowable exact heart rate, and an ECG whose interpretation the patient cannot supply. KR-009 provides real Korean station context: in a whole-task palpitations OSCE with 150 third-year students, history and reasoning performed well while examination, ECG, and education did not, and the checklist scored those as separate domains. That supports keeping interview, examination, investigation, and education as distinct observable actions rather than one narrative stream.

## Stopping point for this task

Contracts and trajectories are executable as provisional gold, prompt v0.1 is frozen, and a 12-run diagnostic probe has been completed. This is not a large benchmark, repeatability distribution, expert acceptance, or production authorization.

G1_RESEARCH_EXPANSION: PAUSED
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
