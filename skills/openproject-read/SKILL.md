---
name: openproject-read
description: "Baca task OpenProject (OP), termasuk task in progress per proyek/assignee, deskripsi, komentar, dan lampiran menggunakan API token lokal .env. Gunakan juga untuk mengambil konteks terbaru sebelum mengerjakan task OP."
---

# Membaca OpenProject

Gunakan API v3 melalui `scripts/read_openproject.py` di skill ini. Script Python
standard library ini hanya menyediakan GET; tidak memerlukan browser atau MCP OP.
Jalankan contoh dari root repository.

## Koneksi

- Script membaca `OPENPROJECT_API_TOKEN` dari `.env` root secara internal. Jangan
  mencetak `.env`, token, atau Authorization; jangan menaruh token pada argumen
  command, URL, file hasil, maupun dokumentasi.
- Server proyek: `https://iproj.my.id:5443`. Override opsional melalui
  `OPENPROJECT_URL` di `.env` atau environment. Environment process diutamakan.
- Autentikasi Basic memakai username `apikey` dan token sebagai password.
  TLS diverifikasi; token tidak diteruskan ke origin lain atau redirect.
- Jika command gagal karena pembatasan sandbox/network, gunakan alur escalation
  terminal untuk mengulang command yang sama. Jangan menyimpulkan token tidak
  valid hanya karena browser tidak tersedia.
- HTTP 401: token tidak diterima; HTTP 403: akses ditolak. Laporkan kegagalan
  aktual dan jangan menyatakan daftar kosong jika pembacaan gagal.

## Task dan komentar

```powershell
python .agents/skills/openproject-read/scripts/read_openproject.py me
python .agents/skills/openproject-read/scripts/read_openproject.py projects --search "Endo"
python .agents/skills/openproject-read/scripts/read_openproject.py statuses
python .agents/skills/openproject-read/scripts/read_openproject.py tasks --project "Endo Medica" --status "In progress"
python .agents/skills/openproject-read/scripts/read_openproject.py task 5507
```

`tasks` default-nya task terbuka milik pemilik token (`--assignee me`). Gunakan
`--assignee all` jika diminta seluruh tim, atau ID user untuk orang tertentu.
`--status all` mencakup task tertutup; `--status open` berarti semua status
terbuka. Nama proyek/status dicocokkan tepat tanpa membedakan kapitalisasi, atau
gunakan ID hasil discovery. Jangan menebak ID. `projects --search` membantu
menemukan ejaan; folder lokal `Endo Medika` berbeda dari nama OP `Endo Medica`.

Script mengambil seluruh halaman. `task ID` memuat detail, seluruh activities
(komentar dan perubahan), serta daftar lampiran. Objek markup `description` dan
`comment` dipertahankan, termasuk `raw`/`html` jika tersedia. Periksa juga gambar
di markup deskripsi/komentar jika lampiran tidak tercantum di daftar task.
Baca koreksi terbaru sebelum implementasi. Catatan lokal `OP-*.md` merupakan
snapshot, bukan bukti status saat ini.

## Lampiran dan output

```powershell
python .agents/skills/openproject-read/scripts/read_openproject.py attachment 3880 --output "tmp/openproject/attachment-3880.png"
```

ID lampiran diperoleh dari `_links.self.href` daftar lampiran atau markup OP.
Script mengikuti metadata `downloadLocation` hanya pada origin OP yang sama dan
menolak menimpa file. Untuk storage eksternal gunakan mekanisme download yang
sesuai tanpa meneruskan token OP. Lihat gambar melalui tool image, atau gunakan
skill PDF/dokumen yang sesuai untuk unduhan.

Output JSON mencantumkan waktu pengambilan UTC. Opsi global `--output FILE`
(sebelum subcommand) menyimpan JSON ke file baru; `--output` setelah `attachment`
khusus berkas unduhan. `--env-file PATH` (sebelum subcommand) mengganti lokasi
`.env`. Simpan respons atau ubah snapshot lokal hanya bila diperlukan oleh task.

Laporkan ID, subject, status, assignee, dan tautan task; bedakan konfirmasi tester
dari verifikasi sendiri. Jangan mengubah status, assignee, komentar, atau jam
kerja lewat skill pembaca. Jika diminta **mengerjakan task**, lanjutkan
implementasi sesuai skill Biz-A yang relevan setelah konteks terbaca.

Referensi resmi: [autentikasi](https://www.openproject.org/docs/api/introduction/),
[work packages](https://www.openproject.org/docs/api/endpoints/work-packages/),
[activities](https://www.openproject.org/docs/api/endpoints/activities/), dan
[attachments](https://www.openproject.org/docs/api/endpoints/attachments/).
