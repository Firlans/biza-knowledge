# Biz-A Control Center: metadata, source domain, dan alur script

Gunakan saat membuat atau memeriksa App Config, `APPLICATION_CONFIG`,
`DOMAIN_CONFIG`, menu domain, dan hubungan script dengan konfigurasi UI.

## 1. Metadata wajib disertakan

Setiap konfigurasi aplikasi dan domain harus menyertakan `metadata` pada object
yang dikembalikan `get`. Versi aplikasi dan versi domain dibaca dari konfigurasi
masing-masing; mengisi versi aplikasi tidak mengisi versi domain.

Contoh metadata aplikasi mengikuti pola ROBYRAJASA/procurementconfig:

```javascript
metadata: {
    appId: 'biz-a-frs',
    name: 'Biz-A FRS',
    version: '1.0.0',
    environment: 'dev',
},
```

Contoh metadata domain Layer 3:

```javascript
metadata: {
    id: 'frs',
    name: 'frs',
    version: '1.0.0',
    rendererVersion: '1.0.0',
    layer: '3',
    description: 'Domain FRS',
},
```

Domain memerlukan nama yang tidak kosong dan versi semantik, misalnya `1.0.0`.
Pertahankan field metadata lain sesuai kontrak runtime dan jenis konfigurasi;
contoh di atas bukan pernyataan bahwa semua field diperiksa oleh validator
yang sama. Jangan menambahkan metadata domain ke file library biasa: library
dan konfigurasi domain merupakan jenis artefak yang berbeda.

Jika muncul `DOMAIN_CONFIG metadata.version is required.`, periksa isi
konfigurasi domain yang benar-benar dikirim/disimpan, hasil parsing `get`,
dan versi domain tersebut. Metadata versi yang terlihat di `application.js`
saja tidak membuktikan bahwa payload domain sudah lengkap.

## 2. Source mengikuti nama domain yang diunggah

`application.domains[key].source` harus sama dengan nama dan versi domain yang
diunggah pada App Config Biz-A. Periksa record yang benar-benar tersimpan.
Pada upload config melalui CLI lokal, nama dan versi record berasal dari
`metadata.name` dan `metadata.version` pada masing-masing file domain.

```javascript
// Metadata konfigurasi domain yang diunggah.
metadata: {
    name: 'Master Data Procurement',
    version: '1.0.0',
},

// Registrasi pada application.js.
domains: {
    masterdata: {
        source: 'Master Data Procurement@1.0.0',
        alias: 'masterdata',
    },
},
```

| Bagian | Peran |
| --- | --- |
| `masterdata` pada key `domains` | Referensi domain pada menu aplikasi |
| `Master Data Procurement@1.0.0` | Nama dan versi config domain yang dimuat |
| `alias: 'masterdata'` | Nama pendek domain dalam aplikasi |
| `masterConfig.js` | Nama file lokal yang berisi konfigurasi |
| `metadata.id` | Identitas metadata, bukan nama source untuk lookup config |

Nama folder, file, key domain, alias, dan `metadata.id` tidak harus sama dengan
nama record yang diunggah. Jangan membentuk source dari salah satunya tanpa
memeriksa nama record domain. Nama dengan spasi dapat digunakan; pertahankan
nama persis seperti yang diunggah beserta versinya.

Jika metadata tetap `Master Data Procurement@1.0.0`, penggunaan source
`masterdata@1.0.0` merupakan ketidakcocokan konfigurasi. Ini temuan terpisah
dari pembuktian penyebab suatu exception pada browser.

## 3. Analisis cara script bekerja

Telusuri hubungan berikut sesuai entry point yang benar-benar dibuka:

1. **Menu aplikasi:** `navigation.menus` menentukan route dan domain. Untuk
   `['./form', 'itemCategoryForm', null]`, domain dipilih melalui key registrasi
   menu, sedangkan `itemCategoryForm` adalah nama entry point.
2. **Config domain:** source mengarah pada nama/versi record domain yang dimuat.
   Periksa bahwa config hasil lookup memang config yang dimaksud.
3. **Entry point:** `ui.entryPoints.itemCategoryForm.entity` harus tersedia
   pada `model.entities`, dan `structureRef` harus tersedia di `ui.structures`.
   Periksa Home/`main` juga, bukan hanya menu transaksi.
4. **Struktur UI:** field/key harus sesuai dengan atribut dan relasi entity
   yang digunakan; tipe struktur form/list harus sesuai dengan route menu.
5. **Event binding:** cocokkan `emitter` dan `trigger` terhadap kontrol/lifecycle
   yang memicu event. Periksa `args`, termasuk `$ref` dan `$default`, agar
   diketahui nilai apa yang diteruskan ke handler.
6. **Handler:** nama pada `eventBindings[].handler` mengacu pada deklarasi event
   di `events`. Handler library seperti
   `procurement.masterDataLib.onItemCategoryAfterLoadData` mengarah pada fungsi
   `onItemCategoryAfterLoadData` di library `masterDataLib` milik paket
   `procurement`.
7. **Library:** pastikan deklarasi `libraries`, fungsi yang diekspor, pemanggilan
   `this.doFunction`, dan paket library yang dimuat di target sesuai. Namespace
   library `procurement` dapat berbeda dari alias domain config `masterdata`.
   Periksa bahwa paket library sudah ditambahkan ke Biz-A target. File library
   yang ada lokal dan upload config saja tidak membuktikan library sudah
   tersedia di server; lihat kasus dan perintah pada bagian 5.
8. **Efek runtime:** periksa perubahan model/form, query, respons, navigasi, atau
   notifikasi yang dilakukan handler pada jalur yang sedang dianalisis.

Pada paket Biz-A lokal yang diperiksa, publisher membentuk template form/list,
menetapkan domain/source dan entry point, serta memasang `useLibrary` untuk
module library yang dikonfigurasi atau diturunkan dari handler. Template
meneruskan lifecycle ke domain service. Hasil pembuatan template membuktikan
wiring yang dihasilkan, bukan keberhasilan pemuatan library atau query pada
server target.

Jangan menyimpulkan semua script bekerja hanya karena menu dapat dibuka.
Tuliskan entry point yang diperiksa, handler yang ditemukan, dependency yang
diperlukan, input/hasil yang diamati, dan bagian yang belum diverifikasi.

## 4. Batas verifikasi

| Pemeriksaan | Bukti yang dihasilkan |
| --- | --- |
| Parsing config dan metadata | Object config dapat dibaca; nama/versi terisi |
| Source dan record domain | Nama/versi registrasi cocok dengan config upload |
| Referensi menu/entity/structure | Target konfigurasi tersedia dan konsisten |
| Handler pada library lokal | Fungsi yang dirujuk ada dalam kode lokal |
| Upload paket library ke Biz-A target | Paket script/library sudah dikirim ke target; periksa hasil perintah |
| Pembuatan template lokal | Template dan referensi source/library dapat dibentuk |
| Uji pada browser/server | Jalur yang benar-benar dicoba berjalan pada target tersebut |

Laporkan level pemeriksaan secara terpisah. Pemeriksaan lokal tidak memastikan
bahwa config/library versi yang sama sudah diunggah, schema database tersedia,
atau eksekusi browser/server berhasil.

## 5. Penyebab error FRS/procurement: library belum ditambahkan

Pada rekaman percobaan, menu tampil dan pembukaan halaman menampilkan:

```text
Cannot read properties of undefined (reading 'id')
```

**Status: penyebab dikonfirmasi pengguna. Library belum ditambahkan ke Biz-A.**

Penambahan library dilakukan menggunakan perintah yang disampaikan pengguna:

```powershell
biza add -s https://server.biz-a.id --sub frs
```

Jalankan dari folder paket library yang akan ditambahkan, misalnya `procurement/`
untuk handler `procurement.masterDataLib.*`. CLI menggunakan working directory
sebagai sumber file jika direktori lain tidak diberikan. Mengunggah folder
config seperti `procurementconfig/` atau `FRS/` tidak menggantikan upload paket
library yang dirujuk handler.

Untuk target lain, gunakan server dan subdomain yang sesuai dengan penugasan;
`https://server.biz-a.id` dan `frs` adalah parameter kasus ini, bukan default
universal. Setelah menambahkan library, periksa hasil command dan uji ulang
halaman yang sebelumnya gagal untuk memverifikasi eksekusi handler di target.
Pencatatan perintah pada dokumentasi bukan instruksi untuk menjalankan upload
saat pengguna hanya meminta pembaruan skill.

Ketidakcocokan source dan referensi entity yang tidak dideklarasikan tetap
merupakan temuan konfigurasi terpisah, bukan penyebab error kasus ini yang
dikonfirmasi pengguna. Keberadaan 53 handler dalam library lokal pada pemeriksaan
sebelumnya tidak membuktikan paket library sudah ditambahkan ke Biz-A.

Konfirmasi penyebab pada bagian ini berasal dari pengguna; agent tidak
menjalankan upload atau uji server ulang saat memperbarui dokumentasi. Jangan
menganggap setiap error `reading 'id'` pasti memiliki penyebab yang sama.

## Lokasi kode untuk verifikasi kontrak

- `node_modules/biz-a-cli/bin/app.js`: `collectConfigUploads`, metadata nama dan
  versi file yang diunggah, pemisahan aplikasi dan domain.
- `node_modules/biz-a-cli/engine/domain/appConfig.js`:
  `parseConfigForVersion`, `extractConfigVersion`, `parseDomainConfig`,
  `readConfigRows`.
- `node_modules/biz-a-cli/engine/domain/applicationConfig.js`:
  `collectFormTargets`, `resolveDomainLibraryModules`,
  `buildHardcodedTemplateContent`, `buildPublishBodyFromConfigs`.
- `node_modules/biz-a-cli/engine/cc/appMenus.js`: pemeriksaan menu dan domain.
- `ROBYRAJASA/branches/dev/src/config/`: contoh pemisahan aplikasi dan domain.
- `procurementconfig/`: contoh konfigurasi aplikasi/domain; periksa konsistensi
  nama dan referensinya sebelum menggunakan contoh tersebut.
- `procurement/`: implementasi handler yang dirujuk oleh contoh procurement.
- `.agents/docs/biz-a-control-center-spec-v1.0.md`: acuan desain Control Center;
  bedakan requirement desain dengan perilaku runtime yang sudah dibuktikan.
