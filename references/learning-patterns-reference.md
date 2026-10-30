# Learning Patterns - Referensi Utama

Referensi praktis dari *Learning Patterns* karya **Lydia Hallie dan Addy Osmani**.
Gunakan untuk mengenali masalah, memilih pattern, dan menilai trade-off sebelum
implementasi. Ringkasan ini tidak menggantikan rules dan contract Biz-A.

## Sumber dan atribusi

- Sumber proyek: [learning-patterns-final-v1.1.pdf](../docs/learning-patterns-final-v1.1.pdf).
  Pengguna memindahkan file dari Downloads ke `.agents/docs/` selama task ini.
- Judul dan penulis diverifikasi dari sampul serta metadata PDF; total **436 halaman**.
- Seluruh nomor halaman dalam seri referensi ini adalah **urutan halaman PDF,
  mulai 1 pada sampul**, bukan nomor cetak atau nomor bab.
- SHA-256 sumber: `26ec3b1274fbeb0ce56634f1418034553d6d0097640ec81d3228dac2c830d7bf`.
- Situs penulis: [Patterns.dev](https://www.patterns.dev/).
- Halaman 4 menyatakan lisensi buku
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
- Perubahan dari sumber: diringkas dan ditulis ulang dalam Bahasa Indonesia,
  dikelompokkan untuk pencarian, serta diberi interpretasi penerapan Biz-A.
  Contoh kode buku tidak disalin. Penyesuaian Biz-A merupakan keputusan proyek,
  bukan klaim bahwa buku mendokumentasikan Biz-A atau penulis mendukung proyek ini.

## Pilih referensi sesuai kebutuhan

| Signal task | Referensi | Cakupan |
|---|---|---|
| Pembuatan object, module, shared state, event, koordinasi, command, penghematan object | [JavaScript Patterns](learning-patterns-javascript-patterns.md) | 10 pattern umum beserta signal, trade-off, dan adaptasi Biz-A |
| Prop drilling, pemisahan view/data, reuse stateful logic, wrapper, kelompok komponen | [Component Patterns](learning-patterns-component-patterns.md) | 6 pola komponen dari bab React dan batas transfer konsep ke Biz-A |
| CSR/SSR/SSG, hydration, islands, bundle, lazy load, preload/prefetch, list besar | [Rendering dan Performance](learning-patterns-rendering-performance.md) | Arsitektur rendering, loading, dan evaluasi performa |
| Keputusan implementasi form/list/helper Biz-A | [Biz-A Design Pattern Recognition](biz-a-design-pattern-recognition.md) | Alur pengenalan wajib, functional/plain object, dan aturan integrasi lokal |

Load hanya bagian yang match dengan task. File ini menyimpan atribusi dan peta
sumber; tautan relatif mengarah ke PDF yang disimpan di `.agents/docs/`.

## Peta buku

| Bagian | Halaman PDF | Isi yang dipetakan |
|---|---|---|
| Pengantar dan Overview of React.js | 5-34 | Komponen, props, state, composition, dan pemisahan tanggung jawab |
| Design patterns | 35-205 | 10 pattern JavaScript umum dan 6 pola komponen; urutan aslinya saling berselang |
| Rendering patterns | 206-324 | Pengantar/KPI 207-213, Next.js 214-217, 9 pendekatan rendering/hydration, dan studi kasus 282-312 |
| Performance | 325-434 | 12 topik loading, import, splitting, caching, resource hints, dan virtualization |
| Penutup | 435-436 | Pilih pattern karena masalah nyata dan evaluasi trade-off |

Pengelompokan pada referensi lokal adalah pengelompokan editorial proyek, bukan
penomoran kategori resmi dari buku. Mediator/Middleware dihitung sebagai satu
topik sesuai judul bab sumber.

## Cara memakai hasil bacaan

1. Identifikasi gejala konkret dan lokasinya: function, caller, config, data flow,
   atau hasil pengukuran. Pilih bab yang membahas masalah tersebut.
2. Bandingkan dengan solusi sederhana dan helper yang sudah tersedia.
3. Tentukan contract yang harus tetap sama: input/output, side effect, lifecycle,
   scope state, error path, serta authorization.
4. Catat **bukti -> pattern -> manfaat/biaya -> keputusan -> verifikasi**.
   Pengenalan wajib tidak berarti setiap perubahan harus menambah abstraksi.

Prinsip ini selaras dengan penutup buku pada halaman 435: pattern membantu saat
menyelesaikan masalah praktis, sedangkan penerapan tanpa kebutuhan dapat menambah
kompleksitas.

## Batas sumber dan implementasi

- PDF adalah snapshot buku yang diberikan pengguna. Nama API, status eksperimen,
  rekomendasi package, benchmark, dan metrik mencerminkan konteks sumber saat itu.
  Tanggal metadata hasil pemrosesan PDF tidak dipakai sebagai tahun publikasi buku.
- Ringkasan mempertahankan konsep, bukan menjadikan kode framework lama sebagai
  template siap jalan. Untuk implementasi library/API, periksa versi lokal dan
  ikuti `.agents/instructions/context7.md`.
- React Hooks, Context, JSX, SSR, dan bundling bukan API otomatis pada module
  Biz-A. Terapkan prinsip yang cocok dengan kemampuan runtime yang diverifikasi.
- Builder, Adapter, Strategy, Decorator/HOF, dan Async Queue pada panduan Biz-A
  sebelumnya tetap berasal dari contoh `javascript_design_patterns.md`; jangan
  mengatribusikannya sebagai bab tersendiri dalam PDF ini.
