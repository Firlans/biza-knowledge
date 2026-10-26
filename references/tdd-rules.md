# TDD Rules — Firlan Style

Seluruh pekerjaan **wajib** mengikuti siklus TDD: **Red → Green → Refactor**.

## Siklus Red-Green-Refactor

1. **Red** — Tulis satu unit test yang gagal yang mendefinisikan slice behavior terkecil berikutnya.
2. **Green** — Implementasikan kode paling sederhana agar test lulus. Jangan over-engineer.
3. **Refactor** — Bersihkan kedua test dan production code, pastikan semua test tetap hijau.

## Aturan

- **Test-first, always**. Dilarang menulis production logic tanpa failing test terlebih dahulu.
- **Satu behavior per test**. Setiap test punya satu assertion inti yang jelas.
- Prioritas unit test:
  - Payload mapping (`build...` helpers)
  - Validation (`validate...`, `validation`)
  - Calculation dan normalization (`normalize...`, calculation helpers)
  - Critical branching (new vs edit mode, auth state, error paths)
- Test harus **deterministic** — mock sisi luar (DB, network, time), jangan mock behavior yang sedang di-test.
- Untuk refactor: jika belum ada test untuk behavior existing, **tulis characterization test dulu**.
- Jalankan test setelah setiap step Red dan Green. Jangan batch tanpa test.
- Gunakan local test patterns project sebelum membuat fixtures baru.
- Ikuti **Section 19 `patterns.md`** untuk struktur test (`testUtils.js`, `bindFunctionInObj`, `loadModuleFactory`).
- Kategori test: `Normal scenarios`, `Edge cases`, `Invalid inputs`, `Deterministic behavior`.

## Checklist (per behavior)

- [ ] Failing test ditulis dulu (Red)
- [ ] Minimal implementation agar test lulus (Green)
- [ ] Refactor dengan test tetap hijau
- [ ] Cover minimal: satu happy path, satu edge case, satu error path
- [ ] Test deterministic dan terisolasi
