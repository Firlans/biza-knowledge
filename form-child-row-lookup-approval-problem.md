# Form Child Row Lookup and Approval Problem

Use this reference when a Biz-A form changes a single-value field into one-to-many child rows, displays related child records as a selectable field, or adds an approval/reopen workflow controlled by custom privileges.

## Problem Signal

- A field currently stores one value, but the expected behavior allows multiple values.
- A header-level field such as `mob_demob_id` or amount is requested to repeat according to existing detail rows such as `QUOTATIONDET`.
- A label such as `spr_number` shows one related record or a comma-joined string, but the user needs to choose from all related records.
- A button opens a record list dialog only to choose or view one existing child record.
- Reopen, approve, or reject behavior is requested per user capability, and the user says not to use group names.
- Firebird insert fails with validation error on a new child table primary key, often because an id/generator was not assigned before `sendModel`.

## Root Cause

Single-value form fields often hide a real one-to-many relationship. Keeping the old scalar value as the source of truth creates several problems:

- multi-select data cannot be saved without a child table payload,
- repeating values may already belong to an existing detail table, so creating a new child table can split the source of truth incorrectly,
- related records cannot be selected reliably when only one display label is available,
- comma-joined display text cannot identify which child record id should be opened,
- approval logic tied to group names breaks when authorization changes to custom privileges,
- child table inserts fail when ids are not generated before sending rows to Firebird.

## Corrected Approach

Use the child rows as the source of truth and keep scalar fields only as the currently selected UI value.

Before creating a new child table, identify the row that owns the repeated value:

- if the repeated value is independent of existing detail rows, create or use a dedicated child table,
- if the repeated value is tied to each existing detail row, add columns to that detail table instead,
- keep the old header scalar columns only as compatibility/summary fields when legacy forms, lists, prints, or reports still read them.

For multi-value categories:

- create or use a child table with one row per selected value,
- load child rows with a dedicated query helper,
- map child rows into an array field for the form control,
- build child payload rows during save,
- assign missing child row ids with the correct `<TABLE>_GEN` generator before `sendModel`,
- delete or replace loaded child rows in a controlled save step before inserting the new payload.

For values tied to existing detail rows, such as quotation mob/demob per equipment type:

- add the lookup and amount fields to the existing repeat/detail row,
- alter the existing detail table, for example add `MOB_DEMOB_ID` and amount columns to `QUOTATIONDET`,
- map load queries from the existing detail table path, not from a new child table,
- include the new fields in the existing detail payload builder such as `jsonQuotationDet`,
- compute any legacy header total from the detail rows before saving,
- backfill detail rows from the legacy header column in the migration when old data exists.

For selectable related records such as SPR:

- keep all related rows in a list field such as `spr_list`,
- make the visible value field such as `spr_number` a `select`,
- build options from `spr_list` using `{ label, value }`,
- store the selected reference number in `spr_number`,
- when opening the related form, resolve the selected reference number back to the row id from `spr_list`,
- if the list is not loaded yet, load it lazily from the button handler, set the first valid option as default, then open that row.

For reopen approval:

- load custom privileges once during form initialization and cache them on the form object,
- use `skip approval reopen` to decide whether reopen is direct or moves to `WAITING APPROVAL REOPEN JOB`,
- use `approve reopen` and `reject reopen` only for approve/reject button visibility and handlers,
- do not branch on user group names,
- treat `WAITING APPROVAL REOPEN JOB` as closed for feature behavior until approved.

## Implementation Checklist

- Add child-row ids to loaded state, for example `loaded_category_ids`.
- Decide whether the repeated value belongs to a new child table or an existing detail row before writing DDL.
- Keep helper names explicit: `build...Options`, `find...By...`, `apply...RowsTo...`, `build...Payloads`, `assign...Ids`.
- Do not join multiple related values into one display string if the UI needs to open a specific related record.
- Do not create a new table merely because a scalar field becomes repeatable if the repeated value is actually part of an existing detail record.
- Do not render primary keys as editable fields. Keep ids in model/payload data only.
- Do not use nested function calls in action handlers; assign intermediate rows, options, selected row, and payloads to variables.
- Keep save flow linear with RxJS operators and a single final `subscribe()`.
- Validate `sendModel` responses before continuing.
- Keep authorization checks privilege-based when custom privileges are the business rule.

## Related Files and Patterns

- `.github/instructions/references/form-rules.md`
- `.github/instructions/references/database-standard-rules.md`
- `.github/instructions/references/dialog-list-problem.md`
- Biz-A Section 13 approval workflow pattern
- Biz-A Section 14 save / CRUD pattern
