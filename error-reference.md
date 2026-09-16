# Error Reference — Biz-A

Daftar error code yang sering ditemui saat development module Biz-A, beserta penyebab dan solusinya.

---

## NG01000

**Pesan**: `NG01000` (Angular / Formly repeat field error)

**Penyebab**: Field bertipe `repeat` (formly repeat section) diisi nilainya menggunakan `setValue()`. Formly repeat field mengelola array internal-nya sendiri — memanggil `setValue()` pada control repeat akan merusak binding internal dan memicu error `NG01000`.

**Gejala**:
- Error `NG01000` muncul di console saat form dibuka atau saat data di-load ke repeat field
- Repeat section tidak merender row yang diharapkan
- Data repeat tampak ada di model tapi tidak tampil di UI

**Solusi**:
- **Jangan** gunakan `this.form.get('repeat_field').setValue(arrayData)` untuk mengisi repeat field
- Isi repeat field melalui **model** — assign array langsung ke `this.model.repeat_field = arrayData`
- Jika perlu update setelah form sudah aktif, manipulasi model lalu trigger change detection
- Untuk detail-grid (Section 10 `patterns.md`), gunakan pattern `assignDetail` yang memanipulasi model, bukan form control

**Contoh salah**:
```js
// ❌ JANGAN — akan memicu NG01000
this.form.get('items').setValue(detailRows);
```

**Contoh benar**:
```js
// ✅ Isi via model
this.model.items = detailRows;
```

**Referensi**: Section 10 (Detail Grid Pattern) dan Section 15 (Listener Pattern) di `patterns.md`

---

## NG01001

**Pesan**: `Database 2 muncul error: Token unknown - line 1, column 9 FROM`

**Penyebab**: Field `key: 'id'` ditempatkan di `fields` lalu nilai `id` juga di-assign ke `this.model` atau `this.form` saat initial load. Kombinasi ini dapat merusak query builder internal dan menghasilkan SQL invalid pada saat form load.

**Gejala**:
- Error muncul segera saat form open atau saat data di-load ke form
- Field `id` sudah ada di `fields` dan `this.model.id` / `this.form.setValue({ id: ... })` di-set
- Error jalan sendiri ke console dengan pesan `Token unknown - line 1, column 9 FROM`

**Solusi**:
- Gunakan `key: 'id'` hanya untuk hidden internal identifier, bukan field input yang terikat di form load
- Hindari assignment `this.form.setValue({ id: ... })` atau `this.model.id = ...` pada load jika ada field `key: 'id'`
- Jika perlu menyimpan identifier hidden gunakan field lain seperti `record_id`, `entity_id`, `id_record`, atau `id_`
- Pastikan field `id` tidak digunakan sebagai key untuk lookup/input yang ikut di-load ke SQL generator

**Contoh benar**:
```js
{ key: 'record_id' },
```

---

<!-- Tambahkan error baru di bawah dengan format yang sama -->

## DataCloneError

**Pesan**: `DataCloneError: Failed to execute 'structuredClone' on 'Window': function () { [native code] } could not be cloned.`

**Penyebab**: `structuredClone` dipakai pada object konfigurasi Biz-A yang berisi function, misalnya `fields`, `props`, detail-grid `columns`, dialog config, lookup config, atau button `onClick`.

**Gejala**:
- Form gagal dibuka saat `beforeLoadData` atau `setGridColumns`
- Error muncul setelah menambahkan tombol/callback pada detail-grid atau dialog
- Stack trace mengarah ke `structuredClone(...)`

**Solusi**:
- Gunakan `structuredClone` hanya untuk data model/payload polos
- Jangan clone konfigurasi Formly/Biz-A dengan `structuredClone`
- Jika konfigurasi perlu disalin, copy properti yang dibutuhkan atau pakai helper clone yang mempertahankan function sebagai reference
