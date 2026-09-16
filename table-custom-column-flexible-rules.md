# Table Custom Column Flexible Rules

Use this reference when a Biz-A table, print table, or detail-grid lets users add or select custom columns, especially when the selected column metadata is stored in model fields such as `visible_column`.

## Problem Signal

- A custom column appears in the table but the cell value is empty or comes from the wrong row key.
- A user-added column should still render even though it is not in a hardcoded mapping.
- A custom column has `type: 'money'`, `typedata: 'number'`, or another metadata type but renders as raw text.
- The table uses a field option object with separate `key`, `value`, `label`, and type metadata.
- The implementation maps labels or aliases loosely and later fails when the form stores a different `value`.

## Root Cause

Flexible table columns have two separate identities:

- `value` is the saved selection value from the form option.
- `key` is the row data property used to read the cell value.

When code treats `value`, `key`, and `label` as interchangeable, existing built-in columns may seem to work, but custom columns break. For example, a selection option can be `{ key: 'set_crew', value: 'jumlah_operator', label: 'Jumlah Operator' }`; the print table must recognize `jumlah_operator` as the selected column but read the row value from `unit.set_crew`.

Custom columns also need to carry type metadata forward. If `{ key: 'harga_tambahan', label: 'Harga Tambahan', type: 'money' }` loses `type`, the renderer cannot apply currency formatting.

## Corrected Approach

Treat the form's selectable column definitions as the source of truth. Built-in mappings must match the option `value` exactly, then resolve to the row `key`.

```javascript
const mapping = {
    jumlah_unit: 'qtyunit',
    jumlah_operator: 'set_crew',
    jumlah_helper: 'qty_helper',
    jumlah_rigger: 'qty_rigger',
    jumlah_hse: 'qty_hse',
    crew_tambahan: 'additional_crew',
};
```

When building render columns:

- read selection objects without losing `key`, `value`, `label`, and `type` or `typedata`,
- map known `value` entries to existing row keys,
- for unknown custom entries, normalize the declared key/value and still render the column,
- use `label` as the header text,
- format the cell based on the column type metadata.

Short example:

```javascript
const rawValue = item.value ?? item.key ?? item.column_name ?? item.label;
const mappedKey = mapVisibleColumnKey(rawValue);
const columnKey = mappedKey || normalizeColumnKey(item.key ?? rawValue);
const label = `${item.label || rawValue || columnKey}`.trim();

return {
    key: columnKey,
    label,
    type: item.type || item.typedata,
};
```

Render cells from the row key and type:

```javascript
const value = row[column.key];
const isFilled = value !== undefined && value !== null && `${value}`.trim() !== '';

if (column.type === 'money') {
    return isFilled ? formatPrintCurrency(value) : '';
}

return isFilled ? value : '';
```

## Implementation Checklist

- Inspect the originating field configuration first, especially `props.listOptions` or helper definitions that populate custom columns.
- Keep built-in map entries exactly aligned with the form option `value`.
- Keep the rendered column `key` aligned with the row data property.
- Preserve `label` for table headers.
- Preserve `type` or `typedata` so renderers can format money, number, date, lookup labels, and future custom types.
- Let unmapped custom columns render instead of dropping them from the selected column list.
- Deduplicate selected columns by final row `key`.
- Keep always-visible base columns separate from user-selected/custom columns.
- Do not use `structuredClone` on column config objects if they may contain functions.
- Avoid broad alias maps unless they are explicitly needed for legacy saved data and validated against current behavior.

## Related Files And Patterns

- `Proton/quotationForm.js`: `visible_column` selection-list and unit custom column definitions.
- `Proton/lib_template.js`: quotation print unit table column rendering.
- `.github/instructions/references/detail-grid-dynamic-column-expression-problem.md`: use for dynamic detail-grid expressions by column key or class marker.
- `.github/instructions/references/repeat-fieldgroup-manipulation-problem.md`: use when custom columns are added to repeat row field groups.
