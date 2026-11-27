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
- Jika privilege menentukan kolom data yang perlu dipilih dan ditampilkan, siapkan
  tombol, filter, `columns`, dan `displayedColumns` pada Observable `beforeLoadData`
  di list yang menunggu hook tersebut. Bentuk key `displayedColumns` dari
  `column.data + column.title` sesuai konfigurasi akhir. Uji dengan daftar key
  awal yang belum memuat kolom berizin, lalu periksa hasilnya sebelum query pertama.
  [Contoh Stock Opname](<../../Endo Medika/stockOpnameList.js>)
- Jaga top-level action buttons tetap deklaratif kecuali project menggunakan pattern lokal lain.
- Delete flow ikuti Section 17 `patterns.md` (detail dulu, baru master untuk Biz-A; atau `delete: 1` untuk FINA).

## Paginasi kembali ke halaman pertama

Jika tombol Next aktif tetapi range tetap pada halaman pertama, periksa nilai
`paginator.pageIndex` dan filter sebelum dan sesudah `beforeLoadData`. Runtime
Page List Pelunasan memanggil hook itu sebelum `loadData` pada setiap event
paginasi. Reset indeks atau filter di dalam hook membuat query kehilangan
halaman atau filter yang baru dipilih.

Jalankan inisialisasi dan pemasangan listener sekali per kunjungan list. Bersihkan
state kunjungan dan subscription ketika keluar. Lakukan reset indeks saat
pengguna menjalankan Search atau Reset. Untuk regresi, jalankan urutan
`beforeLoadData` lalu `loadData` dengan filter aktif, pindah maju dan mundur,
dan periksa indeks serta filter yang dipakai query. Uji juga saat list dibuka
kembali. [List Pelunasan](../../Proton/pelunasanList.js) · [Tes](../../Proton/tests/pelunasanMulti.test.js)

## Mapping Warehouse pada transaksi antargudang

Jika user gudang pemberi memiliki privilege `confirm` tetapi request masuk
hilang dari list, periksa apakah filter cabang dan validasi detail sama-sama
mencakup ID gudang pemberi. Pada Item Transfer Request, mapping admin atau
member berlaku jika `REQUEST_WAREHOUSE_ID` atau `GIVING_WAREHOUSE_ID` cocok.
Bentuk grup filter `OR` untuk kedua kolom dan gabungkan grup itu dengan `AND`
ke filter status dan privilege. Gunakan cakupan yang sama saat membuka detail
melalui list atau URL langsung. [List](<../../Endo Medika/itemTransferRequestList.js>) · [Pemeriksaan detail](<../../Endo Medika/lib_itemTransfer.js>)

Normalisasi ID FINA sebelum mencocokkan dan pertahankan `NULL` pada gudang
pemberi yang belum ditentukan. ID `0` adalah ID gudang yang valid. Untuk Item
Transfer Request, mapping kosong menghasilkan list kosong dan `read all branch`
melewati filter gudang. Konfirmasi pengiriman tetap memerlukan privilege
`confirm`, status yang memenuhi syarat, dan referensi FINA yang sudah Posted.
Uji request keluar, request masuk, request yang melibatkan dua gudang lain,
mapping kosong, dan akses lintas cabang. Periksa hasil query list serta akses
detail request masuk. [Regresi list dan detail](<../../Endo Medika/test/itemTransferRequestList.test.js>)

## Validasi Sebelum Membuka Form

Jika form transaksi memerlukan status tertentu atau referensi FINA, gunakan
pemeriksaan yang sama dari handler aksi list. Periksa privilege, baca status
tersimpan dan referensi melalui helper query yang juga dipakai form, lalu
navigasikan setelah validasi sukses. Tampilkan kegagalan melalui `alert()` pada
list. Validasi di form tetap diperlukan untuk URL langsung dan perubahan data
antara klik dan pemuatan form.

Pada Item Transfer, handler `confirmClicked` memakai
`getItemTransferShippingRequest`. Status pada tampilan list bisa tertinggal dari
data tersimpan atau belum mencerminkan referensi native yang hilang. Uji request
yang belum siap dan referensi yang hilang dengan memastikan pesan muncul sebelum
navigasi. Uji juga request Posted yang memenuhi syarat sampai form terbuka.
[Handler list](<../../Endo Medika/itemTransferRequestList.js>) · [Helper query](<../../Endo Medika/lib_qry.js>) · [Tes](<../../Endo Medika/test/itemTransferRequestList.test.js>)
