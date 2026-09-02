# G-1 status

Date: 2026-09-02
Decision: **REVISION REQUIRED — implementation gate remains closed**

## Completed in this pass

- Created an isolated research-only `cpx-v5` workspace.
- Preserved `cpx-v4` and `CPX_source` without edits.
- Wrote a JBI/PRISMA-ScR-aligned rapid-review protocol.
- Logged 27 executed discovery/database/local searches and one remaining
  database-search family.
- Executed two reproducible PubMed queries through official NCBI E-utilities:
  58 query records, 57 unique PMIDs.
- Title-screened all 58 PubMed query records.
- Built a 50-candidate seed evidence matrix and an eight-class exclusion log;
  inclusion does not imply completed full-text appraisal or final eligibility.
- Added current international standards, human-SP disclosure evidence,
  classical virtual-patient research, LLM-patient evidence, Korean CPX/SP
  evidence, and the prior local research branch.
- Recorded source-rights boundaries and SHA-256 anchors for six local reference
  files.
- Derived 13 candidate disclosure requirements and retained two relocated
  architecture/preservation constraints for traceability.
- Recorded the disposition of an independent machine-assisted evidence audit.
  This audit does not satisfy the protocol's required human second review.

## Evidence-backed decision already available

Opening behavior must be case-configurable. The evidence does not justify a
universal rule that every SP must either volunteer or withhold the chief
complaint at the first greeting. For the current jaundice case, the case author
may set `reason-for-visit question` as the opening trigger and test that
behavior explicitly.

## Remaining blockers

1. Run database-native Korean searches and at least one education or computing
   index search.
2. Retrieve and appraise the full text of high-directness sources.
3. Complete backward and forward citation chasing, including formal screening
   of the Davies 2021 and Peters 2026 role-script records identified by audit.
4. Have an independent reviewer adjudicate inclusion and high-impact evidence
   extraction.
5. Have Korean clinicians or SP educators review the jaundice and palpitations
   expected-response trajectories.
6. Resolve candidate requirement wording before freezing a JSON schema.
7. Obtain authorized primary or lawful library access for HSP-006 and HSP-008
   before treating their detailed full-text extractions as final.

## Explicitly not authorized yet

- Copying `cpx-v4` into an application scaffold.
- Changing the existing 120-scenario dataset.
- Importing the failed SP2D parser or pending SP2D.6 labels.
- Claiming that the provisional disclosure-mode vocabulary is a published
  standard.
- Deploying the seed policy in a high-stakes or unsupervised assessment.
