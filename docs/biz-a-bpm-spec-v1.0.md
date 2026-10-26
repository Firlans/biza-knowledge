# Biz-A BPM

# Specification v1.0 {#specification-v1.0}

## Daftar Isi {#daftar-isi}

[Specification v1.0](#specification-v1.0)

[Daftar Isi](#daftar-isi)

[Tujuan & Scope](#tujuan-&-scope)

[Prinsip Rancangan Inti](#prinsip-rancangan-inti)

[Cakupan BPM](#cakupan-bpm)

[Konsep Kunci dan Definisi](#konsep-kunci-dan-definisi)

[Istilah \- istilah / Definisi :](#istilah---istilah-/-definisi-:)

[Definisi Design-Time vs Runtime (Execution Time)](#definisi-design-time-vs-runtime-\(execution-time\))

[Design-time](#design-time)

[Runtime](#runtime)

[Design-Time](#design-time-1)

[Workflow Definition Template](#workflow-definition-template)

[Metadata](#metadata)

[Settings](#settings)

[Roles](#roles)

[States](#states)

[TaskConfig](#taskconfig)

[Assignment](#assignment)

[SLA Config](#sla-config)

[TimeoutAction](#timeoutaction)

[Transitions](#transitions)

[Guard](#guard)

[Effect](#effect)

[Tipe Primitif](#tipe-primitif)

[Compile](#compile)

[Workflow Versioning](#workflow-versioning)

[Tabel Database (Workflow Definition)](#tabel-database-\(workflow-definition\))

[SYS\$BPM\_WORKFLOW\_DEF](#sys$bpm_workflow_def)

[SYS\$BPM\_STATE\_DEF](#sys$bpm_state_def)

[SYS\$BPM\_TRANS\_DEF](#sys$bpm_trans_def)

[SYS\$BPM\_TRANS\_ROLE](#sys$bpm_trans_role)

[SYS\$BPM\_TRANS\_EFFECT\_DEF](#sys$bpm_trans_effect_def)

[Tabel Database (Workflow Execution)](#tabel-database-\(workflow-execution\))

[SYS\$BPM\_WF\_INSTANCE](#sys$bpm_wf_instance)

[SYS\$BPM\_STATE\_HISTORY](#sys$bpm_state_history)

[SYS\$BPM\_TASK](#sys$bpm_task)

[SYS\$BPM\_TIMER\_JOB](#sys$bpm_timer_job)

[SYS\$BPM\_EFFECT\_LOG](#sys$bpm_effect_log)

[Runtime](#runtime-1)

[Aturan State Lifecycle](#aturan-state-lifecycle)

[User & Role](#user-&-role)

[Timer](#timer)

[API](#api)

[Fungsi](#fungsi)

[Aturan umum](#aturan-umum)

[Error Code](#error-code)

[Entry points](#entry-points)

[Ambil Workflow State](#ambil-workflow-state)

[Tujuan](#tujuan)

[Endpoint](#endpoint)

[Query Parameters](#query-parameters)

[Response](#response)

[Kemungkinan error](#kemungkinan-error)

> > > [Instance not found](#instance-not-found)

[Ambil Transitions yang Tersedia](#ambil-transitions-yang-tersedia)

[Tujuan](#tujuan-1)

[Endpoint](#endpoint-1)

[Request Body](#request-body)

[Response](#response-1)

[Catatan](#catatan)

[Eksekusi Transition](#eksekusi-transition)

[Tujuan](#tujuan-2)

[Endpoint](#endpoint-2)

[Request body](#request-body-1)

[Success Response](#success-response)

[Rejected Response](#rejected-response)

[Failed Response](#failed-response)

[Ambil My Tasks](#ambil-my-tasks)

[Tujuan](#tujuan-3)

[Endpoint](#endpoint-3)

[Request Body](#request-body-2)

[Response](#response-2)

[Catatan](#catatan-1)

[Ambil workflow history](#ambil-workflow-history)

[Tujuan](#tujuan-4)

[Endpoint](#endpoint-4)

[Query Parameter](#query-parameter)

[Response](#response-3)

[Ambil Effect Executions](#ambil-effect-executions)

[Tujuan](#tujuan-5)

[Endpoint](#endpoint-5)

[Query Parameters](#query-parameters-1)

[Response](#response-4)

[Retry Effect Executions](#retry-effect-executions)

[Tujuan](#tujuan-6)

[Endpoint](#endpoint-6)

[Request Body](#request-body-3)

[Response](#response-5)

[Failure Response](#failure-response)

[Perilaku](#perilaku)

[Perilaku Eksekusi Transition](#perilaku-eksekusi-transition)

[Perilaku Handling Task](#perilaku-handling-task)

[Perilaku Handling Timer / SLA](#perilaku-handling-timer-/-sla)

[Perilaku Idempotency](#perilaku-idempotency)

[Perilaku Concurrency](#perilaku-concurrency)

[Perilaku Eksekusi Effect](#perilaku-eksekusi-effect)

[Kebijakan Retry](#kebijakan-retry)

[Perilaku UI](#perilaku-ui)

[HTTP Status](#http-status)

[Apa yang Tidak Tercakup dalam BPM](#apa-yang-tidak-tercakup-dalam-bpm)

[History](#history)

## Tujuan & Scope {#tujuan-&-scope}

Biz-A BPM adalah sebuah engine workflow orchestration yang generik untuk mengelola transisi entity state berdasarkan aturan yang jelas.

Sistem dirancang agar:

* Bisa digunakan untuk domain sistem apa pun (mis: FINA, Biz-A MES, atau ERP lainnya).  
* Menghindari business logic yang diselipkan  
* Minimalisir customization  
* Bisa digunakan lintas industri

Biz-A BPM tidak menyimpan data bisnis, tidak juga implemen business rule.  
Biz-A BPM adalah sebuah mesin lifecycle, bukan sebuah mesin business logic

## Prinsip Rancangan Inti {#prinsip-rancangan-inti}

1. Lifecycle bukan logika  
   1. BPM menangani kapan sesuatu terjadi, bukan bagaimana sebuah logika bisnis bekerja.  
2. Explicit bukan implisit  
   1. Tidak ada auto transition  
   2. Tidak ada perubahan state yang tersembunyi  
3. Definition design time ≠ runtime  
   1. Workflow config akan dikompilasi  
   2. Runtime menggunakan definisi yang sudah dinormalisasi dan disimpan di database.  
4. Immutable History  
   1. State transition hanya bisa ditambahkan  
   2. Tidak ada state yang bisa ditulis ulang  
5. Satu entity, satu lifecycle  
   1. Setiap entity hanya memiliki 1 state aktif  
6. Biz-A BPM menentukan *kapan* sebuah entity boleh berubah state. Domain system menentukan apa yang terjadi saat perubahan itu terjadi.

## Cakupan BPM {#cakupan-bpm}

1. BPM bertanggung jawab terhadap:  
   1. Mendefinisikan workflow  
   2. Mengelola states  
   3. Validasi transisi  
   4. Menjaga roles  
   5. Mencatat state history  
   6. Mengeluarkan event lifecycle  
2. BPM tidak bertanggung jawab atas:  
   1. Menyimpan entity attributes  
   2. Validasi business rules  
   3. Melakukan perhitungan  
   4. Integrasi dengan mesin atau ERP  
   5. Render UI Layout

## Konsep Kunci dan Definisi {#konsep-kunci-dan-definisi}

1. Entity  
   1. Definisi: Sebuah **domain object** yang lifecycle-nya diorkestrasikan oleh BPM.  
   2. Contoh:  
      1. ProductionExecution  
      2. PurchaseApproval  
      3. QualityInspection  
   3. Aturan main:  
      1. Data Entity disimpan di dalam sistem domain  
      2. BPM hanya mengacu ke entity melalui entity\_type \+ entity\_id  
2. Workflow  
   1. Definisi: Sebuah **workflow template** yang mendefinisikan bagaimana sebuah entity bergerak dari satu state ke state yang lain.  
   2. Sebuah workflow terdiri dari:  
      1. States  
      2. Transitions  
   3. Workflow harus  
      1. Dibedakan versinya  
      2. Tidak boleh berubah saat sudah dipublikasi  
      3. Bisa digunakan ulang lintas entity dengan tipe yang sama.  
   4. workflow adalah **definitions**, bukan runtime object.  
3. State  
   1. Definisi: Sebuah **kondisi stabil** dari sebuah entity instance.  
   2. Sifatnya:  
      1. Explicit  
      2. Mutually exclusive  
      3. Hanya ada 1 yang aktif di saat yang bersamaan  
      4. Tidak ada transisi yang implisit  
   3. Contoh:  
      1. DRAFT  
      2. READY  
      3. IN\_PROGRESS  
      4. COMPLETED  
4. Transition  
   1. Definisi: sebuah **pergerakan yang eksplisit** dari satu state ke state lain.   
   2. Sebuah Transition terdiri dari:  
      1. Asal state  
      2. Target state  
      3. Trigger type  
      4. Rule →  menvalidasi apakah perpindahan dari “Asal” state → “Target” state diperbolehkan (True / False).   
      5. Effect  
      6. Roles yang diperbolehkan  
   3. Tidak ada transition \= tidak ada perubahan state  
5. Rule  
   1. Definisi: Sebuah batasan bisnis yang dievaluasi oleh domain.  
   2. Rules didefinisikan oleh domain, di simpan di sistem ini (BPM).  
   3. Domain akan meminta opsi state berikutnya dari BPM dengan mengirimkan, “Asal” state, user role, dan entity\_id. Kemudian BPM kirim semua opsi “Target” state dan “Rule” berdasarkan “asal” state dan role.  
   4. Domain yang akan memvalidasi “Target” state yang mana saja yang valid, berdasarkan rule.  
   5. Domain kemudian initiate proses transisi dengan mengirimkan entity\_id, asal state dan target state ke BPM.  
   6. Karakteristik:  
      1. Read-only  
      2. Deterministik  
      3. Tidak ada side-effect  
6. Event  
   1. Definisi: Sesuatu yang memicu evaluasi dari sebuah transisi.  
   2. Tipe-tipe event:  
      1. USER\_EVENT (mis: klik tombol)  
      2. SYSTEM\_EVENT (domain event)  
      3. TIMER\_EVENT (Transition nya di picu oleh interval waktu di dalam BPM nya, bukan dari luar). Note : belum ada property / field untuk handle intervalnya.  
      4. EXTERNAL\_EVENT (API/Integration)  
7. effect  
   1. Definisi: Sebuah efek sampingan yang dieksekusi setelah sebuah transition yang berhasil.  
   2. Agar BPM tidak dependen dengan domain system, effect yang diperbolehkan hanya emit event.  
   3. effect tidak boleh mengubah BPM state secara langsung.  
8. Role  
   1. Definisi: Sebuah nama untuk mengelompokan tanggung jawab dan otoritas.  
   2. Role menentukan apa yang boleh kamu lakukan, bukan siapa diri anda.  
9. Kosa kata lainnya:  
   1. Actor  
      1. Definisi: Seorang atau sebuah sistem yang melakukan suatu effect.  
      2. Actor ≠ user account  
   2. Task  
      1. Definisi: Sebuah satuan tugas yang ditugaskan ke seorang actor  
      2. Task adalah tugas yang harus diselesaikan, bukan states, sebelum bisa terjadi transition.  
   3. Workflow Instance  
      1. Definisi: Sebuah wujud nyata workflow dari sebuah entity yang sedang berjalan  
      2. Entity yang sudah di \- assign workflow  
   4. Perbedaan antara Workflow instance dan Task

| Aspek | Workflow Instance | Task |
| ----- | ----- | ----- |
| Tujuan | Melacak lifecycle | Drive action |
| Scope | Seluruh proses | Satu langkah |
| Owner | System | User / actor |
| Quantity | 1 per entity | 0..N per state |
| Lifetime | Start → End | Created & completed |
| UI | Status view | “My Task” |

   5. Lifecycle  
      1. Definisi: Semua transition yang mungkin dilalui sebuah instance workflow dari hidup sampai mati.  
   6. Workflow Versioning  
      1. Definisi: Mengelola perubahan atas workflow definition seiring perjalanan waktu.  
      2. Instances yang sedang berjalan tidak boleh error.

## Istilah \- istilah / Definisi : {#istilah---istilah-/-definisi-:}

1. Exception  
   1. Definisi: Sebuah deviasi dari jalur normal  
   2. Exception adalah normal, jangan dianggap sebagai kesalahan.  
2. Escalation  
   1. Definisi: Penugasan ulang atau alert secara otomatis saat kondisi tertentu tidak terpenuhi.  
   2. Awas terhadap waktu & tanggung jawab.  
3. Orchestration  
   1. Definisi: Koordinasi beberapa workflow dan effect untuk mencapai sebuah hasil.  
   2. Orchestration mengendalikan urutan dan dependensi.  
4. Idempotency  
   1. Definisi: Melakukan hal yang sama 2 kali mempunyai efek yang sama seperti sekali.  
   2. Penting untuk kehandalan.  
   3. Contoh 2 kali klik tetap hasilnya 1x yang masuk.  
5. Compensation  
   1. Definisi: Membatalkan atau menyeimbangkan sebuah effect yang sudah dieksekusi.  
   2. Bukan rollback. Ini ada effect untuk perbaikan  
6. Audit Trail  
   1. Definisi: Catatan perubahan state dan effects yang tidak boleh diubah.  
   2. Harus bisa dipercaya  
7. SLA / Timer  
   1. Definisi: Batasan waktu atas state atau task.  
   2. Waktu adalah aturan paling penting

## Definisi Design-Time vs Runtime (Execution Time) {#definisi-design-time-vs-runtime-(execution-time)}

### Design-time {#design-time}

1. Ditangani oleh BPM Compiler  
2. Termasuk  
   1. workflow definitions  
   2. States  
   3. Transitions  
   4. Roles  
   5. UI metadata  
3. Disimpan dalam bentuk definisi yang sudah normalized dan ada versinya.  
4. Disimpan di:  
   1. `Bpm_workflow_definition`  
   2. `Bpm_state_definition`  
   3. `Bpm_transition_definition`  
5. Setelah dipublikasikan:  
   1. Tidak boleh berubah  
   2. Harus dibedakan versinya

### Runtime {#runtime}

1. Ditangani oleh BPM Runtime engine  
2. Termasuk  
   1. workflow instances  
   2. Current state  
   3. Transition execution  
   4. State history  
   5. Event emission  
3. Runtime tidak boleh baca JSON config secara langsung  
4. Disimpan di  
   1. `Bpm_workflow_instance`  
   2. `Bpm_state_history`

## Design-Time {#design-time-1}

### Workflow Definition Template {#workflow-definition-template}

Template berupa format JSON ini merupakan definisi awal pembuatan workflow. Template ini pada saat di-publish, akan di-compile dan disimpan ke dalam [tabel](#tabel-database-\(workflow-definition\)).  
Tujuan template dibuat dulu dalam bentuk json adalah agar mudah dalam membandingkan antar revisi.

Berikut format top level definisi sebuah workflow:

WorkflowDefinition::={  
  metadata    : [Metadata](#metadata),  
  settings    : [Settings](#settings),  
  roles       : [Roles](#roles),  
  states      : [States](#states),  
  transitions : [Transition](#transitions)\[\]  
}

#### Metadata {#metadata}

Metadata::={  
  id           : String,  
  name         : String,  
  version      : String,  
  entityType   : String,  
  description? : String,  
}

Aturan:

1. Id \= key workflow yang unik  
2. Version \= immutable setelah di-publish  
3. entityType \= domain entity

#### Settings {#settings}

Settings::={  
  initialState   : [StateCode](#tipe-primitif),  
  terminalStates : [StateCode](#tipe-primitif)\[\]  
}

#### Roles {#roles}

Roles::={  
  \<roleCode\>: {  
    label        : String,  
    description? : String  
  }  
}

Penjelasan:

* Definisi role hanya digunakan di internal workflow template ini saja.  
* Untuk mapping antara BPM role dengan Biz-A User group akan dilakukan di level application config.

#### States {#states}

States::={  
  \<stateCode\>: {  
    label        : String,  
    description? : String,  
    task         : [TaskConfig](#taskconfig),  
    sla?         : [SlaConfig](#sla-config)  
  }  
}

#### TaskConfig {#taskconfig}

TaskConfig::={  
  enabled     : Boolean,  
  name?       : String,  
  assignment? : [Assignment](#assignment)  
}

#### Assignment {#assignment}

Assignment::={  
  type  : "ROLE" | "USER" | "DYNAMIC",  
  value : String  
}

Penjelasan:

1. Tipe "DYNAMIC" disimpan untuk versi yang akan datang.  
2. 

#### SLA Config {#sla-config}

SlaConfig::={  
  durationMinutes : Number,  
  onTimeout       : [TimeoutAction](#timeoutaction)  
}

#### TimeoutAction {#timeoutaction}

TimeoutAction::={  
  type          : "EMIT\_EVENT" | "AUTO\_TRANSITION",  
  eventName?    : String,  
  transitionId? : String  
}

Penjelasan:

1. "AUTO\_TRANSITION" disimpan untuk versi yang akan datang.

#### Transitions {#transitions}

Transition::={  
  id          : String,  
  from        : [StateCode](#tipe-primitif),  
  to          : [StateCode](#tipe-primitif),  
  triggerType : "USER\_EVENT" | "SYSTEM\_EVENT" |   
                "TIMER\_EVENT" | "EXTERNAL\_EVENT",  
  label       : String,  
  roles       : [RoleCode](#roles)\[\],  
  guard?      : [Guard](#guard),  
  effects?    : [Effect](#effect)\[\]  
}

**⏱️ Mekanisme Eksekusi: Timer Job (SLA Timeout)**

Timer Job berjalan secara otomatis ketika sebuah *State* memiliki slaDurationMinutes dan batas waktu tersebut telah terlewati. Saat SLA terlanggar (*Breached*), terdapat 2 jenis tindakan (Action Types) yang bisa dieksekusi oleh engine:

1. **EMIT EVENT**  
   * **Cara Kerja:** Engine tidak memindahkan posisi state alur kerja. Sebagai gantinya, engine akan secara otomatis men- *generate* tugas CLI\_SCRIPT baru dan memasukkannya ke dalam antrean *Effect Log*.  
   * **Payload Injeksi:** Engine akan secara otomatis menginjeksi payload { "instanceId": \<ID\_Workflow\> } ke dalam script agar pengembang mengetahui *instance* mana yang mengalami pelanggaran waktu.  
2. **AUTO TRANSITION**  
   * **Cara Kerja:** Engine memindai seluruh jalur keluar dari *State* saat ini untuk mencari transisi yang memiliki trigger\_type \= "TIMER\_EVENT".  
   * **Validasi:** Engine akan mengevaluasi *Guard Rules* pada transisi tersebut. Jika ada lebih dari satu jalur yang valid (ambigu), eksekusi akan digagalkan. Jika tepat satu jalur yang valid, sistem akan memaksa alur kerja berpindah secara otomatis.

#### Guard {#guard}

Guard::={  
  type    : "DOMAIN\_RULE",  
  ruleKey : String  
}

#### Effect {#effect}

Effect::={  
  type: "EMIT\_EVENT",  
  eventName: String  
}

**⚙️ Mekanisme Eksekusi: BPM Effect**

BPM Effect adalah tugas otomatis yang dieksekusi oleh *BPM Agent* secara asinkron (di latar belakang) setelah sebuah transisi berhasil dilakukan. Terdapat 3 jenis tipe eksekusi (*Effect Type*):

1. **CLI\_SCRIPT (Background Worker)**  
   * **Cara Kerja:** Menjalankan script internal Biz-A melalui cliWorkerPool pada thread latar belakang. Nama script diambil dari properti eventName.  
   * **Super Power (Chain Transition):** Jika script mengembalikan objek JSON yang memiliki properti { executeTransition: "KODE\_TRANSISI" }, BPM Engine akan secara otomatis memicu transisi lanjutan berjenis SYSTEM\_EVENT menggunakan *System Role*.  
   * **Retry:** Jika terjadi *error* pada script, status akan berubah menjadi RETRYING (maksimal 3 kali percobaan) sebelum akhirnya menjadi FAILED.  
2. **HTTP (Synchronous API Call)**  
   * **Cara Kerja:** Melakukan *request* (Axios) ke sistem eksternal dan **menunggu** hingga ada balasan dari server tujuan (*awaited*). Payload **wajib** memiliki properti `url`. Properti lainnya bersifat opsional karena memiliki nilai *default*: `method` (default: "POST"), `data` (default: `{}`), dan `headers` (default: `{}`). Catatan : resposne yang diterima tidak akan diproses lebih lanjut. Dianggap success bila status code tidak \>= 400\.  
   * **Retry:** Jika HTTP Status Code mengembalikan `>= 400`, engine akan melempar *error* (menganggapnya gagal) dan melakukan *retry* otomatis hingga 3 kali.  
3. **WEBHOOK (Asynchronous Fire-and-Forget)**  
   * **Cara Kerja:** Melakukan pengiriman data secara asinkron tanpa menunggu balasan dari server eksternal.  
   * **Retry:** Tidak ada mekanisme *retry*. Jika server tujuan mati atau gagal (Status \>= 400), log akan mencatat *Silent Failure*, namun status Effect di database tetap dianggap SUCCESS.

#### Tipe Primitif {#tipe-primitif}

StateCode := String  
RoleCode  := String

Konvensi:

* Semua huruf besar dengan underscore (mis: SUBMITTED, APPROVED, WAIT\_ACC)

#### Compile {#compile}

Saat workflow template definition akan di-publish, aturan-aturan berikut harus dijaga:

1. Aturan [State](#states)  
   1. initialState ∈ states  
   2. terminalStates ⊆ states (AA: terminalStates ⊆ states  ∧  terminalStates ≠ ∅)  
   3. TERMINAL state:  
      1. Tidak boleh ada outgoing transition  
      2. Harus task.enabled \= false  
2. Aturan [Transition](#transitions)  
   1. from ∈ states  
   2. to ∈ states  
   3. roles ⊆ Roles  
   4. Tidak ada transition dari terminal state  
   5. Id harus unik  
3. Aturan [Task](#taskconfig)  
   1. Jika task.enabled \= true:  
      1. task.name harus ada  
      2. task.assignment harus ada  
   2. Jika state ∈ terminalStates:  
      1. task.enabled harus false  
4. Aturan [SLA](#sla-config)  
   1. Timer dibuat saat masuk ke state  
   2. Dibatalkan saat keluar dari state  
5. Aturan [Guard](#guard)   
   1. Guard harus **read-only**.  
   2. Tidak ada efek samping.  
   3. Dievaluasi oleh domain sebelum transisi.  
6. Aturan [Effect](#effect)  
   1. Dieksekusi SETELAH transisi berhasil  
   2. Tidak boleh mengubah state BPM  
   3. Domain yang harus handle effect  
7. Aturan [TimeoutAction](#timeoutaction):  
   1. Jika type=EMIT\_EVENT → eventName harus ada  
   2. Jika type \= AUTO\_TRANSITION → transitionId dibutuhkan

### Workflow Versioning {#workflow-versioning}

1. Setiap workflow ada version-nya  
2. Setiap dipublikasi, buat version baru  
3. Workflow instance yang lagi berjalan tetap menggunakan versi sebelumnya  
4. Satu Workflow instance  akan terikat pada **satu workflow version selamanya**.  
5. Tidak boleh ada perubahan versi atas workflow yang aktif.  
6. Multiple versi bisa jalan secara bersamaan

### Tabel Database (Workflow Definition) {#tabel-database-(workflow-definition)}

#### SYS\$BPM\_WORKFLOW\_DEF {#sys$bpm_workflow_def}

Menyimpan 1 versi workflow yang di-publish.

SYS\$BPM\_WORKFLOW\_DEF  
\- id                 PK  
\- workflow\_key       varchar(100)  
\- version            integer null  
\- name               varchar(200)  
\- entity\_type        varchar(100)  
\- description        varchar(500)  
\- initial\_state\_code varchar(100)  
\- status             varchar(20) \-- DRAFT | PUBLISHED | RETIRED  
\- definition\_json    blob/text  
\- created\_at         timestamp not null — must used server timezone  
\- created\_by 	     int not null —- USERS.id at FINA Database  
\- published\_at       timestamp null — must used server timezone  
\- published\_by 	     int null —- USERS.id at FINA Database

Aturan:

* unique (workflow\_key, version)  
* Definition\_json menyimpan compiled snapshot untuk kepentingan audit/debug.

#### SYS\$BPM\_STATE\_DEF {#sys$bpm_state_def}

bpm\_state\_def  
\- id                     PK  
\- SYS\$BPM\_WORKFLOW\_DEF\_ID	   FK  
\- state\_code             varchar(100)  
\- label                  varchar(200)  
\- task\_enabled           boolean  
\- task\_name              varchar(200) null  
\- assignment\_type        varchar(20) null \-- ROLE | USER | DYNAMIC  
\- assignment\_value       varchar(200) null  
\- sla\_duration\_minutes   int null  
\- timeout\_action\_type    varchar(30) null  
\- timeout\_event\_name     varchar(100) null  
\- sort\_no int

#### SYS\$BPM\_TRANS\_DEF {#sys$bpm_trans_def}

bpm\_transition\_def  
\- id                     PK  
\- SYS\$BPM\_WORKFLOW\_DEF\_ID       FK  
\- transition\_code        varchar(100)  
\- from\_state\_code        varchar(100)  
\- to\_state\_code          varchar(100)  
\- trigger\_type           varchar(30) \-- USER\_EVENT | SYSTEM\_EVENT |   
                                        TIMER\_EVENT | EXTERNAL\_EVENT  
\- label                  varchar(100)  
\- guard\_type             varchar(30) null \-- DOMAIN\_RULE  
\- guard\_rule\_key         varchar(100) null  
\- sort\_no int

#### SYS\$BPM\_TRANS\_ROLE {#sys$bpm_trans_role}

bpm\_transition\_role  
\- id                PK  
\- SYS\$BPM\_TRANS\_DEF\_ID FK  
\- role\_code         varchar(100)

#### SYS\$BPM\_TRANS\_EFFECT\_DEF {#sys$bpm_trans_effect_def}

bpm\_transition\_effect\_def  
\- id                       PK  
\- SYS\$BPM\_TRANS\_DEF\_ID     FK  
\- effect\_type              varchar(30) \-- EMIT\_EVENT  
\- event\_name               varchar(100)  
\- payload\_template         text null  
\- sort\_no int

### Tabel Database (Workflow Execution) {#tabel-database-(workflow-execution)}

#### SYS\$BPM\_WF\_INSTANCE {#sys$bpm_wf_instance}

bpm\_workflow\_instance  
\- id                     PK  
\- SYS\$BPM\_WORKFLOW\_DEF\_ID  FK  
\- entity\_type            varchar(100)  
\- entity\_id              varchar(100)  
\- current\_state\_code     varchar(100)  
\- status                 varchar(20) \-- ACTIVE | COMPLETED | TERMINATED  
\- started\_at             — must used server timezone  
\- ended\_at               null — must used server timezone  
\- created\_by             int not null —- USERS.id at FINA Database  
\- updated\_at             — must used server timezone  
\- version\_no             int

Constraints:

* unique(entity\_type, entity\_id, status=’ACTIVE’)  
* Satu instance aktif per entity

#### SYS\$BPM\_STATE\_HISTORY {#sys$bpm_state_history}

History yang hanya append  
bpm\_state\_history  
\- id                       PK  
\- SYS\$BPM\_WF\_INSTANCE\_ID   FK  
\- from\_state\_code          varchar(100) null  
\- to\_state\_code            varchar(100)  
\- SYS\$BPM\_TRANS\_DEF\_ID     FK null  
\- trigger\_type             varchar(30)  
\- actor\_type               varchar(20) \-- USER | SYSTEM | EXTERNAL   
                                          | TIMER  
\- actor\_id                 int null   
					—- USERS.id at FINA Database, if actor\_type=“USER”  
\- request\_id               varchar(100) null  
\- created\_at               — must used server timezone

Constraints:

* unique(workflow\_instance\_id, request\_id)

#### SYS\$BPM\_TASK {#sys$bpm_task}

bpm\_task  
\- id                   PK  
\- SYS\$BPM\_WF\_INSTANCE\_ID FK  
\- state\_code           varchar(100)  
\- name                 varchar(200)  
\- SLA\_MINUTES          int null  
\- status               varchar(20) \-- OPEN | DONE | CANCELLED | EXPIRED  
\- assignment\_type      varchar(20) \-- ROLE | USER  
\- assignment\_value     varchar(200)  
\- assigned\_user\_id     varchar(100) null  
\- created\_at           — must used server timezone   
\- due\_at               null – must used server timezone      
\- completed\_at         null — must used server timezone  
\- completed\_by         int null —- USERS.id at FINA Database  
\- closed\_reason        varchar(30) null \-- TRANSITIONED | CANCELLED   
                                          | EXPIRED

#### SYS\$BPM\_TIMER\_JOB {#sys$bpm_timer_job}

bpm\_timer\_job  
\- id                   PK  
\- SYS\$BPM\_WF\_INSTANCE\_ID FK  
\- SYS\$BPM\_TASK\_ID      FK null  
\- state\_code           varchar(100)  
\- timer\_type           varchar(30) \-- SLA\_TIMEOUT  
\- due\_at               — must used server timezone  
\- SLA\_MINUTES          int null  
\- status               varchar(20) \-- OPEN | FIRED | CANCELLED  
\- fired\_at             null – must used server timezone

Ketika state berubah:

* Timer job sebelumnya di-cancel  
* Yang baru dibuat bila ada SLA

#### SYS\$BPM\_EFFECT\_LOG {#sys$bpm_effect_log}

Untuk melacak effect yang di-emit.  
bpm\_effect\_log  
\- id                       PK  
\- SYS\$BPM\_WF\_INSTANCE\_ID    FK  
\- SYS\$BPM\_TRANS\_DEF\_ID       FK  
\- effect\_type              varchar(30)  
\- event\_name               varchar(100)  
\- status                   varchar(20) \-- SUCCESS | FAILED | PENDING   
                                          | RETRYING  
\- retry\_count              int  
\- error\_message            varchar(1000) null  
\- created\_at               — must used server timezone 

## Runtime {#runtime-1}

### Aturan State Lifecycle {#aturan-state-lifecycle}

1. Setiap entity instance:  
   1. hanya punya 1 state awal.  
   2. Hanya punya 1 active \\ current state  
   3. Bisa punya banyak target state atau tidak ada   
   4. Bila tidak ada target state berarti Terminal state.  
2. State berubah   
   1. Hanya melalui transition  
3. Transition sifatnya atomic (all or nothing)  
   1. Lolos dari rule  
   2. State berubah  
   3. History dicatat  
4. Terminal state:  
   1. Tidak mempunyai state target  
5. State history  
   1. Hanya boleh append  
   2. Tidak boleh berubah

### User & Role {#user-&-role}

1. Workflow definition hanya menetapkan roles internal.  
2. Mapping antara workflow role dengan user group di Biz-A dilakukan di application config.

### Timer {#timer}

1. Timer akan dieksekusi oleh Biz-A Watcher  
2. Watcher akan:  
   1. Scan BPM\_TIMER\_JOB where due\_at \<= now and status \= OPEN  
   2. Kalau ada → emit TIMER\_EVENT

## API {#api}

### Fungsi {#fungsi}

Biz-A BPM API menyediakan runtime service untuk:

* Membaca workflow state dari sebuah entity  
* Membaca transition yang tersedia bagi current user.  
* Mengeksekusi transition  
* Membaca list task seorang user  
* Membaca history workflow  
* Monitor dan mencoba ulang eksekusi effect yang gagal

API ini tidak mengurusi:

* Domain data  
* UI Layout  
* User master  
* Kalkulasi bisnis

### Aturan umum {#aturan-umum}

1. Identitas dari workflow yang dituju  
   1. Setiap runtime request untuk sebuah workflow instance tertentu harus mengidentifikasi domain object dengan cara:  
      1. entityType  
      2. entityId  
   2. Contoh:  
      1. entityType \= “PurchaseRequest”  
      2. entityId \= “PR-001”  
2. Actor context  
   1. Request yang bergantung pada otorisasi harus mencakup:  
      1. actorId  
      2. Roles  
   2. Roles yang dimaksud adalah workflow roles yang didapat secara runtime.  
3. Format response  
   1. Semua endpoints harus mengembalikan JSON  
   2. Kalau sukses  
      {  
        "success": true,  
        "data": {}  
      }

   3. Kalau gagal  
      {  
        "success": false,  
        "error": {  
          "code": "ERROR\_CODE",  
          "message": "Human readable message"  
        }  
      }

### Error Code {#error-code}

Berikut adalah kode-kode error yang digunakan oleh BPM API:

* `INSTANCE_NOT_FOUND`  
* `TRANSITION_NOT_FOUND`  
* `INVALID_CURRENT_STATE`  
* `ROLE_NOT_ALLOWED`  
* `GUARD_REJECTED`  
* `IDEMPOTENCY_CONFLICT`  
* `CONCURRENCY_CONFLICT`  
* `INTERNAL_ERROR`  
* `EFFECT_EXECUTION_NOT_FOUND`  
* `INVALID_REQUEST`

### Entry points {#entry-points}

#### Ambil Workflow State {#ambil-workflow-state}

##### Tujuan {#tujuan}

Mengembalikan state workflow saat ini untuk 1 entity tertentu.

##### Endpoint {#endpoint}

GET /bpm/instances/state

##### Query Parameters {#query-parameters}

* entityType: string, required  
* entityId: string, required

##### Response {#response}

{  
  "success": true,  
  "data": {  
    "entityType": "PurchaseRequest",  
    "entityId": "PR-001",  
    "workflowKey": "purchase-request",  
    "workflowVersion": "1.0.0",  
    "currentState": "SUBMITTED",  
    "instanceStatus": "ACTIVE"  
  }  
}

##### Kemungkinan error {#kemungkinan-error}

###### *Instance not found* {#instance-not-found}

{  
  "success": false,  
  "error": {  
    "code": "INSTANCE\_NOT\_FOUND",  
    "message": "Workflow instance not found"  
  }  
}

#### Ambil Transitions yang Tersedia {#ambil-transitions-yang-tersedia}

##### Tujuan {#tujuan-1}

Mengembalikan semua transition yang tersedia untuk actor saat ini untuk 1 entity.

##### Endpoint {#endpoint-1}

POST /bpm/instances/available-transitions

##### Request Body {#request-body}

{  
  "entityType": "PurchaseRequest",  
  "entityId": "PR-001",  
  "actorId": "USR-002",  
  "roles": \["APPROVER"\]  
}

##### Response {#response-1}

{  
  "success": true,  
  "data": {  
    "entityType": "PurchaseRequest",  
    "entityId": "PR-001",  
    "currentState": "SUBMITTED",  
    "transitions": \[  
      {  
        "id": "approve",  
        "label": "Approve"  
      },  
      {  
        "id": "reject",  
        "label": "Reject"  
      }  
    \]  
  }  
}

##### Catatan {#catatan}

* BPM harus validasi current state di internal  
* BPM harus evaluasi otorisasi role sebelum mengembalikan list transitions.  
* Hanya kembalikan transitions yang:  
  * Lolos validasi role  
  * Lolos validasi guard

#### Eksekusi Transition {#eksekusi-transition}

##### Tujuan {#tujuan-2}

Mengeksekusi 1 transisi dari sebuah workflow instance.

##### Endpoint {#endpoint-2}

POST /bpm/transitions/execute

##### Request body {#request-body-1}

{  
"instanceId": 123,   
"transition": {   
"transition\_code": "APPROVE\_DOC",   
"from\_state\_code": "REVIEW\_DOC",   
"to\_state\_code": "APPROVED"   
},   
"userRoles": \["MANAGER"\],   
"entityData": { "amount": 5000000 },   
"effectData": {   
"clientInstanceId": "CLIENT\_xyz123",   
"customVariable": "Data tambahan untuk CLI Script"   
}   
}

##### Success Response {#success-response}

{  
  "success": true,  
  "data": {  
    "status": "SUCCESS",  
    "entityType": "PurchaseRequest",  
    "entityId": "PR-001",  
    "fromState": "SUBMITTED",  
    "toState": "APPROVED",  
    "instanceStatus": "COMPLETED"  
  }  
}

##### Rejected Response {#rejected-response}

Digunakan saat request-nya secara teknis valid, namun transisi tidak diperbolehkan.  
Contoh:

* Role tidak diperbolehkan  
* Invalid state saat ini  
* Guard menolak  
* Request duplikat  
* Konflik concurrency

{  
  "success": false,  
  "error": {  
    "code": "GUARD\_REJECTED",  
    "message": "Purchase request is incomplete"  
  }  
}

##### Failed Response {#failed-response}

Digunakan saat gagal secara teknis atau error internal.  
{  
  "success": false,  
  "error": {  
    "code": "INTERNAL\_ERROR",  
    "message": "Unexpected error while executing transition"  
  }  
}

#### Ambil My Tasks {#ambil-my-tasks}

##### Tujuan {#tujuan-3}

Mengembalikan task yang masih terbuka yang ditugaskan ke actor tertentu.

##### Endpoint {#endpoint-3}

POST /bpm/tasks/my

##### Request Body {#request-body-2}

{  
  "actorId": "USR-002",  
  "roles": \["APPROVER"\]  
}

##### Response {#response-2}

{  
  "success": true,  
  "data": {  
    "tasks": \[  
      {  
        "taskId": "TASK-001",  
        "entityType": "PurchaseRequest",  
        "entityId": "PR-001",  
        "workflowKey": "purchase-request",  
        "workflowVersion": "1.0.0",  
        "stateCode": "SUBMITTED",  
        "taskName": "Approve Purchase Request",  
        "dueAt": "2026-03-25T10:00:00Z"  
      }  
    \]  
  }  
}

##### Catatan {#catatan-1}

* Endpoint ini hanya mengembalikan task yang aktif/masih terbuka.

#### Ambil workflow history {#ambil-workflow-history}

##### Tujuan {#tujuan-4}

Mengembalikan state history dari sebuah entity.

##### Endpoint {#endpoint-4}

GET /bpm/instances/history

##### Query Parameter {#query-parameter}

* entityType: string, required  
* entityId: string, required  
* page:number, required  
* pageSize:number, required

##### Response {#response-3}

{  
  "success": true,  
  "data": {  
    "entityType": "PurchaseRequest",  
    "entityId": "PR-001",  
    "history": \[  
      {  
        "fromState": null,  
        "toState": "DRAFT",  
        "transitionId": null,  
        "triggerType": "SYSTEM\_EVENT",  
        "actorId": "USR-001",  
        "createdAt": "2026-03-24T08:00:00Z"  
      },  
      {  
        "fromState": "DRAFT",  
        "toState": "SUBMITTED",  
        "transitionId": "submit",  
        "triggerType": "USER\_EVENT",  
        "actorId": "USR-001",  
        "createdAt": "2026-03-24T08:30:00Z"  
      },  
      {  
        "fromState": "SUBMITTED",  
        "toState": "APPROVED",  
        "transitionId": "approve",  
        "triggerType": "USER\_EVENT",  
        "actorId": "USR-002",  
        "createdAt": "2026-03-24T09:00:00Z"  
      }  
    \]  
  }  
}

#### Ambil Effect Executions {#ambil-effect-executions}

##### Tujuan {#tujuan-5}

Mengembalikan catatan eksekusi effect dari 1 entity atau 1 workflow instance

##### Endpoint {#endpoint-5}

GET /bpm/effects

##### Query Parameters {#query-parameters-1}

Paling tidak ada 1 filter yang harus ada:

* entityType: string, optional  
* entityId: string, optional  
* status: string, optional  
* workflowInstanceId: string, optional

##### Response {#response-4}

{  
  "success": true,  
  "data": {  
    "effects": \[  
      {  
        "effectExecutionId": "EFF-001",  
        "workflowInstanceId": "INS-001",  
        "transitionId": "approve",  
        "eventName": "PR\_APPROVED",  
        "status": "FAILED",  
        "retryCount": 3,  
        "errorMessage": "Message broker unavailable",  
        "createdAt": "2026-03-24T09:00:01Z",  
        "processedAt": "2026-03-24T09:03:01Z"  
      }  
    \]  
  }  
}

#### Retry Effect Executions {#retry-effect-executions}

##### Tujuan {#tujuan-6}

Mencoba ulang eksekusi sebuah effect yang sebelumnya gagal.

##### Endpoint {#endpoint-6}

POST /bpm/effects/retry

##### Request Body {#request-body-3}

{  
  "effectExecutionId": "EFF-001"  
}

##### Response {#response-5}

{  
  "success": true,  
  "data": {  
    "effectExecutionId": "EFF-001",  
    "status": "RETRYING"  
  }  
}

##### Failure Response {#failure-response}

{  
  "success": false,  
  "error": {  
    "code": "EFFECT\_EXECUTION\_NOT\_FOUND",  
    "message": "Effect execution not found"  
  }  
}

## Perilaku {#perilaku}

### Perilaku Eksekusi Transition {#perilaku-eksekusi-transition}

Ketika [Eksekusi Transition](#eksekusi-transition) dipanggil, BPM harus memproses request ini dengan urutan berikut:

1. Langkah 1: Validasi request  
   1. BPM harus validasi:  
      1. Ada Workflow instance  
      2. Workflow instance status \= ACTIVE  
      3. Transition ada di definisi yang di-published  
      4. Current state sama dengan transition from.  
      5. Actor ada di salah satu roles yang diperbolehkan.  
      6. requestId belum pernah digunakan di eksekusi yang berhasil.   
   2. Jika ada validasi yang gagal:  
      1. BPM harus kembalikan [rejected response](#rejected-response)  
      2. BPM tidak boleh mengubah state  
      3. BPM tidak boleh menulis history  
      4. BPM tidak boleh mengubah task  
2. Langkah 2: Evaluasi Guard  
   1. Jika transition ada guard:  
      1. BPM harus panggil guard validation melalui domain service.  
      2. Guard harus kembalikan Boolean  
   2. Jika guard mengembalikan false:  
      1. BPM harus kembalikan:  
         1. Success \= false  
         2. Error.code \= GUARD\_REJECTED  
      2. BPM tidak boleh ubah state  
      3. BPM tidak boleh tulis history  
      4. BPM idak boleh ubah task  
3. Langkah 3: Commit Transaction  
   1. Jika lolos validasi dan guard, BPM harus melakukan hal berikut dalam 1 **atomic database transaction**:  
      1. Update workflow instance current state  
      2. Insert state history  
      3. Tutup current task jika current state ada task  
      4. Create task baru jika target state task.enable \= true.  
      5. Update workflow instance status menjadi COMPLETED jika target state adalah terminal.  
      6. Buat record effect execution dengan status awal PENDING.  
   2. Jika transaksi gagal:  
      1. BPM harus rollback semua perubahan  
      2. BPM harus mengembalikan:  
         1. Success \= false  
         2. Error.code \= INTERNAL\_ERROR  
4. Langkah 4: Kembalikan response  
   1. Jika transaksi berhasil BPM harus segera kembalikan response sukses   
   2. BPM tidak boleh menunggu eksekusi effect secara async sebelum mengembalikan success.  
5. Langkah 5: Proses Effect secara asynchronous  
   1. Setelah berhasil commit:  
      1. Jalankan semua proses PENDING eksekusi effect di background.  
   2. Jika effect berhasil:  
      1. Set effect status \= SUCCESS  
   3. Jika effect gagal sementara:  
      1. Set effect status \= RETRYING  
      2. Naikan retry count  
   4. Jika effect gagal permanen  
      1. Set effect status \= FAILED  
      2. Simpan error message  
   5. Kegagalan effect tidak boleh roll back workflow state yang sudah di-commit.

### Perilaku Handling Task {#perilaku-handling-task}

Siklus kehidupan Task merupakan bagian dari BPM Orchestration  
Aturan:

1. Pembuatan task harus dilakukan di dalam transition commit transaction.  
2. Penutupan task harus dilakukan di dalam transition commit transaction.  
3. Pembuatan task tidak boleh tergantung pada asynchronous event/effect.  
4. Memasuki state actionable:  
   1. Jika target state task.enable \= true, BPM harus membuat 1 open task menggunakan konfigurasi task dari target state.  
5. Meninggalkan actionable state  
   1. Jika current state mempunyai open task: BPM harus tutup task itu di transaction yang sama saat mengubah state.  
6. Memasuki terminal state  
   1. Jika target state adalah terminal:  
      1. BPM tidak boleh membuat task baru.  
      2. BPM harus set workflow instance status \= COMPLETED

### Perilaku Handling Timer / SLA {#perilaku-handling-timer-/-sla}

Sistem BPM mengenal 2 jenis eksekusi timer berdasarkan konfigurasi state. Engine akan mengevaluasi ini secara otomatis saat berpindah state:

1. Standalone Timer (Wait State / System Delay)  
   

   \* Kondisi: task\_enabled \= 0 DAN sla\_duration\_minutes \> 0  
   \* Perilaku: BPM tidak membuat Task. BPM hanya membuat 1 record di SYS\$BPM\_TIMER\_JOB yang terikat langsung ke workflow instance (SYS\$BPM\_WF\_INSTANCE\_ID terisi, tetapi SYS\$BPM\_TASK\_ID bernilai NULL).  
   \* Contoh Kasus: State "WAITING\_VENDOR\_REPLY". Tidak ada aksi user di sistem kita, sistem murni menunggu 24 jam secara background. Jika waktu habis, sistem otomatis merubah state atau mengirim email peringatan.

2. Nested Timer (Task SLA / Human Deadline)  
   

   \* Kondisi: task\_enabled \= 1 DAN sla\_duration\_minutes \> 0  
   \* Perilaku: BPM membuat 1 Task untuk user, dan membuat 1 Timer yang berjalan berdampingan dengan Task tersebut. Timer ini akan memiliki nilai SYS\$BPM\_TASK\_ID yang merujuk ke task yang baru dibuat.  
   \* Contoh Kasus: State "PENDING\_APPROVAL". Manager mendapat tugas untuk klik Approve. Jika dalam 24 jam tidak ada tindakan, timer expired dan men-trigger event "ESCALATE\_TO\_DIRECTOR". Saat task di-close oleh Manager, timer ini juga akan otomatis dibatalkan (CANCELLED).

### Perilaku Idempotency {#perilaku-idempotency}

1. requestId wajib ada saat mengeksekusi transition  
2. Aturan  
   1. requestId yang sama tidak boleh mengeksekusi transisi yang sama 2 kali.  
   2. BPM harus mendeteksi duplikat requestId  
3. Respon  
   1. Success \= false  
   2. Error.code \= IDEMPOTENCY\_CONFLICT

### Perilaku Concurrency {#perilaku-concurrency}

1. BPM harus menggunakan optimistic concurrency control.   
2. Aturan:  
   1. Transition hanya boleh diproses jika:  
      1. State yang tersimpan saat ini sama dengan from state.  
   2. Jika transition yang lain sudah mengubah state  
      1. BPM harus menolak request dengan respon:  
         1. Success \= false  
         2. Error.code \= CONCURRENCY\_CONFLICT  
   3. Tidak boleh ada perubahan yang terjadi

### Perilaku Eksekusi Effect {#perilaku-eksekusi-effect}

Effect adalah efek samping dari pasca transition.  
Effect bukan bagian dari mutasi data domain.

Aturan:

* Record eksekusi effect harus dibuat saat berhasil commit transition  
* Eksekusi effect harus tersimpan permanen dan dapat di-query.  
* Pemrosesan effect dilakukan secara asynchronous  
* Kegagalan effect tidak boleh mengubah workflow state  
* Effect yang gagal harus dicoba lagi sesuai dengan [kebijakan retry](#kebijakan-retry).

### Kebijakan Retry {#kebijakan-retry}

Kebijakan Retry default yang disarankan:

* Retry maksimum: 3  
* Retry interval: 60 detik

Konfigurasi Setting ini boleh dibuat global

### Perilaku UI {#perilaku-ui}

UI berinteraksi dengan BPM sebagai berikut:

* Untuk form Entity (Domain)  
  * Panggil [Get Workflow state](#ambil-workflow-state)  
  * Panggil [Get Available Transitions](#ambil-transitions-yang-tersedia)  
  * Render action buttons berdasarkan transitions yang didapat.  
* Saat action button diklik  
  * Panggil [Execute Transition](#eksekusi-transition)  
* Saat di layar my task   
  * Panggil [Get My Tasks](#ambil-my-tasks).  
  * Bila drill down: Buka domain form menggunakan entityType \+ entityId  
* UI tidak boleh  
  * Menentukan sendiri workflow state  
  * Membuat task sendiri  
  * Mengubah workflow state langsung di luar BPM API

### HTTP Status {#http-status}

* Sukses  
  * 200 OK  
* Invalid request payload  
  * 400 Bad Request  
* Rejected Transition  
  * 409 Conflict  
* Not Found  
  * 404 Not Found  
* Internal Failure  
  * 500 Internal Server Error

## Apa yang Tidak Tercakup dalam BPM {#apa-yang-tidak-tercakup-dalam-bpm}

1. BPM tidak:  
   1. Mendefinisikan entity attributes  
   2. Mengeksekusi perhitungan bisnis  
   3. Menyimpan data domain  
   4. Melakukan penyimpanan synchronous ke domain.  
   5. Embed logic per domain  
2. Tester Note Only → Pelanggaran dari aturan ini akan dianggap sebagai bug

## History {#history}

| Tanggal | Keterangan | PIC |
| ----- | ----- | ----- |
| 2 Feb 2026 | Initial Draft | MAS |
| 17 Mar 2026 | Penyelarasan definisi kosa kata | AA |
| 24 Mar 2026 | Lengkapi Requirement | MAS |
| 31 Mar 2026 | foreign key format (nameTable\_ID) | AA |
| 7 Apr 2026 | SYS\$BPM\_TIMER\_JOB.SLA\_MINUTES SYS\$BPM\_TASK..SLA\_MINUTES Firebird server timezone for timestamp field SYS\$BPM\_STATE\_HISTORY.ACTOR\_ID shall used type INTEGER Perilaku Handling Timer / SLA | AA |
| 19 Jun 2026 | Mekanisme eksekusi Effect dan TimeoutAction | AA |
| 16 Jul 2026 | Perubahan requestBody untuk executeTransition | AA |

