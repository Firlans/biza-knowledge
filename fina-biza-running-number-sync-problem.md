# FINA Biz-A Running Number Sync Problem

Use this reference when a Biz-A form must keep its document number aligned with a FINA control-number procedure, especially for Sales Order numbers such as `GETSONUMBER.sonumber` and `SAVECTLNUMBER`.

## Problem Signals

- New Biz-A SO shows only `_____` or a stale preview after `preparingData`.
- SO saves with the masked number instead of the real FINA number.
- FINA and Biz-A SO numbers drift because the FINA control number is not advanced after a successful Biz-A save.
- A new route passes `soid` as `"null"` or `"undefined"`, causing the form to treat the record as existing and skip number generation.
- The user asks to display a masked running segment such as `SO-0121/____` while saving the actual number such as `SO-0121/10024`.

## Root Cause

FINA control-number procedures are authoritative for the next SO number. Do not infer the final SO number from local Biz-A SO history when the business rule says to use FINA.

Two mistakes commonly cause desync:

- Treating preview generation and final number reservation as the same step.
- Checking `model.soid` with a truthy check, where `"null"` is truthy and blocks new-record number lookup.

## Corrected Pattern

For a new SO form:

1. In `preparingData`, call a helper such as `getCurrentSONumber`.
2. Query FINA with `queryData`, not raw SQL, when the source is simple:

```javascript
const param = {
    columns: [
        { data: 'GETSONUMBER.sonumber', key: 'sono' }
    ],
    dbIndex: this.config.api.finaDbIndex
}

return this.dataService.queryData(param, this.config.api, true, true)
```

3. Display a masked preview by replacing the final running-number digit group with `____`.

```javascript
buildSONumberPreview: function (soNumber) {
    const sourceNumber = String(soNumber || '')
    return sourceNumber.replace(/(\d+)(?!.*\d)/, '____')
}
```

4. Before saving a new SO, resolve the real number again from `GETSONUMBER`.
5. Save Biz-A master/detail with the real `sono`.
6. Only after save succeeds, advance FINA control number:

```sql
EXECUTE PROCEDURE SAVECTLNUMBER('<real-so-number>', 3)
```

## Implementation Checklist

- [ ] Use a helper like `hasInternalValue` that treats `null`, `undefined`, empty string, `"null"`, and `"undefined"` as empty.
- [ ] Only call `getCurrentSONumber` for new records without a real Biz-A `soid`.
- [ ] Parse both direct `queryData` arrays and wrapped responses such as `{ data: [...] }`.
- [ ] Accept common key casing: `sono`, `SONO`, `sonumber`, `SONUMBER`.
- [ ] Do not use local SO history (`SO.SONO` order by desc) for final FINA-backed SO numbers.
- [ ] Keep the masked preview out of saved payloads; resolve the real number before `sendModel`.
- [ ] Run `SAVECTLNUMBER` after all relevant Biz-A save operations succeed, not before.
- [ ] Escape single quotes before interpolating document numbers in raw procedure SQL.

## Related Files And Patterns

- `Endo Medika/SOForm.js` for `getCurrentSONumber`, `buildSONumberPreview`, `resolveSONumberBeforeSave`, and `saveSOControlNumber`.
- `.github/instructions/references/form-rules.md` for lifecycle placement: initial/reference data belongs in `preparingData`, save orchestration belongs in the save handler.
