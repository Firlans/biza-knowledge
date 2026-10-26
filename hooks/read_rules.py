"""Load canonical project rules into Codex before prompts and command execution."""

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
EVENTS = {"UserPromptSubmit", "PreToolUse"}


def load_rules(root):
    root = root.resolve()
    rules_dir = root / ".agents/rules"
    required = [
        root / ".agents/instructions/project.md",
        rules_dir / "biz-a.rules.instructions.md",
    ]
    files = required + sorted(
        path for path in rules_dir.rglob("*")
        if path.is_file() and path.suffix in {".md", ".rules"} and path not in required
    )
    sections = [
        "Aturan proyek dimuat dari .agents/ sebelum operasi ini. "
        "Ikuti setiap aturan sesuai cakupan task dan file. "
        "Sebelum mengubah kode Biz-A, baca .agents/references/INDEX.md "
        "dan hanya referensi yang relevan."
    ]
    for path in files:
        if not path.resolve().is_relative_to(root):
            raise ValueError("File rules mengarah ke luar proyek.")
        relative = path.relative_to(root).as_posix()
        if not path.is_file():
            raise ValueError(f"File rules wajib tidak ditemukan: {relative}")
        content = path.read_text(encoding="utf-8-sig").strip()
        if not content:
            raise ValueError(f"File rules kosong: {relative}")
        sections.append(f"## {relative}\n\n{content}")
    return "\n\n".join(sections)


def response(event, root=ROOT):
    if not isinstance(event, dict) or event.get("hook_event_name") not in EVENTS:
        return {"decision": "block", "reason": "Event hook pembaca rules tidak valid."}
    try:
        context = load_rules(root)
    except (OSError, ValueError, UnicodeError) as error:
        return {
            "decision": "block",
            "reason": f"Rules belum dapat dimuat. Pulihkan file .agents/ sebelum melanjutkan. {error}",
        }
    return {
        "hookSpecificOutput": {
            "hookEventName": event["hook_event_name"],
            "additionalContext": context,
        }
    }


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, UnicodeError):
        event = None
    # Never echo prompt, tool_input, command text, environment, or private config.
    json.dump(response(event), sys.stdout, ensure_ascii=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
