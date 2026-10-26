# Pusat kemampuan AI proyek

Semua materi AI yang dipelihara pengguna berada di folder ini.

| Folder | Isi |
|---|---|
| `skills/` | 11 skill pengguna, termasuk Biz-A, Context7, PDF, dan penanda lock-changes yang deprecated |
| `rules/` | Rules Biz-A dan aturan eksekusi Codex di `exec/` |
| `references/` | Referensi aktif, indeks trigger, patterns, dan aturan TDD |
| `docs/` | Manual, spesifikasi, dan dokumen pendukung yang sebelumnya di `.github/doc/` |
| `agents/` | Definisi agent yang dipelihara |
| `commands/` | Sumber command Claude |
| `instructions/` | Instruksi proyek dan prosedur Context7 |
| `config/` | Contoh konfigurasi MCP; konfigurasi asli di `private/` diabaikan Git |
| `archive/claude-references/` | Versi referensi Claude yang berbeda dari referensi aktif |
| `scripts/` | Sinkronisasi entrypoint native aplikasi |
| `hooks/` | Hook Codex pembaca rules sebelum prompt, perintah terminal, dan edit file |

Edit materi di sini. Jalankan dari root proyek:

```powershell
python .agents/scripts/sync-native.py
```

`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`,
`.github/instructions/`, `.github/agents/`, dan `.claude/commands/` hanya
berisi pengarah dan metadata yang diperlukan aplikasi. Skill aktif berada di
`.agents/skills/`; salinan skill global dan `.github/skills/` telah digabungkan.

Codex memerlukan `.codex/config.toml` dan `.codex/rules/default.rules`.
Script menghubungkannya ke sumber di sini memakai hard link NTFS, sehingga
keduanya membaca file yang sama. Jika filesystem tidak mendukung hard link,
script membuat salinan; jalankan ulang setelah perubahan. Jika editor
mengganti sebuah file secara atomik dan koneksi hard link terputus, selaraskan
isinya lalu jalankan script kembali. Script menolak menimpa konfigurasi native
yang berbeda agar perubahan manual tidak hilang.

Konfigurasi MCP Serena dan Context7 dipindahkan dari konfigurasi pengguna ke
`config/private/codex.toml`. File ini dan `.codex/config.toml` diabaikan Git
karena dapat berisi header autentikasi. Saat menyalin proyek ke komputer baru,
gunakan `config/codex.example.toml` sebagai dasar dan isi autentikasi secara
lokal sebelum menjalankan sinkronisasi.

Skill `.system`, paket plugin, metadata kepercayaan hook plugin, integrasi
runtime seperti `node_repl`, preferensi aplikasi, permission native
Claude/VS Code, login, sesi, dan cache tetap dikelola aplikasi masing-masing.
Materi tersebut bergantung pada instalasi aplikasi dan tidak disalin menjadi
skill proyek. Tidak ditemukan file memory pengguna untuk dipindahkan.

`migration-manifest.json` mencatat asal, checksum awal, penggabungan duplikat,
dan lokasi backup pemulihan di folder sementara di luar repository. Backup
bersifat lokal; simpan terpisah jika diperlukan untuk jangka panjang.

Penempatan skill lokal mengikuti
[dokumentasi OpenAI](https://learn.chatgpt.com/docs/build-skills);
entrypoint rules mengikuti
[dokumentasi Rules](https://learn.chatgpt.com/docs/agent-configuration/rules).
Mulai sesi Codex baru setelah migrasi untuk memuat ulang konfigurasi MCP dan
daftar skill dari path lokal.

Hook pembaca rules disinkronkan ke `.codex/hooks.json`. Aktivasi, cakupan,
dan pemeriksaannya dijelaskan di [hooks/README.md](hooks/README.md).
