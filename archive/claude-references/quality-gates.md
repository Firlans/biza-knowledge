# Quality Gates — Firlan Style

Sebelum mengembalikan hasil, verifikasi semua poin berikut.

## Wajib

- [ ] `patterns.md` dibaca untuk section yang relevan dan output selaras
- [ ] TDD dipatuhi: failing test sebelum production code, Red → Green → Refactor
- [ ] Semua unit test hijau
- [ ] Referensi lokal dibaca dulu (`patterns.md` → project) sebelum Proton
- [ ] `APL` dan `BERCA` tidak digunakan sebagai referensi
- [ ] Reuse helpers dari `useLibrary` (Section 2)
- [ ] `sendModel` divalidasi via `response.error` (Section 14)
- [ ] `json2fina` divalidasi via `res.result?.[0]?.error` (Section 14)
- [ ] Captions, lookup shape, navigation style sesuai target project
- [ ] Cover minimal: happy path, edge case, error path
- [ ] `loadingService` dan `notificationService` dipakai sesuai Section 18
