---
name: close
description: Tutup percakapan aktif dengan meninjau dan mendokumentasikan pelajaran baru dari riwayat chat serta menyiapkan pesan commit SVN. Gunakan saat pengguna memanggil $close atau meminta ringkasan akhir chat untuk commit SVN.
---

# Close

1. Tinjau riwayat percakapan aktif yang tersedia dari awal, termasuk ringkasan konteks, koreksi pengguna, hasil percobaan, dan hasil akhir. Kumpulkan perubahan yang benar-benar dikerjakan di semua giliran. Gabungkan revisi berulang berdasarkan hasil akhir dan keluarkan rencana, percobaan yang dibatalkan, serta edit yang sudah dikembalikan dari daftar perubahan.
2. Cari pelajaran terverifikasi yang bisa dipakai pada task berikutnya, seperti akar masalah, perilaku runtime, atau aturan proyek yang dikonfirmasi. Jika ada kandidat, pakai [Biz-A Reviewer](../biz-a-reviewer/SKILL.md) untuk mengecek referensi dan rules yang ada. Simpan materi baru yang berguna sesuai batas penulisan di bawah. Selesaikan dokumentasi sebelum menyusun pesan commit agar status file hasil review ikut diperiksa.
3. Jika working copy SVN tersedia, cocokkan file terkait dengan `svn status` dan periksa `svn diff` bila status saja belum cukup. Jika SVN tidak menemukan file yang ada di disk, periksa folder induknya dengan `svn status --no-ignore`. Batasi pemeriksaan ke perubahan yang bisa dikaitkan dengan chat ini. Untuk satu file yang berisi edit campuran, rangkum bagian yang terkait dan beri catatan jika file perlu ditinjau sebelum commit. Tandai file baru yang masih berstatus unversioned. Laporkan perubahan yang sudah di-commit atau diabaikan SVN di luar pesan commit.
4. Laporkan hasil review dan tautkan dokumentasi yang ditulis. Jika tidak menemukan pelajaran baru, sampaikan bahwa hasil itu berdasarkan riwayat yang tersedia. Sebutkan jika riwayat atau status SVN belum lengkap atau masih ada pekerjaan tertunda. Jika SVN belum bisa diperiksa, dasarkan draf pada perubahan yang terbukti dari chat.
5. Akhiri dengan satu blok teks siap salin. Tulis judul tindakan yang singkat, satu baris kosong, lalu daftar hasil akhir menurut modul atau fitur. Sebutkan file ketika membantu menjelaskan cakupan. Ikuti bahasa pengguna atau format commit yang diminta. Jika tidak ada kandidat commit, laporkan kondisi tersebut dalam teks biasa.

Secara default, penutupan mencakup penulisan dokumentasi yang relevan, kecuali pengguna meminta ringkasan saja atau mode baca-saja. Penulisan file saat penutupan terbatas pada dokumentasi hasil review dan catatan perubahannya. Operasi SVN terbatas pada pemeriksaan.
