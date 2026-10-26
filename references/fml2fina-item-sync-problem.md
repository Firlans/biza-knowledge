# FML2FINA Item Sync Problem

Use this reference when a Biz-A form saves or updates FINA Item data through `TFinaMethod/fml2fina`, especially when detail-grid rows are editable after being loaded from FINA.

## Problem Signal

- `fml2fina` receives an FML XML string, but the generated edit XML only contains audit fields such as `USERGUID` and `FML_GUID`.
- A changed FINA field, for example `PreveredVendor`, `Weight`, `UnitPrice`, or `ItemDescription`, is not emitted in the edit FML.
- The edit payload uses item number as `ITEM ID` instead of the FINA item GUID.
- Insert and edit payloads are shaped the same even though FML expects different attribute names.
- A detail row was pulled from FINA, edited in the grid, then save cannot compare old value versus new value.
- `Tambah Item FINA` fills item fields but consumable `supplier` is empty because `ITEM.PREFEREDVENDOR` was not selected.
- A FINA row has `categoryid: null`, but save does not update item category because the old snapshot fell back to the current form category.
- Category-specific required fields behave incorrectly: `agency_id` should be required only for `PART`, while `supplier` should be required only for `CONSUMABLE`.

## Root Cause

FINA edit FML is diff-based. The form must keep the original FINA values from the first load or the first `Tambah Item FINA` pull. If the old snapshot is rebuilt from the already-edited detail row, old and new values become equal and the changed XML node is skipped.

For Item edit, `ITEM ID` must come from `ITEM.GUID`, not from `ITEM.ITEMNO`. The item number belongs in the `ItemNo` field only when the number changes or when inserting a new item.

Single-item lookup and batch item lookup must select the same FINA fields that save needs to diff later. Missing `ITEM.PREFEREDVENDOR`, `ITEM.ITEMTYPE`, or `ITEM.categoryid` means the grid row cannot preserve a complete old snapshot.

Do not use `row.categoryid ?? formCategoryId` when capturing FINA old values. A FINA value of `null` is meaningful: it must become the old value (`0` after numeric normalization) so saving can emit a category update to the selected form category.

## Corrected Approach

- Query FINA item data with `ITEM.GUID` and map it to a stable row key such as `item_guid`.
- For item lookup queries, select `ITEM.PREFEREDVENDOR`, `ITEM.ITEMTYPE`, and `ITEM.categoryid` in addition to item number, description, unit, price, weight, suspended, and GUID.
- Store the first FINA snapshot in the detail row itself, using a key such as `old_data`.
- When creating an edit payload, read old values from `row.old_data` first. Do not rebuild old values from current grid fields.
- When a FINA row explicitly has `categoryid: null`, preserve that old value as `0`; only fall back to the form category if the FINA row does not contain a `categoryid` property at all.
- Build old snapshots from old row fields (`old_categoryid`, `old_preferedvendor`, etc.), not from current row fields.
- Keep compatibility aliases like `old_master` only as fallback if older code already used them.
- Generate the actual FML XML string before posting to `fml2fina`; do not pass the old `json2fina` object shape.
- Include `USERGUID` and `FML_GUID` inside each `ITEM` transaction.
- In the grid/form validation, keep category-specific requirements explicit: agency for `PART`/`PARTS`, supplier for `CONSUMABLE`.

## FML Format

Insert fields use `Value`.

```xml
<ITEM ID="{NEW-GUID}" TransactionType="ACITM" Status="Insert">
  <ItemNo Value="PART-001" />
  <ItemDescription Value="Sample" />
  <UnitPrice Value="1000" />
  <USERGUID Value="{USER-GUID}" />
  <FML_GUID Value="{FML-GUID}" />
</ITEM>
```

Edit fields use `OldValue` and `NewValue`.

```xml
<ITEM ID="{ITEM-GUID}" TransactionType="ACITM" Status="Edit">
  <PreferedVendor OldValue="10" NewValue="20" />
  <CategorId OldValue="0" NewValue="7" />
  <USERGUID Value="{USER-GUID}" />
  <FML_GUID Value="{FML-GUID}" />
</ITEM>
```

## Implementation Checklist

- In `lib_qry`, select `ITEM.GUID` as `item_guid` for both single-item lookup and batch item lookup.
- In single-item and batch FINA item queries, include `ITEM.PREFEREDVENDOR`, `ITEM.ITEMTYPE`, and `ITEM.categoryid`; otherwise supplier/category diffs cannot be preserved.
- In the detail-grid columns, include hidden metadata keys needed for save, for example `item_guid`, `from_fina`, `before_edit`, and `old_data`.
- When appending a row from FINA lookup, assign both current display fields and `old_data`.
- When merging loaded Biz-A detail rows with FINA data, assign `old_data` from the FINA values at that moment.
- Use property-existence checks for `categoryid` before fallback, so an explicit FINA `null` is preserved as old value `0`.
- When save succeeds, mark the row as FINA-backed and refresh `old_data` to the saved values, so a retry or later edit compares against the latest known FINA state.
- Build insert FML from current values with `Value`.
- Build edit FML by comparing `old_data` to current values and only emit changed fields with `OldValue` and `NewValue`.
- For category sync in `BERCA/itemForm.js`, the expected field name is `CategorId`.
- Throw a clear error if `from_fina=true` but `item_guid` is missing.
- Throw a clear error if `USERGUID` cannot be loaded.
- Validate `fml2fina` response errors from `res.result?.[0]?.error`, `res.error`, or `res.message` before saving Biz-A records.

## Related Files And Patterns

- Example module: `BERCA/itemForm.js`.
- Query helper pattern: `BERCA/lib_qry.js`.
- General form save flow: `.agents/references/form-rules.md`.
