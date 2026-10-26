# Refactor Checklist — Firlan Style

## Form

- [ ] Setup di `beforeLoadData`
- [ ] Load/new flow di `onInit`
- [ ] Reactive wiring di `listener`
- [ ] Save mapping + orchestration di `saveClicked`
- [ ] `dbIndex` untuk setiap `lu-fina` lookup di `setDbIndex` via `findLuFina` (Section 7)
- [ ] Nama helper `build...`, `normalize...`, `apply...`, `set...`, `validation` jika meningkatkan readability
- [ ] Extract repeated header/detail mapping ke small helpers
- [ ] `structuredClone` saat menyalin model state (Quick Reference)

## List

- [ ] Top buttons, columns, order, filter dekat module root
- [ ] Authorization + data scoping di `onPipe` atau reused helpers
- [ ] Button handlers pendek, navigasi-oriented
- [ ] Readable filter builders > inline repeated filter objects

## Helper

- [ ] Query logic di query libraries, UI orchestration di form/list
- [ ] Helper functions deterministic
- [ ] Prefer reusable pure functions
- [ ] Nama selaras target project
- [ ] Dialog di banyak module → extract ke shared dialog library (Section 11)
