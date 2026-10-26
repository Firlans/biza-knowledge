"""Rebuild application entrypoints from the project's canonical .agents folder."""

from pathlib import Path
import json
import os
import re


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / ".agents"


def write(relative, content):
    target = ROOT / relative
    if not target.resolve().is_relative_to(ROOT):
        raise ValueError(f"Entrypoint outside repository: {relative}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_text(encoding="utf-8-sig") == content:
        return
    target.write_text(content, encoding="utf-8")


def frontmatter(source):
    text = source.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\n.*?\n---\n", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {source.relative_to(ROOT)}")
    return match.group(0)


def link_file(source_relative, target_relative):
    """Use one NTFS file for canonical settings and the required native path."""
    source = ROOT / source_relative
    target = ROOT / target_relative
    if not source.resolve().is_relative_to(ASSETS) or not target.resolve().is_relative_to(ROOT):
        raise ValueError("Native configuration paths must stay inside the repository")
    if not source.is_file():
        print(f"Skipped missing local settings: {source_relative}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if os.path.samefile(source, target):
            return
        if target.read_bytes() != source.read_bytes():
            raise ValueError(f"Native settings differ; reconcile before syncing: {target_relative}")
        target.unlink()
    try:
        os.link(source, target)
    except OSError:
        # Other filesystems may not support hard links. Re-running refreshes this copy.
        target.write_bytes(source.read_bytes())


def main():
    write("AGENTS.md", "# Instruksi AI proyek\n\n"
          "Baca dan ikuti [.agents/instructions/project.md](.agents/instructions/project.md) "
          "sebelum mengerjakan proyek ini.\n"
          "Untuk dokumentasi library/API/CLI, baca dan ikuti "
          "[aturan Context7](.agents/instructions/context7.md).\n")
    write("CLAUDE.md", "@.agents/instructions/project.md\n@.agents/instructions/context7.md\n")
    write(".github/copilot-instructions.md", "# Instruksi AI proyek\n\n"
          "Baca dan ikuti `.agents/instructions/project.md` serta "
          "`.agents/instructions/context7.md` dari root repository.\n"
          "Skill dan referensi yang dipelihara tersedia di `.agents/`.\n")
    rules = ASSETS / "rules/biz-a.rules.instructions.md"
    write(".github/instructions/biz-a.rules.instructions.md", frontmatter(rules) +
          "\nBaca dan ikuti seluruh aturan di "
          "[Biz-A Rules](../../.agents/rules/biz-a.rules.instructions.md).\n"
          "Edit sumber di `.agents/`, lalu jalankan `python .agents/scripts/sync-native.py`.\n")
    for source in sorted((ASSETS / "agents").glob("*.agent.md")):
        relative = source.relative_to(ROOT).as_posix()
        write(f".github/agents/{source.name}", frontmatter(source) +
              f"\nRead and follow the complete agent instructions in `{relative}` "
              "from the repository root before performing the request.\n")
    for source in sorted((ASSETS / "commands").glob("*.md")):
        relative = source.relative_to(ROOT).as_posix()
        write(f".claude/commands/{source.name}", frontmatter(source) +
              f"\nBaca dan ikuti seluruh command di `{relative}` dari root repository.\n\n"
              "Permintaan pengguna: $ARGUMENTS\n")
    link_file(".agents/rules/exec/default.rules", ".codex/rules/default.rules")
    link_file(".agents/config/private/codex.toml", ".codex/config.toml")
    template = ASSETS / "hooks/codex.template.json"
    if template.is_file():
        hooks = json.loads(template.read_text(encoding="utf-8-sig"))
        for groups in hooks["hooks"].values():
            for group in groups:
                for handler in group["hooks"]:
                    for key in ("command", "commandWindows"):
                        if key in handler:
                            handler[key] = handler[key].replace("{project_root}", ROOT.as_posix())
        write(".codex/hooks.json", json.dumps(hooks, indent=2, ensure_ascii=False) + "\n")
    print("Native entrypoints synchronized from .agents/.")


if __name__ == "__main__":
    main()
