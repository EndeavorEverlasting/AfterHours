---
description: Teach a topic via pinned upstream teach skill. Use when user types /teach <topic>.
---

Topic: $ARGUMENTS

You are invoked via /teach. Route to the pinned upstream skill, do not use parametric knowledge alone.

1. Load and follow the pinned skill and formats (see pins.json for SHAs):
- `<upstreams>/mattpocock-skills/skills/productivity/teach/SKILL.md`
- `.../teach/MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md`

2. Canonical workspace home (centralized-only): resolve the OS Desktop Known Folder, then `Dev/_teach/<topic-slug>/` (slug = lowercase dash-case, e.g. `two-sum`). That directory IS the teaching workspace (`MISSION.md`, `RESOURCES.md`, `lessons/`, `reference/`, `learning-records/`, `assets/`, `NOTES.md`). Create it lazily. Never write teach workspace files into the invoking repo checkout.

3. If the active repo defines its own teach protocol in AGENTS.md, obey it as binding local law on top of the upstream skill.

4. Flow:
- If MISSION.md missing or topic vague, interview for Why / Success looks like / Constraints / Out of scope before teaching.
- Teach one tightly-scoped mechanism + one code exercise per turn.
- Cite high-trust resources in RESOURCES.md, link them from lessons.
- Record genuine understanding shifts in `learning-records/NNNN-slug.md`, never mere coverage.
- End each turn with one exact next step and a retrieval check.

If $ARGUMENTS is empty, ask what to teach. `recap` resumes from learning-records (first weak frontier).
