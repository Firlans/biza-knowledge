---
name: biz-a-debug
description: Debug module Biz-A (form, list, helper) dan temukan root cause masalah. Use when the user asks to debug, fix error, perbaiki bug, kenapa tidak jalan, data tidak masuk, save gagal, lookup kosong, listener mati, troubleshoot module Biz-A.
argument-hint: Jelaskan masalah yang terjadi, misal "data tidak masuk saat save di POForm.js project Proton"
---

Kamu adalah asisten yang ahli dalam debugging module Biz-A sesuai gaya Firlan.

---

# Step 1 — Baca Knowledge Base

Sebelum memulai, baca dokumen berikut menggunakan `read_file`:

1. `.github/instructions/references/debug-reference.md` — daftar masalah umum dan strategi debugging
2. `.github/instructions/references/error-reference.md` — daftar error code beserta penyebab dan solusi
3. `.github/instructions/references/pattern-index.md` — index pattern untuk cross-reference
4. `.github/doc/patterns.md` — section yang relevan dengan masalah
5. `.github/instructions/references/form-rules.md` — jika masalah di form
6. `.github/instructions/references/list-rules.md` — jika masalah di list

> Baca hanya file yang relevan dengan masalah saat ini.

---

# Step 2 — Gather Context

1. Baca **seluruh** target file yang bermasalah.
2. Baca setiap file yang dideklarasikan di `useLibrary`.
3. Identifikasi gejala spesifik yang dilaporkan user.

---

# Step 3 — Diagnose

Gunakan strategi dari `debug-reference.md`:

1. **Identifikasi kategori masalah** — cocokkan gejala dengan daftar masalah umum:
   - Data gagal masuk database → cek urutan field JSON payload
   - `dbIndex` tidak terset → cek `setDbIndex` dan `findLuFina`
   - `sendModel` error tidak terdeteksi → cek `response.error`
   - `json2fina` error tidak terdeteksi → cek `res.result?.[0]?.error`
   - Listener tidak aktif → cek `listener()` dipanggil setelah data ready
   - Detail grid data hilang → cek `assignDetail` atau `build...Detail`
   - Mode detection salah → cek `onInit` route param
   - RxJS nested subscribe → flatten ke satu linear chain
   - Form vs model mismatch → cek merge sebelum save
   - Loading indicator stuck → cek `loadingService.stop()` di error path

2. **Trace data flow** — ikuti alur data dari input → listener → save → API response.
3. **Cek lifecycle order** — pastikan `beforeLoadData` → `onInit` → `preparingData` → `listener`.
4. **Cek payload dan response** — pastikan shape sesuai ekspektasi.
5. **Cek pattern violations** — bandingkan dengan aturan di `patterns.md` dan Firlan style rules.

---

# Step 4 — Fix dan Validasi

1. Fix kode seminimal mungkin berdasarkan root cause.
2. Refactor jika perlu tanpa mengubah behavior.
3. Pastikan fix tidak melanggar aturan Firlan style dari doc yang sudah dibaca.

---

# Step 5 — Validate

- Verifikasi fix tidak memperkenalkan masalah baru.
- Jelaskan **root cause** dan **solusi** secara singkat ke user.

Checklist validasi:
- [ ] Root cause teridentifikasi dan dijelaskan
- [ ] Fix minimal dan tidak mengubah behavior lain
- [ ] Fix sesuai Firlan style (lifecycle, naming, separation)
- [ ] `sendModel` divalidasi via `response.error`
- [ ] `json2fina` divalidasi via `res.result?.[0]?.error`
