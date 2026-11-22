# After Hours Agent Governance

## P00/P01/P04 canonical product authority
AgentSwitchboard is a retired product; donor evidence/verified existing caller only. TokenCorridor owns the product control plane. Technical cleanup does not reopen retirement. No new ASB work.


Status: canonical repository governance contract.

This file is the single source of truth for how writing agents operate in
AfterHours. Personal learning follows the shared host-local `/teach` route in
the [README](README.md). The router/workspace software is repository code.
Session state always lives on the learner's host outside Git and synced locations.
The operator chooses the exact reviewed artifact, destination, and action for
each transfer. A lesson or graduation request alone grants no transfer authority.

## Agent operating principles

### Evidence before action
Inspect the repo, branch, pins, validators, and recent changes before mutation.

### Floor before furniture
Contracts, pins, validators, and failure behavior before polish or expansion.

### Bounded sprints with declared scope
Every writing sprint declares lane, mission, owned/forbidden scope, expected
artifacts, validation commands, and proof ceiling before mutation.

### One writer per branch
Separate branches or isolated worktrees for parallel work. Never absorb
unowned dirty work.

### Reuse before replacing
Reuse upstream skills, StudySyndicate contracts, and Continuum patterns before
inventing replacements. Cite prior art.

### No completion without proof
Completion requires named changes, executed validation, a commit SHA, and
reported push/PR state. Private host workspace attempts are learner evidence, never commit proof.

### Learning evidence integrity
Assistance is provenance, never mastery. Graduation into StudySyndicate
requires blank-file reconstruction and executable proof per its gates.

## Mandatory sprint declaration

Before any writing sprint, state repo and branch; lane and mission; owned and
forbidden scope; expected artifacts; validation commands; proof ceiling.

## Completion standard

Complete only when: files named; validations run with results reported;
commit SHA exists; push/PR state reported; one exact next command given
unless no safe actionable work remains.

## Forbidden behaviors

- Mutation without declaration when safe declaration is available.
- Plans or summaries substituting for required proof.
- Committing secrets, credentials, tokens, or private learner data.
- Committing learner `learning-records/` or `lessons/` output into this repo.
- Weakening validators or pins to manufacture a pass.
- Reactivating Continuum control-plane responsibilities here.

## Governance enforcement

```bash
python scripts/validate.py
```
