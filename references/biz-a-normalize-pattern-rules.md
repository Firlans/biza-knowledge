# Biz-A Normalize Pattern Rules

Use this reference when a Biz-A task asks to normalize repeated patterns, extract reusable functions, move data/query logic out of forms or lists, or reuse existing utilities.

## Problem Signals

- The same mode, button, navigation, mapping, or grid behavior is copied across multiple forms.
- A form or list builds query params, raw SQL, `executeBlock` SQL, DB filters, or source-row normalization directly inside the UI module.
- Similar helpers exist in more than one file with small naming or formatting differences.
- New code recreates behavior that already exists in `lib_qry`, `lib_utility`, `lib_utils`, or another shared library loaded by `useLibrary`.

## Root Cause

Repeated Biz-A work often starts in the first target form, then gets copied to approved forms, report forms, or source navigation targets. This mixes three responsibilities:

- data access and query shaping,
- reusable utility behavior,
- form/list UI orchestration.

When those responsibilities stay in one file, every future change has to patch several modules and the behavior becomes coupled to implementation details.

## Correct Approach

- Preserve existing behavior while moving responsibilities to the right boundary.
- Move data-related behavior to `lib_qry` or the module's query library:
  - `queryData` calls,
  - `executeBlock` and raw SQL builders,
  - query parameter/filter builders,
  - source-row normalization from DB rows,
  - row builders whose input is query result data.
- Move generic non-query helpers to an existing utility library before creating a new helper file:
  - mode parsing,
  - button visibility rules,
  - back/navigation helpers,
  - shared field lookup or assignment helpers,
  - formatting or numeric helpers that are not module-specific.
- Keep forms and lists focused on orchestration:
  - lifecycle hooks,
  - field and column configuration,
  - calling query helpers,
  - assigning model/grid data,
  - validation and submit flow,
  - routing to source or target forms.
- Prefer existing helpers before adding new ones. Check the current `useLibrary` entries and known utilities such as `findField`, `findLuFina`, `toNumber`, `listData`, and domain-specific builders already present in the module libraries.
- Remove wrappers that only rename another helper and do not add business meaning.

## Implementation Checklist

- [ ] Identify all repeated behavior and group it by responsibility: data/query, utility, or UI orchestration.
- [ ] Extract pure helpers first, then wire forms/lists to call the extracted helpers.
- [ ] Put query/data behavior in `lib_qry` and export it through the existing library pattern.
- [ ] Put shared UI/state/navigation utility behavior in the existing utility library when one is already loaded.
- [ ] Keep extracted helpers deterministic when possible and pass values in explicitly.
- [ ] Avoid runtime-dependent default parameters; resolve fallbacks inside function bodies.
- [ ] Avoid nested function calls in parameters; assign intermediate values to named variables first.
- [ ] Keep helper names aligned with Firlan style: `build...`, `normalize...`, `apply...`, `set...`, `load...`, `validate...`.
- [ ] Delete the old duplicated implementation after all callers use the new helper.

## Related References

- `.agents/references/helper-rules.md`
- `.agents/references/form-rules.md`
- `.agents/references/list-rules.md`
- `.agents/references/refactor-checklist.md`
