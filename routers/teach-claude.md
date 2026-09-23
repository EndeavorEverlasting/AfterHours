---
description: Teach a topic via pinned upstream teach skill. Use when user types /teach <topic>.
---

Topic: $ARGUMENTS

You are invoked via /teach in Claude Code. Route to the pinned upstream skill, do not use parametric knowledge alone.

1. Load and follow the pinned skill and formats (see pins.json for SHAs):
- `<upstreams>/mattpocock-skills/skills/productivity/teach/SKILL.md`
- `.../teach/MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md`

2. Canonical workspace home (centralized-only): resolve the OS Desktop Known Folder, then `Dev/_teach/<topic-slug>/` (slug = lowercase dash-case, e.g. `two-sum`). That directory IS the teaching workspace. Create it lazily. Never write teach workspace files into the invoking repo checkout.

3. If the active repo defines its own teach protocol in AGENTS.md, obey it as binding local law (e.g. StudySyndicate: learning evidence integrity, one mechanism + one exercise, no fabricated mastery).

4. Flow: interview for mission if vague; teach one tightly-scoped mechanism + one exercise per turn; cite high-trust resources; record genuine understanding in `learning-records/`; end with one exact next step + retrieval check. `recap` resumes from learning-records.
