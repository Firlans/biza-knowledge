# Biz-A Design Pattern Recognition

Wajib dibaca sebelum membuat atau mengubah setiap file proyek sesuai
`pattern-recognition.rules.instructions.md`. Untuk file nonkode, kenali pola
struktur/schema dan konvensi file sejenis; panduan design pattern JavaScript
berikut diterapkan pada bagian yang relevan, termasuk form, list, dan helper
Biz-A. Diadaptasi dari `javascript_design_patterns.md`
(contoh pengguna: Functional & Object-Based Design Patterns in JavaScript).
Referensi ini mandiri; file Downloads tidak diperlukan pada penggunaan berikutnya.

## Cara mengenali dan memilih

1. Baca target, caller, dan library dalam `useLibrary`. Catat bagian konkret
   yang berulang atau bervariasi: pembuatan config, mapping data, algoritma,
   listener, atau urutan operasi async.
2. Cocokkan tanggung jawab serta aliran data dengan tabel berikut. Nama function
   saja belum membuktikan pattern; `buildPayload` biasa belum tentu Builder.
3. Bedakan **pattern yang sudah ada** dengan **kandidat perubahan**. Tunjukkan
   file/function pendukung, manfaat, serta behavior yang harus dipertahankan.
4. Reuse helper yang setara sebelum menambah abstraksi. Pilih fungsi biasa atau
   object literal jika sudah cukup; tidak ada target jumlah pattern per module.
5. Untuk implementasi, gunakan functional/plain object sesuai export Biz-A.
   Jangan menambah hierarki `class`/`new` untuk pattern ini. Constructor framework
   yang sudah diperlukan, seperti dialog config, tetap mengikuti contract aslinya.
6. Verifikasi output, side effect, binding `this`, scope state, serta error dan
   completion async sesuai bagian yang berubah. Pengenalan pattern saja tidak
   mengizinkan refactor di luar permintaan pengguna.

## Referensi tambahan dari Learning Patterns

Untuk konsep, trade-off, dan halaman sumber buku pengguna, baca
[Learning Patterns - Referensi Utama](learning-patterns-reference.md). Sumber PDF
tersimpan di `.agents/docs/learning-patterns-final-v1.1.pdf`.

| Signal yang perlu diperdalam | Referensi yang dibaca |
|---|---|
| Factory, Module, Singleton, Observer, Proxy, Prototype, Mixin, Mediator/Middleware, Flyweight, Command | [JavaScript Patterns](learning-patterns-javascript-patterns.md) |
| Provider, Container/Presentational, Render Props, Hooks, HOC, Compound Component | [Component Patterns](learning-patterns-component-patterns.md) |
| CSR/SSR/SSG, hydration, islands, loading sequence, import/splitting, PRPL, tree shaking, preload/prefetch, virtualization | [Rendering dan Performance](learning-patterns-rendering-performance.md) |

Load hanya referensi yang match. Gunakan prinsip functional/plain object dan
contract runtime Biz-A pada dokumen ini ketika mengadaptasi contoh dari buku;
kode class/React serta API historis sumber bukan template otomatis untuk Biz-A.

## Peta signal ke pattern

| Signal dalam kode/kebutuhan | Pattern | Penerapan Biz-A | Kapan fungsi biasa lebih tepat |
|---|---|---|---|
| Struktur object/config berulang dengan parameter berbeda | Factory Function | Function menghasilkan field, column, filter, atau payload baru | Satu object literal sederhana tanpa variasi |
| Banyak opsi opsional dikumpulkan bertahap sebelum hasil final | Functional Builder | Builder config/filter dengan `build()` dan state per instance | Semua input sudah tersedia; cukup `build...` dengan argumen/options |
| State private perlu dibagi beberapa operasi dalam satu instance | Module / Closure | Closure lokal dalam factory `get`, API berupa plain object | Helper pure tanpa state; cukup `functions` yang ada |
| Resource benar-benar harus dipakai bersama dalam scope yang jelas | Singleton via Closure / Module | Reuse service yang memang dikelola runtime terlebih dahulu | State form, user, API, atau `dbIndex` berbeda antar instance |
| Perbedaan nama kolom, satuan, atau shape data antar sumber | Functional Adapter | `normalize...` hasil DB atau `build...` payload pada library domain/query | Mapping satu kali yang sudah jelas di lokasi pemakaian |
| Algoritma berbeda dipilih oleh jenis/mode dengan contract yang sama | Strategy / Function Map | Peta function kalkulasi atau mapping per tipe dokumen | Label/status statis cukup value map; dua cabang pendek cukup conditional |
| Perilaku tambahan yang sama membungkus beberapa operasi | Decorator / Higher-Order Function | Tambahan timing, validasi, atau logging dengan return/error tetap sama | Wrapper hanya mengganti nama function atau mempersulit trace |
| Perubahan nilai memicu beberapa reaksi | Observer / Pub-Sub | Reuse `valueChanges` dan mekanisme event runtime yang sudah ada | Satu aksi langsung dapat memanggil helper; tidak perlu event bus |
| Tahapan pemrosesan dengan context/contract konsisten perlu dirangkai ulang | Middleware / Pipeline | Rangkaian validasi/transformasi; async mengikuti flow module | Urutan save tetap cukup orchestration linear dengan helper bernama |
| Batch independen perlu membatasi jumlah operasi yang berjalan | Async Queue / Concurrency Control | Reuse mekanisme async yang tersedia; batasi concurrency batch | Batch kecil tanpa masalah beban, atau operasi saling bergantung |

## Prioritas dan batas penerapan

Factory, Adapter, Strategy, serta Module adalah pilihan awal ketika signal-nya
ada. Observer mengikuti mekanisme reactive yang sudah dipakai Biz-A. Builder,
Decorator, Singleton, Middleware, dan Queue dipakai bila kebutuhan konkretnya
membenarkan tambahan struktur; jangan menyalin semua contoh menjadi library baru.

### Factory dan Builder

- Factory mengembalikan config baru setiap pemanggilan, termasuk nested array /
  object yang akan dimutasi. Spread hanya membuat shallow copy; jangan berbagi
  `props`, `columns`, atau `fieldGroup` mutable antar field/form secara tidak sengaja.
- Builder menyimpan opsi per instance, bukan global. Hasil `build()` tidak boleh
  ikut berubah karena builder dipakai lagi; salin bagian mutable sesuai contract.
- Hindari `structuredClone` untuk config yang berisi callback. Ikuti rules Biz-A
  untuk cloning dan gunakan function reference yang tetap valid.

Contoh factory murni untuk diletakkan dalam `functions` library yang sesuai:

```javascript
buildRequiredTextField: function (key, label) {
    return {
        key,
        type: 'input',
        props: { label, required: true },
    };
},
```

Function bernama `build...` di atas adalah Factory; chaining bukan syarat factory
dan tidak perlu ditambahkan jika tidak menyelesaikan masalah konfigurasi bertahap.

### Module dan Singleton

- Export standar `get = function () { return { functions: { ... } }; }` dan
  `module.exports = get` tetap dipertahankan. Ini factory konfigurasi module;
  jangan menganggap `get()` selalu mengembalikan singleton.
- Jika perlu closure private, tentukan kapan dibuat dan dibersihkan. State
  instance harus terisolasi saat dua form dibuka atau form dibuka kembali.
- Jangan simpan model aktif, kontrol form, user, koneksi, atau `dbIndex` pada
  singleton buatan sendiri. Reuse service runtime; cache hanya bila scope, key,
  invalidasi, serta kebutuhan berbagi resource sudah jelas.

### Adapter dan Strategy

- Adapter menerjemahkan contract secara eksplisit: ID sumber vs ID lokal, null,
  nilai nol, satuan, dan shape array/object. Jangan menyembunyikan response error.
- Letakkan mapping hasil query di library query/domain, utility murni di library
  utility, dan assignment kontrol/grid di form/list.
- Strategy memiliki input/output yang konsisten. Validasi key peta; jangan
  mengeksekusi property object sewenang-wenang. Default hanya jika behavior bisnis
  memang mendefinisikannya; tipe dokumen tidak dikenal tidak boleh diam-diam
  menggunakan algoritma atau tujuan penyimpanan lain.

Contoh Strategy murni, sebagai method dalam `functions` library kalkulasi/domain:

```javascript
calculateDiscount: function (type, amount, value) {
    const strategies = {
        fixed: (base, discount) => base - discount,
        percentage: (base, percent) => base * (1 - percent / 100),
    };
    const isKnownType = Object.prototype.hasOwnProperty.call(strategies, type);
    if (!isKnownType) {
        throw new Error('Jenis diskon tidak dikenal.');
    }
    const calculate = strategies[type];
    return calculate(amount, value);
},
```

Contoh hanya menunjukkan pemilihan algoritma. Validasi angka, pembulatan, dan
batas diskon tetap mengikuti contract domain target yang sudah diverifikasi.

### Decorator / Higher-Order Function

- Pertahankan argumen, binding `this`, nilai return, serta propagasi error.
  Method Biz-A yang membutuhkan `this` tidak boleh dilepas sebagai bare callback
  tanpa binding; gunakan function/closure yang meneruskan context dengan benar.
- Bedakan synchronous return, Promise, dan Observable. Waktu pemanggilan function
  bukan waktu completion async. Jangan menambahkan `subscribe()` tersembunyi atau
  mengubah Observable menjadi Promise untuk memasang decorator.
- Reuse penanganan loading/error module; wrapper baru hanya jika menambah perilaku
  yang memang berulang. Jangan mencetak payload atau kredensial ke log.

### Observer / Pub-Sub

- Observer berlangganan ke sumber; Pub-Sub memakai perantara event. Jangan
  menyebut setiap callback sebagai event bus atau membangun bus baru untuk
  menggantikan listener yang sudah berfungsi.
- Pasang listener sekali pada lifecycle yang benar. Ikuti mekanisme cleanup
  runtime yang terverifikasi; jangan mengarang hook destroy.
- Verifikasi unsubscribe/cleanup saat reopen, emisi ganda, dan feedback loop saat
  listener menulis kontrol yang dipantaunya. Pisahkan transformasi dari assignment.

### Middleware / Pipeline dan Async Queue

- Gunakan satu flow async yang dapat ditelusuri, dengan error diteruskan. Pipeline
  synchronous tidak otomatis menangani Promise/Observable. Callback `next` tidak
  boleh terpanggil dua kali atau melewati validasi yang gagal.
- Reuse operator async yang tersedia pada module. Pada flow Observable Biz-A,
  pertahankan satu subscription untuk satu flow; jangan membuat queue Promise
  baru hanya untuk membungkus service Observable.
- Pilih urutan dari dependensi: batch independen dapat dibatasi concurrency-nya;
  save header lalu detail yang memerlukan ID header harus tetap berurutan.
  Pembatalan request lama pada pencarian berbeda dengan pemrosesan seluruh writes.
- Jika custom queue memang dibutuhkan, validasi concurrency sebagai integer positif,
  tangani synchronous throw dan async rejection, lalu lepaskan slot pada semua
  completion/error path. Definisikan urutan hasil, kebijakan gagal, dan cleanup.
  Jangan menambah retry writes otomatis tanpa contract idempotensi.

## Integrasi dan verifikasi Biz-A

Rules wajib Biz-A tetap berlaku; design pattern bukan alasan mengganti jalur
write resmi, export module, lifecycle, atau authorization. Baca referensi terkait
dari `INDEX.md` saat implementasi menyentuh area tersebut. Khususnya:

- Reuse `useLibrary`; query/data access di `lib_qry` atau library query module,
  dialog di library dialog yang sesuai, dan UI orchestration di form/list.
- Ambil snapshot form terbaru sebelum mapping/clone/replace model sesuai
  `form-model-value-sync-problem.md`.
- Resolve fallback runtime dalam body function; pisahkan hasil pemanggilan
  function ke variabel sebelum menjadi argumen function lain.
- Saat mengubah async, periksa sukses, response bisnis error, transport error,
  loading selesai, serta completion/cleanup sesuai flow target.

Untuk laporan pengenalan atau rencana perubahan, cukup sebutkan **bukti kode ->
pattern -> manfaat/batas -> keputusan**. Jika tidak ada kandidat yang berguna,
nyatakan bahwa struktur sekarang sudah cukup. Untuk debugging, pattern hanya
petunjuk investigasi; root cause harus dibuktikan dari aliran data/error.

## Rujukan lokal

- [patterns.md](patterns.md), section 1-2: factory export dan `useLibrary`.
- [helper-rules.md](helper-rules.md): boundary query, utility, dan UI.
- [biz-a-normalize-pattern-rules.md](biz-a-normalize-pattern-rules.md): ekstraksi duplikasi.
- `Proton/lib_utils.js`: export plain object dan helper yang sudah tersedia.
- `Proton/lib_qry.js`: query serta mapping domain; periksa contract aktual sebelum reuse.
- `Proton/quotationForm.js`, `listener`: wiring `valueChanges` yang perlu dipahami
  dalam konteks lifecycle target, bukan disalin seluruhnya.

Contoh lokal menunjukkan bentuk yang sudah dipakai, bukan pernyataan bahwa seluruh
file bebas masalah. Contoh pendek dalam referensi ini bersifat ilustratif dan
perlu disesuaikan dengan contract module target.
