# Detail Grid Dynamic Column Expression Problem

Use this reference when a Biz-A form `detail-grid` changes column order, adds columns such as currency/unit measure/action, or the user asks to avoid hardcoded `props.columns[index]` expressions.

## Problem Signal

- A detail-grid expression targets columns with fixed numeric paths such as `props.columns[9].label`.
- Moving a column breaks labels, required rules, lookup visibility, or category-specific behavior.
- The user points out that expressions can be functions and asks to locate columns by `key` or `className`.
- Several columns share category markers such as `hide-part`, `hide-consumable`, or `lu-fina`.

## Root Cause

`detail-grid` column expressions that depend on fixed array positions are brittle. Adding a hidden column, moving `currency` beside `unit_measure`, or adding an `Action` column shifts indexes while the old expression paths still update the previous position.

Biz-A expression functions can update the whole `props.columns` array. This lets the form locate the target column by a stable marker such as `key` or `className` inside the expression scope instead of calculating paths outside the field config.

## Corrected Approach

Keep `props.columns` declared normally. Put the dynamic lookup logic inside the `expressions` block:

```javascript
expressions: {
    'props.columns': function () {
        const detailGrid = (this.fields || []).find(field => field.id === 'item-detail-grid');
        const columns = detailGrid?.props?.columns || this.props?.columns || [];
        const categoryName = this.model.category_name;
        const findByKey = (key) => columns.find(column => column.key === key);
        const findByClassName = (className) => {
            return columns.find(column => `${column.className || ''}`.includes(className));
        };

        const supplierColumn = findByClassName('hide-consumable');
        if (supplierColumn) {
            supplierColumn.label = categoryName === 'CONSUMABLE' ? 'Supplier' : '';
            supplierColumn.required = categoryName === 'CONSUMABLE';
        }

        return columns;
    },
}
```

Prefer `key` for one explicit column. Use `className` when the marker is the business meaning the user wants to target, for example `hide-consumable`.

## Implementation Checklist

- Keep `props.columns` as a normal array on the detail-grid field.
- Add or reuse stable markers: `key` for exact columns, `className` for category groups.
- Put helper functions such as `findByKey` and `findByClassName` inside the `expressions` function scope.
- Return the updated `columns` array from the expression function.
- Do not wrap the entire detail-grid field in an IIFE just to compute expression keys.
- Do not leave string literal expression keys like `props.columns[4].label`.
- If column configs contain functions, do not use `structuredClone` on them.

## Related Files And Patterns

- `.agents/references/detail-grid-manual-action-buttons-problem.md` for manual Add/Delete and `Action` columns.
- `.agents/references/detail-grid-state-sync-problem.md` for custom delete handlers and `assignData`.
- `.agents/references/form-rules.md`.
