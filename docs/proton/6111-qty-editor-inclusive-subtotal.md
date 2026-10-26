# Proton #6111 — Editor Qty dan Total Sub termasuk pajak

Implementasi lokal: 14 Oktober 2026. [Task #6111](https://iproj.my.id:5443/work_packages/6111) diambil ulang dari OpenProject. Komentar terbaru menyatakan alignment sudah sesuai, tetapi angka Qty tertutup kotak saat diedit.

Editor numerik dibatasi pada sel masing-masing dengan positioning lokal, ukuran border-box, dan alignment kanan. Style hanya berlaku di `proton-job-order-grid`; alignment serta lebar header tetap mengikuti konfigurasi sebelumnya. Style dibersihkan saat form ditutup.

Tambahan user mengikuti screenshot FINA: saat Termasuk Pajak aktif, Total Sub tetap sebesar jumlah Qty × Harga Satuan. Dasar sebelum pajak hanya dipakai untuk menghitung PPN. Diskon dihitung dari subtotal yang ditampilkan. Total Pesan = Total Sub − Diskon; PPN yang sudah termasuk tidak ditambahkan lagi. Ketika Termasuk Pajak tidak aktif, PPN ditambahkan ke total setelah diskon.

Contoh tarif master TAX 11%, tanpa diskon:

| Jumlah item | Total Sub | PPN termasuk | Total Pesan |
|---:|---:|---:|---:|
| Rp10.000.000,00 | Rp10.000.000,00 | Rp990.990,99 | Rp10.000.000,00 |
| Rp40.000.000,00 | Rp40.000.000,00 | Rp3.963.963,96 | Rp40.000.000,00 |

Helper yang sama dipakai oleh Sales Invoice dari Job Order. Regresi memeriksa save/reopen, penerusan subtotal/PPN/total ke SI, pajak berbeda per item, baris tanpa pajak, dan diskon 0/10/100%. Tarif berasal dari master TAX, bukan konstanta dalam perhitungan.

## File untuk publish

- `Proton/SOForm.js`
- `Proton/lib_jobOrder.js`

Tidak diperlukan migrasi database. Publish dan perubahan status/comment OpenProject belum dilakukan.

## Verifikasi

- `node node_modules/jest/bin/jest.js Proton/tests --runInBand --silent`: **38 suite, 942 tes lulus**.
- `node .codex/task-6111-openproject/check-editors.cjs`: **12 kasus lulus**, mencakup Material lama/MDC, lebar 390/1280/1920 px, terang/gelap, batas editor, alignment header/sel, mengetik Qty `12.5`, scroll lokal, dan cleanup style.
- Fixture yang sama terhadap SOForm sebelum perubahan gagal pada batas editor (`editorsContained: false`).
- Log dan screenshot tersedia di `.codex/task-6111-openproject/`.

Verifikasi visual menggunakan fixture DOM representatif, bukan aplikasi Proton live. Save/reopen dan payload FINA diuji dengan service mock. Setelah publish, cek mengetik Qty pada runtime Job Order dan cocokkan subtotal/PPN/total dengan FINA. Penyesuaian subtotal mengikuti contoh user; konfirmasi tim support masih terbuka.
