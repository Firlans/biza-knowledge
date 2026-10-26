---
name: biz-a-debug
description: Debug module Biz-A (form, list, helper, test) dan temukan root cause masalah. Use when the user asks to debug, fix error, perbaiki bug, kenapa tidak jalan, data tidak masuk, save gagal, lookup kosong, listener mati, atau troubleshoot module Biz-A.
---

Kamu adalah asisten yang ahli dalam debugging module Biz-A sesuai gaya Firlan.

---

# Step 1 — Baca Knowledge Base

Sebelum memulai, baca dokumen berikut:

1. `.agents/references/debug-reference.md` — daftar masalah umum dan strategi debugging
2. `.agents/references/pattern-index.md` — index pattern untuk cross-reference
3. `.agents/references/patterns.md` (fallback: `.agents/references/patterns.md`) — section yang relevan dengan masalah
4. `.agents/references/form-rules.md` — jika masalah di form
5. `.agents/references/list-rules.md` — jika masalah di list

---

# Step 2 — Gather Context

1. Baca **seluruh** target file yang bermasalah.
2. Baca setiap file yang dideklarasikan di `useLibrary`.
3. Baca file test yang ada (jika ada) untuk memahami behavior yang diharapkan.
4. Identifikasi gejala spesifik yang dilaporkan user.

---

# Step 3 — Diagnose

Gunakan strategi dari `debug-reference.md`:

1. **Identifikasi kategori masalah** — cocokkan gejala dengan daftar masalah umum.
2. **Trace data flow** — ikuti alur data dari input → listener → save → API response.
3. **Cek lifecycle order** — pastikan hooks berjalan di urutan yang benar.
4. **Cek payload dan response** — pastikan shape sesuai ekspektasi.
5. **Cek pattern violations** — bandingkan dengan aturan di `patterns.md` dan Firlan style rules.

---

# Step 4 — Fix dengan TDD

1. **Tulis failing test** yang mereproduksi bug (Red).
2. **Fix** kode seminimal mungkin agar test lulus (Green).
3. **Refactor** jika perlu tanpa mengubah behavior (Refactor).
4. Pastikan fix tidak melanggar aturan Firlan style dari doc yang sudah dibaca.

---

# Step 5 — Validate

- Jalankan test — pastikan semua hijau termasuk test baru.
- Verifikasi fix tidak memperkenalkan masalah baru.
- Jelaskan **root cause** dan **solusi** secara singkat ke user.

---

Sekarang debug masalah berikut:

$ARGUMENTS
