# Workshop Sales Confirmed BO Load Problem

Use this reference when a Workshop Sales form, PSO confirmation flow, or allocation-driven detail load shows saved `bo_qty` changing after edit/load, especially when the database value is correct but the form displays a lower BO value.

## Problem Signal

- After Confirm to PSO, edit/load shows different quantity values than the database.
- Typical confirmed row:
  - `order_qty`: 100
  - `supply_qty`: 30
  - saved `bo_qty`: 70
  - `do_qty`: 30
- The form displays `bo_qty` as 40 because load normalization recalculates BO from `order_qty - (supply_qty + do_qty)`.
- The issue may appear after applying allocation rows with status `done`, because `do_qty` is intentionally set from done allocation or copied from supply during confirm.

## Root Cause

Generic detail calculation helpers such as `calculateDetailRow()` are useful while editing draft/open rows, but they are unsafe as the last normalization step for confirmed Workshop Sales rows. Once a row is confirmed, `do_qty` represents delivery quantity and `bo_qty` is already persisted as the remaining back order. Recalculating BO from both supply and DO double-counts the delivered quantity.

Avoid this pattern during confirmed load:

```javascript
const normalizedDetails = details.map((detail, index) => this.f().calculateDetailRow({
    ...detail,
    seq: detail.seq || index + 1,
}));
```

## Corrected Approach

Use a load-specific normalizer that preserves saved `bo_qty` when the master status is confirmed:

```javascript
normalizeLoadedDetailRow: function (detail, index, status) {
    const calculated = this.f().calculateDetailRow({
        ...(detail || {}),
        seq: detail?.seq || index + 1,
    });

    if (this.f().isConfirmedWorkshopSalesStatus(status)
        && detail?.bo_qty !== null
        && detail?.bo_qty !== undefined) {
        return {
            ...calculated,
            bo_qty: this.f().num(detail.bo_qty),
        };
    }

    return calculated;
},
```

Then pass the master status from `loadData`:

```javascript
const normalizedDetails = (details || []).map((detail, index) => {
    return this.f().normalizeLoadedDetailRow(detail, index, master.status);
});
```

Keep draft/open behavior unchanged. Non-confirmed rows can still use calculated BO so stock, supply, and allocation changes remain reactive.

## Implementation Checklist

- Trace the load flow after raw database rows are mapped, not only allocation helpers.
- Check for every later `calculateDetailRow()` call that can overwrite saved `bo_qty`.
- Preserve database `bo_qty` only for confirmed Workshop Sales rows, not for all statuses.
- Keep allocation status handling separate:
  - `onprogress` allocation may drive `supply_qty`
  - `done` allocation may drive `do_qty`
  - confirmed saved `bo_qty` must remain authoritative when present
- Remove `debugger` statements before finishing.
- Move direct `queryData` helpers from forms into `lib_qry`.
- Move generic non-database helpers such as numeric or HTML escaping helpers into `lib_utils`.
- Delete dead functions only after caller count confirms they are not lifecycle/config callbacks or public helper surface.

## Related Files And Patterns

- `BERCA/workshopSalesForm.js`
- `BERCA/lib_qry.js` for query helpers
- `BERCA/lib_utils.js` for reusable non-query helpers
- `.github/instructions/references/biz-a-normalize-pattern-rules.md`
- `.github/instructions/references/detail-grid-oncalc-event-loop-problem.md`
