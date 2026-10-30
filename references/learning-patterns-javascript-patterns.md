# Learning Patterns - JavaScript Patterns

Sumber: *Learning Patterns*, Lydia Hallie dan Addy Osmani.
[Identitas PDF, penomoran halaman, lisensi, dan perubahan dari sumber](learning-patterns-reference.md#sumber-dan-atribusi).
Bagian **inti buku** merangkum konsep; bagian **adaptasi Biz-A** adalah
interpretasi proyek dengan pendekatan functional/plain object.

## Peta pengenalan

| Signal | Pattern | Halaman PDF |
|---|---|---|
| Semua pemakai memang memerlukan satu resource/state dengan identitas yang sama | Singleton | 35-46 |
| Akses atau perubahan property perlu diintersep secara terpusat | Proxy | 47-54 |
| Banyak object membutuhkan behavior yang sama melalui prototype chain | Prototype | 67-74 |
| Satu perubahan/event perlu memberi tahu beberapa consumer independen | Observer | 85-94 |
| Tanggung jawab membesar, nama bertabrakan, atau detail internal perlu disembunyikan | Module | 95-109 |
| Beberapa object perlu mendapat kumpulan behavior tanpa hierarki inheritance baru | Mixin | 110-116 |
| Komponen saling memanggil banyak arah atau tahap request perlu dikoordinasikan | Mediator/Middleware | 117-123 |
| Banyak object memiliki data intrinsik identik sehingga konsumsi memory berulang | Flyweight | 182-186 |
| Object dengan struktur mirip perlu dibuat berulang berdasarkan input | Factory | 187-189 |
| Pemicu aksi perlu dipisah dari pelaksana, antrean, atau waktu eksekusinya | Command | 200-205 |

## Singleton

**Inti buku:** satu instance dibagi kepada seluruh pemakai dalam scope aplikasi.
Implementasi JavaScript dapat berupa satu object yang diekspor; class bukan
keharusan. Shared mutable state membawa dependency tersembunyi, ketergantungan
urutan eksekusi, dan kebutuhan reset saat pengujian (hlm. 42-46).

**Adaptasi Biz-A:** reuse service runtime yang sudah ada. `get()` yang membuat
config baru adalah factory; kesamaan method tidak membuktikan singleton.
Jangan letakkan model aktif, user, atau `dbIndex` lintas form dalam state global.
Jika memang perlu resource bersama, tentukan owner, scope, key, dan invalidasi.

**Verifikasi:** dua form/user/database tidak saling mencemari; reopen serta
urutan pemanggilan tidak mengubah hasil secara tak disengaja.

## Proxy

**Inti buku:** perantara dapat mengubah perilaku membaca/menulis property, misalnya
untuk validasi atau logging; bab juga membahas `Reflect` untuk meneruskan operasi
ke target (hlm. 47-54). Semua akses yang ingin dikendalikan harus melalui perantara.

**Adaptasi Biz-A:** pahami konsep intercept, tetapi utamakan validation dan
listener native yang sudah tersedia. Jangan membungkus kontrol/framework/model
aktif dengan proxy baru tanpa memeriksa identitas object, binding, dan sinkronisasi.
Interceptor pada JavaScript juga tidak menggantikan authorization backend.

**Verifikasi:** akses langsung ke target, nilai tidak valid, propagasi error,
serta behavior method dan serialisasi yang dipakai caller.

## Prototype

**Inti buku:** behavior dapat dibagi melalui prototype chain; sumber memberi
contoh class dan `Object.create` (hlm. 67-74). Property yang diwarisi berbeda
dengan property milik object itu sendiri.

**Adaptasi Biz-A:** pertahankan export plain object dan reuse library sebelum
menambah inheritance. Jangan memodifikasi prototype global untuk berbagi helper.
Untuk config/payload, jangan mengandalkan inherited property ketika consumer
mengharapkan own enumerable properties atau data JSON biasa.

**Verifikasi:** own vs inherited property, method lookup, enumerasi, dan shape
payload hasil serialisasi. Prototype bukan perintah untuk memakai `class`.

## Observer

**Inti buku:** observable mengelola subscription dan memberi notifikasi kepada
observer saat event terjadi. Consumer dapat subscribe dan unsubscribe tanpa
mengikat produser ke implementasi masing-masing consumer (hlm. 85-94).
Handler yang berat tetap dapat membuat notifikasi mahal.

**Adaptasi Biz-A:** reuse `valueChanges` serta alur reactive yang sudah ada.
Pisahkan perhitungan dari assignment kontrol. Pasang listener pada lifecycle
yang tepat dan gunakan mekanisme cleanup yang benar-benar disediakan runtime.
Observer langsung dan Pub-Sub dengan event broker tidak identik.

**Verifikasi:** listener tidak terpasang ganda, cleanup saat tutup/reopen,
feedback loop saat menulis kontrol, serta error/completion async.

## Module

**Inti buku:** pecah kode menjadi unit reusable dengan public surface eksplisit
dan detail internal yang tidak diekspor. Sumber menjelaskan named/default export,
alias, dan dynamic import pada ES modules (hlm. 95-109).

**Adaptasi Biz-A:** pertahankan `get = function () { return { functions: { ... } }; }`
dan `module.exports = get`. Reuse melalui `useLibrary`; tempatkan query di library
query, utility di library utility, dan lifecycle/assignment UI pada form/list.
ES module dalam buku tidak otomatis dapat menggantikan loader Biz-A.

**Verifikasi:** nama helper, public caller, dependency library, dan keterjangkauan
function melalui mekanisme runtime. Hapus implementasi duplikat setelah migrasi.

## Mixin

**Inti buku:** kumpulan behavior ditambahkan ke object tanpa membangun hierarki
inheritance. Bab menyorot risiko asal behavior yang sulit dilacak dan modifikasi
prototype, termasuk konteks penggunaan mixin React lama (hlm. 110-116).

**Adaptasi Biz-A:** `useLibrary` dapat dikenali sebagai komposisi behavior yang
mirip mixin, tetapi aturan merge runtime harus diperiksa sebelum menyimpulkan
semantiknya. Periksa nama function yang bertabrakan dan method yang bergantung
pada `this`; jangan menambal prototype framework.

**Verifikasi:** asal setiap helper jelas, override yang disengaja tetap benar,
serta state dan context method tidak tercampur antar module.

## Mediator/Middleware

**Inti buku:** mediator menjadi titik koordinasi komunikasi antarkomponen.
Contoh middleware Express menyusun callback dalam siklus request-response
(hlm. 117-123). Keduanya dibahas dalam satu bab tetapi perannya perlu dibedakan:
mediator mengoordinasikan pihak, middleware menyusun tahap pemrosesan.

**Adaptasi Biz-A:** form dapat menjadi orchestration yang memanggil query,
validasi, mapping, dan assignment tanpa helper saling mengakses kontrol UI.
Untuk alur async, gunakan contract yang sudah ada dan satu chain yang jelas;
tidak perlu membawa engine `next()` Express ke module Biz-A.

**Verifikasi:** urutan tahap dan short-circuit saat gagal, completion/error yang
diteruskan, serta mediator tidak menjadi tempat seluruh logika bisnis menumpuk.

## Flyweight

**Inti buku:** reuse object yang memiliki data intrinsik sama; data spesifik
setiap pemakaian tetap terpisah. Contoh buku memisahkan identitas judul buku dari
copy buku yang dimiliki perpustakaan (hlm. 182-186).

**Adaptasi Biz-A:** pertimbangkan metadata referensi yang benar-benar sama dan
read-only jika pengukuran menunjukkan duplikasi memory. Jangan berbagi model,
row detail, atau config Formly mutable sebagai flyweight; perubahan satu pemakai
dapat mengubah pemakai lain. Flyweight bukan sinonim cache semua hasil query.

**Verifikasi:** key identitas tepat, data per baris tetap terpisah, scope/invalidation
jelas, dan penghematan memory terukur. Factory tetap harus membuat bagian mutable
baru meskipun beberapa metadata immutable dibagi.

## Factory

**Inti buku:** function membuat dan mengembalikan object baru, dengan variasi
berdasarkan parameter. Tidak memerlukan `new`. Kemudahan membuat object perlu
dipertimbangkan bersama biaya alokasi object/function berulang (hlm. 187-189).

**Adaptasi Biz-A:** `build...` dapat membuat field/filter/payload, sedangkan
`get()` membuat konfigurasi module. Satu object literal sederhana belum perlu
factory baru. Contoh dan batas cloning ada pada
[panduan Biz-A](biz-a-design-pattern-recognition.md#factory-dan-builder).

**Verifikasi:** dua pemanggilan tidak berbagi nested mutable config; callback
tetap function, hasil dan default mengikuti contract caller.

## Command

**Inti buku:** pemicu tidak perlu mengetahui implementasi pelaksana; operasi
direpresentasikan sebagai command yang dapat diteruskan atau dijadwalkan.
Biaya utamanya tambahan lapisan/boilerplate jika hanya ada pemanggilan langsung
yang sederhana (hlm. 200-205).

**Adaptasi Biz-A:** gunakan function atau plain object berisi jenis aksi, data,
dan handler hanya bila ada kebutuhan pemisahan pemicu/pelaksana. Bedakan dari
Strategy: Strategy memilih algoritma, Command mewakili operasi yang diminta.
Command bukan bukti bahwa undo, retry, atau transaksi sudah tersedia.

**Verifikasi:** whitelist jenis aksi, validasi/authorization pada waktu eksekusi,
snapshot vs state terbaru, urutan dependensi, dan propagasi hasil/error. Writes
tetap melalui jalur resmi Biz-A/FINA; retry perlu contract idempotensi terpisah.

## Memilih tanpa menambah kompleksitas

Factory/Module/Observer sering sudah hadir dalam bentuk native Biz-A. Kenali
yang sudah ada sebelum menambah abstraksi. Proxy, Prototype, Singleton, Flyweight,
dan Command perlu kebutuhan konkret serta pemeriksaan contract lebih dahulu.
Baca [Component Patterns](learning-patterns-component-patterns.md) jika masalah
utamanya pembagian view, state, atau reuse logic UI.
