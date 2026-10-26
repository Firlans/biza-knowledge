---
name: biz-a-refactor
description: Refactor module Biz-A yang sudah ada (form, list, helper, test) sesuai Firlan style dan patterns.md. Use when the user asks to refactor, samakan style, ikuti style saya, normalize, perbaiki lifecycle, pisahkan tanggung jawab, rapikan form/list Biz-A, atau refactor ke style Firlan/Proton/Endo Medika.
---

Kamu adalah asisten yang ahli dalam merefactor module Biz-A sesuai gaya Firlan.

---

# Step 1 — Baca Knowledge Base

Sebelum memulai, baca dokumen berikut secara berurutan:

1. `.agents/references/pattern-index.md` — index pattern dan urutan referensi
2. `.agents/references/patterns.md` (fallback: `.agents/references/patterns.md`) — section yang relevan dengan task
3. `.agents/references/form-rules.md` — jika refactor form
4. `.agents/references/list-rules.md` — jika refactor list
5. `.agents/references/helper-rules.md` — jika refactor helper/library
6. `.agents/references/tdd-rules.md` — wajib untuk semua refactor
7. `.agents/references/refactor-checklist.md` — checklist wajib

---

# Step 2 — Gather Context

1. Baca target file secara lengkap dan file-file terkait di folder yang sama.
2. Baca setiap file yang dideklarasikan di `useLibrary`.
3. Identifikasi behavior existing yang perlu dipertahankan.
4. Cari referensi: current project → `patterns.md` → `Proton` → `Endo Medika`.
5. **Jangan gunakan `APL` atau `BERCA`** sebagai referensi.

---

# Step 3 — TDD Workflow (Wajib)

Ikuti siklus **Red → Green → Refactor** dari `.agents/references/tdd-rules.md`:

1. Jika behavior existing **belum ter-cover test**, tulis **characterization test dulu** sebelum refactor.
2. Untuk setiap behavior baru yang ditambahkan: failing test dulu → minimal implementation → refactor.
3. Jangan refactor tanpa test yang menjamin behavior tidak berubah.

---

# Step 4 — Refactor

Lakukan refactor terkecil yang aman tanpa mengubah business behavior:

- **Form**: rapikan lifecycle sesuai `form-rules.md` — pindahkan logic ke hook yang benar
- **List**: rapikan struktur sesuai `list-rules.md`
- **Helper**: rapikan separation dan naming sesuai `helper-rules.md`
- Jaga agar refactor **tidak mengubah behavior bisnis**
- Gunakan `structuredClone` saat menyalin model state

---

# Step 5 — Validate

Verifikasi semua poin di `.agents/references/quality-gates.md` dan `.agents/references/refactor-checklist.md`.

Jalankan test, pastikan semua hijau sebelum task selesai.

---

Sekarang kerjakan task berikut:

$ARGUMENTS
