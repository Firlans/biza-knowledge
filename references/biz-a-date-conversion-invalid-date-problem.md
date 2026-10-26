# Biz-A DATE Conversion and Empty Detail Date Problem

## Problem signal

- A blank `type: 'date'` cell in a Biz-A detail-grid displays `Invalid Date`.
- Saving a form fails with `Database 2 muncul error: conversion error from string "2026-09-23 00:00:00:000"`.
- The corresponding database column is Firebird `DATE`, but the form or query supplied a date-time string or JavaScript `Date`.

## Root cause

The detail-grid date renderer may format an empty value into the literal `Invalid Date`. That text is a display artifact and must never be treated as a valid date. Biz-A `sendModel` does not guarantee conversion of all date-control and query values to a Firebird-compatible `DATE` value. A string with the time suffix `00:00:00:000` can reach the database unchanged.

## Corrected approach

1. Initialize empty detail date fields as `null` and validate only rows that will be saved.
2. Before `sendModel`, normalize every value targeting a `DATE` column to `YYYY-MM-DD`. Handle both header dates loaded by `queryData` and detail dates entered in the grid.
3. Reject missing or invalid dates before saving. Do not convert `Invalid Date` into a payload value.
4. If the grid still renders the literal `Invalid Date` for an empty cell, clear only that cell's displayed text or input value. Scope DOM handling to the module's grid and date column; disconnect observers/listeners on destroy. Do not remove the date picker or alter other columns.

## Verification

- Test a blank detail date: the cell appears empty, and a row with receipt qty cannot be saved without a valid date.
- Test payloads containing `2026-09-23 00:00:00:000`, a date control value, and `Invalid Date`: valid values become `2026-09-23`; invalid values are rejected.
- Inspect both header and detail payloads at the `sendModel` boundary. A fix limited to the detail date can leave the header date failing first.

## Related files

- `BERCA/poMaintainForm.js` (`normalizeDateForDb`, `patchEmptyInvoiceDates`, `buildPayload`)
- `BERCA/boMaintainForm.js` (existing date-grid display guard)
- `.agents/references/cli-script-ftp-data-sync-problem.md` (date-time serialization in CLI scripts)
