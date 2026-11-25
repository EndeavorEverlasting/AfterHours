# Canonical teaching ownership handoff

Teaching entry point only; curriculum authority remains with the selected curriculum owner.

## Required behavior

- AfterHours owns the cross-harness teaching entry point and verified host-local workspace routing.
- A learner-selected curriculum repository owns its approved curriculum and assessment methodology. It is a read-only reference during lessons; the live learner workspace owns actual attempts, progress, notes and evidence.
- A clear practice request starts with one concrete challenge, not an architecture sprint. No separate study product, graduation, graph application or engineering orchestrator is required.
- The learner chooses exact reviewed material, destination and operation before any repository transfer. Never publish personal learning data by default.
- Preserve existing workspace identity on resume; do not create a parallel progress store or silently migrate paths.

## Successor execution

On the actual learner host, identify this checkout and the learner-selected curriculum checkout independently (verify Git origin, clean/dirty state and intended revision; never assume presence). Fetch without overwriting unrelated work, inspect current governance, run `python scripts/validate.py` and `python -m unittest discover -s tests -v`, then check installed routers with `python scripts/install-routers.py --check`. Before replacing active instructions, archive and verify their current bytes; follow the installer backup and approval boundary.

Conduct one real teaching turn in a local agent, using the selected curriculum as a read-only reference. Present a challenge, await an attempt, give feedback, record observed evidence in the verified workspace, close the session, and reopen the same topic. Confirm continuity and no repository writes. A synthetic fixture, successful CI, merge or router installation is not live teaching proof. If the host is unavailable, report HOST_UNVERIFIED and continue safe repository work; never fabricate a clone path or live receipt.
