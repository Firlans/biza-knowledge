# FINA Detail Group Row Dedupe Problem

Use this reference when a FINA-backed form loads document detail rows and the query returns duplicated rows because item group metadata such as `groupno` or `group_quantity` is joined into the detail result.

## Problem Signal

- A saved DO, SI, SO, or other FINA document opens with an empty `detail-grid` even though FINA has detail rows.
- Filtering by `groupno` removes every row when all returned rows have a `groupno`.
- The query result contains repeated rows with the same real detail identity, for example the same `detail_extended_guid`, `ARINVDET` row, `seq`, and `itemno`, but different group labels.
- The expected UI should show one saved document detail per real FINA detail row, not every group metadata row.

## Root Cause

FINA detail queries can multiply one document detail row when the query joins item group or package metadata. A filter like this is unsafe:

```javascript
const groupno = rows.filter(row => !row.groupno).map(row => row.itemno)
const detail = rows.filter(row => groupno.includes(row.groupno) || !row.groupno)
```

That pattern assumes every group child has a non-group parent row in the same result. When the source result only has group rows, `groupno` becomes empty and all detail rows are eliminated.

## Corrected Approach

Normalize the loaded FINA rows before mapping them to grid details:

1. Identify the stable detail key. Prefer `detail_extended_guid`; otherwise use the FINA detail id; only fall back to a composite such as `seq-itemno` if there is no better key.
2. Keep one row per stable detail key.
3. If both a grouped and non-grouped version exist, prefer the non-grouped row.
4. Remove query-only group metadata from saved FINA detail rows before assigning the edit/view grid, unless the business flow truly needs to edit group children.
5. Sort after normalization by numeric `seq`.
6. Map normalized rows through the existing `build...DetailFrom...Row` helper.

Short pattern:

```javascript
normalizeDocumentDetailRows: function (rows) {
    const sourceRows = Array.isArray(rows) ? rows : []
    const rowsByDetailKey = sourceRows.reduce((acc, row) => {
        const detailKey = row.detail_extended_guid || row.id_detail || `${row.seq}-${row.itemno}`
        const existingRow = acc.get(detailKey)

        if (!existingRow || (existingRow.groupno && !row.groupno)) {
            const normalizedRow = { ...row }
            delete normalizedRow.groupno
            delete normalizedRow.group_quantity
            acc.set(detailKey, normalizedRow)
        }

        return acc
    }, new Map())

    return Array.from(rowsByDetailKey.values())
        .sort((a, b) => Number(a.seq) - Number(b.seq))
}
```

## Implementation Checklist

- [ ] Inspect the actual FINA query result before changing filters.
- [ ] Check whether duplicates share `detail_extended_guid`, detail id, or another stable detail key.
- [ ] Add a named normalization helper, such as `normalizeDODetailRows` or `normalizeDocumentDetailRows`.
- [ ] Call the helper in the edit/view load path before `build...DetailFrom...Row`.
- [ ] Do not use `filter(index => Boolean(index))` for detail row indexes, because index `0` is valid and would be dropped.
- [ ] Do not preserve `groupno` on saved FINA detail rows unless the loaded grid intentionally supports group child editing.
- [ ] Keep SO/new-document group expansion separate from saved DO/SI edit load normalization.

## Related Files And Patterns

- `Endo Medika/DOForm.js`: `normalizeDODetailRows`, `existItem`, `buildDeliveryOrderDetailFromDORow`.
- `detail-grid-fina-extended-field-problem.md`: use this separately when the issue is a missing or scaled FINA extended field, not duplicated group metadata.
- `detail-grid-state-sync-problem.md`: use this separately when the grid UI still shows stale rows after data assignment.
