# Proton 5805 — Job Order

Requirement: [Requirement SO.md](Requirement%20SO.md).

## Implementasi

- Menu **Sales → Job Order** membuka `Proton/SOList.js`; create/edit/view membuka `Proton/SOForm.js`.
- JO memakai **SO/SODET FINA sebagai satu-satunya penyimpanan transaksi** untuk create/edit/view/delete dan sumber SI. Tidak ada tabel, generator, snapshot, atau migrasi JOB_ORDER Biz-A. Status FINA: `2` Queue, `3` Waiting, `0` Proceeded, `1` Closed. Total list = `INVAMOUNT - CASHDISCOUNT`, ditambah `TAX1AMOUNT + TAX2AMOUNT` hanya bila `TAXINCLUSIVE` tidak aktif.
- Filter customer, periode, nomor JO, customer/description, dan beberapa status diterapkan bersama. Reset menghapus semua parameter. Sorting dan pagination memakai komponen list Biz-A.
- Filter **Order By** memuat customer saat dibuka, 20 customer per halaman. Scroll memuat halaman berikutnya; pencarian nama/kode customer memakai debounce 300 ms dan membatalkan request sebelumnya. Pilihan Semua menghapus filter customer.
- Query langsung `queryData` memakai posisi kolom SQL mulai dari 1: detail JO diurutkan pada posisi 1 (`SODET.SEQ`), customer pada posisi 3 (`PERSONDATA.NAME`).
- Hak aksi di **SOList** dibaca dari custom privilege menu **Job Order** melalui `getCustomPrivileges`: `create`, `view`, `edit`, dan `delete`. Link Sales Invoice memakai `view` untuk membuka invoice yang sudah ada; membuat invoice dari Waiting juga membutuhkan `create`. Custom privilege `sales invoice` dari konfigurasi lama tetap diterima. Delete memeriksa ulang izin terbaru. Form JO dan SI tidak melakukan pemeriksaan privilege.
- Nomor JO diinput manual. Kandidat duplikat dicari melalui filter `SO.SONO containing` pada FINA, lalu dicocokkan persis setelah trim dan uppercase di JavaScript. Ekspresi `UPPER(TRIM(...))` tidak ditempatkan pada `filter.column` query builder. Nomor transaksi sendiri dikecualikan saat edit.
- Customer, salesman, Terms, item, pajak, departemen, dan supir memakai master FINA. Nama Customer menjadi lookup yang hanya mencari NAME; Kode Customer menjadi lookup yang hanya mencari PERSONNO. Keduanya menyimpan ID customer yang sama dan saling mengisi saat dipilih/dikosongkan. Penjual menampilkan `SALESMAN.FIRSTNAME` dan bisa dicari lewat FIRSTNAME/LASTNAME. Lookup Supir mengembalikan teks INFO2 dari master EXTENDEDDET (EXTENDEDTYPEID = 3). Nama disimpan di **SODET.ITEMRESERVED4** per sequence, lalu diteruskan ke **ARINVDET.ITEMRESERVED4** saat membuat SI. Load JO/SI membaca kembali ITEMRESERVED4; nama kosong mengosongkan field tersebut.
- Checkbox Termasuk Pajak disimpan ke **SO.TAXINCLUSIVE**, bukan `SO.INCLUSIVETAX`. Harga SODET tetap sesuai input, termasuk pajak bila flag aktif. Payload INVAMOUNT, CASHDISCOUNT, dan Total Sub UI mengikuti nilai harga bruto FINA. Dasar pajak dipisahkan hanya untuk menghitung PPN. Reopen JO memuat kembali flag dan harga aslinya. SI dari JO meneruskan harga dan flag ke `ARINV.INCLUSIVETAX` sehingga pajak tidak ditambahkan dua kali.
- Navigasi tambah JO dan SI menggunakan string `"null"` sebagai parameter route form baru, mengikuti pola Proton dan menghindari `NG04008` dari segmen route null.
- Klik sel **Deskripsi Item** membuka dialog melalui event `grid.beforeEdit`, mengikuti pola batch number DOForm Endo Medika. Editor inline dihentikan lewat `afterEdit`; dialog menyediakan Description Option (TYPE_PRODUCT + TONASE) dan Description Manual. Textarea tidak memakai `maxLength`. Dialog tidak dibuka pada mode view dan tidak ditumpuk saat masih aktif atau focus kembali setelah ditutup.
- Diskon header dihitung dari Total Sub dan mengurangi dasar pajak. Include tax mengekstrak pajak dari nilai harga; Total Sub tetap sebesar jumlah item dan Total Pesan = Total Sub − Diskon. Jika include tax tidak aktif, PPN ditambahkan ke Total Pesan. Rate berasal dari master TAX. Listener menghitung dari nilai event terbaru karena `valueChanges` kontrol dapat berjalan sebelum parent form memperbarui nilainya.
- Pajak yang dipilih **per item** menjadi sumber perhitungan PPN dan selalu dikirim ke `SODET.TAXCODES`. Default pajak customer tidak menghapus pilihan tersebut; Kena Pajak otomatis aktif ketika ada pajak item. Item tanpa kode pajak menyumbang PPN nol. Payload header mengisi `TAX1ID`/`TAX2ID` sesuai pilihan item, dan jumlah pajak dikelompokkan pada slot kode yang sama untuk seluruh baris. FINA menyediakan dua slot pajak per dokumen; kode gabungan dikirim tanpa separator sesuai field TAXCODES. SI dari JO mempertahankan pilihan/slot pajak dan menghitung memakai nilai event terbaru.
- Save memvalidasi status terbaru dan menyimpan satu payload SO/SODET melalui `json2fina`. Nomor SOID dan sequence detail dipertahankan setelah konfirmasi save. Deskripsi header/detail dikirim langsung ke SO/SODET, mengikuti kapasitas field FINA; tidak ada salinan BLOB Biz-A.
- Edit/delete hanya untuk Queue. Edit tetap terlihat pada semua status; status selain Queue menampilkan pesan requirement. Guard juga berlaku saat membuka URL form langsung dan saat save. Setelah memeriksa privilege dan status Queue, delete langsung memanggil FINA. Penolakan foreign key dari FINA menampilkan notifikasi bisnis dan menghentikan success/reload.
- Sales Invoice hanya terlihat untuk Waiting/Proceeded. Waiting membuka SI baru dari sisa `QUANTITY - QTYSHIPPED`, dengan `SOID` dan `SOSEQ`. Sebelum save SI, status dan sisa qty diperiksa ulang. Proceeded membuka invoice yang sudah terhubung; jika ada beberapa invoice, user memilih invoice yang ingin dibuka.

## Persiapan deployment

1. Publish `SOForm.js`, `SOList.js`, `lib_jobOrder.js`, perubahan `lib_qry.js`, `SIForm.js`, dan `menu.json` ke konfigurasi Proton. Tidak diperlukan migrasi tabel JO.
2. Pada administrasi privilege usergroup Biz-A, aktifkan menu **Job Order** dan custom privilege `create`, `view`, `edit`, serta `delete` sesuai kebutuhan. Tidak perlu menambah privilege `sales invoice` untuk menampilkan link pada group yang sudah memiliki `view`/`create`. Untuk memenuhi requirement Admin Finance, berikan izin tersebut kepada group yang menaungi Pak Dicki, Pak Arya, Bu Ade, Bu Ita, dan Pak Davin; group lain mengikuti konfigurasi yang sama.
3. Verifikasi di runtime: create → reload, edit Queue, warning status lanjutan, filter/sorting/pagination, dan navigasi SI parsial. Cocokkan nomor, PO, Terms, detail, diskon, dan total dengan FINA. Untuk input termasuk pajak, pastikan TAXINCLUSIVE, harga asli, dan total tetap konsisten setelah reload dan saat membuat SI.

Publish belum dijalankan dari workspace ini. Belum ada smoke test terhadap database/API FINA live; batas penyimpanan deskripsi mengikuti kemampuan field/engine FINA. Jika tabel JOB_ORDER dari versi sebelumnya sudah dibuat, modul ini tidak lagi menggunakannya; tabel/data lama belum dihapus dari database.

Perbaikan lanjutan #6104–#6111 dan pemeriksaan read-only database lokal pada 13 Oktober 2026 dicatat di [6104-6111-job-order-fixes.md](6104-6111-job-order-fixes.md).

Perbaikan editor Qty #6111 dan penyesuaian Total Sub termasuk pajak pada 14 Oktober 2026 dicatat di [6111-qty-editor-inclusive-subtotal.md](6111-qty-editor-inclusive-subtotal.md).

## Verifikasi lokal

Jalankan dari root repository:

```powershell
node node_modules/jest/bin/jest.js Proton/tests --runInBand --silent
```

Tes khusus ada di `Proton/tests/jobOrder.test.js` dan `Proton/tests/jobOrderList.dom.test.js`: sinkronisasi lookup nama/kode customer, round-trip TAXINCLUSIVE/harga/Supir, total saat reload, query dan save/delete hanya ke FINA, validasi nomor/status, custom privilege hanya di list, sequence detail, payload deskripsi panjang, popup, lazy load/filter DOM, visibility action, serta qty parsial dan revalidasi sebelum save SI.
