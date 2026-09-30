#!/usr/bin/env python3
"""Integration tests for full CLI execution."""

import sys
import os
import subprocess
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.application import main


class TestIntegration(unittest.TestCase):
    """Integration tests using the main entry point."""

    def _run_cli(self, args: list[str], cwd: str | None = None) -> tuple[int, str, str]:
        """Run CLI via subprocess."""
        if cwd is None:
            cwd = str(Path(__file__).parent.parent.parent)

        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}

        result = subprocess.run(
            [sys.executable, "rtg.py"] + args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=cwd,
            env=env,
        )
        return result.returncode, result.stdout, result.stderr

    def test_no_args_shows_void(self):
        """Test running with no args shows void."""
        code, stdout, stderr = self._run_cli([])
        self.assertEqual(code, 0)
        self.assertIn("Usage:", stdout)
        self.assertIn("rtg", stdout)

    def test_version(self):
        """Test --version."""
        code, stdout, stderr = self._run_cli(["--version"])
        self.assertEqual(code, 0)
        self.assertIn("RtG-CLI v1.2.0", stdout)

    def test_version_short(self):
        """Test -v."""
        code, stdout, stderr = self._run_cli(["-v"])
        self.assertEqual(code, 0)
        self.assertIn("RtG-CLI v1.2.0", stdout)

    def test_help(self):
        """Test --help."""
        code, stdout, stderr = self._run_cli(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("RtG-CLI", stdout)

    def test_help_short(self):
        """Test -h."""
        code, stdout, stderr = self._run_cli(["-h"])
        self.assertEqual(code, 0)

    def test_help_command(self):
        """Test help command."""
        code, stdout, stderr = self._run_cli(["help"])
        self.assertEqual(code, 0)

    def test_help_with_target(self):
        """Test help with target."""
        code, stdout, stderr = self._run_cli(["help", "image"])
        self.assertEqual(code, 0)
        self.assertIn("RtG Image", stdout)

    def test_help_with_language(self):
        """Test help with language."""
        code, stdout, stderr = self._run_cli(["help", "image", "-en"])
        self.assertEqual(code, 0)

    def test_help_list_langs(self):
        """Test help -lang."""
        code, stdout, stderr = self._run_cli(["help", "image", "-lang"])
        self.assertEqual(code, 0)
        self.assertIn("Available languages", stdout)

    def test_rules(self):
        """Test --rules."""
        code, stdout, stderr = self._run_cli(["--rules"])
        self.assertEqual(code, 0)
        self.assertIn("RtG-CLI", stdout)

    def test_rules_short(self):
        """Test -r."""
        code, stdout, stderr = self._run_cli(["-r"])
        self.assertEqual(code, 0)

    def test_rules_with_language(self):
        """Test rules with language."""
        code, stdout, stderr = self._run_cli(["--rules", "-en"])
        self.assertEqual(code, 0)

    def test_lang(self):
        """Test --lang."""
        code, stdout, stderr = self._run_cli(["--lang"])
        self.assertEqual(code, 0)
        self.assertIn("Available languages", stdout)

    def test_lang_short(self):
        """Test -l."""
        code, stdout, stderr = self._run_cli(["-l"])
        self.assertEqual(code, 0)

    def test_commands(self):
        """Test --commands."""
        code, stdout, stderr = self._run_cli(["--commands"])
        self.assertEqual(code, 0)
        self.assertIn("RtG-CLI internal commands", stdout)

    def test_commands_short(self):
        """Test -c."""
        code, stdout, stderr = self._run_cli(["-c"])
        self.assertEqual(code, 0)

    def test_addons(self):
        """Test --addons."""
        code, stdout, stderr = self._run_cli(["--addons"])
        self.assertEqual(code, 0)
        self.assertIn("Available addons", stdout)
        self.assertIn("image", stdout)
        self.assertIn("preview", stdout)
        self.assertIn("test-addon", stdout)

    def test_addons_short(self):
        """Test -a."""
        code, stdout, stderr = self._run_cli(["-a"])
        self.assertEqual(code, 0)

    def test_language_option(self):
        """Test -language option."""
        code, stdout, stderr = self._run_cli(["-language", "en"])
        self.assertEqual(code, 0)
        self.assertIn("Usage:", stdout)

    def test_addon_image(self):
        """Test image addon."""
        code, stdout, stderr = self._run_cli(["image"])
        self.assertEqual(code, 0)
        self.assertIn("RtG Image", stdout)

    def test_addon_preview(self):
        """Test preview addon."""
        code, stdout, stderr = self._run_cli(["preview"])
        self.assertEqual(code, 0)
        self.assertIn("RtG Preview", stdout)

    def test_addon_test_addon(self):
        """Test test-addon."""
        code, stdout, stderr = self._run_cli(["test-addon"])
        self.assertEqual(code, 0)
        self.assertIn("Test Addon", stdout)

    def test_test_addon_echo(self):
        """Test test-addon echo."""
        code, stdout, stderr = self._run_cli(["test-addon", "echo", "hello"])
        self.assertEqual(code, 0)
        self.assertIn("hello", stdout)

    def test_test_addon_fail(self):
        """Test test-addon fail."""
        code, stdout, stderr = self._run_cli(["test-addon", "fail"])
        self.assertEqual(code, 1)

    def test_test_addon_exit_code(self):
        """Test test-addon exit-code."""
        code, stdout, stderr = self._run_cli(["test-addon", "exit-code", "42"])
        self.assertEqual(code, 42)

    def test_test_addon_stdout(self):
        """Test test-addon stdout."""
        code, stdout, stderr = self._run_cli(["test-addon", "stdout", "test"])
        self.assertEqual(code, 0)
        self.assertIn("test", stdout)

    def test_test_addon_stderr(self):
        """Test test-addon stderr."""
        code, stdout, stderr = self._run_cli(["test-addon", "stderr", "error"])
        self.assertEqual(code, 0)
        self.assertIn("error", stderr)

    def test_unknown_command(self):
        """Test unknown command shows void (legacy behavior)."""
        code, stdout, stderr = self._run_cli(["unknowncmd"])
        self.assertEqual(code, 0)
        self.assertIn("Usage:", stdout)

    def test_addon_with_double_hyphen_args(self):
        """Test addon with double-hyphen arguments."""
        code, stdout, stderr = self._run_cli(["test-addon", "echo", "--custom", "value"])
        self.assertEqual(code, 0)
        self.assertIn("custom", stdout)

    def test_addon_lang_option(self):
        """Test addon -lang option."""
        code, stdout, stderr = self._run_cli(["test-addon", "-lang"])
        self.assertEqual(code, 0)
        self.assertIn("Available languages", stdout)


if __name__ == "__main__":
    unittest.main()