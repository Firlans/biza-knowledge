# Biz-A Reference Index

Gunakan tabel di bawah untuk menentukan reference file mana yang harus di-load
berdasarkan task, error, UI pattern, atau module behavior yang sedang dikerjakan.
Scan kolom **Trigger keywords / signals**, lalu load file di kolom **Reference file**
yang paling cocok. Load hanya yang relevan agar context tetap efisien.

| Trigger keywords / signals | Reference file |
|---|---|
| Tidak ada reference yang match | Cari contoh lokal di repo dulu, baru sumber eksternal. |
| opening record lists, history rows, selectable grids, previously created records from a form | `dialog-list-problem.md` |
| changing scalar form field into one-to-many child rows, moving header value into existing detail rows (`QUOTATIONDET`), selectable related records (`spr_number`), Firebird child-row generator failures, reopen approval buttons, custom privileges (`skip approval reopen`, `approve reopen`, `reject reopen`) | `form-child-row-lookup-approval-problem.md` |
| recent user input disappears after dialog, step change, lookup selection, repeat update, detail-grid refresh, model replacement, `form.value` newer than `model`, spread order | `form-model-value-sync-problem.md` |
| detail-grid header overlap, clipped headers, misaligned headers, generated item print table columns | `detail-grid-table-header-layout-problem.md` |
| detail-grid horizontal scroll, table outside frame, nowrap columns, clipped number or money values, column width in rem, centering rendered cells with `justifyContent` instead of `textAlign` | `detail-grid-scroll-sizing-alignment-problem.md` |
| detail-grid background color, text color, column-level visual styling, `backgroundColor`, `rowStyleFn`, style like `contractForm.js` | `detail-grid-column-style-problem.md` |
| detail-grid column expressions, avoiding hardcoded `props.columns[index]`, moving detail-grid columns, dynamic labels/required rules by `key` or `className`, markers such as `hide-consumable` | `detail-grid-dynamic-column-expression-problem.md` |
| detail-grid rows remain visible after model/form data changed, custom detail delete buttons, stale `gridItems`, `assignData`, `dataSubject`, multiple conditional grids with same `detailKey` | `detail-grid-state-sync-problem.md` |
| hiding or manually controlling Biz-A form detail-grid Add/Delete button, `props.addBtn`, `props.deleteBtn`, custom `Action` column buttons, mode-specific row action visibility | `detail-grid-manual-action-buttons-problem.md` |
| detail-grid Enter key behavior, keyboard cell navigation, FINA-like data entry, focusing next column/row, adding new detail row only from last row | `detail-grid-enter-navigation-problem.md` |
| `Maximum call stack size exceeded`, repeated `onCalc` firing, auto-calculated detail-grid totals, detail-grid handler writing to a watched control | `detail-grid-oncalc-event-loop-problem.md` |
| custom table columns, user-selected table columns, `visible_column`, column metadata with `key` / `value` / `label` / `type`, print table custom columns, formatting custom money columns | `table-custom-column-flexible-rules.md` |
| dynamically adding/removing fields inside Formly `repeat`, `selection-list` controlled repeat columns, custom-column fields in repeat rows, stale/duplicated repeat fields, listener looping after repeat `fieldGroup` changes | `repeat-fieldgroup-manipulation-problem.md` |
| adding or debugging FINA-backed `detail-grid` field, `EXTENDED.CUSTOMFIELD*`, `extended.customfield*`, form-only grid columns, fields that must load/save but not affect totals, FINA loaded amount scale mismatches | `detail-grid-fina-extended-field-problem.md` |
| FINA document detail rows duplicated/eliminated because of item group metadata (`groupno`, `group_quantity`, `detail_extended_guid`) | `fina-detail-group-row-dedupe-problem.md` |
| Workshop Sales after Confirm to PSO, `supply_qty`, `bo_qty`, `do_qty`, allocation `done`/`onprogress` rows, saved BO values changing when edit/load displays confirmed record | `workshop-sales-confirmed-bo-load-problem.md` |
| overlapping, clipped, or crowded buttons in Biz-A list `Action` column | `list-action-button-wrap-problem.md` |
| enabling, disabling, hiding, or changing Biz-A list row action per row, button config properties ignored, `tbody`, `tr:nth-child`, rendered action-cell selectors | `list-row-action-dom-state-problem.md` |
| adding a field beside a Biz-A/Formly list table, inline input next to `body > app-root > app-list > div > table`, table wrapper flex, keeping list body siblings in their original position, built-in `fields` component on a list | `formly-list-inline-field-table-problem.md` |
| file attachments, PDF/image BLOB columns, `input-file`, `updateImg`, `btoa`, attachment `queryData` errors, `n.map is not a function`, `Bad control character in string literal` while loading attachment | `attachment-blob-querydata-problem.md` |
| `token unknown` from `queryData`, long relation paths, collect/search filters across many tables, BO Maintain collect by `doc_no`/customer | `biz-a-query-join-depth-problem.md` |
| JV-backed FINA approved forms/lists, Other Payment/Other Receipt approved flows, `JV.ID` vs `JV.JVID`, `jvid_fina`, Firebird error `Column unknown JV.ID` | `fina-biza-jv-key-mismatch-problem.md` |
| saving edited local Biz-A `JVDET` rows, preserving `JVDET.ID`, avoiding delete-all/recreate-all detail saves, deleting only detail IDs removed during edit, Other Payment/Other Receipt header rows with `SEQ = 0`, `header_jvdet_id` | `jvdet-incremental-save-problem.md` |
| Bank Book rows opening source forms, `openSourceForm`, `buildSourceFormQueryParams`, `mode=from_bankbook`, inconsistent readonly/back behavior after navigating from Bank Book, target forms using `applyFromBankBookMode` | `bankbook-source-navigation-mode-problem.md` |
| Bank Book Biz-A rows, filtering approved/unapproved rows, Vendor Payment approved rows still appearing, `chequeid_fina`, `isfinasend`, `jvid_fina`, `APPROVED_BY_CTRL_PUSAT` | `bankbook-biza-approved-filter-problem.md` |
| `previewTemplateFina`, selectable or persisted FINA print templates, `templateid`, `TEMPLATE.TEMPLATETYPE`, named template filters, saved template resets to first option, Biz-A Print/Close preview, direct browser print, jsPDF Letter/Half Letter, landscape paper, fit to paper, hidden print iframe | `fina-template-print-selection-problem.md` |
| saving or updating FINA Item through `fml2fina`, FML XML, `ITEM.GUID`, `USERGUID`, `FML_GUID`, `PreferedVendor`, `PREFEREDVENDOR`, `categoryid`, `CategorId`, old/new value diffs from detail-grid data | `fml2fina-item-sync-problem.md` |
| FINA-backed document running numbers, SO number previews, `GETSONUMBER`, `SAVECTLNUMBER`, masked numbers like `SO-0121/____`, keeping Biz-A and FINA SO numbers synchronized | `fina-biza-running-number-sync-problem.md` |
| repeated Biz-A patterns, extracting reusable helpers, moving query/data access out of form/list files, normalizing mode/navigation/button logic, reusing utilities | `biz-a-normalize-pattern-rules.md` |
| converting master lookup table from business-code `ID` to integer `ID` plus `CODE`, separating stored foreign keys from displayed/searchable codes, branch-like lookups where `branch_id` becomes numeric while document numbers still need old code | `lookup-code-id-split-problem.md` |
| renaming database column already used by another table, foreign key, primary key, trigger, queryData path, list action column, save payload, Firebird dependency errors (`Column <field> from table <table> is referenced in <trigger>`), system-table verification queries after rename | `rename-used-column-rules.md` |
| creating or changing Biz-A database tables, Firebird DDL, migrations, generators, triggers, primary keys | `database-standard-rules.md` |
| renaming Firebird generators/sequences, standardizing generator names to `<TABLE>_GEN`, `GEN_ID`, `NEXT VALUE FOR`, `RDB$DEPENDENCIES`, `RDB$GENERATORS`, Firebird error `cannot delete GENERATOR ... there are dependencies` | `firebird-generator-rename-problem.md` |
| `cli-script/` files, watcher scripts, callback scripts, converting standalone Node scripts to Biz-A CLI format, `onInit(data, socket)`, packages used only by CLI scripts (`basic-ftp`) | `cli-script-standard-problem.md` |
| Biz-A CLI FTP watcher, FTP CSV files, saving pulled file names, scheduler `data.arguments` API config, `totalSaved: 0`, `Missing API config: url/dbindex`, Firebird date conversion errors from ISO strings, logging CSV rows as JSON, reducing large logs to error plus summary logs | `cli-script-ftp-data-sync-problem.md` |
