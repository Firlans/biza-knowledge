# Excel Export OOXML Recovery Problem

Use this reference for Biz-A `.xlsx` downloads that trigger Microsoft Excel
recovery, especially after adding header colors with SheetJS and ExcelJS.

## Problem Signal

- Excel reports `We found a problem with some content` or asks to recover a report.
- The download completes, the ZIP is readable, and automated tests still pass.
- A workbook is built with `this.XLSX`, loaded into ExcelJS for styling, and saved
  again with `workbook.xlsx.writeBuffer()`.
- Worksheet XML contains `<sheetFormatPr customHeight="1"/>` without
  `defaultRowHeight`.

Inspect the actual downloaded file first. Recovery has multiple possible causes;
do not apply this diagnosis to every damaged workbook without checking its XML
or Excel repair log.

## Root Cause

In the observed SheetJS-to-ExcelJS path, SheetJS omits `sheetFormatPr`. ExcelJS
4.4.0 imports the sheet with empty worksheet properties, losing its constructor
default of 15 for `defaultRowHeight`. Its writer then emits `sheetFormatPr` without
the required `defaultRowHeight` attribute. A readable ZIP and well-formed XML do
not establish a valid Excel workbook.

The earlier tests wrote the file and reopened it with ExcelJS. That reader also
accepts this incomplete metadata, so successful round trips through the same
library did not detect Microsoft Excel rejecting the output.

Standard SheetJS `cell.s` assignments also do not by themselves establish that
custom fills survived export. Check the saved file, rather than just the
in-memory worksheet or an HTML preview.

## Corrected Approach

Normalize missing or invalid default row height after ExcelJS loads the source
and before writing the final file. Apply it to each sheet in the shared report
helper, rather than separately in each report form.

For the CAR text reports, the implemented fallback is 15:

```javascript
workbook.eachSheet(sheet => {
    const defaultRowHeight = sheet.properties.defaultRowHeight
    if (!Number.isFinite(defaultRowHeight) || defaultRowHeight <= 0) {
        sheet.properties.defaultRowHeight = 15
    }
    // Apply the existing report header styles here.
})
```

Preserve existing positive default heights and explicit per-row heights. For a
different template with intentional zero-height behavior, inspect that design
before adopting the CAR fallback. Keep values, cell types, number formats,
column widths, merges, sheet names, and header colors intact.

Keep identifiers such as NPWP/KTP and customer codes as strings throughout the
query-to-export mapping. Numeric conversion can lose leading zeros or precision
in a 16-digit identifier. Null identifiers should stay blank, and print HTML
must escape their contents.

## Implementation Checklist

1. Read the relevant report form, its shared export helper, and an actual failing
   download. Inspect ZIP integrity, worksheet XML, and repair logs when available.
2. Confirm the malformed metadata before changing the writer. Record the failure
   in a regression check that fails before the fix.
3. Patch the shared helper after import and before final serialization. Do not
   overwrite valid source formatting or hide a failed export as success.
4. Inspect the final ZIP's `xl/worksheets/sheet*.xml`. Whenever `sheetFormatPr`
   exists, verify `defaultRowHeight` is present and appropriate for the report.
   XML parsing alone is insufficient to check required attributes.
5. Compare original and new cell values and types. Include leading-zero codes,
   punctuated NPWP, 16-digit KTP, null/missing identifiers, and formula-like text.
   Verify the new header fill, column widths, and any affected merges/formats.
6. For a reported Microsoft Excel recovery issue, verify normal opening in Excel
   when available. Use a separate instance, disable macros and link updates,
   open read only, close without saving, and quit only the created instance.
   Opening with repair enabled is not proof that the export is fixed. If native
   validation is unavailable, state that limitation explicitly.
7. Keep fixture databases, local test workbooks, native Excel results, and deployed
   Biz-A runtime results distinct. Passing repository checks does not mean the
   helper was uploaded to the application.
8. Upload the corrected helper, reload the report, and download again. Previously
   downloaded files retain their original incomplete metadata.

## Regression Check Example

Check the serialized file in addition to reopening it with ExcelJS:

```javascript
const bytes = await workbook.xlsx.writeBuffer()
const archive = await require('jszip').loadAsync(bytes)
const xml = await archive.file('xl/worksheets/sheet1.xml').async('string')
expect(xml).toMatch(/<sheetFormatPr\b[^>]*\bdefaultRowHeight="15"/)
```

This assertion targets the CAR default. Test explicit custom heights against
their own expected values, and inspect every affected sheet in multi-sheet
workbooks. Do not replace all workbook validation with this single assertion.

## Verified Local Example

In CAR #6309, the old download failed normal read-only opening in Microsoft
Excel. A workbook produced with the corrected helper opened normally, and all
report cell values matched the original. The regression run passed 23 suites /
364 tests. This was local verification, not a deployment or production-runtime
check.

## Related Files and Patterns

- `CAR/lib_report.js`: shared import, header styling, and download helper; start
  here for this export path.
- `CAR/reportCustomerForm.js`: NPWP/KTP string mapping and Excel columns.
- `CAR/test/reportCustomerForm.test.js`: saved XML and workbook-value regression
  checks.
- `CAR/task-6309.md`: implementation and installation record.
- `CAR/lib_html.js`: report header color and escaped print template.
- `pattern-index.md`: Print Pattern and Loading & Error Handling Pattern.
- [ExcelJS worksheet properties](https://github.com/exceljs/exceljs#worksheet-properties).
