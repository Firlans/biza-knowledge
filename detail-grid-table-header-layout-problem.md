# Detail Grid Table Header Layout Problem

Use this reference when a Biz-A form detail-grid or generated print HTML has item table headers that overlap, truncate badly, or no longer align with body columns after adding several item/quantity/price columns.

## Problem Signal

- User says the item table header is overlapping, stacked badly, or "tumpang tindih".
- A `detail-grid` has many visible columns but only one or two columns define `style.flex`.
- Print HTML uses `table-layout: fixed` while header cells also use `white-space: nowrap`.
- Quantity or price labels such as `Order Qty`, `Supply Qty`, `Unit Price`, or `Ext Price` are squeezed into narrow columns.

## Root Cause

Biz-A detail-grid columns share remaining width when most columns do not define an explicit flex basis. Long labels then compete with lookup and description columns, so the header can overlap even when the row data still looks acceptable.

Generated print tables have a similar failure mode: fixed table layout plus `white-space: nowrap` forces long headers to overflow their assigned column instead of wrapping inside it.

## Correct Pattern

Keep layout fixes declarative and local to the table configuration.

For form `detail-grid` columns:

- Add explicit `style: { flex: '0 0 N%' }` on all visible columns in dense item grids.
- Give lookup/description columns enough width first, then reserve smaller fixed widths for quantity columns.
- Keep the total near 100 percent for predictable alignment.
- Do not change detail payload keys, lookup config, or calculation logic when the issue is only header layout.

For generated print HTML:

- Keep `table-layout: fixed` when stable column alignment is needed.
- Let header cells wrap with `white-space: normal`.
- Add `overflow-wrap: anywhere` and a tighter `line-height` for dense dot-matrix style tables.
- Keep body cell alignment classes (`text-center`, `text-right`) unchanged unless the user asked for visual alignment changes.

## Implementation Checklist

- Identify whether the issue is the on-screen `detail-grid`, generated print HTML, or both.
- Search the target file for `type: 'detail-grid'`, `.item-table`, and any print-specific table class such as `.pso-item-table`.
- Add or adjust column width styles on visible grid columns only.
- For print CSS, replace header `white-space: nowrap` with wrapping header rules.
- Preserve business behavior: no changes to save payloads, calculations, lookups, listeners, or FINA calls.
- Avoid broad CSS selectors that affect unrelated tables in the same generated HTML.

## Related Files And Patterns

- `.github/instructions/references/form-rules.md`
- `.github/instructions/references/refactor-checklist.md`
- `.github/instructions/references/detail-grid-scroll-sizing-alignment-problem.md` for local horizontal scrolling, content-based widths, and flex alignment.
- `BERCA/workshopSalesForm.js` shows the corrected pattern for a dense workshop sales item grid and Picklist/PSO print table headers.
