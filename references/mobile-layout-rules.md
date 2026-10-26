# Biz-A Mobile Layout Rules

Gunakan reference ini saat membuat layout mobile dari prototipe atau mengubah
form, filter, list, detail-grid, dialog, dan menu master menjadi responsif.
Baca bersama [visual-design-theming-index.md](visual-design-theming-index.md).
Reference implementasi lokal: Missi Idea `lib_ui`, `quotationForm`, dan
`masterDataForm`. Adaptasikan kontrak runtime dan aturan bisnis setiap project.

## Problem signals

- Header/master form atau filter masih dua kolom sempit pada HP.
- Pasangan tanggal perlu bersebelahan tetapi semua field ditumpuk ke bawah.
- List memiliki data dan jumlah baris, tetapi kartu kosong atau tombol hilang.
- Warna kartu tetap polos/abu-abu atau menu tidak memiliki keterangan prototipe.
- Lookup hanya menampilkan placeholder saat membuat data baru.
- Layout lolos fixture tetapi berbeda pada runtime Angular/Biz-A.
- Callback tertunda gagal setelah navigasi, misalnya fungsi kalkulasi tidak ada.

## Root causes

| Gejala | Penyebab yang perlu diperiksa |
|---|---|
| Header/filter tetap sempit | Struktur `fieldGroup` masih membagi field ke dua grup; `col-6`, fixed width, flex basis, dan wrapper Formly belum ditangani. |
| Tanggal tidak bisa berdampingan | Aturan mobile `flex-direction: column` diterapkan juga pada grup pasangan tanggal. |
| Kartu list kosong | Pemetaan hanya mengandalkan header/posisi kolom; renderer dapat menyembunyikan atau tidak membuat sel. Native `td`/`span` juga dapat masih tersembunyi. |
| Baris atau aksi salah | Header dengan `role="row"` ikut dihitung, datasource bukan halaman yang dirender, atau callback menyimpan ID lama. |
| Menu master polos | Tombol teks dianggap cukup; ikon, surface, deskripsi, hierarchy, dan target sentuh prototipe belum dibuat. |
| Aksen tidak berwarna | Token theme netral dipakai untuk kategori yang prototipenya membutuhkan warna semantik berbeda. |
| Lookup tidak tersedia | `readonly`, mode, aturan client, atau `dbIndex` salah; perubahan kolom tidak sampai ke grid yang sudah aktif. |
| Error setelah kembali ke list | Timer/subscription/observer masih hidup dan membaca `this.f()` dari halaman baru. |

## Corrected approach

### 1. Tentukan struktur sebelum menulis CSS

- Baca prototipe dan koreksi terbaru user. Tentukan urutan field, field satu
  kolom, pasangan field, ringkasan, dan aksi; jangan memakai satu aturan untuk
  seluruh layar.
- Header panjang dan filter pencarian memakai satu kolom pada mobile. Ratakan
  dua grup header menjadi satu urutan jika grup tersebut mengunci layout lama.
- Pasangan tanggal merupakan pengecualian eksplisit: dua kolom dengan lebar
  sama bila user meminta bersebelahan. Field lain tetap mengikuti urutannya.
- Gunakan `col-12` untuk field filter mobile, dengan `col-md-*`/`col-lg-*`
  sesuai layout desktop. Hindari fixed width/min-width yang memperlebar body.
- Tambahkan class milik module pada field/group; jangan bergantung pada
  `nth-child` untuk menentukan makna field.

Contoh CSS pasangan tanggal dalam scope helper halaman mobile:

```css
@media (max-width: 767.98px) {
    .mi-page .mi-quotation-period {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        align-items: stretch !important;
        gap: 8px;
    }
    .mi-page .mi-quotation-period > formly-field {
        width: 100%;
        min-width: 0;
    }
}
```

`minmax(0, 1fr)` mencegah ukuran intrinsik kontrol memperlebar kolom. Periksa
lebar form-field, infix, ikon datepicker, label, dan tanggal berisi nilai pada
runtime. Override internal Material hanya jika DOM target sudah diperiksa;
scope pada grup tanggal. Separator `s/d` jangan mengambil kolom ketiga jika
desain meminta dua kontrol dengan lebar sama.

### 2. Reuse helper tampilan dengan scope halaman

- Pisahkan CSS, dekorasi DOM, dan cleanup ke library UI lokal yang dipakai
  melalui `useLibrary`. Query, save, dan authorization tetap pada alur bisnis.
- Pasang style/observer melalui lifecycle setup; setelah root tersedia,
  batasi observer pada `app-form`/`app-list` yang aktif.
- Pertahankan kontrol, nilai input, handler native, readonly, sorting, dan
  pagination. Utamakan perubahan struktur deklaratif dan CSS.
- Hindari observer/timer berulang. Dekorasi harus idempotent: label, deskripsi,
  sel, dan tombol yang sama tidak dibuat dua kali. Tulis text hanya jika berubah.
- Jika mengamati `characterData`, pastikan perubahan buatan helper berhenti
  setelah DOM mencapai state yang sama; jangan membuat loop dekorasi.

### 3. Bedakan native list dan form detail-grid

| Jenis | Metadata | Perilaku yang harus dipertahankan |
|---|---|---|
| Native `app-list` | `columns[].data`, `title`, `button`; datasource list | Filter, urutan baris, pagination, lookup display, typed record ID. |
| Form detail-grid untuk hasil list | `props.columns[].key`, `label`, `buttons` | Data dari alur form, status, tanggal, money, aksi dokumen. |
| Detail-grid editable | Field/grid aktif dan kontrol per baris | Input asli, perhitungan, lookup, readonly, Add/Delete sesuai mode. |

- Dukung DOM aktual: `table/tbody/tr/td` dan `mat-table/mat-row/mat-cell`.
- Cocokkan class `mat-column-*`/`cdk-column-*` dengan `key` atau `data` serta
  label/title yang dinormalisasi. Header membantu, tetapi tidak wajib tersedia.
- Contoh native class: `cdk-column-PROGRAM_TYPE-IDAction`. Jangan mengasumsikan
  class selalu hanya berisi nama key lowercase.
- Gunakan index kolom hanya sebagai fallback setelah memeriksa kolom yang
  hilang atau berubah urutan. Field yang sama harus tetap memperoleh labelnya.
- Pilih satu kolom judul per kartu. Pada PO, `so_no` dapat menjadi judul;
  `quotation_no` tetap nilai berlabel, agar kedua nomor tidak bertumpuk.

Untuk list kosong, periksa secara terpisah: response data, datasource aktif,
keberadaan sel, pemetaan kolom, lalu computed `display`/`visibility` sel dan
wrapper nilainya. Jangan menyimpulkan datanya tidak ada dari tampilan kosong.

### 4. Fallback data/aksi hanya setelah kontraknya jelas

- Periksa `this.dataSource.dataSubject.value`/`_value` pada runtime. `onPipe`
  dapat menyimpan data untuk dekorasi, tetapi harus mempertahankan bentuk dan
  return pipeline asli.
- Cocokkan raw key, full data path, alias, dan casing sesuai response aktual.
  Jangan memakai `value || '-'`: `0` dan `false` merupakan nilai valid.
- Format boolean menjadi `Aktif`/`Tidak aktif` atau `Default`/`Non-default`.
  Jika nilai native disembunyikan untuk badge, pastikan hanya satu representasi
  terlihat dan kontrol asli tidak ikut disembunyikan.
- Isi sel kosong dengan `textContent`; jangan menyisipkan data user sebagai
  HTML. Jangan mengganti lookup display/native text yang sudah tersedia.
- Jika sel kode/aksi benar-benar tidak dirender, fallback sel dapat dibuat
  dari metadata dan data baris. Hapus sel buatan saat sel native tersedia.
- Sebelum memakai index baris, keluarkan header `role="row"` dari daftar.
  Pastikan urutan datasource sama dengan DOM setelah sorting/pagination.
  Jangan terapkan asumsi ini pada grouped/virtualized list tanpa verifikasi.
- Tombol fallback hanya boleh mengikuti aksi deklaratif yang memang diizinkan.
  Master Missi Idea tidak memakai privilege; ini bukan aturan untuk semua list.
  Jangan memunculkan kembali aksi yang disembunyikan authorization.
- Pertahankan ID number/string sesuai kontrak handler. Tanpa ID yang diketahui,
  jangan buat aksi. Saat klik, baca ID baris saat ini agar pagination tidak
  memakai ID dari halaman sebelumnya.
- Prioritaskan tombol native dan handlernya. Hapus tombol fallback saat native
  tersedia; jangan menampilkan dua versi Lihat/Ubah/Hapus.

### 5. Kartu master mengikuti isi prototipe

- Hub master memakai satu kartu navigasi per kategori: ikon dalam badge
  berwarna, judul, deskripsi singkat, dan petunjuk navigasi.
- Seluruh kartu harus memiliki target klik yang jelas melalui button/link
  asli. Deskripsi yang menimpa area button tidak boleh menyerap klik.
- List master memakai ikon/aksen kategori, identitas record, nilai berlabel,
  status, dan aksi. Tambahkan deskripsi halaman yang sesuai kategori.
- Utamakan token theme untuk surface, teks, border, dan muted text. Jika
  kategori membutuhkan palette berbeda, sediakan variable semantik lokal
  dengan fallback sesuai prototipe; jangan mengganti theme global.
- Periksa warna hasil computed style: token secondary/tertiary dapat netral
  pada theme target. Ikon, teks, dan badge harus tetap terbaca pada light/dark.
- Gunakan spacing konsisten dan target sentuh mobile minimum 48px. Pagination
  dan toolbar harus muat tanpa membuat body scroll horizontal.
- Muat font ikon pada preview. Nama ligature seperti `description` yang tampil
  sebagai teks merupakan font belum tersedia, bukan ikon yang sudah tervalidasi.

### 6. Lookup dan kolom dinamis tetap mengikuti aturan bisnis

- Pisahkan masalah lookup dari CSS: periksa `dbIndex`, opsi, readonly, status,
  dan mode New/Edit/View/Approve.
- Jangan memaksa lookup readonly setelah initial load tanpa aturan bisnis.
  Pada Quotation, form baru dapat memilih pajak; client yang dipastikan Non PPN
  mengunci/mengosongkannya. Mode View/Approve tetap mengunci seluruh detail.
- Simpan konfigurasi dasar sebelum perubahan dinamis. Buat array kolom baru
  dengan copy yang mempertahankan function, lalu refresh grid aktif beserta
  data detail terbaru dari kontrol agar input tidak hilang.
- Jangan `structuredClone` konfigurasi kolom berisi callback. Jangan menangkap
  readonly sementara sebagai default permanen saat berganti mode/client.
- Detail pola ada pada reference kolom dinamis dan state sync di bawah.

### 7. Cleanup sebelum dan saat navigasi

- Simpan dan bersihkan timer, subscription, observer, serta style helper.
- Capture fungsi terikat sebelum menjadwalkan callback. Callback tertunda
  tidak boleh mencari fungsi melalui registry `this.f()` halaman baru.
- Untuk komponen yang digunakan ulang saat navigasi, hentikan pekerjaan
  tertunda sebelum `router.navigate`, lalu lakukan cleanup idempotent pada
  `onDestroy`.
- Hapus class kategori, CSS variable ikon, deskripsi, label boolean, sel/tombol
  fallback, dan data cache milik helper. Warna/data halaman lama tidak boleh
  terbawa saat root `app-list` dipakai ulang.

## Implementation checklist

- [ ] Struktur mengikuti prototipe dan koreksi terakhir user; pasangan tanggal eksplisit.
- [ ] Lebar 360/390px tidak membuat body scroll horizontal atau kontrol terpotong.
- [ ] Metadata tetap benar tanpa header, dengan kolom hilang/berubah urutan.
- [ ] Kode, nama, status false/zero, lookup display, serta ID baris tetap benar.
- [ ] Satu judul per kartu; aksi asli/cadangan tidak diduplikasi atau melanggar authorization.
- [ ] Sorting/pagination dan pergantian data tidak memakai nilai atau ID lama.
- [ ] New/Edit/View/Approve, client PPN/Non PPN, serta input detail tetap berfungsi.
- [ ] Ikon, deskripsi, badge, minimum touch target, dan light/dark diperiksa.
- [ ] Navigasi membersihkan observer, timer, subscription, class, dan fallback DOM.

## Verification and limits

Gunakan browser untuk memeriksa bounding box pasangan tanggal, overflow body,
computed visibility, ikon, dan warna. JSDOM tidak menghitung layout CSS seperti
browser. Untuk label/date control, gunakan juga nilai terisi dan DOM Material
yang menyerupai runtime; input HTML sederhana tidak membuktikan hasil Angular.

Uji mobile 360/390px, tablet 768px, dan desktop 1280px sesuai scope, dengan
light/dark. Pastikan perubahan scheme benar-benar diterapkan; perubahan hash
saja tidak menjalankan ulang script inisialisasi halaman. Periksa computed token
atau reload preview sebelum menyatakan dark mode sudah diuji.

Tes perilaku yang bermakna mencakup headerless/omitted cells, ID berubah setelah
pagination, false/zero, renderer native menyusul fallback, lookup readonly, input
detail bertahan, dan cleanup navigasi. Perubahan CSS kecil cukup diperiksa melalui
render; jangan membuat unit test yang hanya menyalin selector implementasi.

Fixture dan mock API merupakan pemeriksaan lokal. Nyatakan batas ini pada hasil
kerja; verifikasi runtime Biz-A target diperlukan untuk perilaku renderer dan
integrasi database. Sebutkan library dan module yang perlu di-upload ulang.

## Related files and patterns

- [visual-design-theming-index.md](visual-design-theming-index.md)
- [form-rules.md](form-rules.md), [list-rules.md](list-rules.md)
- [form-model-value-sync-problem.md](form-model-value-sync-problem.md)
- [detail-grid-dynamic-column-expression-problem.md](detail-grid-dynamic-column-expression-problem.md)
- [detail-grid-state-sync-problem.md](detail-grid-state-sync-problem.md)
- [detail-grid-scroll-sizing-alignment-problem.md](detail-grid-scroll-sizing-alignment-problem.md)
- [list-row-action-dom-state-problem.md](list-row-action-dom-state-problem.md)
- [list-action-button-wrap-problem.md](list-action-button-wrap-problem.md)
- [Missi Idea/lib_ui.js](<../../Missi Idea/lib_ui.js>)
- [Missi Idea/quotationForm.js](<../../Missi Idea/quotationForm.js>)
- [Missi Idea/masterDataForm.js](<../../Missi Idea/masterDataForm.js>)
- [Prototipe Quotation dan PO Client](<../docs/missie idea/UI Mobile Fitur Quo - PO Client.md>)
- [Tes layout/aksi](<../../Missi Idea/tests/responsiveUi.test.js>),
  [tes lookup pajak](<../../Missi Idea/tests/quotationTaxLookup.test.js>), dan
  [tes lifecycle](<../../Missi Idea/tests/quotationLifecycle.test.js>)
