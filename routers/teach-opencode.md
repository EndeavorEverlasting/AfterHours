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
   Use the returned workspace for all session data, including lesson files, answers, workbooks, recordings, notes, and learning records. Reuse the same subject name on resume. For a known older host workspace, append `--existing "<absolute workspace path>"`. Before each artifact write, validate its relative destination with `--check-path "<relative path>"`.
   If the local runner or host is unavailable, continue practice in memory and request host recovery only for durable persistence. Keep the source checkout read-only. The learner must choose the exact artifact, destination, and operation before any repository copy, staging, commit, or publication.

3. Apply a repository's teaching and evidence conventions only when the learner explicitly selects it as curriculum or exercise reference; do not infer a product dependency from the active checkout.

4. Flow:
- If the topic is vague, interview for Why / Success looks like / Constraints / Out of scope before teaching. If the topic is clear but MISSION.md is missing, initialize a minimal mission locally and begin the exercise.
- Teach one tightly-scoped mechanism + one code exercise per turn.
- Cite high-trust resources in RESOURCES.md, link them from lessons.
- Record genuine understanding shifts in `learning-records/NNNN-slug.md`, never mere coverage.
- End each turn with one exact next step and a retrieval check.

If $ARGUMENTS is empty, ask what to teach. `recap` resumes from learning-records (first weak frontier).

## Demonstration-first practice

A standalone teaching session must not require another learning product or an engineering orchestrator. Other projects are optional read-only references or explicitly selected tools. Graduation is opt-in, not a lesson gate.

For interview practice or professional skill claims, start with one concrete challenge (premise, inputs, expected output, constraints, allowed assistance) if the topic is clear. Treat claims as practice targets, not mastery. Ask for an attempt before showing a solution; assess against explicit criteria or executable tests, explain gaps, provide graduated hints, and retry with a fresh transfer exercise. Record assistance, observed results and next unproven step in the verified local workspace; recap reopens the same workspace. Without a verified host runner, practice in memory without claiming persistence.
