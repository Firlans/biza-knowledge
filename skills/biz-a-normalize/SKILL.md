---
name: biz-a-normalize
description: "Normalize repeated Biz-A form, list, and helper patterns into reusable helpers and libraries. Use when: pola berulang, repeated pattern, normalize, reusable function, pindah query/data logic ke lib_qry, manfaatkan lib_utility/helper yang tersedia, rapikan data access dari form/list."
---

# Biz-A Normalize

Use this skill when existing Biz-A code already works but has repeated patterns, query/data logic inside form/list files, or duplicated utility-like logic across modules.

## Load Relevant References

Always read:
- `.agents/rules/biz-a.rules.instructions.md`
- `.agents/references/helper-rules.md`
- `.agents/references/biz-a-normalize-pattern-rules.md`

If editing forms, also read:
- `.agents/references/form-rules.md`
- `.agents/references/pk-field-config.md`

If editing lists, also read:
- `.agents/references/list-rules.md`

If the task touches a known local problem signal, read the matching problem reference from `.agents/references/` before broad repo search.

## Workflow

1. Preserve existing behavior while moving responsibilities to the right boundary.
2. Inventory repeated behavior and classify it as data/query, reusable utility, or UI orchestration.
3. Move data-related behavior to `lib_qry` or the module query library:
   - `queryData` calls,
   - `executeBlock` and raw SQL builders,
   - query parameter/filter builders,
   - source-row normalization from DB rows,
   - row builders whose input is query result data.
4. Move generic non-query behavior to an existing utility library before creating a new one:
   - mode parsing,
   - button visibility rules,
   - back/navigation helpers,
   - shared field lookup or assignment helpers,
   - formatting or numeric helpers that are not module-specific.
5. Keep forms and lists focused on orchestration: lifecycle hooks, field/column config, calling helpers, assigning grids/models, validation, printing, and routing.
6. Prefer helpers already available through `useLibrary`, such as `findField`, `findLuFina`, `toNumber`, `listData`, and existing domain builders.
7. Remove wrappers that only rename another helper and do not add business meaning.
8. Remove duplicated code after callers are migrated.

## Constraints

- Do not introduce runtime-dependent default parameters. Resolve runtime fallbacks inside function bodies.
- Do not pass nested function calls as parameters; assign intermediate values to named variables first.
- Do not move UI lifecycle code into query libraries.
- Do not leave duplicated implementations after callers are migrated.
- Keep names aligned with Firlan style: `build...`, `normalize...`, `apply...`, `set...`, `load...`, `validate...`.
