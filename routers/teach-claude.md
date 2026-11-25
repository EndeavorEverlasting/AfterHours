---
description: Teach a topic via pinned upstream teach skill. Use when user types /teach <topic>.
---

Topic: $ARGUMENTS

You are invoked via /teach in Claude Code. Route to the pinned upstream skill, do not use parametric knowledge alone.

1. Load and follow the pinned skill and formats (see pins.json for SHAs):
- `<upstreams>/mattpocock-skills/skills/productivity/teach/SKILL.md`
- `.../teach/MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md`

2. Before generating any personal learning artifact, run this command on the learner's host:
   `python "<teach-workspace-runner>" --topic "<stable subject name>"`
   Use the returned workspace for all session data, including lesson files, answers, workbooks, recordings, notes, and learning records. Reuse the same subject name on resume. For a known older host workspace, append `--existing "<absolute workspace path>"`. Before each artifact write, validate its relative destination with `--check-path "<relative path>"`.
   If the local runner or host is unavailable, keep preparation in memory and ask the host agent to resume. Keep the source checkout read-only. The learner must choose the exact artifact, destination, and operation before any repository copy, staging, commit, or publication.

3. If the active repo defines its own teach protocol in AGENTS.md, follow its teaching and evidence conventions within the host-local boundary (e.g. StudySyndicate: learning evidence integrity, one mechanism + one exercise, no fabricated mastery).

4. Flow: interview for mission if vague; teach one tightly-scoped mechanism + one exercise per turn; cite high-trust resources; record genuine understanding in `learning-records/`; end with one exact next step + retrieval check. `recap` resumes from learning-records.

## Demonstration-first practice

A standalone teaching session must not require another learning product or an engineering orchestrator. Other projects are optional read-only references or explicitly selected tools. Graduation is opt-in, not a lesson gate.

For interview practice or professional skill claims, start with one concrete challenge (premise, inputs, expected output, constraints, allowed assistance) if the topic is clear. Treat claims as practice targets, not mastery. Ask for an attempt before showing a solution; assess against explicit criteria or executable tests, explain gaps, provide graduated hints, and retry with a fresh transfer exercise. Record assistance, observed results and next unproven step in the verified local workspace; recap reopens the same workspace. Without a verified host runner, practice in memory without claiming persistence.
