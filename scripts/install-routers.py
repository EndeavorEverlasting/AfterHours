"""Install or verify host-local teaching routers from this checkout."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def destinations() -> list[tuple[str, str, Path]]:
    home = Path.home()
    opencode = Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config")
    claude = Path(os.environ.get("CLAUDE_CONFIG_DIR") or home / ".claude")
    legacy_codex = Path(os.environ.get("CODEX_HOME") or home / ".codex") / "skills/teach/SKILL.md"
    selected = [
        ("opencode", "teach-opencode.md", opencode / "opencode/commands/teach.md"),
        ("claude", "teach-claude.md", claude / "commands/teach.md"),
        ("codex", "teach-codex-SKILL.md", home / ".agents/skills/teach/SKILL.md"),
        ("cursor", "teach-codex-SKILL.md", home / ".cursor/skills/teach/SKILL.md"),
    ]
    if legacy_codex.is_file():
        selected.append(("codex-legacy", "teach-codex-SKILL.md", legacy_codex))
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify deployed routers without writing")
    parser.add_argument("--upstreams", type=Path, default=Path.home() / "Dev/_upstreams",
                        help="location of the existing upstream pedagogy sources")
    parser.add_argument("--backup-dir", type=Path, help="archive and verify existing routers before replacement")
    args = parser.parse_args()
    runner = ROOT / "scripts/teach-workspace.py"
    if not runner.is_file():
        parser.exit(1, "Teaching workspace runner missing from this checkout.\n")
    pending = []
    previous = []
    for agent, name, dest in destinations():
        body = (ROOT / "routers" / name).read_text(encoding="utf-8")
        body = body.replace("<upstreams>", str(args.upstreams.resolve()))
        body = body.replace("<teach-workspace-runner>", str(runner))
        current = dest.read_bytes() if dest.is_file() else None
        if current is not None and current.replace(b"\r\n", b"\n") == body.encode("utf-8"):
            continue
        pending.append((dest, body))
        if current is not None:
            previous.append((agent, current))
    if args.check:
        for dest, _ in pending:
            print(f"DRIFT: {dest}")
        if not pending:
            print("Teaching routers match the checkout.")
        return int(bool(pending))
    if previous and args.backup_dir is None:
        parser.exit(1, "Existing routers differ. Supply --backup-dir to archive and verify them before replacement.\n")
    if previous:
        backup = args.backup_dir
        backup.mkdir(parents=True, exist_ok=True)
        for agent, content in previous:
            archived = backup / (agent + "-teach.md")
            with archived.open("xb") as file:
                file.write(content)
            if archived.read_bytes() != content:
                parser.exit(1, "Router archive verification failed.\n")
    for dest, body in pending:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8")
        print(f"Installed {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
