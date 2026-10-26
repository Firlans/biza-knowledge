# Pattern Knowledge Base Index

Sumber kebenaran utama untuk semua module Biz-A Firlan style.

## Lokasi Pattern
2. `.agents/references/patterns.md`

## Urutan Referensi

| Prioritas | Sumber | Kapan dipakai |
|---|---|---|
| 1 | `patterns.md` | Selalu — standar baku |
| 2 | Target file + nearby files | Konteks project saat ini |
| 3 | Files di `useLibrary` | Shared functions yang sudah ada |
| 4 | `Proton` | Referensi lifecycle dan best practice |
| 5 | `Endo Medika` | Fallback referensi jika Proton tidak cukup |

> **Dilarang**: `APL` dan `BERCA` sebagai referensi — kecuali user secara eksplisit memintanya dan semua referensi di atas masih tidak cukup.

## Problem References

Load these before broad repo search when the task signal matches:

| Reference | Kapan dipakai |
|---|---|
| `excel-export-ooxml-recovery-problem.md` | Excel downloads request recovery, SheetJS/ExcelJS header styling loses required `defaultRowHeight`, or library round trips pass while native Excel rejects the file |
| `mobile-layout-rules.md` | Mobile layouts from prototypes, stacked header/filter fields, paired dates, master hub icon/description cards, blank mobile list cards, omitted native columns/actions, typed row IDs, and UI lifecycle cleanup |
| `dialog-list-problem.md` | Opening record lists, history rows, selectable grids, or previously created records from a form |
| `form-child-row-lookup-approval-problem.md` | Scalar form fields changed to one-to-many child rows, header values moved into existing detail rows such as `QUOTATIONDET`, selectable related records such as `spr_number`, child-row generator failures, or reopen approval controlled by custom privileges |
| `form-model-value-sync-problem.md` | Recent form input disappears after a dialog/action because `this.form.value` was not merged over stale `this.model` before model replacement |
| `detail-grid-table-header-layout-problem.md` | Overlapping, clipped, or misaligned headers in detail-grid or generated item print tables |
| `detail-grid-scroll-sizing-alignment-problem.md` | Horizontal detail-grid scroll containment, nowrap columns, content-aware widths, clipped number/money values, or flex centering with `justifyContent` |
| `detail-grid-dynamic-column-expression-problem.md` | Detail-grid column expressions, avoiding hardcoded `props.columns[index]`, moving columns, or dynamic labels/required rules by `key` / `className` |
| `detail-grid-state-sync-problem.md` | Detail-grid rows stay visible after model/form data changed, custom delete buttons, stale grid references, or multiple conditional grids sharing one `detailKey` |
| `detail-grid-manual-action-buttons-problem.md` | Hiding or manually controlling detail-grid Add/Delete buttons, `props.addBtn`, `props.deleteBtn`, or custom `Action` column row buttons |
| `detail-grid-enter-navigation-problem.md` | Detail-grid Enter key behavior, FINA-like keyboard cell navigation, moving across columns/rows, or adding a new row only from the last row |
| `detail-grid-oncalc-event-loop-problem.md` | `Maximum call stack size exceeded`, repeated detail-grid `onCalc` firing, watched controls writing to themselves, or stale totals during row edits |
| `repeat-fieldgroup-manipulation-problem.md` | Dynamic fields inside Formly `repeat`, selection-list controlled repeat columns, custom-column repeat fields, or listener loops after `fieldGroup` changes |
| `detail-grid-fina-extended-field-problem.md` | FINA-backed detail-grid fields, `EXTENDED.CUSTOMFIELD*`, form-only grid columns, load/save without affecting totals, or loaded FINA amount scale mismatches |
| `fina-detail-group-row-dedupe-problem.md` | FINA document detail rows duplicated or eliminated because item group metadata such as `groupno`, `group_quantity`, or `detail_extended_guid` multiplies query rows |
| `workshop-sales-confirmed-bo-load-problem.md` | Workshop Sales after Confirm to PSO, saved `bo_qty` changing on edit/load, `supply_qty`/`do_qty` double-counting, or allocation `done` rows affecting confirmed BO |
| `list-action-button-wrap-problem.md` | Overlapping, clipped, or crowded buttons in a Biz-A list Action column |
| `list-row-action-dom-state-problem.md` | Per-row Biz-A list action button state when config properties are ignored and rendered `tbody` / action-cell selectors are needed |
| `formly-list-inline-field-table-problem.md` | Inline field beside a Biz-A/Formly list table, table-only flex wrapper, `body > app-root > app-list > div > table`, or root `fields` on a list |
| `attachment-blob-querydata-problem.md` | File attachments, PDF/image BLOB columns, `input-file`, `updateImg`, `btoa`, attachment `queryData` errors, `n.map is not a function`, or `Bad control character in string literal` while loading attachment |
| `biz-a-query-join-depth-problem.md` | `token unknown` from `queryData`, long relation paths, collect/search filters across many tables, or BO Maintain collect by `doc_no`/customer |
| `fina-biza-jv-key-mismatch-problem.md` | JV-backed FINA approved forms/lists, Other Payment/Other Receipt approved flows, `JV.ID` vs `JV.JVID`, `jvid_fina`, or `Column unknown JV.ID` |
| `fina-template-print-selection-problem.md` | `previewTemplateFina`, selectable FINA print templates, `templateid`, `TEMPLATE.TEMPLATETYPE`, or replacing custom HTML print with a FINA template |
| `jvdet-incremental-save-problem.md` | Edited local Biz-A `JVDET` rows, preserving `JVDET.ID`, avoiding delete-all/recreate-all detail saves, deleting only removed detail IDs, or preserving Other Payment/Receipt `SEQ = 0` header row IDs via `header_jvdet_id` |
| `fml2fina-item-sync-problem.md` | Saving or updating FINA Item via `fml2fina`, FML XML format, `ITEM.GUID`, `USERGUID`, `FML_GUID`, `PreferedVendor`, `categoryid` / `CategorId`, or detail `old_data` snapshots |
| `fina-biza-running-number-sync-problem.md` | FINA-backed document running numbers, SO number previews, `GETSONUMBER`, `SAVECTLNUMBER`, masked numbers like `SO-0121/____`, or Biz-A/FINA SO number synchronization |
| `bankbook-source-navigation-mode-problem.md` | Bank Book rows opening source forms without `mode=from_bankbook`, inconsistent readonly/back behavior from Bank Book, or `buildSourceFormQueryParams` / `openSourceForm` navigation fixes |
| `biz-a-normalize-pattern-rules.md` | Repeated Biz-A patterns, reusable helper extraction, query/data movement to `lib_qry`, mode/navigation/button normalization, or utility reuse |
| `lookup-code-id-split-problem.md` | Master lookup table changes from business-code `ID` to integer `ID` plus `CODE`, stored FK values split from displayed/searchable document codes, or branch-like lookup migrations |
| `database-standard-rules.md` | Creating or changing Biz-A database tables, Firebird DDL, migrations, generators, triggers, or primary keys |
| `rename-used-column-rules.md` | Renaming used database columns, Firebird FK/PK/trigger dependencies, `queryData` paths, list action keys, save payloads, or system-table verification after a rename |
| `firebird-generator-rename-problem.md` | Renaming Firebird generators/sequences, standardizing to `<TABLE>_GEN`, dependency errors when dropping generators, `RDB$DEPENDENCIES`, `GEN_ID`, or `NEXT VALUE FOR` |
| `cli-script-standard-problem.md` | `cli-script/` files, watcher/callback scripts, converting standalone Node scripts into Biz-A CLI `get = function (lib)` + `onInit` format, or CLI-only dependencies such as `basic-ftp` |

## Section Index

| # | Section patterns.md | Kapan dipakai |
|---|---|---|
| 1 | Module Export Pattern | Setiap file module (form/list/library) |
| 2 | Library Pattern (`useLibrary`) | Reuse shared functions antar module |
| 3 | Form Structure Pattern | Setiap form baru atau refactor form |
| 4 | List Structure Pattern | Setiap list baru atau refactor list |
| 5 | Query Data Pattern (`lib_qry`) | Akses data via `dataService.queryData` |
| 6 | Raw SQL / Execute Block Pattern | Query kompleks via `executeBlock` |
| 7 | Utility Library Pattern (`lib_utils`) | Helper umum (`openDialog`, `findLuFina`, `toNumber`, dsb.) |
| 8 | Authorization & Privilege Pattern | Otorisasi user group, `setAction`, `setActionUsingKey` |
| 9 | HTML Template Pattern (`lib_template`) | Template print/report |
| 10 | Detail Grid Pattern | Master-detail grid (`detail-grid` formly type) |
| 11 | Dialog Pattern | Modal form, dialog pre-fill, read-only detail dialog |
| 12 | Running Number Pattern | Nomor urut dokumen (`PREFIX/ROMAWI-YEAR/CODE/NUM`) |
| 13 | Approval Workflow Pattern | Multi-step approval, status map, role shortcuts |
| 14 | Save / CRUD Pattern | `sendModel`, `json2fina`, sequential save |
| 15 | Listener Pattern (`valueChanges`) | Reactive wiring, auto-fill, auto-calculation |
| 16 | Print Pattern | Print flow dan export ke Excel |
| 17 | Delete Pattern (Master-Detail) | Delete Biz-A dan FINA |
| 18 | Loading & Error Handling Pattern | `loadingService`, `notificationService`, validation |
| 20 | Menu Structure Pattern | Konfigurasi menu JSON |
| 21 | Control Data by User Group Pattern | Filter data per user group |

## Aturan Konflik

Jika ada konflik antara aturan Firlan style dan `patterns.md`, **`patterns.md` menang** — ia adalah referensi baku yang diekstrak dari Proton. Aturan Firlan style hanya menambahkan constraint yang lebih sempit di atas pattern dasar.

## Fallback Rule

baca `.agents/references/patterns.md`. Jika keduanya tidak tersedia dan kode Proton atau Endo Medika juga tidak tersedia secara lokal, nyatakan secara eksplisit bahwa implementasi hanya bergantung pada repo saat ini, dan minta user untuk menyediakan `patterns.md` atau akses ke referensi Proton/Endo Medika.
