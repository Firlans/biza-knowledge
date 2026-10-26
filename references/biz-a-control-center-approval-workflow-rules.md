# Biz-A Control Center: workflow approval berdasarkan PR_BPM

Gunakan saat menganalisis atau membuat workflow approval, BPM Purchase Request,
task approver, assignment role, dan hubungan workflow dengan script domain.
Acuan yang dianalisis: `procurementconfig/PR_BPM.json` dan `procurement/prLib.js`.

## 1. Identitas dan cakupan workflow

| Field JSON | Nilai acuan | Makna |
| --- | --- | --- |
| `workflowKey` | `PROCUREMENT_PR` | Identitas workflow |
| `name` | `Purchase Request Lifecycle` | Nama yang ditampilkan |
| `entityType` | `PURCHASE_REQUEST_ITEM` | Jenis objek runtime untuk setiap item PR |
| `initialStateCode` | `PR_SUBMITTED` | Instance langsung dimulai pada tahap menunggu keputusan |
| `version` | `0` | Versi draft pada file acuan |
| `status` | `DRAFT` | Status definisi workflow, bukan status transaksi PR |

Workflow BPM memakai field root tersebut. Jangan membungkusnya ke dalam
`metadata` konfigurasi domain atau mengganti versi numerik BPM menjadi versi
semantik domain. Dalam engine lokal, publish mensyaratkan definisi `DRAFT`,
menentukan versi publikasi berikutnya, dan menyimpan status `PUBLISHED`.
Menyimpan file JSON tidak berarti workflow sudah dipublikasikan atau diinisiasi.

Di jalur submit yang diperiksa, `prLib.js` mengirim
`entityType: 'PURCHASE_REQUEST_ITEM'` dan `entityIds` dari `savedDetailRows[].id`
ke `initiatePurchaseRequestWorkflowInstance`. Jadi setiap detail `pr_det.id`
memiliki instance sendiri. Jangan memakai `pr.id` atau `instanceId` sebagai
pengganti ID detail, meskipun semuanya berupa angka.

## 2. State, task, dan pelaku

| State | Task saat masuk | Assignment |
| --- | --- | --- |
| `PR_SUBMITTED` | Approve PR | ROLE `APPROVER` |
| `PR_APPROVED` | Process Approved PR | ROLE `PURCHASING` |
| `PR_FULFILLED` | Confirm PR Fulfillment | ROLE `REQUESTER` |
| `PR_RECEIVING` | Confirm Receiving PR | ROLE `REQUESTER` |
| `PR_REJECTED` | Tidak ada; terminal | Tidak ada |
| `PR_CONFIRMED` | Tidak ada; terminal | Tidak ada |
| `PR_NOT_CONFIRMED` | Tidak ada; terminal | Tidak ada |
| `PR_CLOSED` | Tidak ada; terminal | Tidak ada |

Empat state aktif memakai `taskEnabled: 1`, `taskName`,
`assignmentType: 'ROLE'`, dan `assignmentValue`. Empat terminal memakai
`taskEnabled: 0` serta assignment kosong.

Assignment task dan otorisasi transisi berbeda. Contohnya task pada
`PR_APPROVED` ditugaskan ke Purchasing, tetapi transisi Close PR dari state
tersebut diberikan kepada Approver. Jangan menentukan hak transisi hanya
dengan membaca pemilik task.

`roles.APPROVER.label: 'Manager Requester'` hanya label. JSON ini tidak
mendefinisikan siapa atasan requester atau menjamin keputusan hanya dilakukan
oleh atasan langsung. Demikian pula role `REQUESTER` tidak otomatis berarti
user pembuat PR. Periksa pemetaan user/group dan aturan kepemilikan di target.

## 3. Seluruh transisi pada acuan

Semua transisi menggunakan `triggerType: 'USER_EVENT'`. Setiap baris berikut
memiliki satu role yang diizinkan dan satu effect `EMIT_EVENT`.

| Transition code | Dari | Ke | Role | Event |
| --- | --- | --- | --- | --- |
| `PR_SUBMITTED_TO_APPROVED` | `PR_SUBMITTED` | `PR_APPROVED` | `APPROVER` | `PR_APPROVED` |
| `PR_SUBMITTED_TO_REJECTED` | `PR_SUBMITTED` | `PR_REJECTED` | `APPROVER` | `PR_REJECTED` |
| `PR_APPROVED_TO_FULFILLED` | `PR_APPROVED` | `PR_FULFILLED` | `PURCHASING` | `PR_FULFILLED` |
| `PR_APPROVED_TO_RECEIVING` | `PR_APPROVED` | `PR_RECEIVING` | `PURCHASING` | `PR_RECEIVING` |
| `PR_FULFILLED_TO_CONFIRMED` | `PR_FULFILLED` | `PR_CONFIRMED` | `REQUESTER` | `PR_CONFIRMED` |
| `PR_RECEIVING_TO_CONFIRMED` | `PR_RECEIVING` | `PR_CONFIRMED` | `REQUESTER` | `PR_CONFIRMED` |
| `PR_FULFILLED_TO_NOT_CONFIRMED` | `PR_FULFILLED` | `PR_NOT_CONFIRMED` | `REQUESTER` | `PR_NOT_CONFIRMED` |
| `PR_RECEIVING_TO_NOT_CONFIRMED` | `PR_RECEIVING` | `PR_NOT_CONFIRMED` | `REQUESTER` | `PR_NOT_CONFIRMED` |
| `PR_APPROVED_TO_CLOSED` | `PR_APPROVED` | `PR_CLOSED` | `APPROVER` | `PR_CLOSED` |
| `PR_RECEIVING_TO_CLOSED` | `PR_RECEIVING` | `PR_CLOSED` | `APPROVER` | `PR_CLOSED` |

Alur utamanya: Approver menyetujui/menolak; Purchasing memilih Fulfilled atau
Receiving; Requester mengonfirmasi atau tidak mengonfirmasi hasilnya. Approver
dapat menutup PR dari Approved atau Receiving. Tidak ada Close dari Fulfilled
pada JSON ini; jangan menambahkan jalur tersebut tanpa kebutuhan bisnis.

`PR_REJECTED` dan `PR_NOT_CONFIRMED` adalah terminal, bukan jalur revisi.
Tidak ada transisi keluar dari empat terminal. Semua delapan state dapat
dicapai dari `PR_SUBMITTED`.

## 4. Bentuk deklarasi untuk workflow baru

Gunakan bentuk JSON flat yang benar-benar dibaca engine lokal. Contoh berikut
merupakan potongan `transitions`, bukan definisi workflow lengkap:

```json
{
  "transitionCode": "PR_SUBMITTED_TO_APPROVED",
  "fromStateCode": "PR_SUBMITTED",
  "toStateCode": "PR_APPROVED",
  "triggerType": "USER_EVENT",
  "label": "Approve PR",
  "guardType": null,
  "guardRuleKey": null,
  "roles": [{ "roleCode": "APPROVER" }],
  "effects": [{
    "effectType": "EMIT_EVENT",
    "eventName": "PR_APPROVED",
    "payloadTemplate": null
  }]
}
```

Untuk menyusun workflow approval baru:

1. Tentukan objek yang disetujui: header atau detail. Pilih `entityType` dan
   sumber `entityId` yang konsisten dari create, initiate, lookup instance,
   inbox, history, hingga eksekusi transisi.
2. Tentukan state awal, state aktif, dan hasil terminal sesuai kebutuhan.
   Acuan ini dimulai saat submitted; draft transaksi, revisi, resubmit,
   approval bertingkat, dan pembukaan ulang belum dimodelkan.
3. Tentukan task/assignment pada tiap state aktif dan role pada tiap transisi.
   Bentuk role transisi adalah array object `{ "roleCode": "APPROVER" }`.
   Pada engine lokal, role transisi kosong berarti terbuka bagi semua role;
   jangan mengosongkannya untuk aksi yang harus dibatasi.
4. Tentukan aturan tambahan yang memang diperlukan. Seluruh `guardType` dan
   `guardRuleKey` acuan bernilai null: tidak ada syarat nominal, larangan
   approve sendiri, alasan penolakan wajib, atau pemeriksaan kelengkapan pada
   guard BPM. Jangan mengklaim aturan tersebut tersedia hanya dari nama role.
5. Tentukan effect setelah transisi berhasil. `EMIT_EVENT` mengumumkan event;
   ia bukan perintah untuk melakukan transisi lain, membuat PO, atau posting
   FINA secara otomatis. Periksa subscriber/handler terpisah bila diperlukan.
6. Tentukan SLA/timeout hanya bila dibutuhkan. Acuan seluruhnya null dan tidak
   memiliki transisi timer atau eskalasi. Verifikasi dukungan guard/effect
   tambahan terhadap engine target sebelum memilihnya.
7. Cocokkan deklarasi `terminalStates` dengan graph transisi. Engine lokal
   menentukan terminal dari tidak adanya outgoing transition; label terminal
   saja tidak cukup. State terminal tidak boleh memiliki task aktif.

Nama dan kode PR pada contoh bukan persyaratan universal. Buat kode baru
sesuai proses pengguna dan jaga konsistensinya pada seluruh pemanggil.

## 5. Hubungan dengan script dan domain config

Jalur custom pada `procurement/prLib.js` yang perlu ditelusuri:

1. Submit menyimpan header/detail dan memperoleh ID detail yang tersimpan.
   Pada jalur submit baru yang diperiksa, helper initiate dipanggil per ID
   detail; edit PR yang sudah ada melewati initiate pada jalur tersebut.
2. `initiatePurchaseRequestWorkflowInstance` memanggil
   `workflowRTSvc.initiate(entityType, entityId)`. Pastikan definisi yang sesuai
   sudah tersedia/published di target sebelum mencoba jalur ini.
3. `loadApprovalPurchaseRequestAvailableActions` mencari instance berdasarkan
   `entityType` dan ID detail, memuat role user, lalu memanggil
   `workflowRTSvc.availableTransitions(instanceId, userRoles, entityData)`.
   Role user pada contoh dibaca melalui membership `SYS$UGMEMBER` dan
   `SYS$USERGROUP`; object `roles` pada file BPM tidak membuat membership.
4. Tombol dibentuk dari transisi yang tersedia, bukan daftar hardcode untuk
   semua state. Kode action membaca konteks workflow terbaru sebelum eksekusi.
5. Handler approve/reject/generic menggunakan
   `workflowRTSvc.executeTransition(instanceId, transition, userRoles, entityData)`.
   ID detail, ID instance, dan `transitionCode` memiliki arti berbeda.
6. Verifikasi state/history/task serta hasil refresh setelah aksi. Untuk
   effect tambahan, verifikasi subscriber dan hasil effect secara terpisah.

Config `procurementconfig/purchaseRequestConfig.js` menyediakan entry point
`aprovalPRForm` dan `approvalPRDetailForm` yang memanggil handler lewat
`afterLoadData`. Nama `aprovalPRForm` mengikuti ejaan yang ada pada config;
jangan menggantinya sebagian tanpa memperbarui pemanggil/menu.

File acuan memakai adapter custom `PURCHASE_REQUEST_ITEM`, sedangkan entity
domain config bernama `purchase_request` dan `purchase_request_detail`.
Jangan menganggap nama-nama tersebut otomatis sama. Pada jalur Workflow Studio
yang memvalidasi `domain`/`entityType` terhadap `model.entities`, tentukan
mapping yang sah dan sesuaikan pemanggil secara utuh. Jangan menyalin identitas
custom tersebut ke domain lain tanpa memeriksa kontrak integrasinya.

## 6. Validasi dan batas hasil analisis

Pada pemeriksaan lokal, `validateWorkflow` dari paket terpasang menerima
`procurementconfig/PR_BPM.json` tanpa error atau warning, baik profil `engine`
maupun `ai`: 8 state, 10 transisi, 3 role, 4 state dengan task, dan 4 terminal.
Ini bukan bukti bahwa workflow, role, dan library sudah tersedia di server.

Untuk memeriksa definisi dari root repository:

```javascript
const fs = require('node:fs');
const workflow = JSON.parse(fs.readFileSync('procurementconfig/PR_BPM.json', 'utf8'));
import('./node_modules/biz-a-cli/engine/bpm/validateWorkflow.js').then(({ validateWorkflow }) => {
    console.log(validateWorkflow(workflow));
    console.log(validateWorkflow(workflow, { profile: 'ai' }));
});
```

Selain validasi struktur, periksa reachability, tidak adanya outgoing dari
terminal, assignment task, serta hak tiap role pada setiap state. Pada target,
uji minimal approve, reject, kedua cabang pemenuhan, confirm/not confirmed,
close, role yang tidak diizinkan, dan usaha melakukan transisi setelah terminal.
Verifikasi ID item tetap sama sepanjang proses. Jangan menyatakan workflow
siap runtime hanya karena JSON valid atau tombol UI muncul.

Untuk permintaan analisis/update skill, cukup dokumentasikan dan validasi
lokal; jangan mengubah definisi PR, membuat role user, memulai instance, atau
melakukan publish ke server.

## Referensi implementasi

- `procurementconfig/PR_BPM.json`: definisi acuan yang dianalisis.
- `procurementconfig/purchaseRequestConfig.js`: UI/config domain PR.
- `procurement/prLib.js`: initiate instance, role loader, available actions,
  dan handler eksekusi approval.
- `node_modules/biz-a-cli/engine/bpm/validateWorkflow.js`: validator definisi.
- `node_modules/biz-a-cli/engine/bpm/rules.js`: compile, role, terminal, dan task.
- `node_modules/biz-a-cli/engine/bpm/workflow.js`: save/publish/versioning.
- `node_modules/biz-a-cli/engine/bpm/workflow-runtime.js`: runtime dan effect.
- `node_modules/biz-a-cli/engine/cc/configValidate.js`: validasi workflow/domain.
- `ROBYRAJASA/branches/dev/docs/biz-a-bpm-spec-v1.0.md`: acuan desain BPM;
  verifikasi kontrak aktual terhadap runtime lokal yang terpasang.
