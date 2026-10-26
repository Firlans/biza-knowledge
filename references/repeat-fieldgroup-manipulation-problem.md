# Repeat FieldGroup Manipulation Problem

Use this reference when a Biz-A form dynamically adds, removes, hides, or rebuilds fields inside a Formly `repeat`, especially from a `selection-list`, `valueChanges` listener, or custom-column style feature.

## Problem Signal

- A `selection-list` controls which fields should appear in each row of a `repeat`.
- Static repeat fields are moved to a dynamic child `fieldGroup`.
- A listener such as `visible_column.valueChanges` keeps firing repeatedly after the field config is changed.
- Optional repeat columns must be saved to a child/custom table instead of fixed query columns.
- A rendered repeat row shows stale fields, duplicated fields, or missing newly selected fields.

## Root Cause

Formly repeat fields keep both a source field config and rendered per-row field configs. Mutating a row control value, replacing the wrong config object, or rebuilding the dynamic `fieldGroup` on every emitted value can cause Formly to rerender and emit the same watched value again.

The loop usually appears when a listener does this:

```javascript
this.form.get('visible_column').valueChanges.subscribe((value) => {
    this.f().syncUnitCustomColumns(value);
});
```

and `syncUnitCustomColumns` always rebuilds the repeat `fieldGroup`, even when the normalized selected columns are unchanged.

## Corrected Approach

Treat repeat field manipulation as configuration work, not row value work:

- Put a stable placeholder group inside the repeat, for example `unit-custom-column-group`.
- Locate the repeat field and placeholder group from `this.fields`, then update only that group's `fieldGroup`.
- Copy config objects shallowly so callbacks/functions are preserved; do not use `structuredClone` on field configs.
- Normalize the controlling selection into canonical keys before rebuilding dynamic fields.
- Add a re-entrant guard plus a selection snapshot so the same selection does not rebuild fields again.
- After changing the source group, apply equivalent field configs to already rendered repeat rows if the runtime keeps row-level rendered configs.
- Store optional values in model rows and map them explicitly to child/custom-table payloads during save.

Short pattern:

```javascript
syncUnitCustomColumns: function (value) {
    const selectedColumns = this.f().normalizeUnitCustomColumnSelection(value);
    const snapshot = this.f().buildUnitCustomColumnSelectionSnapshot(selectedColumns);

    if (this.unitCustomColumnSyncing || this.unitCustomColumnSelectionSnapshot === snapshot) {
        return selectedColumns;
    }

    this.unitCustomColumnSyncing = true;
    try {
        this.f().applyUnitCustomColumnFields(selectedColumns);
        this.unitCustomColumnSelectionSnapshot = snapshot;
    } finally {
        this.unitCustomColumnSyncing = false;
    }

    return selectedColumns;
}
```

## Implementation Checklist

- Keep the controlling field outside the repeat when it controls which repeat row fields are visible.
- Define allowed dynamic columns in one helper such as `get...CustomColumnDefinitions()`.
- Normalize selection values from strings, arrays, `{ value }`, or `{ key }` objects before comparison.
- Use an explicit placeholder group inside the repeat and replace that group's `fieldGroup`.
- Do not call `setValue()` on the repeat control to refresh dynamic fields; update `this.model.repeat_key` for data and field config for UI.
- Do not rebuild dynamic field config if the normalized selection snapshot has not changed.
- Remove temporary `debugger` and `console.log` before finishing.
- Save dynamic values through explicit custom/child payload builders and delete-reinsert or update rows according to the owning table's expected behavior.

## Related Patterns

- `.agents/references/form-rules.md`
- `.agents/references/error-reference.md` for repeat data assignment pitfalls
- `.agents/references/patterns.md` Section 15: Listener Pattern
