# Excel Import Template Dropdowns

Use this reference when a Biz-A Excel import template needs dropdowns backed
by allowed values or a master-data lookup.

## Implementation

- In the form handler, load the current master values before generating the
  template. Reuse the same allowed labels as the import parser so a dropdown
  choice remains valid when the file is uploaded.
- With the existing ExcelJS loader, create the input worksheet and a hidden
  options worksheet. Put each option in a separate cell and give each source
  range a workbook-level name. Set an Excel list validation on the matching
  input range below the header, referring to that name. Cell-backed options
  can contain commas.
- Build input columns for codes with text formatting where leading zeros are
  significant. Keep the input worksheet first for import paths that fall back
  to the first worksheet.
- Keep validation in the importer so files edited by other tools and older
  templates are checked on upload.

## Verification

Inspect the serialized workbook. Check the validation type, formula names,
range limits, and hidden options worksheet in the XLSX XML. Open the workbook
normally in Microsoft Excel and verify the dropdown at the beginning and end
of each configured range. Fill and save a copy, then run it through the actual
import parser and verify that a code such as `001` survives.

The Spiritia COA template was verified locally using that sequence. Its form
loads currency names from FINA at download time. The workbook uses the same
account-type labels as the parser and keeps the generated source values on a
hidden sheet.
[Template generator](../../Spiritia/Trunk/lib_utility.js)
[Import form](../../Spiritia/Trunk/importMasterForm.js)
[Import parser](../../Spiritia/Trunk/lib_dataProcessing.js)

If Microsoft Excel asks to repair the downloaded file, inspect the workbook
metadata using the [OOXML recovery reference](excel-export-ooxml-recovery-problem.md).
