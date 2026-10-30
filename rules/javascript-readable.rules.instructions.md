---
name: javascript-readable-rules
description: "Keep JavaScript readable: multiline logic and configuration, consistent indentation, and natural line breaks instead of forced one-liners."
applyTo: "**/*.{js,cjs,mjs}"
---

# Format JavaScript yang Readable

Berlaku saat membuat atau mengubah JavaScript, termasuk form/list/helper Biz-A,
script, serta contoh JavaScript dalam dokumentasi dan jawaban. Tujuannya agar
alur kode mudah dipindai, diperiksa, dan di-debug.

## Prinsip dan indentasi

- Utamakan keterbacaan daripada jumlah baris yang sedikit. Jangan memadatkan
  kode menjadi satu baris hanya karena masih muat atau untuk menghemat output.
  Pertahankan bentuk multiline yang sudah jelas pada bagian yang diedit.
- Ikuti konfigurasi formatter lokal jika tersedia. Jika tidak ada, ikuti
  indentasi konsisten pada file; untuk file baru tanpa acuan gunakan 4 spasi.
  Hindari campuran tab/spasi. Ikuti konvensi quote, semicolon, dan trailing comma
  file/module selama tidak mengurangi keterbacaan.
- Gunakan satu statement per baris. Pisahkan kelompok langkah seperti validasi,
  persiapan data, pemanggilan service, dan penanganan hasil dengan baris kosong.
- Targetkan panjang baris sekitar 100 karakter; pecah baris di atas 120 karakter
  pada batas sintaks yang wajar. Batas ini panduan, bukan alasan memecah literal
  string, URL, regex, atau teks lain hingga mengubah nilainya.

## Kapan wajib multiline

- Tulis body function, method, dan callback berbentuk block pada baris tersendiri.
  Gunakan braces dan body multiline untuk `if`, `else`, loop, serta `try/catch`,
  termasuk guard clause pendek seperti `if (!record) { return; }`.
- Object dengan beberapa property ditulis satu property per baris. Konfigurasi
  bertingkat seperti `fields`, `props`, `columns`, `filter`, dialog, dan payload
  tetap multiline meskipun total teksnya pendek. Object kosong atau satu
  property sederhana boleh inline bila jelas.
- Array berisi object/config ditulis satu item per blok multiline. Array pendek
  berisi nilai sederhana, misalnya `['draft', 'approved']`, boleh satu baris.
- Parameter dan argumen pendek boleh satu baris. Jika panjang atau kompleks,
  tulis satu parameter/argumen per baris dengan penutup sejajar awal pemanggilan.
  Argumen object atau callback mengikuti aturan multiline di atas.
- Pecah kondisi panjang dengan satu bagian logis per baris. Ternary sederhana
  boleh inline; ternary panjang memakai baris terpisah untuk `?` dan `:`.
  Gunakan `if/else` untuk percabangan bertingkat yang sulit dipindai.
- Pecah chain panjang menjadi satu tahap per baris. Arrow expression singkat
  seperti `rows.map(row => row.id)` boleh satu baris; callback dengan beberapa
  langkah, assignment, atau efek samping memakai block multiline.
- Gunakan nama variabel antara yang menjelaskan maksud jika ekspresi sulit
  dibaca. Tetap ikuti larangan nested function call pada rules Biz-A; pemecahan
  baris saja tidak menggantikan kebutuhan variabel antara.

## Contoh

Hindari pemadatan seperti ini:

```javascript
if (!record) return;
const field = { key: 'name', type: 'input', props: { label: 'Nama', required: true } };
rows.forEach(row => { row.selected = false; row.error = null; });
```

Gunakan bentuk yang mudah diperiksa:

```javascript
if (!record) {
    return;
}

const field = {
    key: 'name',
    type: 'input',
    props: {
        label: 'Nama',
        required: true,
    },
};

rows.forEach(row => {
    row.selected = false;
    row.error = null;
});
```

## Pemeriksaan sebelum selesai

- Periksa ulang bagian yang dibuat/diubah: tidak ada beberapa statement dalam
  satu baris, body block inline, atau object/config bertingkat yang dipadatkan.
- Pertahankan behavior, urutan evaluasi, binding `this`, return, dan alur async.
  Saat memecah baris, jaga sintaks seperti `return` agar tidak terkena automatic
  semicolon insertion; letakkan ekspresi atau pembuka `(` / `{` pada baris yang
  sama dengan `return`.
- Terapkan pada bagian yang dikerjakan. Reformat seluruh file/repository hanya
  bila diminta. File generated/minified/vendor mengikuti sumber atau generator;
  jangan mengedit hasilnya secara manual.
