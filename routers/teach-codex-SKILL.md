---
name: teach
description: Teach the user a topic via a stateful learning workspace. Use when the user asks to teach, learn, drill, or recap a topic, or invokes /teach.
---

Run this `teach` skill for Codex or Cursor.

Route to the pinned upstream skill, do not rely on parametric knowledge alone.

1. Load and follow the pinned skill and formats (see pins.json for SHAs):
- `<upstreams>/mattpocock-skills/skills/productivity/teach/SKILL.md`
- `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md` alongside it.

2. Before generating any personal learning artifact, run this command on the learner's host:
   `python "<teach-workspace-runner>" --topic "<stable subject name>"`
   Use the returned workspace for all session data, including lesson files, answers, workbooks, recordings, notes, and learning records. Reuse the same subject name on resume. For a known older host workspace, append `--existing "<absolute workspace path>"`. Before each artifact write, validate its relative destination with `--check-path "<relative path>"`.
   If the local runner or host is unavailable, keep preparation in memory and ask the host agent to resume. Keep the source checkout read-only. The learner must choose the exact artifact, destination, and operation before any repository copy, staging, commit, or publication.

3. If the active repo defines its own teach protocol in AGENTS.md, follow its teaching and evidence conventions within the host-local boundary (StudySyndicate: learning evidence integrity, premise-first, one mechanism + one exercise, blank-file reconstruction for mastery, never treat assistance as mastery).

4. Flow: interview for mission if vague; teach one mechanism + one exercise per turn; reuse `./assets/` components across lessons; cite high-trust resources; record genuine understanding shifts in `learning-records/NNNN-slug.md`; end with one next step + retrieval check. `recap` resumes from learning-records.

## Demonstration-first practice

A standalone teaching session must not require another learning product or an engineering orchestrator. Other projects are optional read-only references or explicitly selected tools. Graduation is opt-in, not a lesson gate.

For interview practice or professional skill claims, start with one concrete challenge (premise, inputs, expected output, constraints, allowed assistance) if the topic is clear. Treat claims as practice targets, not mastery. Ask for an attempt before showing a solution; assess against explicit criteria or executable tests, explain gaps, provide graduated hints, and retry with a fresh transfer exercise. Record assistance, observed results and next unproven step in the verified local workspace; recap reopens the same workspace. Without a verified host runner, practice in memory without claiming persistence.
