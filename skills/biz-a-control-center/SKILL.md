---
name: biz-a-control-center
description: "Create, inspect, and document Biz-A Control Center application/domain configs and BPM approval workflows. Use for App Config, APPLICATION_CONFIG, DOMAIN_CONFIG, required metadata, uploaded source names, script handler wiring, PR_BPM, workflow states/transitions, task assignment, and approval roles. Ordinary legacy form/list business logic uses the relevant Biz-A skill."
---

# Biz A Control Center

Gunakan untuk konfigurasi aplikasi/domain, analisis script, dan workflow approval
Biz-A Control Center.

## Referensi proyek

Di workspace Biz-A, baca `.agents/references/biz-a-control-center-config-rules.md`
sebelum mengubah konfigurasi atau mendokumentasikan hasil analisis. File ini
memuat contoh metadata, aturan source, alur eksekusi, dan batas verifikasi.
Jika referensi tersebut tidak tersedia di workspace lain, terapkan aturan inti
di bawah dan verifikasi kontraknya terhadap config serta runtime lokal.

Untuk perubahan pada editor Control Center, baca bagian relevan dari
`.agents/docs/biz-a-control-center-spec-v1.0.md` jika tersedia. Gunakan
ROBYRAJASA, procurementconfig, dan procurement sebagai contoh sesuai konteks;
periksa konsistensinya sebelum menyalin.

## Aturan inti

- Sertakan `metadata` pada setiap konfigurasi aplikasi dan domain. Pastikan
  `metadata.name` dan versi semantik `metadata.version` terisi untuk domain;
  metadata aplikasi tidak menggantikan metadata domain.
- Samakan `domains[key].source` dengan nama dan versi domain yang benar-benar
  diunggah pada App Config Biz-A. Pada upload CLI, identitas ini berasal dari
  `metadata.name@metadata.version`. Alias, nama folder, nama file, dan
  `metadata.id` bukan pengganti nama source.
- Analisis script melalui menu, entry point, entity/structure, event binding,
  event handler, dan library yang dimuat. Cocokkan namespace handler dengan
  paket library; jangan menyamakannya otomatis dengan alias domain config.
- Pastikan library sudah ditambahkan ke Biz-A target, bukan hanya tersedia
  lokal atau dideklarasikan di config. Pada kasus FRS/procurement, pengguna
  mengonfirmasi error `Cannot read properties of undefined (reading 'id')`
  disebabkan library belum ditambahkan. Perintah yang digunakan:
  `biza add -s https://server.biz-a.id --sub frs`, dari folder library yang
  akan diunggah. Detail dan batas penerapannya ada pada referensi proyek.
- Pisahkan pemeriksaan struktur lokal, pembuatan template, dan eksekusi pada
  browser/server. Kelulusan lokal tidak membuktikan alur runtime berhasil.
- Temuan source/entity tetap diperiksa terpisah; keduanya bukan penyebab error
  kasus tersebut yang dikonfirmasi pengguna. Pesan error serupa pada kasus lain
  tetap memerlukan pemeriksaan, bukan otomatis dianggap library belum diunggah.

## Workflow approval BPM

Untuk `PR_BPM`, workflow approval/approvement, state/transisi, assignment task,
dan role approver, baca
`.agents/references/biz-a-control-center-approval-workflow-rules.md`.
Referensi memuat analisis `procurementconfig/PR_BPM.json`, matriks transisi,
hubungan dengan `procurement/prLib.js`, dan panduan pembuatan workflow baru.

- Bedakan definisi BPM flat (`workflowKey`, `entityType`, `initialStateCode`,
  `states`, `transitions`, versi numerik/status definisi) dari metadata domain.
- Tentukan sejak awal approval berlaku per header atau per detail. Pada PR
  acuan, instance menggunakan `PURCHASE_REQUEST_ITEM` dan ID detail `pr_det.id`.
  Jaga kesesuaian initiate, lookup instance, inbox, history, dan execute.
- Pisahkan assignment task dari hak role transisi. Label role tidak otomatis
  memetakan atasan requester atau menjamin hanya pembuat PR yang bisa confirm.
- Ambil aksi dari available transitions sesuai state/role. Jangan menetapkan
  state bisnis langsung untuk menggantikan eksekusi transisi engine.
- Jangan menganggap acuan memiliki revisi, resubmit, approval bertingkat,
  guard, atau SLA. Tambahkan hanya sesuai kebutuhan pengguna dan kontrak target.
- Validasi definisi dengan validator BPM lokal dan periksa graph/role/task;
  pisahkan hasil tersebut dari pengujian server. Permintaan analisis/update
  skill tidak mengizinkan publish atau menjalankan instance workflow.

## Hasil analisis

Laporkan metadata/source yang diperiksa, hubungan antarbagian script, cakupan
verifikasi yang benar-benar dijalankan, dan masalah yang masih terbuka. Untuk
tugas dokumentasi, jangan mengubah kode aplikasi atau melakukan publish.
