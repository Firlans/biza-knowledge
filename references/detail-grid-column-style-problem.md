# Detail Grid Column Style Problem

## Problem Signal

- A Biz-A `detail-grid` needs a background color for a specific table or group of columns.
- The requested result is "like `contractForm.js`" or should follow an existing column-level visual pattern.
- The first implementation reaches for injected CSS, table DOM selectors, or `rowStyleFn`, but the desired behavior is column styling through grid configuration.

## Root Cause

Biz-A `detail-grid` columns already accept a `style` object. When the visual requirement is tied to the grid columns, styling should stay in `props.columns[].style` so it is declarative, testable, and consistent with modules such as `BERCA/contractForm.js`.

Injected CSS is still acceptable for cross-column layout fixes, such as header alignment, but it is a poor first choice for simple column background colors because it depends on generated DOM classes and can affect unrelated grids. `rowStyleFn` is useful for row-dependent styling, not for static column-level colors.

## Corrected Approach

Use `backgroundColor` and text `color` inside each target column's `style` object:

```javascript
{
    key: 'amount',
    label: 'Balance',
    readonly: true,
    type: 'money',
    style: {
        flex: '0 0 14%',
        textAlign: 'right',
        backgroundColor: '#f8d7da',
        color: '#842029',
    },
}
```

Prefer soft solid colors when the user asks for full opacity but "not too red". For example, use `#f8d7da` for a light red background and `#842029` for readable dark red text.

## What To Avoid

- Do not inject global CSS just to color a single `detail-grid`'s columns.
- Do not use generated Material table selectors as the primary styling hook for column backgrounds.
- Do not use `rowStyleFn` for static column styling; reserve it for row-dependent states such as odd/even rows or highlighted rows.
- Do not use transparent `rgba(...)` when the user explicitly asks for opacity `1`.

## Implementation Checklist

- Find the target `detail-grid` by `id`, `detailKey`, or surrounding caption.
- Apply `backgroundColor` and `color` to each visible `props.columns[]` entry that should be styled.
- Keep existing column settings such as `flex`, `textAlign`, `type`, `readonly`, `buttons`, and `onClick`.
- Leave unrelated grids unchanged.
- If CSS injection already exists for layout-only concerns, keep it narrowly scoped to that layout concern.

## Related Patterns

- `BERCA/contractForm.js`: column-level `style.backgroundColor` on `detail-grid` columns.
- `APL/bankBookForm.js`: Biz-A Bank Book grid uses column `style.backgroundColor` for a soft red background.
- `.agents/references/detail-grid-table-header-layout-problem.md`: use this only for header layout, clipping, or alignment problems.
