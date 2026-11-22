"""Run the host workspace boundary against disposable machine-local fixtures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TeachWorkspaceTests(unittest.TestCase):
    def setUp(self):
        area = tempfile.TemporaryDirectory()
        self.addCleanup(area.cleanup)
        self.root = Path(area.name).resolve()
        self.repo = self.root / "checkout"
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.data = self.root / "private-data"
        self.env = dict(os.environ)
        for key in ("CI", "GITHUB_ACTIONS", "CODESPACES", "CODEX_CLOUD", "CODEX_REMOTE",
                    "CODEX_ENVIRONMENT_ID", "CODEX_EXEC_SERVER_REMOTE_BASE_URL",
                    "CODEX_HOME", "CLAUDE_CONFIG_DIR", "XDG_CONFIG_HOME"):
            self.env.pop(key, None)
        self.env.update(HOME=str(self.root), USERPROFILE=str(self.root),
                        LOCALAPPDATA=str(self.data), XDG_DATA_HOME=str(self.data))

    def run_script(self, name, *args, env=None):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name), *map(str, args)],
            cwd=self.repo, env=self.env if env is None else env,
            text=True, capture_output=True, check=False,
        )

    def workspace(self, *args, env=None):
        return self.run_script("teach-workspace.py", "--topic", "Synthetic topic", *args, env=env)

    def test_create_and_resume_outside_checkout(self):
        first = self.workspace()
        self.assertEqual(first.returncode, 0, first.stderr)
        payload = json.loads(first.stdout)
        path = Path(payload["workspace"])
        self.assertTrue(path.is_relative_to(self.root))
        self.assertFalse(path.is_relative_to(self.repo))
        self.assertEqual(payload["repository_transfer"], "OPERATOR_SELECTED_ONLY")
        artifact = path / "learning-records" / "private-record.md"
        artifact.write_text("synthetic learner evidence")
        mission = path / "MISSION.md"
        mission.write_text("synthetic retained mission")
        second = self.workspace()
        self.assertEqual(second.stdout, first.stdout)
        self.assertEqual(artifact.read_text(), "synthetic learner evidence")
        self.assertEqual(mission.read_text(), "synthetic retained mission")
        self.assertEqual(list(self.repo.iterdir()), [self.repo / ".git"])

    def test_resumes_existing_flat_workspace(self):
        previous = self.root / "previous"
        previous.mkdir()
        (previous / "MISSION.md").write_text("original")
        result = self.workspace("--existing", previous)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(json.loads(result.stdout)["workspace"]), previous)
        self.assertEqual((previous / "MISSION.md").read_text(), "original")
        self.assertFalse((previous / ".teach").exists())

    def test_refuses_git_marker_as_file(self):
        nested = self.root / "linked-worktree"
        nested.mkdir()
        (nested / ".git").write_text("gitdir: anywhere")
        result = self.workspace("--existing", nested)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside Git", result.stderr)
        self.assertEqual(list(nested.iterdir()), [nested / ".git"])

    def test_refuses_redirected_root_and_hosted_environment(self):
        for env in (dict(self.env, CI="true"), dict(self.env, CODEX_ENVIRONMENT_ID="synthetic-id"),
                    dict(self.env, LOCALAPPDATA=str(self.root / "OneDrive - Example"),
                         XDG_DATA_HOME=str(self.root / "OneDrive - Example"),
                         HOME=str(self.root / "OneDrive - Example"))):
            with self.subTest(env=env.get("CI", "sync")):
                result = self.workspace(env=env)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("TEACH_WORKSPACE_BLOCKED", result.stderr)
        self.assertFalse((self.root / "OneDrive - Example").exists())

    def test_path_validation_blocks_escape_and_symlinks(self):
        result = self.workspace("--check-path", "../outside.txt")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.data.exists())
        first = self.workspace()
        self.assertEqual(first.returncode, 0, first.stderr)
        path = Path(json.loads(first.stdout)["workspace"])
        try:
            (path / "redirect").symlink_to(self.repo, target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable on this host")
        result = self.workspace("--check-path", "redirect/session.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / "session.md").exists())

    def test_topic_name_does_not_match_sync_path_rules(self):
        result = self.run_script("teach-workspace.py", "--topic", "OneDrive admin commands")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_punctuation_distinguishes_topics(self):
        one = self.run_script("teach-workspace.py", "--topic", "C++")
        two = self.run_script("teach-workspace.py", "--topic", "C#")
        self.assertEqual(one.returncode, 0, one.stderr)
        self.assertEqual(two.returncode, 0, two.stderr)
        self.assertNotEqual(json.loads(one.stdout)["workspace"], json.loads(two.stdout)["workspace"])

    def test_check_path_refuses_hardlink_to_checkout(self):
        first = self.workspace()
        self.assertEqual(first.returncode, 0, first.stderr)
        path = Path(json.loads(first.stdout)["workspace"])
        source = self.repo / "source.md"
        source.write_text("preserved")
        try:
            os.link(source, path / "notes.md")
        except OSError:
            self.skipTest("hardlinks unavailable on this host")
        result = self.workspace("--check-path", "notes.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("linked to another path", result.stderr)
        self.assertEqual(source.read_text(), "preserved")

    def test_router_replacement_requires_a_verified_archive(self):
        router = self.root / ".claude" / "commands" / "teach.md"
        router.parent.mkdir(parents=True)
        router.write_bytes(b"original router")
        first = self.run_script("install-routers.py")
        self.assertNotEqual(first.returncode, 0)
        self.assertEqual(router.read_bytes(), b"original router")
        backup = self.root / "before-install"
        installed = self.run_script("install-routers.py", "--backup-dir", backup)
        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertEqual((backup / "claude-teach.md").read_bytes(), b"original router")
        for path in (
            ".claude/commands/teach.md", ".config/opencode/commands/teach.md",
            ".agents/skills/teach/SKILL.md", ".cursor/skills/teach/SKILL.md",
        ):
            body = (self.root / path).read_text()
            self.assertIn(str(ROOT / "scripts" / "teach-workspace.py"), body)
            self.assertNotIn("<teach-workspace-runner>", body)
        self.assertEqual(self.run_script("install-routers.py", "--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
