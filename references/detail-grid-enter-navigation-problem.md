# Detail Grid Enter Navigation Problem

Use this reference when a Biz-A form `detail-grid` must navigate cells or add rows with Enter, especially when the user asks for FINA-like entry behavior.

## Problem Signal

- Pressing Enter in a detail row should move to the next editable column.
- Pressing Enter on the last editable column should move to the first editable column in the next row.
- Pressing Enter on the last editable column of the last row should add a new row.
- A user reports that with multiple detail rows, Enter from row index 1 does not move to row index 2.
- Existing `editOnEnter: true` is present but does not fully match the desired FINA keyboard workflow.

## Root Cause

Biz-A `detail-grid` can enter edit mode with `editOnEnter`, but that flag does not define the whole row and column navigation policy.

Custom keyboard handlers often check only for "no next column" and then add a new row. That is wrong when the active row is not the last row. The handler must first check whether a next row exists and move there before calling `grid.newRow`.

Another common cause is relying on visible column indexes. Detail-grid columns often include hidden metadata columns, duplicate lookup columns, or action columns. Index-based navigation breaks when the column list changes.

## Corrected Approach

Create a small navigation column map for editable cells, keyed by business column names and rendered `mat-cell` classes. Drive Enter from the active DOM cell to a `{ row, colKey }` position.

The Enter decision order must be:

1. If the current row has a next editable column, focus it.
2. If the current row has no next editable column but another row exists, focus the first editable column in the next row.
3. If the current row is the last row, add a new row and focus the first editable column in that new row.

Keep row creation in one helper such as `getEmpty...DetailRow()` so the new row shape is explicit.

## Implementation Checklist

- Define `getDetailGridNavigationColumns()` with only the editable columns that should participate in Enter navigation.
- Resolve the active cell from `document.activeElement.closest('mat-cell')` first, then fall back to `mat-cell.focus`.
- Convert the active cell to `{ row, colKey }` by querying all cells with the matched column class.
- Move horizontally inside the same row before considering row changes.
- Add a helper like `getNextDetailGridRowFirstColumnPosition(position)` and call it before `grid.newRow`.
- Only call `grid.newRow({ data: ... })` when the active position is on the last row.
- Register the keydown handler after the grid instance is available, commonly in `beforeLoadData`.
- Remove any previous keydown handler before adding a new one to avoid duplicate events after reinitialization.
- Do not use `props.columns[index]` as the navigation source; hidden and moved columns make indexes brittle.

## Related Files And Patterns

- `.agents/references/patterns.md` Section 10: Detail Grid Pattern.
- `.agents/references/detail-grid-dynamic-column-expression-problem.md` for avoiding brittle column indexes.
- `.agents/references/detail-grid-state-sync-problem.md` for stale rendered grid rows after row add/delete.
