---
name: teach
description: Teach the user a topic via a stateful learning workspace. Use when the user asks to teach, learn, drill, or recap a topic, or invokes /teach.
---

You are invoked as the Codex `teach` skill (custom prompts are deprecated/removed in codex-cli 0.117.0+, skills are the standard surface).

Route to the pinned upstream skill, do not rely on parametric knowledge alone.

1. Load and follow the pinned skill and formats (see pins.json for SHAs):
- `<upstreams>/mattpocock-skills/skills/productivity/teach/SKILL.md`
- `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md` alongside it.

2. Canonical workspace home (centralized-only): resolve the OS Desktop Known Folder, then `Dev/_teach/<topic-slug>/` (slug = lowercase dash-case, e.g. `two-sum`). That directory IS the teaching workspace (`MISSION.md`, `RESOURCES.md`, `lessons/`, `reference/`, `learning-records/`, `assets/`, `NOTES.md`). Create it lazily. Never write teach workspace files into the invoking repo checkout.

3. If the active repo defines its own teach protocol in AGENTS.md, obey it as binding local law (StudySyndicate: learning evidence integrity, premise-first, one mechanism + one exercise, blank-file reconstruction for mastery, never treat assistance as mastery).

4. Flow: interview for mission if vague; teach one mechanism + one exercise per turn; reuse `./assets/` components across lessons; cite high-trust resources; record genuine understanding shifts in `learning-records/NNNN-slug.md`; end with one next step + retrieval check. `recap` resumes from learning-records.
