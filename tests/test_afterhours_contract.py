"""Contract tests mirroring scripts/validate.py."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class AfterHoursContract(unittest.TestCase):
    def test_pins(self):
        pins = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
        self.assertEqual(pins["schema"], "after-hours/pins/v1")
        self.assertEqual(len(pins["sources"]), 4)
        for s in pins["sources"]:
            self.assertRegex(s["resolved_sha"], r"^[0-9a-f]{40}$")

    def test_routers(self):
        for name in ("teach-opencode.md", "teach-claude.md", "teach-codex-SKILL.md"):
            text = (ROOT / "routers" / name).read_text(encoding="utf-8")
            self.assertIn("Dev/_teach", text)
            self.assertIn("Never write teach workspace files into the invoking repo", text)

    def test_classifier_contract(self):
        contract = json.loads(
            (ROOT / "graduation" / "classifier-contract.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["schema"], "after-hours/universal-classifier/v1")
        self.assertIn("flashcard", contract["emit_study_sets"])
        self.assertIn("recall_drill", contract["emit_study_sets"])

    def test_templates(self):
        for name in ("MISSION.md", "RESOURCES.md", "NOTES.md"):
            text = (ROOT / "workspace-template" / name).read_text(encoding="utf-8")
            self.assertIn("{{", text)


if __name__ == "__main__":
    unittest.main()
