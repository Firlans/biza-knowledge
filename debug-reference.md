# Debug Reference — Firlan Style

Daftar masalah umum dan strategi debugging untuk module Biz-A.

## Masalah Umum

### 1. Data gagal masuk database
- **Penyebab**: Urutan field pada JSON payload berpengaruh — data bisa terlambat diproses dan gagal masuk.
- **Solusi**: Pastikan urutan field di payload sesuai urutan yang diharapkan oleh API FINA. Cek `sendModel` payload shape.

### 2. `dbIndex` tidak terset
- **Gejala**: Lookup FINA tidak menampilkan data, atau menampilkan data dari database yang salah.
- **Solusi**: Pastikan semua `dbIndex` assignment ada di `setDbIndex`. Cek `findLuFina` mengembalikan index yang benar.

### 3. `sendModel` error tidak terdeteksi
- **Gejala**: Save terlihat sukses tapi data tidak masuk.
- **Solusi**: Pastikan ada pengecekan `response.error` setelah `sendModel` (Section 14 `patterns.md`).

### 4. `json2fina` error tidak terdeteksi
- **Gejala**: Data Biz-A tersimpan tapi FINA tidak terupdate.
- **Solusi**: Pastikan cek `res.result?.[0]?.error` setelah `json2fina` (Section 14 `patterns.md`).

### 5. Listener tidak aktif / reactive wiring mati
- **Gejala**: Field berubah tapi dependent fields tidak terupdate.
- **Solusi**: Pastikan `listener()` dipanggil setelah data ready di `onInit`. Jika ada `setInterval` pattern, pastikan `model.loaded` terset.

### 6. Detail grid data hilang saat save
- **Gejala**: Master tersimpan tapi detail kosong.
- **Solusi**: Pastikan detail grid data di-extract dan di-map sebelum save. Cek `assignDetail` atau `build...Detail` helper.

### 7. Mode detection salah (new vs edit)
- **Gejala**: Form edit menampilkan form kosong, atau form new memuat data lama.
- **Solusi**: Cek `onInit` mode detection — pastikan `this.id` atau route param di-cek dengan benar.

### 8. RxJS nested subscribe
- **Gejala**: Race condition, data tidak konsisten, memory leak.
- **Solusi**: Flatten ke satu linear chain dengan `switchMap`/`concatMap`. Satu `subscribe()` di akhir.

### 9. Form value vs model value mismatch
- **Gejala**: Save mengirim data stale atau kosong.
- **Solusi**: Merge `this.model` dan `this.form.value` sebelum validation/save mapping.

### 10. Loading indicator tidak berhenti
- **Gejala**: Spinner berputar terus setelah error.
- **Solusi**: Pastikan `loadingService.stop()` dipanggil di error path juga (Section 18 `patterns.md`).

### 11. NG01000 — repeat field diisi dengan setValue
- **Gejala**: Error `NG01000` di console, repeat section tidak render, data ada di model tapi tidak tampil.
- **Solusi**: Jangan `setValue()` pada repeat field — isi via `this.model.repeat_field = arrayData`. Lihat detail lengkap di `error-reference.md`.

## Strategi Debugging

1. **Cek payload**: Log payload sebelum `sendModel`/`json2fina` — pastikan shape dan value benar.
2. **Cek response**: Log full response setelah API call — cek `error` field.
3. **Cek lifecycle order**: Pastikan `beforeLoadData` → `onInit` → `preparingData` → `listener` berjalan berurutan.
4. **Cek dbIndex**: Log `this.dbIndex` dan setiap lookup field `dbIndex` — pastikan menunjuk ke database yang benar.
5. **Cek subscription**: Pastikan tidak ada nested subscribe. Cek apakah subscribe terpanggil lebih dari sekali.
6. **Cek form state**: Log `this.form.value` dan `this.model` sebelum save — pastikan data merged.
