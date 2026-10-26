# Pattern Knowledge Base Index

Sumber kebenaran utama untuk semua module Biz-A Firlan style.

## Lokasi Pattern

1. `.claude/doc/patterns.md` — salinan lokal (prioritas pertama)
2. `.github/doc/patterns.md` — fallback jika `.claude/doc` tidak tersedia

## Urutan Referensi

| Prioritas | Sumber | Kapan dipakai |
|---|---|---|
| 1 | `patterns.md` | Selalu — standar baku |
| 2 | Target file + nearby files | Konteks project saat ini |
| 3 | Files di `useLibrary` | Shared functions yang sudah ada |
| 4 | `Proton` | Referensi lifecycle dan best practice |
| 5 | `Endo Medika` | Fallback referensi jika Proton tidak cukup |

> **Dilarang**: `APL` dan `BERCA` sebagai referensi — kecuali user secara eksplisit memintanya dan semua referensi di atas masih tidak cukup.

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
| 19 | Test Pattern | Test setup, RxJS, categories |
| 20 | Menu Structure Pattern | Konfigurasi menu JSON |
| 21 | Control Data by User Group Pattern | Filter data per user group |

## Aturan Konflik

Jika ada konflik antara aturan Firlan style dan `patterns.md`, **`patterns.md` menang** — ia adalah referensi baku yang diekstrak dari Proton. Aturan Firlan style hanya menambahkan constraint yang lebih sempit di atas pattern dasar.

## Fallback Rule

Jika `.claude/doc/patterns.md` tidak tersedia, baca `.github/doc/patterns.md`. Jika keduanya tidak tersedia dan kode Proton atau Endo Medika juga tidak tersedia secara lokal, nyatakan secara eksplisit bahwa implementasi hanya bergantung pada repo saat ini, dan minta user untuk menyediakan `patterns.md` atau akses ke referensi Proton/Endo Medika.
