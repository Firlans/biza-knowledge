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

<!-- Tambahkan error baru di bawah dengan format yang sama -->
