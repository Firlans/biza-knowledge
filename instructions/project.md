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
