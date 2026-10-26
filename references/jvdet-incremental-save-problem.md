# JVDET Incremental Save Problem

Use this reference when a Biz-A JV-backed form edits local `JVDET` rows and the requirement is to update existing detail rows instead of deleting all rows and recreating them. This commonly applies to Other Payment, Other Receipt, and Journal Voucher forms that save the local Biz-A `JV` / `JVDET` tables.

## Problem Signal

- Saving an edited JV-backed form calls `deleteModelNonId('JVDET', 'JV_ID', jvid, ...)` before inserting all current rows again.
- Edited detail rows lose their original `JVDET.ID`.
- New detail rows are not clearly marked as new in the payload.
- A detail-grid load maps `id` from `seq`, so the save flow cannot distinguish existing rows from new rows.
- The first local `JVDET` row (`SEQ = 0`) is used as the bank/cash header row and is not rendered in the detail grid, so the save payload sends `id: null` for `seq: 0` during edit.
- A user asks to delete only rows removed during editing.

## Root Cause

`JVDET` has its own primary key (`ID`) and a parent foreign key (`JV_ID`). When the form rebuilds details by deleting every `JVDET` row for a parent `JV_ID`, it destroys stable detail IDs and makes edit tracking impossible.

Another common mistake is loading the grid row `id` from `JVDET.SEQ`. `SEQ` is only the line number. It is not the primary key and must not be used as the update identifier.

In Other Payment and Other Receipt, the row with `JVDET.SEQ = 0` represents the header bank/cash account. That row is sliced out before assigning detail-grid rows (`dt.slice(1)`), so its `JVDET.ID` will not survive through the grid row `id`. If the load flow does not copy `dt[0].id` into model state, `masterDataBiza()` sends the header row back with `id: null`, and Firebird may insert a duplicate `(JV_ID, SEQ = 0)` row instead of updating the existing row.

## Corrected Approach

Load the local Biz-A `JVDET.ID` into the detail-grid row and send that same `id` back in the `jvdet` payload. For new rows, send `id: null` explicitly.

```javascript
columns: [
    { data: 'JV.id.jv_id.JVDET.id', key: 'id' },
    { data: 'JV.id.jv_id.JVDET.seq', key: 'seq' },
]
```

```javascript
const rows = model.other_paymentdet.map((row, index) => ({
    id: row.id ?? null,
    seq: index + 1,
    glaccount: row.glaccount,
    jv_id: jvid,
}));
```

For Other Payment and Other Receipt header rows, preserve the `SEQ = 0` row ID separately during edit load:

```javascript
this.model.header_jvdet_id = dt[0].id;
```

Then send it when building the unshifted header `jvdet` row:

```javascript
json.jvdet.unshift({
    id: model.header_jvdet_id ?? null,
    seq: 0,
    glaccount: model.glaccount,
});
```

Before saving details, query existing local `JVDET` rows by `JV_ID`, compare existing IDs with current payload IDs, and delete only IDs that are no longer present. Then call `sendModel` for every current row so rows with an `id` update and rows with `id: null` insert.

## Implementation Checklist

1. Identify the database boundary. This rule is for local Biz-A `JVDET`, not FINA `JVDET`.
2. Add `JVDET.ID` to the local load query and map grid row `id` from that field.
3. Preserve `seq` separately from `id`; never use `seq` as the primary key.
4. If the form slices the header row out of the grid, preserve `dt[0].id` in model state before `grid.assignData({ data })`.
5. Build every `jvdet` payload row with an explicit `id`:
   - existing row: loaded `JVDET.ID`
   - Other Payment/Receipt header row (`seq: 0`): `model.header_jvdet_id`
   - new row: `null`
6. Query existing rows with `JVDET.JV_ID = jvid` and columns `JVDET.ID`, `JVDET.SEQ`.
7. Delete only existing IDs missing from the current payload.
8. Save current rows sequentially with `sendModel(row, this.config.api, 'JVDET')`.
9. Keep the save flow as one RxJS chain with one final subscription.

## What To Avoid

- Do not delete every `JVDET` row for a `JV_ID` during normal edit save.
- Do not use `id: true`, empty strings, or other sentinels for new rows; use `id: null`.
- Do not map grid `id` from `JVDET.SEQ`.
- Do not compare deleted rows by `seq`; compare by `JVDET.ID`.
- Do not assume the header `SEQ = 0` row is covered by detail-grid row mapping; preserve its ID separately when the grid only receives rows from `dt.slice(1)`.
- Do not apply this rule blindly to FINA database paths. For FINA key boundaries, load `fina-biza-jv-key-mismatch-problem.md`.

## Related Files And Patterns

- `APL/otherPaymentForm.js`
- `APL/otherReceiptForm.js`
- `APL/journalVoucherForm.js`
- `.agents/references/fina-biza-jv-key-mismatch-problem.md`
- `.agents/references/detail-grid-state-sync-problem.md`
- `.agents/references/rename-used-column-rules.md`
