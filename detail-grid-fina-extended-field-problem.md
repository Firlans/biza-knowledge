# Detail Grid FINA Extended Field Problem

Use this reference when adding, loading, saving, or debugging a Biz-A `detail-grid` field backed by FINA `EXTENDED.CUSTOMFIELD*` data.

## Problem Signal

- A new detail-grid column appears in the form but is empty when editing an existing FINA document.
- A field saves visually in Biz-A but does not round-trip from FINA on reload.
- A FINA amount displays at the wrong scale, for example `22` displays as `22.00` when the business value should be `0.22`.
- A display-only field accidentally affects row `amount`, `subtotal`, `ppn`, `totalorder`, custom print output, or `onCalc`.

## Root Cause

FINA extended fields are not automatically available just because a grid column exists. The field must be wired through every relevant boundary:

- detail-grid column configuration
- FINA query columns in `lib_qry` or the local query helper
- load mapping from FINA rows into the grid detail model
- save payload using `extended.customfieldN`
- calculation/watchers only when the field is supposed to affect totals
- print templates only when the user asks for it

Wrong assumptions usually happen when a field is inferred from a similar FINA column, for example treating an off-discount display value as part of `ITEMDISCPC` instead of its real `CUSTOMFIELD7` source.

## Corrected Approach

Trace the field from the real FINA source first. If the source is `CUSTOMFIELD7`, query it as an explicit key and save it back to the matching extended payload field.

```javascript
// lib_qry.js
{ data: 'ARINV.ARINVOICEID.USEDINSIID.ARINVDET.EXTENDEDID.EXTENDEDID.EXTENDED.CUSTOMFIELD7', key: 'disoff' }
```

```javascript
// form save payload
'extended.customfield7': dt.disoff || 0,
```

Keep display-only fields out of `watchKey`, `gridListener`, row amount formulas, header totals, and print HTML unless the requirement says otherwise.

## Implementation Checklist

- Add the grid column with a lowercase key and the correct type.
- Add FINA query columns for every load path that can populate the form, such as DO load and SI edit load.
- Map the query key into the detail row model in one named helper when possible.
- Save the value with the matching `extended.customfieldN` key.
- Confirm whether the field should affect calculations. If not, do not add it to `onCalc.watchKey` or `gridListener()`.
- Confirm whether the field should affect custom print. If not, leave print HTML unchanged.
- Normalize loaded numeric values if FINA returns a stored/scaled representation different from the form field expectation.

## Related Patterns

- `.github/instructions/references/form-rules.md`
- `.github/instructions/references/detail-grid-oncalc-event-loop-problem.md`
- `.github/instructions/references/detail-grid-state-sync-problem.md`
