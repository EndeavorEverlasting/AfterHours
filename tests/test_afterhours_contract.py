"""Contract tests mirroring scripts/validate.py."""
import json
import shutil
import subprocess
import sys
import tempfile
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
            self.assertIn("<teach-workspace-runner>", text)
            self.assertIn("exact artifact, destination, and operation", text)

    def test_canonical_handoff_fails_closed(self):
        with tempfile.TemporaryDirectory() as area:
            root = Path(area) / "checkout"
            root.mkdir()
            for name in ("scripts", "routers", "workspace-template", "graduation", "docs"):
                shutil.copytree(ROOT / name, root / name)
            for name in ("AGENTS.md", "pins.json"):
                shutil.copy2(ROOT / name, root / name)
            def run():
                return subprocess.run([sys.executable, str(root / "scripts/validate.py")],
                                      capture_output=True, text=True)
            self.assertEqual(run().returncode, 0)
            handoff = root / "docs/TEACHING-OWNERSHIP-HANDOFF.md"
            original = handoff.read_text(encoding="utf-8")
            handoff.write_text(original.replace("HOST_UNVERIFIED", ""), encoding="utf-8")
            self.assertNotEqual(run().returncode, 0)
            handoff.unlink()
            self.assertNotEqual(run().returncode, 0)

    def test_classifier_contract(self):
        contract = json.loads(
            (ROOT / "graduation" / "classifier-contract.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["schema"], "after-hours/universal-classifier/v1")
        self.assertIn("flashcard", contract["emit_study_sets"])
        self.assertIn("recall_drill", contract["emit_study_sets"])
        self.assertIs(contract["repository_transfer"]["automatic"], False)

    def test_templates(self):
        for name in ("MISSION.md", "RESOURCES.md", "NOTES.md"):
            text = (ROOT / "workspace-template" / name).read_text(encoding="utf-8")
            self.assertIn("{{", text)


if __name__ == "__main__":
    unittest.main()
