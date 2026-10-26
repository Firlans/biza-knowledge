# Biz-A Visual Design and Theming Index

Gunakan reference ini ketika task meminta tampilan Biz-A yang lebih baik,
lebih rapi, lebih modern, responsif, atau konsisten. Dokumen sumber utama adalah
`.agents/docs/dok-6-biz-a-theming.md`; index ini memilih bagian yang perlu dibaca
agar perubahan visual tidak berhenti pada penggantian warna.

## Problem signals

- UI dinilai jelek, padat, berantakan, atau tidak konsisten.
- Form, list, detail-grid, dialog, kasir, atau kiosk perlu diperbaiki tampilannya.
- Ada hardcoded color, radius, font, spacing, atau override Material.
- Layout nyaman di desktop tetapi sulit disentuh di tablet, mobile, atau kiosk.
- Theme light/dark, preset, custom theme, logo, atau preview perlu dibuat.
- Perubahan visual berisiko merusak config lama atau berbeda antar-device.

## Root cause to avoid

Perbaikan visual sering diperlakukan sebagai pemilihan warna saja. Padahal
kualitas tampilan Biz-A juga ditentukan oleh spacing, tipografi, alignment,
density, ukuran target sentuh, hierarchy surface, dan konsistensi komponen.
Hardcoded styling juga memutus hubungan komponen dengan theme dan membuat dark
mode, profile device, serta migrasi Material sulit dirawat.

## Reading map

| Kebutuhan | Baca bagian Dok. 6 | Keputusan utama |
|---|---|---|
| Memahami fondasi visual | Bagian 2 dan 6.5 | Gunakan satu skala spacing 4px dan perlakukan tipografi, alignment, density, serta konsistensi sebagai bagian dari desain. |
| Memilih karakter tampilan | Bagian 6.1-6.4 | Mulai dari preset Klasik, Teduh, atau Tegas; jangan merancang token secara acak per layar. |
| Mengatur warna dan token | Bagian 5, 7, dan 8.1 | Gunakan token Biz-A dan seed/preset sebagai basis; simpan override minimum, bukan salinan seluruh palette. |
| Membuat komponen custom | Bagian 10 dan 11 | Referensikan CSS variable theme; hindari nilai warna, radius, dan font mentah. |
| Desktop/tablet/mobile/kiosk | Bagian 5.1 | Warna tetap konsisten; ergonomi boleh berbeda. Hormati `density`, `fontScale`, `spacingScale`, dan `minTouchTarget`. |
| Light/dark mode | Bagian 4.2, 6, dan 14 | Uji kedua scheme; jangan membuat dark theme dengan sekadar membalik warna light. |
| Theme perusahaan atau device | Bagian 4-4.3 | Ikuti urutan resolusi fallback -> application -> company -> device -> user -> profile. |
| Custom theme dan preview | Bagian 7.1.1 | Preview form, list, detail-grid, dialog, kasir, dan kiosk pada semua scheme/profile sebelum menyimpan. |
| Menambah preset platform | Bagian 7.1.2 | Lengkapi token, uji kontras, dokumentasi, versioning, dan snapshot regresi visual. |
| Migrasi Material 2 ke 3 | Bagian 9 dan 15 | Inventarisasi override `.mat-*`, `::ng-deep`, `!important`, palette M2, dan atribut warna lama sebelum migrasi. |
| Kriteria selesai | Bagian 16 | Gunakan acceptance criteria dokumen sebagai quality gate, bukan penilaian visual subjektif saja. |

## Corrected approach

1. Tentukan konteks layar dan `uiProfile` yang harus didukung.
2. Pilih preset terdekat sebagai fondasi visual.
3. Perbaiki hierarchy dengan spacing, typography, alignment, surface, dan
   density sebelum menambah dekorasi.
4. Gunakan token theme atau CSS variable Biz-A untuk semua nilai visual yang
   memang harus mengikuti theme.
5. Pertahankan override lokal hanya untuk kebutuhan semantik komponen; `Style`
   komponen boleh menang, tetapi tetap merujuk token theme.
6. Preview dan verifikasi pada light/dark serta profile yang relevan.
7. Jalankan pemeriksaan kontras dan regresi visual sebelum menyatakan selesai.

## Implementation checklist

- [ ] Tidak ada warna, font, atau radius baru yang di-hardcode tanpa alasan.
- [ ] Spacing memakai skala 4, 8, 12, 16, 24, atau 32px.
- [ ] Angka pada tabel memakai `font-variant-numeric: tabular-nums`.
- [ ] Kolom angka dan action memiliki alignment serta ruang yang konsisten.
- [ ] Target sentuh minimum: tablet 44px, mobile 48px, kiosk 56px.
- [ ] Density tidak membuat kontrol sentuh lebih kecil dari target minimum.
- [ ] Light dan dark memenuhi WCAG AA: 4.5:1 untuk teks normal, 3:1 untuk
      teks besar dan batas komponen.
- [ ] Form, list, detail-grid, dan dialog tetap terbaca pada ukuran yang diuji.
- [ ] Config versi lama tetap bekerja dan tidak bergantung pada selector
      internal Material yang rapuh.
- [ ] Snapshot atau pemeriksaan visual mencakup kondisi sebelum dan sesudah.

## Related references

- `mobile-layout-rules.md` untuk layout mobile dari prototipe, header/filter,
  pasangan tanggal, kartu master/list dengan ikon serta deskripsi, kolom/aksi
  native yang hilang, dan verifikasi DOM serta lifecycle helper UI.
- `detail-grid-table-header-layout-problem.md` untuk header tabel overlap,
  terpotong, atau tidak sejajar.
- `detail-grid-scroll-sizing-alignment-problem.md` untuk lebar kolom, nowrap,
  horizontal scroll, angka terpotong, dan alignment cell.
- `detail-grid-column-style-problem.md` untuk styling visual kolom detail-grid.
- `list-action-button-wrap-problem.md` untuk tombol action yang bertumpuk.
- `formly-list-inline-field-table-problem.md` untuk layout field di samping
  tabel list.

## Verification

Cari hardcoded dan override rapuh pada area yang diubah, lalu cek hasil render
pada profile serta scheme yang relevan. Untuk perubahan theme platform, ikuti
matriks snapshot di Dok. 6 bagian 7.1.2: enam layar referensi, dua color scheme,
dan empat `uiProfile`.
