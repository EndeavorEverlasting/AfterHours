"""Prepare private teaching state on the learner's host."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

DIRECTORIES = ("lessons", "learning-records")
TEMPLATES = {
    "MISSION.md": "# Mission\n\nTopic: {topic}\n\nGoal, constraints, and next practice step go here.\n",
    "RESOURCES.md": "# Resources\n\nRecord trusted sources and useful references here.\n",
}
HOSTED_ENV = ("CI", "GITHUB_ACTIONS", "CODESPACES", "CODEX_CLOUD", "CODEX_REMOTE")
MANAGED_ENV = ("CODEX_ENVIRONMENT_ID", "CODEX_EXEC_SERVER_REMOTE_BASE_URL")
SYNC_NAMES = ("onedrive", "dropbox", "google drive", "icloud drive", "cloudstorage")


def is_hosted() -> bool:
    return any(os.environ.get(key) for key in MANAGED_ENV) or any(
        os.environ.get(key, "").lower() in {"true", "1", "yes"} for key in HOSTED_ENV
    )


def host_data_home() -> Path:
    if sys.platform == "win32":
        value = os.environ.get("LOCALAPPDATA")
        if not value:
            raise ValueError("LOCALAPPDATA is unavailable")
        return Path(value)
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support"
    value = os.environ.get("XDG_DATA_HOME")
    return Path(value) if value else Path.home() / ".local" / "share"


def guard(path: Path) -> None:
    if not path.is_absolute() or path.anchor.startswith(("\\\\", "//")) or ".." in path.parts:
        raise ValueError("teaching workspace must be an absolute path on the learner's host")
    if sys.platform == "win32":
        import ctypes

        if ctypes.windll.kernel32.GetDriveTypeW(str(path.anchor)) != 3:
            raise ValueError("teaching workspace must be on a local fixed drive")
    sync_roots = [
        Path(value).resolve()
        for key in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial")
        if (value := os.environ.get(key))
    ]
    resolved = path.resolve()
    if any(resolved.is_relative_to(root) for root in sync_roots) or any(
        part.casefold() in SYNC_NAMES or part.casefold().startswith("onedrive - ")
        for part in (*path.parts, *resolved.parts)
    ):
        raise ValueError("teaching workspace must be outside known sync folders")
    for parent in (path, *path.parents):
        try:
            info = parent.lstat()
        except FileNotFoundError:
            info = None
        if info and (stat.S_ISLNK(info.st_mode) or
                     getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise ValueError("teaching workspace cannot traverse a symlink or junction")
        if info and stat.S_ISREG(info.st_mode) and info.st_nlink > 1:
            raise ValueError("existing artifact is linked to another path")
        git_marker = parent / ".git"
        if git_marker.exists() or git_marker.is_symlink() or (
            (parent / "HEAD").is_file() and (parent / "objects").is_dir()
            and (parent / "refs").is_dir()
        ):
            raise ValueError("teaching workspace must be outside Git repositories and worktrees")


def topic_slug(topic: str) -> str:
    normalized = " ".join(topic.casefold().split())
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    if not re.fullmatch(r"[a-z0-9]+(?:[ -][a-z0-9]+)*", normalized):
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]
        slug = f"{slug or 'topic'}~{digest}"
    if not normalized or len(slug) > 80 or re.fullmatch(r"con|prn|aux|nul|com[1-9]|lpt[1-9]", slug):
        raise ValueError("provide a topic that yields a usable directory name")
    return slug


def resolve_workspace(topic: str, existing: Path | None) -> Path:
    if is_hosted():
        raise ValueError("run private teaching on the learner's host")
    if existing is None:
        return host_data_home() / "MoonWake" / "Teaching" / topic_slug(topic) / ".teach"
    if not existing.is_absolute():
        raise ValueError("an existing workspace must be an absolute host path")
    guard(existing)
    if not existing.is_dir():
        raise ValueError("the specified existing workspace was not found")
    nested = existing / ".teach"
    if nested.exists() or nested.is_symlink():
        if any((existing / name).exists() for name in (*DIRECTORIES, *TEMPLATES)):
            raise ValueError("workspace has both flat and .teach state; select the exact directory")
        return nested
    if not any((existing / name).exists() for name in (*DIRECTORIES, *TEMPLATES)):
        raise ValueError("existing workspace does not contain teaching state")
    return existing


def prepare(workspace: Path, topic: str) -> None:
    for name in (*DIRECTORIES, *TEMPLATES):
        guard(workspace / name)
    for name in DIRECTORIES:
        if (path := workspace / name).exists() and not path.is_dir():
            raise ValueError("expected a teaching directory: " + name)
    for name in TEMPLATES:
        if (path := workspace / name).exists() and not path.is_file():
            raise ValueError("expected a teaching file: " + name)
    workspace.mkdir(mode=0o700, parents=True, exist_ok=True)
    for name in DIRECTORIES:
        (workspace / name).mkdir(mode=0o700, exist_ok=True)
    for name, template in TEMPLATES.items():
        try:
            with (workspace / name).open("x", encoding="utf-8") as output:
                output.write(template.format(topic=" ".join(topic.split())))
        except FileExistsError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="stable subject name, including when resuming")
    parser.add_argument("--existing", type=Path, help="known topic directory on the learner's host")
    parser.add_argument("--check-path", type=Path, help="validate an intended path relative to the workspace without writing")
    args = parser.parse_args()
    try:
        workspace = resolve_workspace(args.topic, args.existing)
        guard(workspace)
        if args.check_path is None:
            prepare(workspace, args.topic)
        else:
            if args.check_path.anchor or ".." in args.check_path.parts:
                raise ValueError("intended artifact path must stay inside the workspace")
            guard(workspace / args.check_path)
    except (OSError, RuntimeError, ValueError) as exc:
        parser.exit(1, f"TEACH_WORKSPACE_BLOCKED: {exc}\n")
    print(json.dumps({"workspace": str(workspace), "repository_transfer": "OPERATOR_SELECTED_ONLY"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
