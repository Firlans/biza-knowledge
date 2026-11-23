---
name: biz-a-reviewer
description: Review completed Biz-A work for verified, reusable lessons and document new findings in project references or rules. Use when asked to document lessons from a completed Biz-A chat or task.
---

# Biz-A Reviewer

Use this workflow to document lessons from completed Biz-A work, including during `$close`.

## Workflow

1. Read the available conversation from the beginning, including any context summaries, user corrections, implementation choices, and the final outcome. Use the evidence and confirmed project requirements to identify lessons that would change how a similar task is handled. If part of the history is unavailable, report that limit.
2. Check `.agents/references/INDEX.md` and the relevant references and rules. Skip lessons that are already covered, specific to one task with no reusable guidance, or still speculative. If no verified new guidance remains, report the result without creating files.
3. Add missing detail to the existing reference or rule that owns the topic. For a new topic, write a focused file under `.agents/references/` and add searchable triggers to `.agents/references/INDEX.md`. Update the index for an existing reference when the new material adds a distinct search trigger. Change project rules when the finding establishes or corrects a mandatory requirement.
4. Capture the signal and applicable conditions, the evidence or root cause when established, the verified approach, and how to check it. Link relevant source files or patterns. Keep examples focused and omit private chat details.
5. Check the resulting references and index links, record documentation edits according to project instructions, and report the paths changed and verification performed.

## Reference Writing Rules

- Prefer names like `<module-or-pattern>-problem.md` or `<pattern>-rules.md`.
- Use ASCII only unless the surrounding file already uses non-ASCII.
- Link related references so each topic can be maintained in one place.
