from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MODULE_DIR = ROOT / "tools/pilot/g2_7a"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import build_bundle as builder


class BundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = builder.load_working_sources_for_tests(ROOT)
        cls.outputs = builder.render_artifacts(
            ROOT,
            cls.sources,
            "CPX-G2-ISO-00000000000000000000000000000000",
        )

    def test_canonical_prompt_extraction(self) -> None:
        block = builder.extract_prompt_block(self.sources.prompt_document.content)
        self.assertFalse(block.endswith(b"\n"))
        self.assertEqual(53, len(block.splitlines()))
        self.assertNotIn(b"```", block)

    def test_prompt_block_hash(self) -> None:
        block = builder.extract_prompt_block(self.sources.prompt_document.content)
        self.assertEqual(builder.PROMPT_BLOCK_SHA256, hashlib.sha256(block).hexdigest())

    def test_payload_fact_counts(self) -> None:
        j_ids = re.findall(rb"(?m)^(J-T\d{2}) \|", self.outputs[builder.J_PAYLOAD])
        p_ids = re.findall(rb"(?m)^(P-T\d{2}) \|", self.outputs[builder.P_PAYLOAD])
        self.assertEqual(25, len(j_ids))
        self.assertEqual(25, len(set(j_ids)))
        self.assertEqual(30, len(p_ids))
        self.assertEqual(30, len(set(p_ids)))

    def test_forbidden_fact_retention(self) -> None:
        j = self.outputs[builder.J_PAYLOAD].decode("utf-8")
        p = self.outputs[builder.P_PAYLOAD].decode("utf-8")
        for number in range(19, 25):
            self.assertRegex(j, rf"(?m)^J-T{number:02d} .*공개=절대")
        for number in range(26, 31):
            self.assertRegex(p, rf"(?m)^P-T{number:02d} .*공개=절대")
        self.assertRegex(p, r"(?m)^P-T25 .*정확한 수치는 절대")

    def test_system_message_assembly(self) -> None:
        prompt = self.outputs[builder.PROMPT_FIXTURE]
        header = "\n\n[환자 정보]\n".encode("utf-8")
        self.assertEqual(prompt + header + self.outputs[builder.J_PAYLOAD], self.outputs[builder.J_SYSTEM])
        self.assertEqual(prompt + header + self.outputs[builder.P_PAYLOAD], self.outputs[builder.P_SYSTEM])

    def test_builder_render_is_idempotent(self) -> None:
        nonce = "CPX-G2-ISO-11111111111111111111111111111111"
        first = builder.render_artifacts(ROOT, self.sources, nonce)
        second = builder.render_artifacts(ROOT, self.sources, nonce)
        self.assertEqual(first, second)

    def test_input_bundle_id_recomputation(self) -> None:
        bundle_path = ROOT / builder.INPUT_BUNDLE
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        canonical = json.dumps(
            bundle["components"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual("sha256:" + hashlib.sha256(canonical).hexdigest(), bundle["input_bundle_id"])

    def test_manifest_58_48_64_accounting(self) -> None:
        manifest = json.loads((ROOT / builder.EXECUTION_MANIFEST).read_text(encoding="utf-8"))
        self.assertEqual(58, len(manifest["scored_units"]))
        self.assertEqual(48, len(manifest["execution_units"]))
        self.assertEqual(64, len(manifest["planned_calls"]))
        self.assertEqual(57, sum(call["scored_turn"] for call in manifest["planned_calls"]))

    def test_sequence_memberships(self) -> None:
        manifest = json.loads((ROOT / builder.EXECUTION_MANIFEST).read_text(encoding="utf-8"))
        by_id = {unit["execution_unit_id"]: unit for unit in manifest["execution_units"]}
        for sequence_id, members in builder.SEQUENCES.items():
            self.assertEqual(list(members), by_id[sequence_id]["scored_unit_ids"])

    def test_p14_setup_linkage(self) -> None:
        manifest = json.loads((ROOT / builder.EXECUTION_MANIFEST).read_text(encoding="utf-8"))
        setup = [
            call
            for call in manifest["planned_calls"]
            if call["constituent_or_setup_id"] == builder.P14_SETUP_ID
        ]
        self.assertEqual(1, len(setup))
        self.assertFalse(setup[0]["scored_turn"])
        self.assertIsNone(setup[0]["scored_unit_id"])
        self.assertEqual(["P14", "P15"], setup[0]["response_referenced_by_scored_units"])

    def test_p29_six_call_linkage(self) -> None:
        manifest = json.loads((ROOT / builder.EXECUTION_MANIFEST).read_text(encoding="utf-8"))
        calls = [call for call in manifest["planned_calls"] if call["execution_unit_id"] == "P29-STATION-01"]
        self.assertEqual(6, len(calls))
        self.assertTrue(all(call["scored_unit_id"] == "P29" for call in calls))
        self.assertTrue(all(call["source_trajectory_id"] is None for call in calls))
        self.assertTrue(all(not call["scored_turn"] for call in calls))

    def test_scorecard_has_58_unscored_rows(self) -> None:
        text = (ROOT / builder.SCORECARD_TEMPLATE).read_text(encoding="utf-8")
        rows = list(csv.DictReader(io.StringIO(text)))
        self.assertEqual(58, len(rows))
        self.assertEqual(1, sum(row["scored_unit_id"] == "P29" for row in rows))
        self.assertTrue(all(not row["disposition"] for row in rows))


if __name__ == "__main__":
    unittest.main()
