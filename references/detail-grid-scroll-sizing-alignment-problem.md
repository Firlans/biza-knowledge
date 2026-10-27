# Detail Grid Scroll, Sizing, And Alignment Problem

## Problem Signal

- A dense Biz-A `detail-grid` makes the whole page overflow instead of scrolling inside its frame.
- Headers or values wrap into two lines, or numeric and money values are clipped.
- Lookup text needs more room than quantity columns.
- A column must center its rendered control, but `style.textAlign = 'center'` does not produce the expected result.

## Root Cause

Biz-A detail-grid rows use flex columns. A dense grid needs both a local scroll container and explicit column sizing. Percentage widths that fit a simple grid are often too small for formatted money, while `auto` is not reliable for values rendered inside an input.

Column `textAlign` controls text alignment semantics. It does not center a rendered child control inside a flex cell. Centering that cell content requires flex layout with `justifyContent`.

## Corrected Approach

Give the grid a stable, module-specific class and apply horizontal overflow to that frame. Give table rows a minimum width so the table creates local overflow without expanding the page. Scope selectors for both legacy Angular Material elements and MDC classes.

```javascript
{
    className: 'workshop-sales-detail-grid',
    type: 'detail-grid',
    props: {
        detailKey: 'details',
        columns: [/* ... */],
    },
}
```

Use column widths based on content type:

```javascript
{ key: 'agency_id', type: 'lookup_combo', style: { flex: '0 0 20%' } },
{
    key: 'order_qty',
    type: 'number',
    style: { flex: '0 0 8rem', display: 'flex', justifyContent: 'center' },
},
{
    key: 'amount',
    type: 'money',
    style: { flex: '0 0 14rem', display: 'flex', justifyContent: 'center' },
}
```

- Use wider percentage widths for lookup or description columns.
- Use stable `rem` widths for formatted numeric and money values when digits are clipped.
- Use `display: 'flex'` plus `justifyContent: 'center'` to center the rendered column content.
- Use `textAlign` only when the requirement is specifically text alignment and the renderer honors it.
- Keep `white-space: nowrap` local to the scrollable grid when wrapping is not allowed.
- To fill a wide dialog without a blank strip after the final column, set table
  and row widths to `100%` and let a description/remarks column grow, for example
  `flex: '1 0 24rem'`. Keep its minimum width and the other columns' fixed bases
  so narrow screens still scroll. Do not add unused width to the sum of visible
  column widths. Verify the final cell reaches the frame edge on a wide viewport,
  not just that it becomes visible after scrolling.
- Install injected layout CSS during `beforeLoadData` and remove it during `onDestroy`.

## What To Avoid

- Do not put `overflow-x: auto` on the page or an unrelated parent container.
- Do not assume all visible columns must total 100 percent after horizontal scrolling is introduced.
- Do not use narrow percentage widths for long formatted currency values.
- Do not use `textAlign` as a substitute for flex child positioning.
- Do not use brittle generated Formly IDs when a stable grid class is available.
- Do not change payload, lookup, calculation, or save behavior for a layout-only task.

## Implementation Checklist

- Add a unique class to the target detail-grid.
- Constrain the grid to `width` and `max-width` of 100 percent with local horizontal overflow.
- Set a suitable minimum row width and prevent header/cell wrapping.
- Assign explicit widths to every visible column in a dense grid.
- Reserve larger fixed widths for `number` and `money` columns when formatted values are clipped.
- Center rendered numeric controls with `display: flex` and `justifyContent: center` when requested.
- Remove any superseded `textAlign` configuration.
- Clean up injected style elements in `onDestroy`.
- Test the grid class, widths, flex alignment, CSS scope, and cleanup behavior.
- Run the target form test and the full project suite when a shared helper changes.

## Related Files And Patterns

- `BERCA/lib_utils.js`: shared scoped detail-grid scroll style helper.
- `BERCA/workshopSalesForm.js`: lookup, quantity, and money sizing plus flex centering.
- `BERCA/boSourcingListForm.js`: explicit widths for a dense readonly grid.
- `BERCA/boMaintainForm.js`: local scrolling for a very wide detail grid.
- `detail-grid-table-header-layout-problem.md`: header overlap and print table layout.
- `detail-grid-column-style-problem.md`: declarative column colors and other static styles.
