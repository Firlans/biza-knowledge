# Proton Lifecycle Reference

Section 3 di `patterns.md` adalah referensi kanonik. Berikut ringkasan pola lifecycle.

## Pola Lifecycle Form

### `Proton/PIForm.js`
- `beforeLoadData`: debug state, grid ref, panggil `setDbIndex`
- `onInit`: mode, `preparingData`, new/edit flow, aktifkan `listener` setelah data ready
- `preparingData`: initial reference data
- `listener`: reactive `valueChanges` wiring
- `setDbIndex`: `dbIndex` untuk `lu-fina` lookups

### `Proton/POForm.js`
- `beforeLoadData`: cache grid refs, reset setup state, `setDbIndex`
- `preparingData`: company info dan reference data
- `listener`: supplier dan date reactions
- `setDbIndex`: main fields + detail-grid lookups, terbatas pada index assignment

### `Proton/SIForm.js`
- `beforeLoadData`: lean, delegasi ke `setDbIndex`
- `onInit`: `preparingData`, load edit data, `listener` di async flow yang sama
- `preparingData`: running number dan tax data
- `listener`: lookup-driven master/detail recalculation

## Pola Lifecycle List

- Mirror `PIList.js` dan `POList.js` (Section 4)
- `beforeLoadData`: db index dan first-load flags
- `onPipe`: authorization, data scoping, top-button shaping
- Action handlers: pendek, fokus navigasi

## Normalisasi untuk Module Baru

Gunakan pembagian ini meskipun form target saat ini masih mencampur tanggung jawab:

| Data | Hook |
|---|---|
| Initial data | `preparingData` |
| Semua lookup `dbIndex` | `setDbIndex` |
| Reactive subscriptions | `listener` |
| Action button behavior | Named handlers |
