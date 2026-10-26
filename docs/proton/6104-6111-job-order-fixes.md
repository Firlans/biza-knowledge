# Proton #6104–#6111 — Perbaikan Job Order

Implementasi lokal: 13 Oktober 2026. Task diambil ulang dari OpenProject; delapan task Proton berstatus **In progress**. Status OpenProject tidak diubah.

| Task | Penyebab / perubahan | Verifikasi |
|---|---|---|
| [#6104](https://iproj.my.id:5443/work_packages/6104) Diskon | Listener membaca parent `form.value` sebelum Angular memasukkan perubahan kontrol. `recalculate(key, value)` memakai nilai yang baru dipancarkan. | Rp10.000.000 × 10% = Rp1.000.000; 1% = Rp100.000. Tes mereproduksi kedua hasil salah sebelum perbaikan. |
| [#6105](https://iproj.my.id:5443/work_packages/6105) Link Sales Invoice | Database Biz-A hanya mendaftarkan create/edit/delete/view. Tombol sebelumnya memerlukan privilege tambahan `sales invoice`. Link mengikuti `view`; Waiting juga membutuhkan `create`, atau privilege invoice lama. | Admin dengan privilege yang ada mendapat link Waiting/Proceeded; view-only dapat membuka invoice Proceeded dan tidak dapat membuat invoice Waiting. Queue/Closed tetap disaring. |
| [#6106](https://iproj.my.id:5443/work_packages/6106) Penjual | Lookup menggunakan ekspresi concatenation sebagai nama kolom display. Display diganti kolom `FIRSTNAME`, search memakai FIRSTNAME/LASTNAME. | Konfigurasi lookup diuji; 10 salesman ditemukan di FINA lokal. |
| [#6107](https://iproj.my.id:5443/work_packages/6107) Customer | `customerid` menjadi lookup dengan display/search NAME saja. `customer_code` juga lookup dengan display/search PERSONNO saja. Keduanya menyimpan ID customer yang sama dan saling mengisi tanpa loop. | Memilih/dikosongkan lewat nama maupun kode menyinkronkan pasangannya; customer yang dipilih mengisi alamat/pajak dan ID payload. Lookup kode terisi saat reopen. Database memiliki 5.304 customer. |
| [#6108](https://iproj.my.id:5443/work_packages/6108) Termasuk Pajak | Nilai event digunakan langsung; Total Sub dihitung sebagai DPP sebelum diskon. Flag disimpan/dimuat lewat SO.TAXINCLUSIVE; harga SODET tetap sesuai input. List menghitung INVAMOUNT − CASHDISCOUNT dan hanya menambah pajak bila flag tidak aktif. SI dari JO mengikuti flag sumber. | Input Rp1.000.000, rate 11%: inclusive DPP Rp900.900,90, PPN Rp99.099,10, total Rp1.000.000; exclusive DPP Rp1.000.000, PPN Rp110.000, total Rp1.110.000. Save/reopen mempertahankan flag/harga/Supir dan SI tidak menambah pajak dua kali. Query list diuji pada SO FINA lokal dengan TAXINCLUSIVE=1 dan =0. |
| [#6109](https://iproj.my.id:5443/work_packages/6109) Nama Supir | Save membaca `sodet.getRawValue()` agar memakai kontrol baris terbaru. Lookup master Supir mengembalikan teks INFO2; nama disimpan langsung pada SODET.ITEMRESERVED4 dan diteruskan/dimuat melalui ARINVDET.ITEMRESERVED4 pada SI. Clearing mengirim string kosong; ID numerik dan nama lebih dari 80 karakter ditolak pada JO. | Dua baris dengan nama Yasir/Sukandi tetap berbeda tanpa perubahan item/qty/harga/departemen. Save/reopen dan JO → SI mempertahankan nama. Metadata FINA mengonfirmasi ITEMRESERVED4 adalah VARCHAR(80) di SODET/ARINVDET; contoh native berisi ASEP/NANO. |
| [#6110](https://iproj.my.id:5443/work_packages/6110) Delete Queue | Setelah pemeriksaan privilege dan status Queue, delete langsung memanggil FINA. Penolakan FK dari FINA diterjemahkan menjadi notifikasi bisnis. | Delete tidak menjalankan query relasi; error FINA mencegah pesan sukses dan reload. |
| [#6111](https://iproj.my.id:5443/work_packages/6111) Alignment | Kolom numerik dan header memakai lebar serta alignment kanan yang sama. Grid memiliki scroll lokal; style hanya berlaku pada kelas `proton-job-order-grid` dan dibersihkan saat destroy. | 12 kasus fixture browser: Material lama/MDC, 390/1280/1920 px, terang/gelap. Semua batas kolom sejajar dan halaman tidak melebar; screenshot diperiksa. |

## Penyimpanan pajak dan PPN per item

Kondisi `model.customeristaxable` sebelumnya mengosongkan kode pajak pada payload dan menonaktifkan hitungan meskipun user sudah memilih pajak item. Hitungan sekarang memakai tarif master TAX untuk setiap baris, setelah diskon dan pemisahan DPP bila TAXINCLUSIVE aktif. Baris tanpa pajak menyumbang PPN nol. Kena Pajak otomatis aktif ketika terdapat pilihan pajak item.

Payload SO menyimpan kode pada `SODET.TAXCODES` dan memilih `SO.TAX1ID`/`SO.TAX2ID` dari pajak item. TAX1AMOUNT/TAX2AMOUNT dikelompokkan menurut slot pajak dokumen, termasuk ketika urutan kode antarbaris berbeda. Field TAXCODES FINA berukuran tiga karakter; kode gabungan dikirim tanpa separator. Kode native seperti `11`/`PP` mempertahankan dua slot pajaknya. Dokumen yang memerlukan lebih dari dua slot ditolak sebelum save. Mengosongkan pilihan terakhir mengosongkan kode detail dan kedua ID/amount header.

SI dari JO mempertahankan kode serta ID pajak tersebut. Listener SI memakai detail terbaru dari event ketika parent form belum memperbarui nilainya. Regresi mencakup pilihan 11%/12% pada item berbeda, item tanpa pajak, customer tanpa default pajak, harga termasuk pajak, diskon, kode numerik, kode gabungan, pengosongan pajak, serta penerusan ke SI.

## File implementasi untuk publish

- `Proton/SOForm.js`
- `Proton/SOList.js`
- `Proton/lib_jobOrder.js`
- `Proton/lib_qry.js`
- `Proton/SIForm.js`

Tidak diperlukan migrasi schema atau perubahan privilege database untuk perbaikan ini. `SIForm.js` memakai helper hitungan yang sama; seluruh tes SI dan Proton dijalankan untuk memeriksa dampaknya.

## Hasil pemeriksaan

- **38 suite, 925 tes lulus**: `node node_modules/jest/bin/jest.js Proton/tests --runInBand --silent`.
- Database diperiksa melalui transaksi read-only, lalu rollback:
  - Biz-A: `C:\Users\user.DESKTOP-ULVVQS2\Documents\imamatek\Proton\BIZ-A PROTON.FDB`.
  - FINA: `C:\Users\user.DESKTOP-ULVVQS2\Documents\imamatek\Proton\FINA PROTON 30122025.FDB`.
- Artefak pemeriksaan ada di `.codex/proton-6104-6111/`: `item-tax-tests.log` (hasil tes terakhir), `biza-db.log`, `fina-db.log`, `taxinclusive-db.log`, `itemreserved4-db.log`, `item-tax-db.log`, SQL pemeriksaan, `grid-results.json`, dan screenshot fixture grid.
- Regresi mencakup parent-value lag, customer selection/reopen, payload Supir per baris, diskon/PPN, invoice navigation/permission, dan validasi delete.

Publish belum dijalankan. Pemeriksaan database adalah read-only; save/delete `json2fina` diuji dengan service mock, bukan terhadap server FINA live. Pemeriksaan visual memakai fixture representatif DOM Material, bukan sesi aplikasi Biz-A live. Setelah publish, verifikasi lookup, save/reopen dua baris Supir, dan navigasi invoice pada runtime Proton.
