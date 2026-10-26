---
name: biz-a-create
description: Buat module Biz-A baru (form, list, helper, test) sesuai Firlan style dan patterns.md. Use when the user asks to create, scaffold, buat form Biz-A, buat list Biz-A, create module Biz-A, buat module baru, atau generate scaffold.
---

Kamu adalah asisten yang ahli dalam membuat module Biz-A baru sesuai gaya Firlan.

---

# Step 1 — Baca Knowledge Base

Sebelum memulai, baca dokumen berikut secara berurutan:

1. `.agents/references/pattern-index.md` — index pattern dan urutan referensi
2. `.agents/references/patterns.md` (fallback: `.agents/references/patterns.md`) — section yang relevan dengan task
3. `.agents/references/form-rules.md` — jika membuat form
4. `.agents/references/list-rules.md` — jika membuat list
5. `.agents/references/helper-rules.md` — jika membuat helper/library
6. `.agents/references/tdd-rules.md` — wajib untuk semua creation
7. `.agents/references/proton-lifecycle.md` — referensi lifecycle
8. `.agents/references/creation-checklist.md` — checklist wajib

---

# Step 2 — Gather Context

1. Baca target folder dan file-file terkait di project yang sama.
2. Baca setiap file yang dideklarasikan di `useLibrary`.
3. Cari form, list, helper, atau test yang sudah ada di project saat ini yang menggunakan pattern yang dibutuhkan.
4. Jika project saat ini tidak cukup, cari referensi: `patterns.md` → `Proton` → `Endo Medika`.
5. Jika Proton/Endo Medika tidak tersedia lokal, gunakan repo saat ini + `patterns.md` sebagai proxy.
6. **Jangan gunakan `APL` atau `BERCA`** sebagai referensi.

---

# Step 3 — TDD Workflow (Wajib)

Ikuti siklus **Red → Green → Refactor** dari `.agents/references/tdd-rules.md`:

1. **Red**: Tulis unit test yang gagal untuk helper/mapper/validation terlebih dahulu.
2. **Green**: Implementasikan kode seminimal mungkin agar test lulus.
3. **Refactor**: Bersihkan tanpa mengubah behavior, pastikan test tetap hijau.

Mulai dengan unit test untuk helper/mapper/validation, lalu hasilkan scaffold terkecil yang mengikuti lifecycle split.

---

# Step 4 — Generate Module

Gunakan aturan dari doc yang sudah dibaca:

- **Form**: ikuti lifecycle dan style targets dari `form-rules.md`
- **List**: ikuti struktur dari `list-rules.md`
- **Helper**: ikuti separation dan naming dari `helper-rules.md`
- **Naming**: `build...`, `apply...`, `normalize...`, `set...`, `load...`, `validation`

---

# Step 5 — Validate

Verifikasi semua poin di `.agents/references/quality-gates.md` dan `.agents/references/creation-checklist.md`.

Jalankan test yang paling sempit yang tersedia.

---

Sekarang kerjakan task berikut:

$ARGUMENTS
