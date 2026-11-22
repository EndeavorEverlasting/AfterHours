---
description: Teach a topic via pinned upstream teach skill. Use when user types /teach <topic>.
---

Topic: $ARGUMENTS

You are invoked via /teach. Route to the pinned upstream skill, do not use parametric knowledge alone.

1. Load and follow the pinned skill and formats (see pins.json for SHAs):
- `<upstreams>/mattpocock-skills/skills/productivity/teach/SKILL.md`
- `.../teach/MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md`

2. Before generating any personal learning artifact, run this command on the learner's host:
   `python "<teach-workspace-runner>" --topic "<stable subject name>"`
   Use the returned workspace for all session data, including lesson files, answers, workbooks, recordings, notes, and learning records. Reuse the same subject name on resume. For a known older host workspace, append `--existing "<absolute workspace path>"`. Before writing into an existing or unfamiliar subdirectory, validate the relative artifact destination with `--check-path "<relative path>"`.
   If the local runner or host is unavailable, keep preparation in memory and ask the host agent to resume. Keep the source checkout read-only. The learner must choose the exact artifact, destination, and operation before any repository copy, staging, commit, or publication.

3. If the active repo defines its own teach protocol in AGENTS.md, follow its teaching and evidence conventions within the host-local boundary.

4. Flow:
- If MISSION.md missing or topic vague, interview for Why / Success looks like / Constraints / Out of scope before teaching.
- Teach one tightly-scoped mechanism + one code exercise per turn.
- Cite high-trust resources in RESOURCES.md, link them from lessons.
- Record genuine understanding shifts in `learning-records/NNNN-slug.md`, never mere coverage.
- End each turn with one exact next step and a retrieval check.

If $ARGUMENTS is empty, ask what to teach. `recap` resumes from learning-records (first weak frontier).
