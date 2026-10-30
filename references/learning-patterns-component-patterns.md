# Learning Patterns - Component Patterns

Sumber: *Learning Patterns*, Lydia Hallie dan Addy Osmani.
[Identitas PDF, penomoran halaman, lisensi, dan perubahan dari sumber](learning-patterns-reference.md#sumber-dan-atribusi).
Ringkasan mengikuti konsep pada PDF. Kolom adaptasi adalah interpretasi proyek,
bukan API React yang dapat langsung dipasang pada module Biz-A.

## Fondasi komponen

Overview of React.js pada **hlm. 8-34** membahas pemecahan UI melalui composition,
props sebagai input, state sebagai data yang berubah, dan hierarki komponen.
Prinsip yang dapat dipindahkan: tanggung jawab jelas, data flow dapat ditelusuri,
dan state ditempatkan pada owner yang tepat. Nama hook/lifecycle React bukan
padanan otomatis hook lifecycle Biz-A.

## Peta pattern

| Pattern dan halaman PDF | Signal dan inti konsep buku | Trade-off yang perlu diperiksa | Adaptasi Biz-A |
|---|---|---|---|
| Provider, 55-66 | Data dibutuhkan banyak descendant; provider menyediakan akses tanpa melewatkan prop melalui semua perantara | Dependency dapat tersembunyi; tentukan scope dan consumer perubahan data | Reuse config/service runtime dengan scope jelas; jangan membuat shared global model atau menganggap `useLibrary` sebagai React Context |
| Container/Presentational, 75-84 | Pemilihan/pengambilan data bercampur dengan cara menampilkannya; pisahkan logic/data dari view | Lapisan tambahan tidak selalu membantu komponen kecil; buku membahas Hooks sebagai alternatif reuse logic | Query dan normalisasi di library, field/grid dan assignment di form/list; tidak perlu menambah komponen React |
| Render Props, 124-137 | Satu pengelola logic/data perlu memberi caller kendali atas tampilan melalui function prop | Data flow menjadi bertingkat jika callback/wrapper berlapis; contract argumen harus jelas | Renderer/callback config dapat memakai prinsip serupa jika didukung runtime; pertahankan signature, return, dan `this` yang sebenarnya |
| Hooks, 138-164 | Stateful logic berulang perlu diekstrak ke function yang dapat digunakan beberapa komponen | Reuse logic tidak otomatis berarti state instance ikut dibagi; effect dan cleanup perlu dipahami | Ekstrak helper sesuai concern, tetapi pemasangan listener dan cleanup tetap lewat lifecycle Biz-A yang terverifikasi |
| Higher-Order Component (HOC), 165-181 | Behavior yang sama membungkus beberapa komponen dan meneruskan props | Wrapper bertumpuk menyulitkan trace; nama prop bisa bertabrakan atau menimpa nilai caller | Pertimbangkan HOF/decorator helper hanya jika behavior memang berulang; jangan membawa struktur HOC/JSX ke form config |
| Compound Component, 190-199 | Sekumpulan komponen saling bergantung untuk satu tugas, misalnya toggle, list, dan item | Shared state, batas nesting, serta collision pada prop hasil shallow merge | Kelompok field/action dapat berbagi orchestration milik form; pastikan identitas field dan sumber state, bukan menyalin React Context/cloneElement |

## Perbedaan penting

- **Provider vs Singleton:** provider memberi akses dalam scope tertentu; ia
  tidak berarti hanya ada satu instance global. Isolasi dua pohon UI/form tetap
  perlu dijaga.
- **Container/Presentational vs Module:** yang pertama membagi concern data/view;
  Module membagi unit kode dan public surface. Keduanya dapat dipakai bersama.
- **HOC vs Hooks vs Render Props:** sama-sama dapat membantu reuse logic, tetapi
  bukan substitusi universal. Pilih dari contract komponen dan kebutuhan caller,
  bukan sekadar ukuran function. Sumber membandingkan pilihan ini pada hlm. 176.
- **Compound vs komponen bersebelahan:** compound mempunyai tugas dan contract
  state bersama; sekadar menaruh field dalam satu `fieldGroup` belum membuktikannya.

## Validasi saat menerapkan prinsip ke Biz-A

1. Trace siapa memiliki state, siapa mengubah, dan siapa mengonsumsi perubahan.
2. Periksa helper/config caller dan collision nama saat library atau wrapper
   digabung. Callback pada config harus tetap dapat dipanggil.
3. Pertahankan nilai input aktif sebelum replace/clone model sesuai
   [form-model-value-sync-problem.md](form-model-value-sync-problem.md).
4. Verifikasi dua instance, reopen, listener cleanup, serta perubahan data
   yang tidak boleh memicu render atau update loop berulang.
5. Ikuti [helper-rules.md](helper-rules.md),
   [form-rules.md](form-rules.md), dan [list-rules.md](list-rules.md) sesuai target.

Untuk implementasi React yang benar-benar diminta pengguna, periksa versi dan
dokumentasi melalui aturan Context7. Referensi ini tidak menetapkan API dari
snapshot buku sebagai rekomendasi versi saat ini.
