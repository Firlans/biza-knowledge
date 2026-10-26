# Detail Grid OnCalc Event Loop Problem

Use this reference when a Biz-A form reports `Maximum call stack size exceeded`, repeated `onCalc` calls, or a detail-grid total that must include the value currently being edited.

## Problem Signal

- Editing a watched detail-grid column triggers `Maximum call stack size exceeded`.
- A detail-grid `onCalc` handler calls `rowCtls.get(watchedKey).setValue(...)` for the same key that fired the handler.
- Header totals are stale because `this.form.get(detailKey).value` still contains the row's previous value while the current edit event is being processed.

## Root Cause

`onCalc` is already running because a watched key changed. Calling `setValue()` on that same watched control inside the handler emits another change event, so the handler calls itself repeatedly.

This is most common in total handlers like:

```javascript
const amount = (rowCtls, amount) => {
    rowCtls.get('amount').setValue(amount);
    const total = this.form.get('details').value
        .reduce((acc, row) => acc + Number(row.amount), 0);
    this.form.get('total').setValue(total);
};
```

## Corrected Approach

Do not write back to the watched control that triggered the handler. Treat the `value` argument as the current edited value and adjust the aggregate using the row control's previous value.

```javascript
const amount = (rowCtls, amount) => {
    const currentAmount = Number(rowCtls.get('amount').value || 0);
    const newAmount = Number(amount || 0);
    const total = this.form.get('details').value
        .reduce((acc, row) => acc + Number(row.amount), 0) - currentAmount + newAmount;

    this.form.get('total').setValue(total);
};
```

It is acceptable to call `setValue()` on a different derived control, such as a header total or a readonly calculated column that is not in `watchKey`. Avoid writing to the same key that is currently watched unless the implementation explicitly suppresses event emission and the user requested that behavior.

## Implementation Checklist

- Identify the `watchKey` that fires the `onCalc` handler.
- Check every handler returned by `gridListener()` or inline `onCalc` function.
- Remove `rowCtls.get(watchedKey).setValue(...)` calls from the same watched-key handler.
- For totals, use `value` from `function(rowCtls, value, key)` as the new row value.
- Subtract the row control's current value from the aggregate before adding the new value.
- Keep the header or dependent field update as the only `setValue()` in the handler.

## Related Patterns

- `.agents/references/patterns.md` Section 10: Detail Grid Pattern
- `.agents/references/patterns.md` Section 15: Listener Pattern
