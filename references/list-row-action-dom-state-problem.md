# List Row Action DOM State Problem

Use this reference when a Biz-A list row action must be enabled, disabled, hidden, or rewritten differently per row, but the list renderer does not support the desired per-row button property.

## Problem Signal

- A list `Action` column has one button whose state differs by row status, approval state, branch mapping, or another row value.
- Adding a button config property such as `disabled`, expression strings, or custom metadata has no visible effect in the rendered list.
- The user points to the rendered Angular/Material table DOM, `tbody`, `tr:nth-child(...)`, or an action-cell `span`.
- The existing action button must remain in the `Action` column because authorization helpers still filter by button `id`.

## Root Cause

Biz-A list button config is not a full per-row renderer API in every runtime. Some button properties may be ignored after `setAction`, privilege filtering, or table rendering. When a per-row state is not supported declaratively, the visible DOM can diverge from the `columns[].button` config.

The rendered table row order normally matches `this.dataSource.dataSubject._value`. That makes a narrow DOM fallback possible: read rendered rows from the table body, use each row index to read the corresponding source row, then update only the target action button in that rendered row.

## Correct Pattern

Keep the action button declaration simple and privilege-compatible. Do not rely on unsupported per-row button properties.

Add small helpers for:

- the table body selector,
- the action-cell selector,
- source rows from `this.dataSource.dataSubject._value`,
- rendered rows from `document.querySelector(...).children`,
- target button lookup inside the action cell,
- applying the DOM state,
- scheduling after `loadData()` renders.

Keep the click handler guard even when the button is disabled in the DOM. DOM state is a UX layer; the handler is the behavior boundary.

Example:

```javascript
getListTableBodySelector: function () {
    return 'body > app-root > app-list > div > table > tbody'
},
getActionCellSelector: function () {
    return 'td.mat-mdc-cell.mdc-data-table__cell.cdk-cell.cdk-column-SO-IDAction.mat-column-SO-IDAction.ng-star-inserted > span'
},
getRenderedRows: function () {
    if (typeof document === 'undefined') {
        return []
    }

    const tbody = document.querySelector(this.f().getListTableBodySelector())
    return Array.from(tbody?.children || [])
},
applyForwardButtonStateByRow: function () {
    const sourceRows = this.dataSource?.dataSubject?._value || []
    const renderedRows = this.f().getRenderedRows()
    const actionCellSelector = this.f().getActionCellSelector()

    renderedRows.forEach((renderedRow, index) => {
        const sourceRow = sourceRows[index]
        const actionContainer = renderedRow.querySelector(actionCellSelector)
        const forwardButton = Array.from(actionContainer?.querySelectorAll('button') || [])
            .find(button => String(button.textContent || '').toLowerCase().includes('forward'))
        const disabled = String(sourceRow?.status || '').toLowerCase() === 'dibuat'

        if (forwardButton) {
            forwardButton.disabled = disabled
            forwardButton.setAttribute('aria-disabled', String(disabled))
        }
    })
}
```

Schedule the DOM update after each data reload path that can render rows:

```javascript
return this.loadData().pipe(
    this.map(data => {
        this.f().scheduleApplyForwardButtonStateByRow()
        return data
    })
)
```

## Implementation Checklist

- Keep `columns[].button[]` declarative: `id`, `caption`, `icon`, `color`, and `onClick`.
- Do not add unsupported per-row config properties when the runtime has already shown they are ignored.
- Put selectors in named helpers, not inline inside the action logic.
- Use `typeof document === 'undefined'` guard so non-browser flows do not crash.
- Match rendered row to data row by index only after confirming the list is not grouped, virtualized, or sorted differently from `dataSource.dataSubject._value`.
- Apply DOM state after every `loadData()` path, including first load and post-action reload.
- Keep the action handler guard for the same business rule.
- Avoid broad selectors that affect other lists or other action buttons.

## Related Files And Patterns

- `.agents/references/list-rules.md`
- `.agents/references/list-action-button-wrap-problem.md` for layout-only action button issues.
- `Endo Medika/SOList.js` shows row-index DOM state for the `Forward` button when status is `Dibuat`.
