---
name: pattern-recognition-rules
description: "Mandatory pattern recognition before creating or modifying any project file. Identify existing conventions, reuse suitable patterns, and preserve file contracts."
applyTo: "**/*"
---

# Pattern Recognition Wajib

- Sebelum membuat atau mengubah **setiap file proyek**, wajib lakukan pattern
  recognition, meskipun pengguna tidak menyebut pattern. Berlaku untuk kode,
  SQL, konfigurasi, skill, rules, dokumentasi, dan file pendukung.
- Baca `.agents/references/biz-a-design-pattern-recognition.md` sebelum edit.
  Referensi cukup dibaca sekali per task selama masih tersedia dalam context;
  evaluasi penerapannya tetap dilakukan untuk setiap target file.
- Untuk file existing, pahami bagian yang akan diubah, contract, caller atau
  pemakainya, dan dependensi relevan. Untuk file baru, periksa contoh setara
  serta konvensi folder/module tujuan.
- Kenali struktur yang sudah dipakai, bagian yang berulang atau bervariasi,
  batas tanggung jawab, serta helper/library yang dapat direuse. Pilih pattern
  umum yang sesuai dari referensi berdasarkan bukti kode dan kebutuhan nyata.
- Untuk kode Biz-A, utamakan functional/plain object, export dan lifecycle
  standar, serta library yang sudah tersedia melalui `useLibrary`. Rules Biz-A
  dan contract bisnis tetap berlaku.
- Untuk file nonkode, terapkan pengenalan pada pola struktur, schema, penamaan,
  dan konvensi file sejenis; design pattern JavaScript diterapkan hanya pada
  bagian yang relevan.
- Tahap pengenalan selalu wajib. Hasilnya boleh mempertahankan struktur yang
  ada atau memakai fungsi/object sederhana bila itu pilihan yang sesuai.
  Jangan menambah abstraksi hanya untuk memenuhi nama pattern.
- Terapkan hasil pengenalan dalam perubahan yang diminta dan verifikasi
  contract/behavior yang terdampak. Catat keputusan singkat pada catatan task:
  bukti struktur -> pattern/konvensi yang dipakai -> alasan pemilihan. Keputusan
  untuk beberapa file dengan pola yang sama boleh dicatat bersama.
- File hasil generator mengikuti pattern sumber/generator yang diperiksa
  sebelum regenerasi; pemilihan pattern tidak dilakukan dengan mengedit hasil
  generator secara manual. Pengenalan pattern tidak memperluas lingkup task.
