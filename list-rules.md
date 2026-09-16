# List Rules — Firlan Style

Ikuti **Section 4 (List Structure Pattern)** dan **Section 8 (Authorization & Privilege Pattern)** di `patterns.md`.

## Struktur

- `buttons`, `columns`, `filter`, dan `order` dekat dengan module root.
- `beforeLoadData` untuk db index, flags, dan one-time setup (`this.dbIndex = this.config.api.finaDbIndex` atau `this.config.api.dbIndex`).
- `onPipe` untuk authorization (`setAction`/`setActionUsingKey`), data scoping (`setControlDataList`), button setup, dan first-load orchestration.
- Button handlers pendek dan fokus pada navigasi atau satu action yang jelas.
- Navigasi: `this.router.navigate(['../../form', 'FormName', id])` dengan optional `queryParams: { mode: 'view' | 'approve' | ... }`.
- Untuk pesan error/sukses di list, gunakan `alert()`; list runtime tidak selalu menyediakan `this.notificationService`.

## Aturan Filter dan Alur

- Pindahkan repeated filter objects ke small builder helpers (`build...Filter`).
- Simpan authorization dan privilege shaping di `onPipe` atau shared libraries.
- Jaga top-level action buttons tetap deklaratif kecuali project menggunakan pattern lokal lain.
- Delete flow ikuti Section 17 `patterns.md` (detail dulu, baru master untuk Biz-A; atau `delete: 1` untuk FINA).
