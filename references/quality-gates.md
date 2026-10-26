# Quality Gates — Firlan Style

Sebelum mengembalikan hasil, verifikasi semua poin berikut.

## Wajib

- [ ] `patterns.md` dibaca untuk section yang relevan dan output selaras
- [ ] Referensi lokal dibaca dulu (`patterns.md` → project) sebelum Proton
- [ ] `APL` dan `BERCA` tidak digunakan sebagai referensi
- [ ] Reuse helpers dari `useLibrary` (Section 2)
- [ ] `sendModel` divalidasi via `response.error` (Section 14)
- [ ] `json2fina` divalidasi via `res.result?.[0]?.error` (Section 14)
- [ ] Captions, lookup shape, navigation style sesuai target project
- [ ] `loadingService` dan `notificationService` dipakai sesuai Section 18
