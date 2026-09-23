"""After Hours contract validator: pins, routers, templates, graduation."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = []


def check(condition, label):
    if not condition:
        FAILURES.append(label)


def main():
    pins = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
    check(pins.get("schema") == "after-hours/pins/v1", "pins schema")
    sources = pins.get("sources", [])
    check(len(sources) == 4, "pins source count == 4")
    for s in sources:
        sha = s.get("resolved_sha", "")
        check(bool(re.fullmatch(r"[0-9a-f]{40}", sha)), f"pin sha 40-hex for {s.get('id')}")

    for name in ("teach-opencode.md", "teach-claude.md", "teach-codex-SKILL.md"):
        text = (ROOT / "routers" / name).read_text(encoding="utf-8")
        check("Dev/_teach" in text, f"router {name} canonical home")
        check("Never write teach workspace files into the invoking repo" in text,
              f"router {name} no-repo-pollution rule")

    for name in ("MISSION.md", "RESOURCES.md", "NOTES.md"):
        text = (ROOT / "workspace-template" / name).read_text(encoding="utf-8")
        check("{{" in text, f"template {name} has placeholders")

    contract = json.loads((ROOT / "graduation" / "classifier-contract.v1.json").read_text(encoding="utf-8"))
    check(contract.get("schema") == "after-hours/universal-classifier/v1", "classifier schema")
    check("flashcard" in contract.get("emit_study_sets", {}), "classifier emits flashcards")
    check("recall_drill" in contract.get("emit_study_sets", {}), "classifier emits recall drills")

    ag = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    check("learning-records" in ag or "learner" in ag, "governance covers learner evidence")

    if FAILURES:
        print("FAIL:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("After Hours validation PASS: 4 pins, 3 routers, 3 templates, classifier contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
