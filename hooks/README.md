# Hook pembaca rules

Sumber hook berada di `read_rules.py` dan `codex.template.json`.
Jalankan `python .agents/scripts/sync-native.py` dari root proyek untuk
menghasilkan `.codex/hooks.json`. Path script dibuat absolut agar hook tetap
berjalan saat Codex dibuka dari subfolder, termasuk folder dengan Git sendiri.
Jalankan sinkronisasi ulang jika lokasi proyek berubah.

- `UserPromptSubmit` memuat rules sebelum model mulai mengerjakan permintaan.
- `PreToolUse` membaca ulang rules sebelum perintah terminal (`Bash`, termasuk
  `exec_command`) dan edit file (`apply_patch`, alias `Edit`/`Write`).
- Isi `.agents/instructions/project.md`, `.agents/rules/**/*.md`, dan
  `.agents/rules/**/*.rules` dimasukkan sebagai `additionalContext`.
- `.agents/rules/pattern-recognition.rules.instructions.md` terdaftar eksplisit
  sebagai file wajib bersama instruksi proyek dan rules Biz-A. Isi lengkapnya
  dimuat sekali pada setiap event, dibaca ulang dari disk, dan diprioritaskan
  sebelum rules Biz-A. File hilang/kosong menghasilkan keputusan `block`.
- Rules pattern mengarahkan pembacaan
  `.agents/references/biz-a-design-pattern-recognition.md` sebelum perubahan file;
  isi referensi tersebut tetap dibaca oleh agent sesuai instruksi rules.
- `.agents/rules/javascript-readable.rules.instructions.md` juga terdaftar
  sebagai file wajib. Rules format JavaScript dimuat lengkap tepat sekali,
  setelah pattern recognition dan sebelum rules Biz-A, pada kedua event.
  File hilang atau kosong menghasilkan keputusan `block`.
- Kedua handler memakai `additionalContextLimit: 8000`. Batas 5.000 sebelumnya
  terlampaui setelah penambahan rules JavaScript. Pengaturan ini menaikkan
  ambang preview terpotong sesuai
  [dokumentasi resmi OpenAI Hooks](https://learn.chatgpt.com/docs/hooks#large-hook-output);
  jika rules bertambah hingga melewati batas baru, evaluasi kembali ukurannya.
- Referensi rinci dipilih melalui `.agents/references/INDEX.md` sesuai task;
  hook tidak memuat semua referensi sekaligus.
- Jika rules wajib hilang, kosong, atau gagal dibaca, hook mengembalikan
  keputusan `block`. Tidak ada izin otomatis atau perubahan command.
- Hook tidak membaca `.env`, konfigurasi private, prompt pengguna, maupun
  isi command, dan tidak menyimpan log command.

Setelah sinkronisasi, mulai ulang sesi Codex dan buka `/hooks` di Codex CLI
untuk meninjau serta mempercayai dua hook proyek ini. Codex melewati hook
lokal yang belum dipercaya. Ini persyaratan runtime Codex, dijelaskan dalam
[dokumentasi resmi Hooks](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).
Hook tidak mengubah status kepercayaan sendiri.

Verifikasi lokal tanpa menjalankan perintah dari model:

```powershell
python -X utf8 -m unittest discover -s .agents/hooks -p "test_*.py" -v
```

Hook ini mengirim rules sebagai konteks model dan memeriksa ketersediaannya;
hook tidak membuktikan kepatuhan semantik setiap command. Pengiriman input
lanjutan ke proses yang sudah berjalan melalui `write_stdin` tidak memicu
`PreToolUse` baru. Error runtime atau timeout hook dapat dilaporkan Codex tanpa
memblokir tool; pemblokiran di atas berlaku saat script berjalan dan berhasil
mengembalikan keputusan `block` yang valid.
