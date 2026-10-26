---
name: biz-a-reviewer
description: "Review completed Biz-A work after a chat/task is done, read the conversation from the beginning, identify reusable problems or pitfalls, document the problem in a new .agents/references/ file, and update Biz-A rules or reference indexes so future agents can find the lesson before searching elsewhere. Use when the user asks to document a completed Biz-A chat, create a post-task problem reference, update project instructions from a resolved issue, or maintain Biz-A review knowledge."
---

# Biz-A Reviewer

Use this skill only after a Biz-A task or chat is considered complete and the user wants the lesson documented for future work.

## Workflow

1. Read the conversation from the beginning, including user corrections, tool failures, implementation choices, and final outcome.
2. Identify the reusable problem, not just the final code diff.
   - Capture what went wrong or changed direction.
   - Capture the corrected pattern.
   - Capture where future agents should look first.
3. Inspect the current repo references under `.agents/references/`.
   - If an existing reference already covers the problem, update it narrowly.
   - If not, create a new problem-specific reference file with a concise, searchable name.
4. Write the new reference as a reusable rule, not a transcript.
   - Include: problem signal, root cause, corrected approach, implementation checklist, and related files/patterns.
   - Keep examples short and Biz-A specific.
   - Avoid mentioning private chat details unless needed to reproduce the lesson.
5. Update `.agents/rules/biz-a.rules.instructions.md` so future agents know to search the new reference before falling back to broader repo search or external assumptions.
6. Validate with a syntax/read check when practical.

## Reference Writing Rules

- Create files in `.agents/references/`.
- Prefer names like `<module-or-pattern>-problem.md` or `<pattern>-rules.md`.
- Use ASCII only unless the surrounding file already uses non-ASCII.
- Do not duplicate long content from existing references; link or name the related reference instead.
- Keep the guidance actionable: what to do, what to avoid, and how to verify.

## Required Output

In the final response, list:
- The skill path created or updated.
- The reference file created or updated.
- The Biz-A instruction file updated.
- Any validation command run and its result.
