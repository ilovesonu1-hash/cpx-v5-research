# G2.7a scorecard v1

Classification: **PILOT_ONLY / NON_PRODUCTION**

The scorecard has exactly 58 rows, one for each scored unit J01 through J28 and
P01 through P30. P29 has one station-level row referencing the ordered six
authoritative constituent run IDs. The P14/P15 setup response is referenced by
both rows but is not a scored row.

## Fixed columns

`scored_unit_id`, `case`, `execution_unit_id`, `planned_evidence_call_ids`,
`authoritative_run_ids`,
`disposition`, `failure_class`, `responsible_layer`,
`critical_required_omissions`, `ordinary_required_omissions`,
`ambiguity_trigger`, `evidence_excerpt`, `scorer_id`,
`scoring_spec_sha256`, `input_bundle_id`, `scored_at_utc`.

The candidate template prepopulates scored-unit, case, execution-unit, ordered
planned-evidence-call, and scoring-spec identities. `planned_evidence_call_ids`
is a compact JSON array. A later `authoritative_run_ids` value must map
one-to-one and in the same order from those calls in the selected authoritative
attempt. Run IDs, the aggregate bundle binding, semantic
results, scorer, evidence, and time remain blank because no run or scoring is
authorized. A future accepted scoring copy must bind every row to the exact
`input_bundle_id` before scoring; the canonical template itself remains blank
there to avoid a circular identity because its SHA-256 is a bundle component.

## Dispositions and authority

Allowed future dispositions are `PASS`, `FAIL`, `ORACLE_AMBIGUOUS`, and
`EXECUTION_ERROR`. No disposition is prefilled.

Official semantic scorer: `HUMAN`. `MODEL_JUDGE = NONE`.

Deterministic scripts may validate identities, counts, formats, explicit
numeric patterns, and other nonauthoritative candidate flags. They may not
populate a final semantic disposition. Raw final responses must be frozen
before human scoring begins. An independent automatic failure takes precedence
over an ambiguity trigger; REQUIRED omissions always fail the scored unit.

Before scoring any real output, the scoring record must bind directly or
through a separately accepted execution-control bundle to the accepted
fixture/runner checkpoint, runner file or accepted runner commit identity, real
transport-adapter identity, execution-authorization ID, passing
preflight-evidence ID, and `input_bundle_id`. None is created by this candidate.
