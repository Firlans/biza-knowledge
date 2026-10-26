# Form Rules — Firlan Style

Ikuti **Section 3 (Form Structure Pattern)** dan **Section 10 (Detail Grid Pattern)** di `patterns.md` sebagai dasar, lalu terapkan batas-batas Firlan style berikut.

## Lifecycle

| Lifecycle hook | Tanggung jawab |
|---|---|
| `beforeLoadData` | Setup only (grid ref, debug state), panggil `setDbIndex` |
| `onInit` | Mode detection, new/edit flow, panggil `preparingData`, aktifkan listener |
| `preparingData` | Initial data dan reference data |
| `setDbIndex` | Setiap `dbIndex` assignment (pakai `findLuFina` — Section 7 `patterns.md`) |
| `listener` | `valueChanges` dan reactive wiring only (Section 15 `patterns.md`) |
| `saveClicked` | Payload dan save flow (Section 14 `patterns.md`) |
| Named handlers | `printClicked`, `backClicked`, atau business-specific action names (Section 16 untuk print) |

## Batas Tanggung Jawab

- **Jangan** pindahkan initial data loading ke dalam `listener`.
- **Jangan** sebarkan `dbIndex` assignment ke `beforeLoadData`, `onInit`, atau button handlers — `dbIndex` wajib hanya di `setDbIndex`.
- **Jangan** sembunyikan button logic inline ketika action lebih dari simple navigation call.
- Simpan save flow di satu named action handler dan merge `this.model` dengan `this.form.value` sebelum validation/payload mapping.
- Validasi respons `sendModel` dengan `response.error` dan `json2fina` dengan `res.result?.[0]?.error` sebelum success path.

## Style Targets

- Pertahankan standard Biz-A module export: `get = function () { return { ... } }` dan `module.exports = get` (Section 1).
- Form deklaratif dengan `model`, `tableName`, `fields`, dan `functions`.
- Semua `fields[].key` harus lowercase dan prefer `snake_case`.
- Prefer small helpers dengan nama bisnis eksplisit, hindari one-use pass-through helpers jika logikanya lebih jelas di call site.
- **Jangan** buat tiny generic form wrappers (`getFormValue`, `setFormValue`, `watchControl`) — prefer langsung: `this.form.get(...).value`, `this.form.get(...).setValue(...)`, `this.form.get(...).valueChanges.subscribe(...)`.
- **Hindari** `this.form.patchValue(...)` saat target controls sudah diketahui.
- **Jangan** tambahkan `{ emitEvent: false }` pada `setValue(...)` kecuali user meminta.
- **Jangan** buat wrapper `showError` — panggil langsung `this.notificationService.showError(...)` (Section 18).
- Gunakan `model` untuk field-backed state atau initial values eksplisit. Jangan duplikasi nilai di `model` jika field sudah ada tanpa initial value.
- Jangan letakkan transient guards (`listener_loaded`) di `model` jika lifecycle bersih tanpanya.
- Date/time: prefer `this.dayjs(...)` daripada `new Date()` atau manual string slicing (Section 12).
- **Jangan** gunakan object-literal default parameters (`options = {}`, `config = {}`). Terima `undefined`, normalisasi di function body.
- **Jangan** gunakan default parameter yang membaca runtime state (`this.form`, `this.model`, services). Terima `undefined` di signature, resolve fallback di function body.
- Listener yang menunggu load: ikuti pola `quotationForm` — setup di `beforeLoadData`, `setInterval` di `onInit`, tunggu `model.loaded`, panggil `listener()`, clear di `onDestroy`.
- Prefer nama helper: `build...`, `apply...`, `normalize...`, `set...`, `load...`, `validation`.
- Mode handling (`new`, `edit`, `view`, `approve`): gunakan `expressions` pada field (Section 3).

## Defaults

- RxJS flows linear, satu async flow → satu `subscribe()` final (Section 14).
- Reuse `useLibrary` sebelum membuat helpers baru (Section 2).
- Selalu merge `this.model` dan `this.form.value` sebelum validation/save mapping.
- Selalu validasi `sendModel` → `response.error`, `json2fina` → `res.result?.[0]?.error`.
- Prefer explicit mapping, explicit defaults, explicit error messages — bukan clever abstractions.
- Pertahankan captions, lookup filters, payload shape, dan naming target project.
- Running number → Section 12. Approval workflow → Section 13 (`STATUS_MAP`, `approvalStatusMap`).
