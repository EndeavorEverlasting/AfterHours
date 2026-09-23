# After Hours

> Like going to the professor's office and finding it closed — but still getting the help.

After Hours is the cross-harness learning system: `/teach` routers, a centralized
private-workspace convention, pinned upstream skills, and a graduation bridge
into StudySyndicate reusable study sets.

It owns *how learning happens everywhere*. StudySyndicate owns *what is worth
keeping*. Private findings graduate forward; reusable lessons never flow backward.

## Status

Active scaffold. Upstream teach skill pinned to `mattpocock/skills@c55ee46`
(same pin as the operator contract floor).

## Structure

```text
routers/                  Canonical /teach router sources (OpenCode, Claude Code, Codex skill)
workspace-template/       MISSION / RESOURCES / NOTES scaffolds for Dev/_teach/<topic>/
pins.json                 Pinned upstream SHAs (machine-readable)
graduation/               Universal classifier contract: any knowledge bit -> study set
scripts/install-routers.py  Deploys routers to global harness homes (--check for CI)
scripts/validate.py       Repository contract validator
tests/                    Contract tests mirroring the validator
```

## Canonical paths

- Teaching home: OS Desktop Known Folder → `Dev/_teach/<topic-slug>/`
  (slug = lowercase dash-case, e.g. `two-sum`). Never inside a repo checkout.
- Reusable lessons: StudySyndicate `content/` via the graduation contract.

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
