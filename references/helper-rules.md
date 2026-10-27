# Helper Rules — Firlan Style

Ikuti **Section 2, 5, 6, 7, 8, 9, 11** di `patterns.md` untuk naming dan separation.

## Separation

| Jenis logic | Lokasi |
|---|---|
| Query logic | Query libraries (`lib_qry`) |
| SELECT kompleks/read-only | `lib_queryRaw` dengan pola `setSql` + `executeBlock` (Section 6); penulisan data Biz-A memakai `sendModel`, data FINA memakai `json2fina` |
| Utility umum | `lib_utils` — `openDialog`, `findLuFina`, `findField`, `toNumber`, `numberToRomawi`, `convertToWord` (Section 7) |
| Authorization | `lib_authorization` — `getGroupNames`, `setAction`, `setActionUsingKey`, `setControlDataList` (Section 8) |
| HTML template print/report | `lib_template` (Section 9) |
| Dialog reusable | `lib_dialog` — jika dialog dipakai >1 module (Section 11) |
| UI orchestration | Form atau list modules |

## Naming Convention

| Prefix | Tujuan |
|---|---|
| `build...` | Payload atau filter builders |
| `apply...` | Push data ke form atau model state |
| `normalize...` | Reshape query results |
| `set...` | Direct assignments atau configuration |
| `load...` | Async fetch orchestration |
| `validation` / `validate...` | Final checks sebelum save (Section 18) |

## Prinsip

- Helper functions harus **deterministic** agar mudah diverifikasi.
- Prefer reusable **pure functions** untuk calculation, normalization, payload mapping.
- Nama selaras dengan target project, meskipun idenya dari Proton/Endo Medika.
- Reuse `useLibrary` helpers sebelum membuat yang baru (Section 2).
