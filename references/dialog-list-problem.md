# Dialog List Problem

Use this reference when a Biz-A form needs to show previously created records, selectable rows, or historical data from the same workflow.

## Problem Signal

- User asks for a table/list in a form, then clarifies it should be opened from a button or dialog.
- A list grid is added directly to the main `fields`, making the form crowded or loading data too early.
- User has already adjusted the grid columns, lookup type, or labels; future changes must start from the current file state and preserve those edits.

## Root Cause

Record history and selection lists are navigation aids, not primary form detail data. Putting them as permanent form `detail-grid` fields can:

- mix selection UI with editable/detail payload UI,
- trigger unnecessary data loading during `onInit`,
- complicate `setDbIndex` because dialog-only lookup configs are not always present in `this.fields`,
- make it harder to close the selector before loading a selected record.

## Correct Pattern

Use a button on the form toolbar and open a dialog containing the list grid.

Recommended flow:

1. Add a form button such as `View BO Sourcing List`.
2. Build dialog fields in a named helper such as `buildBoSourcingListDialogFields`.
3. Load rows lazily in the button handler, not during `onInit`.
4. Open the dialog with `this.f().openDialog(title, model, fields, afterOpenedOperator)`.
5. Store a dialog ref from the opened config when a row action needs to close the dialog.
6. In the row `View` button, close the dialog and call the existing load function for the selected id.

## Implementation Checklist

- Keep the actual form detail grid in `fields`; move the history/list grid into a dialog field builder.
- Keep dialog list state in `model` only if row action handlers need access to selected rows.
- Set lookup `dbIndex` for dialog-only columns inside the dialog field builder, using `this.config?.api?.finaDbIndex || ''`.
- Do not scan `this.fields` for dialog-only columns in `setDbIndex`; those fields do not live in the main form field tree.
- Do not use `structuredClone` for dialog fields or grid column configs because button handlers and callbacks are functions.
- Avoid nested calls when practical: assign `model` and `fields` to variables before calling `openDialog`.
- Preserve user edits to grid columns, such as `lookup_combo`, captions, and lookup display rules.

## Related References

- `.agents/references/form-rules.md`
