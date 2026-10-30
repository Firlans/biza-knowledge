# Learning Patterns - Rendering dan Performance

Sumber: *Learning Patterns*, Lydia Hallie dan Addy Osmani.
[Identitas PDF, penomoran halaman, lisensi, dan perubahan dari sumber](learning-patterns-reference.md#sumber-dan-atribusi).
Ringkasan konsep bersumber dari PDF; kriteria implementasi dan penyesuaian Biz-A
di bawah adalah interpretasi proyek.

## Baca sebelum memakai contoh implementasi

Buku membahas API serta dukungan framework dalam konteks historisnya. Misalnya,
halaman 353 menyebut keterbatasan SSR/Suspense saat itu, sedangkan hlm. 272-281
membahas selective hydration dalam konteks React 18. Jangan memakai pernyataan
dukungan atau nama API dari satu bab sebagai status runtime sekarang.

Pengantar/KPI ada pada **hlm. 207-213** dan Overview of Next.js pada
**hlm. 214-217**. Metrik yang dibahas mencakup TTFB, FCP, LCP, TTI, dan TBT;
bagian performa juga menyebut FID dan CLS. Daftar, definisi singkat, serta angka
benchmark buku tidak dijadikan standar audit terkini atau jaminan peningkatan.

## Peta rendering

| Pattern dan halaman PDF | Inti konsep | Signal pemilihan | Biaya/contract yang diperiksa |
|---|---|---|---|
| Client-Side Rendering (CSR), 218-223 | Browser menjalankan rendering UI dan mengambil data yang diperlukan | Aplikasi sangat interaktif dengan banyak perubahan setelah load | Ukuran/eksekusi JS awal, waterfall request, state loading/error, dan kebutuhan konten awal |
| Server-Side Rendering (SSR), 224-232 | Server menghasilkan HTML sebagai respons request; client dapat menambahkan interaktivitas sesuai arsitektur | Konten awal bergantung request dan perlu tersedia sebelum rendering client penuh | Waktu server/TTFB, beban request, caching, serta biaya JS/hydration jika masih dibutuhkan |
| Static Rendering / SSG, 233-239 | HTML dibuat lebih dahulu saat build dan disajikan sebagai hasil statis | Konten dapat dipersiapkan dan relatif sama bagi pemakai | Freshness, jumlah route, waktu rebuild, dan batas personalisasi |
| Incremental Static Generation (iSSG), 240-245 | Sebagian halaman diperbarui/dibuat tanpa membangun ulang seluruh situs | Banyak halaman dengan konten yang dapat disajikan dari hasil sebelumnya sementara regenerasi berlangsung | Kebijakan stale data, regenerasi gagal, cache, dan kapan perubahan terlihat |
| Progressive Hydration, 246-256 | Aktivasi JS ditunda per bagian menurut prioritas atau trigger | Sebagian UI belum perlu interaktif pada load awal | UI terlihat siap sebelum handler tersedia, urutan aktivasi, dan dependensi antarbagian |
| Streaming SSR, 257-266 | HTML dikirim bertahap agar client mulai memproses sebelum seluruh respons selesai | Bagian halaman bisa tersedia pada waktu berbeda | Buffering transport, error setelah sebagian respons terkirim, backpressure, dan metadata/style yang diperlukan lebih awal |
| React Server Components, 267-271 | Sebagian komponen berjalan di server dan hasilnya digabung dengan bagian client | Rendering/data access dapat tetap di server untuk mengurangi code client | Batas server/client, format data yang dapat melewatinya, dan interaksi yang membutuhkan client; konsep ini melengkapi SSR |
| Selective Hydration, 272-281 | Bagian UI yang sudah siap dapat dihidrasi tanpa menunggu seluruh bagian lambat selesai | Streaming dengan beberapa bagian interaktif memiliki waktu siap berbeda | Boundary, fallback, prioritas interaksi, serta konsistensi server/client |
| Islands Architecture, 313-324 | HTML utama bersifat statis dengan beberapa area interaktif yang diaktifkan secara independen | Halaman dominan konten dengan widget interaktif terisolasi | Koordinasi state antar-island dan kecocokan untuk halaman yang interaktivitasnya rapat |

### Bedakan keputusan yang sering tercampur

- **Kapan HTML dibuat:** build time (SSG), request time (SSR), atau di browser
  (CSR). Aplikasi dapat menggabungkan beberapa pendekatan sesuai bagian/route.
- **Kapan code diunduh:** initial load, navigasi, visibility, interaksi, atau
  prefetch. Dynamic import tidak otomatis berarti hydration.
- **Kapan UI aktif:** HTML yang sudah terlihat dapat belum memiliki handler.
  Streaming respons dan hydration adalah tahap berbeda.
- **Di mana komponen berjalan:** server/client boundary pada Server Components
  berbeda dari sekadar mengirim HTML hasil SSR.

## Peta loading dan optimasi

| Topik dan halaman PDF | Inti konsep dan signal | Trade-off / verifikasi |
|---|---|---|
| Optimize Loading Sequence, 326-343 | Urutkan resource menurut kebutuhan konten awal dan interaksi; periksa CSS/font/image, JS aplikasi, dan JS pihak ketiga | Network dan main thread mempunyai kendala berbeda; terlalu banyak inline/preload juga bisa bersaing dengan resource penting |
| Static Import, 344-347 | Dependency diketahui dari struktur module; cocok untuk kebutuhan yang selalu ada | Periksa hasil build aktual; static import sendiri tidak membuktikan semua code masuk satu initial bundle |
| Dynamic Import, 348-355 | Minta code saat dibutuhkan untuk mengurangi pekerjaan awal | Ada biaya unduh/eksekusi setelah trigger; periksa chunk aktual, fallback, dan failure path |
| Import on Visibility, 356-360 | Tunda code nonkritis sampai area terkait mendekati/masuk viewport | Jangan menunda konten awal yang penting; periksa trigger berulang, cleanup, dan pengalaman scrolling |
| Import on Interaction, 361-382 | Muat fitur/third-party widget setelah aksi atau indikasi kebutuhan; facade ringan dapat tampil lebih dahulu | Pekerjaan pindah ke saat interaksi; ukur waktu tunggu setelah klik, akses keyboard, dan first interaction yang tetap berfungsi |
| Route Based Splitting, 383-384 | Muat code berdasarkan route yang dibuka | Periksa latency navigasi, error chunk, shared dependency, serta loading state |
| Bundle Splitting, 385-392 | Pisahkan code agar hanya kebutuhan relevan dikirim dan dieksekusi | Terlalu banyak chunk kecil menambah request/overhead; ukur duplikasi dan dependency graph |
| PRPL, 393-407 | Prioritaskan resource kritis, render initial route, precache route yang mungkin dikunjungi, dan lazy load sisanya | Buku membahas HTTP/2 push dan service worker; jangan menyalin konfigurasi protokol tanpa verifikasi dukungan dan cache policy runtime |
| Tree Shaking, 408-410 | Build menghilangkan code yang terbukti tidak diperlukan berdasarkan dependency dan side effect | Periksa format module/toolchain serta efek inisialisasi; nama function tanpa caller tekstual belum berarti aman dihapus |
| Preload, 411-417 | Bantu resource kritis untuk kebutuhan sekarang ditemukan lebih awal | Bukan perintah mengeksekusi JS atau mengambil semua resource; ukur persaingan dengan CSS/font/image dan request ganda |
| Prefetch, 418-422 | Ambil resource yang diperkirakan dibutuhkan kemudian | Salah prediksi membuang bandwidth/memory; jangan bersaing dengan kebutuhan utama dan periksa cache reuse |
| List Virtualization, 423-434 | Render subset item yang tampak sambil memindahkan window saat scroll; grid dapat memakai dua sumbu | Identitas row, ukuran, scroll, fokus, selection/edit state, dan aksesibilitas harus tetap benar |

### PRPL sesuai sumber

PDF menguraikan empat tujuan pada **hlm. 393**: **Push** resource kritis,
**Render** initial route, **Pre-cache** route berikutnya, dan **Lazy-load** bagian
lain. Pada **hlm. 400** buku juga membahas preload untuk discovery resource.
Gunakan tujuan prioritasi/caching sebagai konsep; implementasi HTTP/2 server push
dan rekomendasi tool pada buku bukan prasyarat universal yang ditambahkan ke Biz-A.

### Virtualization berbeda dari pagination

Windowing mengurangi jumlah elemen yang dirender; pagination membatasi kelompok
data yang diambil/ditampilkan. Keduanya tidak otomatis mengurangi seluruh biaya
query atau memory data yang sudah diunduh. Pilih berdasarkan bottleneck terukur,
bukan jumlah row saja. Snapshot print/export mungkin memerlukan data lengkap,
sehingga tidak boleh mengambil hanya elemen DOM yang sedang terlihat.

## Pelajaran dari studi kasus

Studi kasus Next.js Movies pada **hlm. 282-312** mengevaluasi dependency,
CSS/image, request paralel untuk data independen, preconnect, dan preload data
yang sudah dapat diprediksi. Pelajaran yang dapat digunakan ulang adalah
**ukur -> ubah satu aspek -> ukur lagi -> pertahankan behavior**.

Nama library, ukuran bundle, persentase peningkatan, dan hasil perangkat dalam
studi kasus adalah hasil contoh tersebut; tidak dipakai sebagai rekomendasi
package atau target performa otomatis untuk proyek ini.

## Penerapan pada Biz-A

- Pastikan batas kendali: file module belum tentu dapat mengubah host runtime,
  bundler, SSR, atau server. Jangan mengubah arsitektur host hanya karena pattern
  tercantum di buku.
- Terapkan prioritas data dan kerja nonkritis pada lifecycle yang sudah ada.
  Query independen boleh direncanakan paralel jika contract mendukung; operasi
  yang membutuhkan hasil sebelumnya tetap berurutan.
- `useLibrary` tidak otomatis sama dengan static import ES module, dynamic import,
  atau tree shaking. Verifikasi loader yang sebenarnya sebelum membuat klaim.
- Untuk grid/list besar, periksa kemampuan pagination/virtualization native dan
  behavior keyboard, edit, authorization, serta export/print sebelum mengganti UI.
- Ikuti aturan Context7 untuk API/bundler/framework versi target; ringkasan ini
  sengaja tidak menyediakan salinan kode React/Next.js historis.

## Verifikasi keputusan performa

Catat baseline dan kondisi ukur (route/data, perangkat, network, cold/warm cache).
Bandingkan konten pertama yang berguna, waktu interaksi, long task, request,
ukuran code, dan jumlah node/memory sesuai bottleneck. Uji load gagal, navigasi
cepat, reopen, dan cleanup pada bagian yang berubah. Laporkan hasil terukur
serta batasnya; lazy loading atau splitting belum membuktikan peningkatan.
