# Instruksi AI proyek

Semua skill, rules, referensi, dokumen pendukung, agent, dan command yang
dipelihara untuk proyek ini berpusat di `.agents/`. Path dalam instruksi
berawalan `.agents/` dihitung dari root repository.

- Sebelum mengubah kode Biz-A, baca `.agents/rules/biz-a.rules.instructions.md`
  dan `.agents/references/INDEX.md`, lalu hanya referensi yang relevan.
- Gunakan skill Biz-A yang sesuai dari `.agents/skills/`: create, debug,
  refactor, simplify, normalize, planner, reviewer, atau control-center.
- Untuk dokumentasi library, framework, SDK, API, CLI, atau cloud service,
  ikuti `.agents/instructions/context7.md`.
- Untuk membaca task OpenProject (OP), termasuk task in progress, deskripsi,
  komentar, dan lampiran, gunakan `.agents/skills/openproject-read/SKILL.md`.
  Token dibaca secara internal dari `.env`; jangan mencetak isinya.
- Tambahkan dan perbarui pengetahuan AI di `.agents/`. File di lokasi native
  aplikasi merupakan entrypoint, bukan tempat menambah aturan baru.
- Setelah mengubah metadata agent/command atau konfigurasi native, jalankan
  `python .agents/scripts/sync-native.py` dari root proyek.
- Hook Codex di `.agents/hooks/` memuat instruksi proyek dan rules aktif pada
  `UserPromptSubmit` serta sebelum perintah terminal dan edit file (`PreToolUse`).
  Jika hook melaporkan file rules hilang atau kosong, pulihkan file tersebut.
- `.agents/archive/` menyimpan versi referensi lama untuk penelusuran;
  gunakan `.agents/references/` untuk pekerjaan baru.

Skill sistem dan plugin bawaan, kredensial login aplikasi, serta riwayat/cache
runtime dikelola oleh aplikasi masing-masing. Konfigurasi MCP khusus proyek
tersimpan lokal di `.agents/config/private/codex.toml` dan diabaikan Git.

## Organisasi catatan perubahan

- Setiap task yang mengubah file wajib memiliki catatan Markdown di folder
  `codex` pada masing-masing folder utama proyek/modul yang diubah. Perubahan
  dalam subfolder tetap dicatat pada folder utama tersebut; misalnya perubahan
  `BERCA/inputQuotationForm.js` atau `BERCA/sql/example.sql` dicatat di
  `BERCA/codex/changes-1.md`.
- Jika satu task mengubah beberapa folder utama, buat catatan terpisah di
  masing-masing folder, berisi perubahan yang relevan untuk folder tersebut.
  Pertahankan ejaan dan kapitalisasi folder yang sudah ada.
- Buat folder `codex` jika belum ada. Gunakan nama `changes-N.md`, mulai dari
  `changes-1.md`; untuk task baru gunakan nomor terbesar yang sudah ada di
  folder tersebut ditambah satu. Penomoran berlaku secara lokal per folder.
  Jangan menimpa catatan task lain; pembaruan dalam task yang sama memakai
  catatan yang sama.
- Catatan memuat tanggal, tujuan/ringkasan perubahan, daftar path file yang
  diubah, serta hasil validasi atau keterangan jika belum divalidasi.
- Untuk file langsung di root repository, gunakan `codex/changes-N.md`.
  Untuk perubahan di `.agents/`, gunakan `.agents/codex/changes-N.md`.
  Penambahan atau pembaruan catatan itu sendiri tidak memerlukan catatan baru.
- Aturan dan pengetahuan AI yang dapat digunakan ulang tetap dipelihara di
  `.agents/`; folder `codex` menyimpan catatan perubahan per task. Catatan lama
  tidak perlu dipindahkan kecuali diminta pengguna.
