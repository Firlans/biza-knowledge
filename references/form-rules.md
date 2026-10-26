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
- Validasi respons `sendModel` dengan `response.error`, `json2fina` dengan `res.result?.[0]?.error`, dan `fml2fina` dengan `res.result?.[0]?.error` / `res.error` / `res.message` sebelum success path.

## Style Targets

- Pertahankan standard Biz-A module export: `get = function () { return { ... } }` dan `module.exports = get` (Section 1).
- Form deklaratif dengan `model`, `tableName`, `fields`, dan `functions`.
- Semua `fields[].key` harus lowercase dan prefer `snake_case`.
- `key: 'id'` hanya boleh digunakan untuk hidden internal identifier. Hindari menggunakan field `id` sebagai property input yang di-assign langsung saat load, karena bisa memicu query builder `Database 2` error.
- Prefer small helpers dengan nama bisnis eksplisit, hindari one-use pass-through helpers jika logikanya lebih jelas di call site.
- **Jangan** buat tiny generic form wrappers (`getFormValue`, `setFormValue`, `watchControl`) — prefer langsung: `this.form.get(...).value`, `this.form.get(...).setValue(...)`, `this.form.get(...).valueChanges.subscribe(...)`.
- **Hindari** `this.form.patchValue(...)` saat target controls sudah diketahui.
- **Jangan** tambahkan `{ emitEvent: false }` pada `setValue(...)` kecuali user meminta.
- **Jangan** buat wrapper `showError` — panggil langsung `this.notificationService.showError(...)` (Section 18).
- Gunakan `model` untuk field-backed state atau initial values eksplisit. Jangan duplikasi nilai di `model` jika field sudah ada tanpa initial value.
- Jangan letakkan transient guards (`listener_loaded`) di `model` jika lifecycle bersih tanpanya.
- Date/time: prefer `this.dayjs(...)` daripada `new Date()` atau manual string slicing (Section 12).
- `structuredClone` hanya boleh dipakai untuk data model/payload polos. Jangan gunakan `structuredClone` untuk `fields`, `props`, `columns`, dialog config, lookup config, atau object konfigurasi lain karena konfigurasi Biz-A sering berisi function (`onClick`, callback native, handler button) yang memicu `DataCloneError`.
- **Jangan** gunakan object-literal default parameters (`options = {}`, `config = {}`). Terima `undefined`, normalisasi di function body.
- **Jangan** gunakan default parameter yang membaca runtime state (`this.form`, `this.model`, services). Terima `undefined` di signature, resolve fallback di function body.
- Listener yang menunggu load: ikuti pola `quotationForm` — setup di `beforeLoadData`, `setInterval` di `onInit`, tunggu `model.loaded`, panggil `listener()`, clear di `onDestroy`.
- Prefer nama helper: `build...`, `apply...`, `normalize...`, `set...`, `load...`, `validation`.
- Mode handling (`new`, `edit`, `view`, `approve`): gunakan `expressions` pada field (Section 3).

## No redundant model assignment for fields without defaults

- Jika sebuah variable sudah dideklarasikan sebagai field dan tidak memerlukan default value, **jangan** assign ulang di `model` atau `initModel`.
- Redundant assignment menambah noise dan membuat field yang memang punya default bermakna jadi lebih sulit dikenali.

**Forbidden — unnecessary re-assignment:**

```javascript
fields: [
	{ key: 'customerId', type: 'input' },
	{ key: 'itemName',   type: 'input' },
],
model: {
	customerId: null,   // already implied by the field; no default needed
	itemName:   null,   // same
}
```

**Correct — only assign when a non-trivial default is required:**

```javascript
fields: [
	{ key: 'customerId', type: 'input' },
	{ key: 'qty',        type: 'input' },
	{ key: 'discount',   type: 'input' },
],
model: {
	qty:      1,
	discount: 0,
	// customerId omitted — no default needed
}
```

- Simpan entri `model` / `initModel` hanya untuk field yang initial value-nya memang harus berbeda dari `undefined` / empty.

## Primary key fields must NOT be rendered in form fields

- Primary key fields (`id`, `header_id`, `master_id`, atau field lain yang merupakan database primary key) **tidak boleh** muncul di `fields` atau `fieldGroup`.
- Primary key harus tetap ada di `model`, tetapi tidak dirender sebagai form control.
- Jika primary key dirender di form, hasilnya bisa memicu error `token unknown` dan form gagal load.

**Forbidden — id in fieldGroup:**

```javascript
model: {
	id: null,
	name: null,
},
fields: [
	{ key: 'id', type: 'input' },
	{ key: 'name', type: 'input' },
]
```

**Correct — id in model only:**

```javascript
model: {
	id: null,
	name: null,
},
fields: [
	// { key: 'id' },
	{ key: 'name', type: 'input' },
]
```

- Primary key dikelola backend (`genId()` untuk record baru atau hasil load database saat edit), jadi tidak boleh diedit lewat UI.
- Cek baik top-level `fields` maupun nested `fieldGroup` arrays.
- Untuk detail konfigurasi dan diagnosis PK, load `.agents/references/pk-field-config.md`.

## Defaults

- RxJS flows linear, satu async flow → satu `subscribe()` final (Section 14).
- Reuse `useLibrary` sebelum membuat helpers baru (Section 2).
- Selalu merge `{ ...this.model, ...this.form.value }` sebelum validation,
  payload mapping, cloning, atau mengganti model pada form aktif. Urutan wajib
  model lebih dulu agar nilai form terbaru menang tanpa membuang nilai
  model-only/disabled. Lihat `form-model-value-sync-problem.md`.
- Selalu validasi `sendModel` -> `response.error`, `json2fina` -> `res.result?.[0]?.error`, dan `fml2fina` -> `res.result?.[0]?.error` / `res.error` / `res.message`.
- Prefer explicit mapping, explicit defaults, explicit error messages — bukan clever abstractions.
- Pertahankan captions, lookup filters, payload shape, dan naming target project.
- Running number → Section 12. Approval workflow → Section 13 (`STATUS_MAP`, `approvalStatusMap`).
