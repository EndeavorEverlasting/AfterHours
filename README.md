# After Hours

> Like going to the professor's office and finding it closed — but still getting the help.

After Hours is the cross-harness learning system: `/teach` routers, a centralized
private-workspace convention, pinned upstream skills, and a graduation bridge
into StudySyndicate reusable study sets.

It owns the shared teaching route across agents. The learner owns personal records
and chooses what, if anything, to share with an owning repository.

## Status

Active scaffold. Upstream teach skill pinned to `mattpocock/skills@c55ee46`
(same pin as the operator contract floor).

## Structure

```text
routers/                  Canonical /teach router sources (OpenCode, Claude Code, Codex skill)
workspace-template/       MISSION / RESOURCES / NOTES scaffolds for local topic workspaces
pins.json                 Pinned upstream SHAs (machine-readable)
graduation/               Universal classifier contract: any knowledge bit -> study set
scripts/install-routers.py  Installs or verifies routers in local agent homes
scripts/teach-workspace.py  Resolves and prepares private topic workspaces
scripts/validate.py       Repository contract validator
tests/                    Contract tests mirroring the validator
```

## Canonical paths

Run this on the learner's computer with Python 3.10+:

```sh
python scripts/teach-workspace.py --topic "example subject"
```

Windows uses `%LOCALAPPDATA%\MoonWake\Teaching\<topic>\.teach`, macOS uses its
local Application Support folder, and Linux uses the local XDG data directory.
Use the returned workspace for workbooks, notes, recordings, exercises and
assessments. Use the same subject to resume, or pass `--existing` with the exact
known machine-local path to continue older work in place. `--check-path` validates
a workspace-relative destination before a write. The runner rejects Git
worktrees, symlinks, known sync locations and recognized hosted environments.
Run only from the learner's verified host or continue the lesson without
persisting state until the local agent takes over.

Personal records stay on the host by default. A graduation request may prepare
a shareable candidate on that same host. Copy, stage, commit or publish only
the exact reviewed material and destination the learner explicitly chooses. Graduate reusable derivatives to the relevant project without transferring raw private session folders.

### Local agent routers

From this checkout, run `python scripts/install-routers.py --check` to inspect
Codex, Cursor, Claude Code, and OpenCode router drift. For an authorized
installation run `python scripts/install-routers.py`. To replace an existing
router, pass `--backup-dir <new-local-directory>`; its exact bytes are archived
and verified before writing. Supply `--upstreams <local-path>` during installation
and verification when the pinned pedagogy sources are outside the default
`~/Dev/_upstreams`. The routers reference this checkout's workspace runner.

## Validation

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

## Prior art

- `mattpocock/skills` teach skill (+ formats) — pedagogy and workspace shape.
- `EndeavorEverlasting/Continuum` (dormant) — task/result packet split,
  completion gates, git-evidence pins. Cited, not reactivated.
- `EndeavorEverlasting/StudySyndicate` — factored domain, evidence integrity,
  mastery gates. Graduation target.

## License

MIT — see [LICENSE](LICENSE).
