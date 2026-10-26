"""Verify rules delivery and blocking behavior without executing agent commands."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from read_rules import response


class RulesHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rules hook ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rules = self.root / ".agents/rules"
        self.rules.mkdir(parents=True)
        instructions = self.root / ".agents/instructions/project.md"
        instructions.parent.mkdir(parents=True)
        instructions.write_text("Project instructions: baca aturan.", encoding="utf-8")
        (self.rules / "biz-a.rules.instructions.md").write_text(
            "Core rules: preserve business behavior.", encoding="utf-8"
        )

    def test_delivers_full_rules_for_both_events_without_echoing_inputs(self):
        nested = self.rules / "exec/default.rules"
        nested.parent.mkdir()
        nested.write_text('prefix_rule(pattern=["test"], decision="prompt")', encoding="utf-8")
        for name in ["UserPromptSubmit", "PreToolUse"]:
            with self.subTest(event=name):
                result = response({
                    "hook_event_name": name,
                    "cwd": str(self.root / "module with spaces"),
                    "prompt": "PRIVATE_PROMPT_MARKER",
                    "tool_input": {"command": "PRIVATE_COMMAND_MARKER"},
                }, self.root)
                output = result["hookSpecificOutput"]
                self.assertEqual(output["hookEventName"], name)
                context = output["additionalContext"]
                self.assertIn("Project instructions: baca aturan.", context)
                self.assertIn("Core rules: preserve business behavior.", context)
                self.assertIn(nested.read_text(encoding="utf-8"), context)
                self.assertNotIn("PRIVATE_", json.dumps(result))
                self.assertNotIn("permissionDecision", output)

    def test_missing_core_rules_block_instead_of_returning_partial_context(self):
        (self.rules / "biz-a.rules.instructions.md").unlink()
        result = response({"hook_event_name": "PreToolUse"}, self.root)
        self.assertEqual(result["decision"], "block")
        self.assertIn("biz-a.rules.instructions.md", result["reason"])
        self.assertNotIn("hookSpecificOutput", result)

    def test_empty_rules_block_prompt(self):
        (self.rules / "biz-a.rules.instructions.md").write_text("  ", encoding="utf-8")
        result = response({"hook_event_name": "UserPromptSubmit"}, self.root)
        self.assertEqual(result["decision"], "block")

    def test_rules_are_reread_after_changes(self):
        event = {"hook_event_name": "PreToolUse"}
        response(event, self.root)
        (self.rules / "new-rule.md").write_text("Fresh rule loaded immediately.", encoding="utf-8")
        self.assertIn("Fresh rule loaded immediately.",
                      response(event, self.root)["hookSpecificOutput"]["additionalContext"])

    def test_private_files_and_references_are_not_loaded(self):
        for name in [".env", ".agents/config/private/codex.toml", ".agents/references/example.md"]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("PRIVATE_FILE_MARKER", encoding="utf-8")
        result = response({"hook_event_name": "PreToolUse"}, self.root)
        self.assertNotIn("PRIVATE_FILE_MARKER", json.dumps(result))

    def test_malformed_stdin_returns_block_json(self):
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(Path(__file__).with_name("read_rules.py"))],
            input="not-json", capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(result.stdout)["decision"], "block")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
