"""Install (or check) global /teach routers from canonical sources."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_UPSTREAMS = r"C:\Users\pa_rperez26\OneDrive - Northwell Health\OG Laptop Backup\Desktop\dev\_upstreams"
MAPPING = {
    "teach-opencode.md": Path.home() / ".config" / "opencode" / "commands" / "teach.md",
    "teach-claude.md": Path.home() / ".claude" / "commands" / "teach.md",
    "teach-codex-SKILL.md": Path.home() / ".codex" / "skills" / "teach" / "SKILL.md",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify deployed routers match sources")
    parser.add_argument("--upstreams", default=DEFAULT_UPSTREAMS,
                        help="absolute path substituted for <upstreams>")
    args = parser.parse_args()
    failures = []
    for src_name, dest in MAPPING.items():
        src = ROOT / "routers" / src_name
        body = src.read_text(encoding="utf-8").replace("<upstreams>", args.upstreams)
        if args.check:
            if not dest.exists() or dest.read_text(encoding="utf-8") != body:
                failures.append(str(dest))
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(body, encoding="utf-8")
            print(f"installed {dest}")
    if failures:
        print("DRIFT:")
        for f in failures:
            print(f"  - {f}")
        return 1
    if args.check:
        print("Router deployment CHECK PASS: 3 routers in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
