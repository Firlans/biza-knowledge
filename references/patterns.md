# Biz-A Pattern Documentation (Knowledge Base)

> Didokumentasikan dari analisis folder **Proton** — sebagai referensi pattern yang bisa dipakai ulang di project lain.

---

## Table of Contents

1. [Module Export Pattern](#1-module-export-pattern)
2. [Library Pattern (useLibrary)](#2-library-pattern-uselibrary)
3. [Form Structure Pattern](#3-form-structure-pattern)
4. [List Structure Pattern](#4-list-structure-pattern)
5. [Query Data Pattern (lib_qry)](#5-query-data-pattern-lib_qry)
6. [Raw SQL / Execute Block Pattern (lib_queryRaw)](#6-raw-sql--execute-block-pattern-lib_queryraw)
7. [Utility Library Pattern (lib_utils)](#7-utility-library-pattern-lib_utils)
8. [Authorization & Privilege Pattern (lib_authorization)](#8-authorization--privilege-pattern-lib_authorization)
9. [HTML Template Pattern (lib_template)](#9-html-template-pattern-lib_template)
10. [Detail Grid Pattern](#10-detail-grid-pattern)
11. [Dialog Pattern](#11-dialog-pattern)
12. [Running Number Pattern](#12-running-number-pattern)
13. [Approval Workflow Pattern](#13-approval-workflow-pattern)
14. [Save / CRUD Pattern](#14-save--crud-pattern)
15. [Listener Pattern (valueChanges)](#15-listener-pattern-valuechanges)
16. [Print Pattern](#16-print-pattern)
17. [Delete Pattern (Master-Detail)](#17-delete-pattern-master-detail)
18. [Loading & Error Handling Pattern](#18-loading--error-handling-pattern)
19. [Test Pattern](#19-test-pattern)
20. [Menu Structure Pattern](#20-menu-structure-pattern)
21. [Control Data / Data Filtering by User Group Pattern](#21-control-data--data-filtering-by-user-group-pattern)

---

## 1. Module Export Pattern

Semua file menggunakan pola `get = function()` yang mengembalikan object konfigurasi. Ini adalah pattern dasar biz-a.

### Form Module

```js
get = function () {
    return {
        model: { /* default values */ },
        tableName: "",
        fields: [ /* formly field configs */ ],
        functions: { /* semua function handler */ }
    }
}
module.exports = get
```

### List Module

```js
get = function () {
    return {
        caption: 'Nama List',    // opsional
        buttons: [],              // tombol di atas list
        columns: [],              // kolom datatable
        filter: [],               // filter default
        distinct: true,           // opsional
        functions: { /* handler */ }
    }
}
module.exports = get
```

### Library Module

```js
get = function () {
    return {
        functions: { /* reusable functions */ }
    }
}
module.exports = get
```

---

## 2. Library Pattern (useLibrary)

Pattern untuk me-load dan me-reuse function dari file library di folder yang sama.

```js
functions: {
    useLibrary: function () {
        return ['lib_qry', 'lib_utils', 'lib_authorization']
    },
    // Setelah ini, semua function dari library bisa diakses via this.f().namaFunction()
}
```

### Konvensi Penamaan Library

| Prefix | Kegunaan | Contoh |
|--------|----------|--------|
| `lib_qry` | Query data dari database (biz-a & FINA) | `getShipto()`, `getSI()`, `getPermohonanSparepart()` |
| `lib_queryRaw` | Raw SQL via `executeBlock` | `getAgingByExchange()`, `setSql()` |
| `lib_utils` | Utility / helper umum | `openDialog()`, `toNumber()`, `findLuFina()` |
| `lib_authorization` | Otorisasi user group & privilege | `getGroupNames()`, `setAction()` |
| `lib_template` | HTML template untuk print/report | `getHTMLSalesInvoice()`, `getHTMLAgingReportByExchangeDate()` |

---

## 3. Form Structure Pattern

### Struktur Dasar

```js
get = function () {
    return {
        model: {
            mode: null,       // 'new' | 'edit' | 'view' | 'approve' | custom modes
            loaded: null,     // flag apakah data sudah loaded
        },
        tableName: "",
        fields: [
            { key: 'id' },                                  // hidden id
            { template: '<h2>Form Title</h2>' },            // judul form
            { /* field definitions menggunakan formly */ },
            { /* detail-grid untuk one-to-many */ },
            { /* action buttons: Simpan, Print, Kembali */ }
        ],
        functions: {
            useLibrary: function () { return ['lib_qry', 'lib_utils'] },
            beforeLoadData: function () { /* setup awal */ },
            onInit: function (id) { /* load data berdasarkan id */ },
            listener: function () { /* valueChanges reactive */ },
            // ... function lainnya
        }
    }
}
```

### Field Types yang Umum Dipakai

| Type | Kegunaan | Contoh Key |
|------|----------|------------|
| `input` | Text input standar | `no_permohonan`, `nama_pemohon` |
| `textarea` | Multi-line text | `description`, `shipto` |
| `date` | Date picker | `invoicedate`, `tanggal_permohonan` |
| `lookup` | Lookup ke tabel lain | `customerid`, `salesmanid` |
| `select` | Dropdown statis | `fob` |
| `money` | Format currency | `subtotal`, `totalorder` |
| `boolean` | Checkbox / toggle | `accepted`, `select_all_aging` |
| `label` | Read-only label | `positionText`, `emailText` |
| `button` | Tombol aksi | Simpan, Print, ACC |
| `selection-list` | Multi-select list | `aging` |
| `detail-grid` | Master-detail grid | Detail barang |
| `input-file` | Upload file | `attachment` |
| `repeat` | Repeating section | `attachments` |

### Lookup Field dengan FINA Database

Lookup ke database FINA ditandai dengan className `lu-fina`. DbIndex di-set secara dinamis:

```js
{
    className: 'col-6 lu-fina',
    key: "customerid",
    type: "lookup",
    props: {
        label: "Customer",
        lookupOptions: {
            table: 'persondata',
            key: 'id',
            display: 'name',
            dbIndex: "",              // di-set di beforeLoadData via findLuFina
            searchKey: ['name']
        }
    }
}
```

### Dynamic DbIndex Setting

```js
beforeLoadData: function () {
    // Set dbIndex untuk semua lookup lu-fina di fields
    this.f().findLuFina(this.fields, (el, dbIndex) => el.props.lookupOptions.dbIndex = dbIndex)
    
    // Set dbIndex untuk lookup lu-fina di detail-grid columns
    const grid = this.fields.find(el => el.type === 'detail-grid')
    this.f().findLuFina(grid?.props.columns, (el, dbIndex) => el.lookup.dbIndex = dbIndex)
    
    // Simpan referensi ke grid instance
    this.grid = grid._componentRefs[0].instance.grid
}
```

### Mode Handling Pattern

Form biasanya mendukung beberapa mode yang dikontrol via model dan queryParams:

```js
onInit: function (id) {
    const mode = this.route.snapshot.queryParams["mode"];
    
    if (!isNaN(id)) {
        // Edit mode: load data
        this.model.mode = mode || 'edit';
    } else {
        // New mode
        this.model.mode = mode || 'new';
    }
}
```

### Expressions untuk Readonly/Disabled berdasarkan Mode

```js
{
    key: "fieldname",
    type: "input",
    expressions: {
        "props.readonly": 'model.mode === "view"',
        // atau untuk banyak mode:
        "props.readonly": 'model.mode !== "new" && model.mode !== "edit"',
    }
}
```

---

## 4. List Structure Pattern

### Struktur Dasar

```js
get = function () {
    return {
        buttons: [],              // tombol di atas (biasanya "New")
        columns: [
            { title: "Column Name", data: "table.column" },
            {
                title: "Action",
                data: "table.id",
                button: [
                    { caption: "Edit", icon: "edit", onClick: "editClicked" },
                    { caption: "Delete", icon: "delete", onClick: "deleteClicked" },
                    { caption: "Print", icon: "print", onClick: "printClicked" },
                ]
            }
        ],
        filter: [],               // default filter
        functions: {
            useLibrary: function () { return ['lib_qry', 'lib_authorization'] },
            beforeLoadData: function () {
                this.dbIndex = this.config.api.finaDbIndex  // atau this.config.api.dbIndex
            },
            onPipe: function (...data) { /* authorization & setup */ },
            editClicked: function (id) { 
                this.router.navigate(['../../form', 'FormName', id]) 
            },
            // ...
        }
    }
}
```

### Column Types

```js
// Text biasa
{ title: "Name", data: "table.column" }

// Boolean display
{ title: "Status", data: "table.flag", type: "boolean", arg1: "✅", arg2: " " }

// Money format
{ title: "Amount", data: "table.amount", type: "money" }

// Subquery / computed column
{
    title: "Status",
    data: `(select CASE WHEN ... END from ...)`.replace(/\s+/g, " ").trim(),
    alias: "status"
}

// Action buttons
{
    title: "Action",
    data: "table.id",
    button: [
        { caption: "Edit", icon: "edit", color: "primary", onClick: "editClicked" },
        { caption: "Delete", icon: "delete", color: "warn", onClick: "deleteClicked" },
    ]
}
```

### Navigasi dari List

```js
// Ke form untuk edit
this.router.navigate(['../../form', 'FormName', id])

// Ke form untuk view/print
this.router.navigate(['../../form', 'FormName', id], { queryParams: { mode: 'view' } })

// Ke form untuk approve
this.router.navigate(['../../form', 'FormName', id], { queryParams: { mode: 'approve' } })
```

---

## 5. Query Data Pattern (lib_qry)

Pattern standar untuk query data menggunakan `dataService.queryData`.

### Basic Query

```js
getEntityById: function (id) {
    const param = {
        columns: [
            { data: 'table_name.column1', key: 'alias1' },
            { data: 'table_name.column2', key: 'alias2' },
        ],
        filter: [
            { junction: '', column: 'table_name.id', operator: '=', value1: id }
        ],
    };
    return this.dataService.queryData(param, this.config.api, true, true)
}
```

### Query ke FINA Database

Untuk query ke database FINA, tambahkan `dbIndex`:

```js
getFinaData: function (id) {
    const param = {
        columns: [ /* ... */ ],
        filter: [ /* ... */ ],
        dbIndex: this.config.api.finaDbIndex   // <-- menandakan query ke FINA DB
    };
    return this.dataService.queryData(param, this.config.api, true, true)
}
```

### Query dengan Sorting & Pagination

```js
getLastRecord: function () {
    const param = {
        columns: [ /* ... */ ],
        filter: [ /* ... */ ],
        order: [{ column: 1, dir: 'desc' }],
        length: 1                              // limit 1 record
    };
    return this.dataService.queryData(param, this.config.api, true, true)
}
```

### Query One-to-Many (Master-Detail)

Pattern untuk query master beserta detail-nya dalam satu call:

```js
getMasterWithDetail: function (id) {
    const param = {
        columns: [
            // Header columns
            { data: "master_table.id", key: "id" },
            { data: "master_table.name", key: "name" },
            
            // Detail columns (menggunakan relasi via foreign key)
            { data: "master_table.id.fk_column.detail_table.id", key: "detail_id" },
            { data: "master_table.id.fk_column.detail_table.column1", key: "detail_col1" },
        ],
        filter: [
            { junction: '', column: 'master_table.id', operator: '=', value1: id }
        ]
    };
    return this.dataService.queryData(param, this.config.api, true, true)
}
```

### Filter Operators yang Umum

| Operator | Kegunaan | Contoh |
|----------|----------|--------|
| `=` | Exact match | `value1: id` |
| `like` | Pattern match | `value1: "'prefix%'"` |
| `in` | Multiple values | `value1: "(1,2,3)"` |
| `is` / `is not` | NULL check | `value1: "null"` |
| `>=`, `<=`, `>`, `<` | Comparison | `value1: "'2024-01-01'"` |

### Multi-Junction Filter

```js
filter: [
    { junction: '', column: 'table.col1', operator: '=', value1: 'val1' },
    { junction: 'and', column: 'table.col2', operator: '=', value1: 'val2' },
    { junction: 'and', filter: [   // nested filter group (OR condition)
        { junction: '', column: 'table.col3', operator: 'is', value1: 'null' },
        { junction: 'or', column: 'table.col3', operator: '=', value1: '0' },
    ]}
]
```

---

## 6. Raw SQL / Execute Block Pattern (lib_queryRaw)

Untuk query kompleks yang tidak bisa dilakukan via `queryData`, gunakan `executeBlock`:

### setSql Helper

```js
setSql: function (dataReturns, mainQuery) {
    // dataReturns = [{ column: 'COL_NAME', type: 'VARCHAR(50)' }, ...]
    // Menghasilkan EXECUTE BLOCK statement Firebird
    // Return: formatted SQL string
}
```

### Penggunaan

```js
getComplexData: function (param1) {
    const returnData = [
        { column: 'COLUMN1', type: 'VARCHAR(50)' },
        { column: 'COLUMN2', type: 'DECIMAL(18,2)' },
        { column: 'COLUMN3', type: 'DATE' },
    ];
    
    const blocksql = this.f().setSql(returnData, `
        SELECT col1, col2, col3
        FROM table1
        WHERE condition = '${param1}'
    `);
    
    return this.dataService.executeBlock(blocksql, {
        ...this.config.api,
        dbIndex: this.config.api.finaDbIndex
    });
}
```

---

## 7. Utility Library Pattern (lib_utils)

### openDialog

Membuka dialog modal dengan formly fields:

```js
openDialog: function (title, model, fields, ...afterOpened) {
    // Membuka MatDialog dengan FormlyDialogComponent
    // Return: Observable yang emit result saat dialog ditutup
}

// Penggunaan:
this.f().openDialog('Dialog Title', { field1: null }, [
    { key: 'field1', type: 'input', props: { label: 'Field 1' } }
]).subscribe(result => {
    if (!result) return;  // dialog dibatalkan
    // process result
})
```

### findLuFina

Mencari dan mengatur dbIndex untuk semua field dengan className `lu-fina`:

```js
findLuFina: function (fields, setField) {
    // Rekursif menelusuri fields termasuk fieldGroup
    // Memanggil setField(el, finaDbIndex) untuk setiap field lu-fina
}
```

### findField

Mencari field secara rekursif berdasarkan properti:

```js
findField: function (fields, key, value, setField) {
    // Cari field di mana field[key] mengandung value
    // Mendukung nested fieldGroup
}
```

### toNumber

Konversi aman ke number:

```js
toNumber: function (v) {
    if (isNaN(v)) return 0;
    if (typeof v === "number") return v;
    return Number(String(v).replaceAll(",", "."));
}
```

### numberToRomawi

Konversi angka ke angka Romawi:

```js
numberToRomawi: function (num) {
    // 1 -> 'I', 4 -> 'IV', 9 -> 'IX', dll
}
```

### blobToBase64

Konversi blob ke base64:

```js
blobToBase64: function (blob) {
    return new Promise((resolve, _) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.readAsDataURL(blob);
    });
}
```

### convertToWord (Terbilang)

Konversi nominal ke kata-kata (Bahasa Indonesia):

```js
convertToWord: function (nominal) {
    // 1500000 -> "satu juta lima ratus ribu"
}
```

---

## 8. Authorization & Privilege Pattern (lib_authorization)

### getGroupNames

Ambil daftar user group dari user yang sedang login:

```js
getGroupNames: function (userid) {
    // Query SYS$UGMEMBER untuk mendapatkan group user
    // Return: Observable<[{ usergroup: 'group_name' }]>
}
```

### setAction

Mengatur tombol Action di list berdasarkan group privilege:

```js
onPipe: function (...data) {
    return this.f().setAction(
        { name: 'editor', privileges: ['Edit'] },           // group 'editor' bisa Edit
        { name: 'admin', privileges: ['Edit', 'Delete'] },  // group 'admin' bisa Edit & Delete
        { name: 'all', privileges: ['Print'] },              // semua bisa Print
    ).pipe(
        this.map(res => {
            // Cek apakah user bisa membuat data baru
            if (res.some(el => el.usergroup?.toLowerCase() === 'creator')) {
                this.buttons = [{ caption: 'New', onClick: 'newClicked' }]
            }
            return data
        })
    )
}
```

### setActionUsingKey

Sama seperti `setAction` tetapi menggunakan field `id` sebagai key matching (bukan `caption`):

```js
this.f().setActionUsingKey(
    'id',
    { name: 'supir', privileges: ['edit', 'delete'] },
    { name: 'mekanik', privileges: ['approve-mekanik'] },
    // ...
)
```

### setControlDataList

Filter data list berdasarkan konfigurasi per user group:

```js
return this.f().setControlDataList(
    this.storageService.getCurrentUser(), 
    'permohonanSparepartList'       // nama halaman
).pipe(
    this.switchMap(() => this.loadData())
)
```

---

## 9. HTML Template Pattern (lib_template)

Pattern untuk membuat template HTML untuk keperluan print/export.

### Struktur Umum

```js
getHTMLReport: function (model) {
    const moneyFormat = new this.NumberParser('id', "IDR", false)
    
    // 1. Process data (grouping, calculation, dll)
    // 2. Build HTML rows
    // 3. Return HTML string lengkap dengan <style> dan <body>
    
    return `
        <style>/* CSS styles */</style>
        <body id="output">
            <div class="header">...</div>
            <table>...</table>
            <div class="footer">...</div>
        </body>
    `.replace(/\s+/g, " ").trim();
}
```

### Money Formatting

```js
const moneyFormat = new this.NumberParser('id', "IDR", false)
moneyFormat.format(1500000)  // "1.500.000"

// Atau menggunakan Intl.NumberFormat
const formatCurrency = (value) => {
    return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
    }).format(Number(value || 0));
}
```

---

## 10. Detail Grid Pattern

Pattern untuk master-detail relationship menggunakan `detail-grid` formly type.

### Konfigurasi

```js
{
    type: "detail-grid",
    props: {
        detailKey: "details",           // key di model untuk array detail
        editOnEnter: true,
        deleteBtn: { show: true, icon: 'delete', label: 'Hapus' },
        addBtn: { show: true, icon: 'add' },
        columns: [
            { key: 'detail_id' },                                         // hidden
            { key: "nama_item", label: "Nama Item", required: true },
            { key: "qty", label: "Qty", type: "number", required: true },
            { key: "harga", label: "Harga", type: "money" },
            { key: "amount", label: "Amount", type: "money", readonly: true },
            {
                key: "taxcodes",
                label: "Pajak",
                className: "lu-fina",
                type: 'lookup_combo',
                lookup: { table: 'TAX', key: 'TAXCODE', display: "TAXCODE" }
            },
        ],
        onCalc: [{
            watchKey: ["qty", "harga"],
            function: function (rowCtls, value, key) {
                // Kalkulasi otomatis saat value berubah
                const qty = Number(rowCtls.get('qty').value || 0);
                const harga = Number(rowCtls.get('harga').value || 0);
                rowCtls.get('amount').setValue(qty * harga);
            }
        }]
    }
}
```

### Mengakses Grid Instance

```js
beforeLoadData: function () {
    this.grid = this.fields.find(el => el.type === 'detail-grid')._componentRefs[0].instance.grid
}

// Untuk multiple grid (gunakan id)
beforeLoadData: function () {
    this.detailGrid = this.fields.find(el => el.id === 'po-detail-grid')._componentRefs[0].instance.grid
    this.termGrid = this.fields.find(el => el.id === 'ketentuan-grid')._componentRefs[0].instance.grid
}
```

### Assign Data ke Grid

```js
this.grid.assignData({ data: arrayOfDetails })
```

### Conditional Readonly pada Grid Columns

```js
{
    type: "detail-grid",
    expressions: {
        "props.columns[1].readonly": 'model.mode === "view"',
        "props.columns[2].readonly": 'model.mode === "view"',
    }
}
```

### Conditional Visibility pada Grid Columns

Gunakan className pattern `hide-{mode}`:

```js
{
    className: 'hide-new hide-edit hide-mekanik',
    key: "harga_terakhir",
    label: "Harga Terakhir",
    type: "money",
}
```

---

## 11. Dialog Pattern

### Dialog sebagai Modal Form

```js
someAction: function (id) {
    const model = { field1: null, field2: null };
    const fields = [
        { key: 'field1', type: 'input', props: { label: 'Field 1' } },
        { key: 'field2', type: 'date', props: { label: 'Field 2' } },
    ];
    
    return this.f().openDialog('Dialog Title', model, fields)
}
```

### Dialog dengan Data Pre-fill

```js
this.f().getSomeData(id).pipe(
    this.mergeMap(res => {
        model.field1 = res[0].value1;
        return this.f().openDialog('Edit', model, fields);
    }),
    this.mergeMap(result => {
        if (!result) return this.rx.get.empty();   // dialog dibatalkan
        // process result
        return this.dataService.sendModel(/* ... */);
    })
).subscribe(/* ... */)
```

### Dialog untuk Menampilkan Detail Grid (Read-only)

```js
showLog: function (id) {
    const fields = [{
        type: 'detail-grid',
        props: {
            detailKey: 'logs',
            columns: [
                { key: 'statusname', type: 'input', label: 'Status', readonly: true },
                { key: 'created_at', type: 'datetime', label: 'Updated', readonly: true },
            ]
        }
    }];
    
    this.f().getLogs('module', id).pipe(
        this.mergeMap(logs => this.f().openDialog('History', { logs }, fields))
    ).subscribe(/* ... */)
}
```

---

## 12. Running Number Pattern

Pattern otomatis generate nomor urut dokumen.

### Format: `PREFIX/ROMAWI_BULAN-TAHUN/KODE/NOMOR`

Contoh: `FPS/I-2024/JKT/001`, `PO/II/PLP/2024/0001`

### Implementasi

```js
setRunningNumber: function () {
    const date = this.dayjs(this.form.get('tanggal').value)
    const year = date.format('YYYY')
    const month = this.f().numberToRomawi(Number(date.format('MM')))
    const brc = this.form.get('branch_code').value
    const prefix = `FPS/${month}-${year}/${brc}/`
    const filter = `FPS/%%-${year}/${brc}/`    // %% for LIKE query
    
    return this.f().getLastNumber(filter).pipe(
        this.map(res => {
            const lastNumber = res[0]?.no || `${prefix}000`;
            const match = lastNumber.match(/(\d+)([^\d]*)$/);
            const numStr = match[1];
            const suffix = match[2];
            const next = String(Number(numStr) + 1).padStart(numStr.length, "0");
            return lastNumber.replace(/(\d+)([^\d]*)$/, next + suffix);
        })
    )
}
```

### Auto-update saat Tanggal Berubah

```js
this.form.get('tanggal')?.valueChanges.pipe(
    this.mergeMap(date => {
        const dayjs = this.dayjs(date)
        const currentYear = this.form.get("current_year").value
        if (!currentYear || dayjs.format('YYYY') !== currentYear) {
            this.form.get("current_year").setValue(dayjs.format('YYYY'))
            return this.f().setRunningNumber()
        }
        // Hanya update bulan di nomor yang sudah ada
        const number = this.form.get("no").value.split('/')
        number[1] = `${this.f().numberToRomawi(Number(dayjs.format('MM')))}-${dayjs.format('YYYY')}`
        return this.of(number.join('/'))
    })
).subscribe(number => this.form.get("no").setValue(number))
```

---

## 13. Approval Workflow Pattern

Pattern untuk multi-step approval process.

### Status Map

```js
beforeLoadData: function () {
    this.STATUS_MAP = {
        new: 'dibuat supir',
        edit: 'dibuat supir',
        mekanik: 'mengetahui mekanik',
        general_manager: 'acc general manager',
        admin_purchasing: 'dicek admin purchasing',
        manager_purchasing: 'disetujui manager purchasing',
        director: 'disetujui direktur',
    }
    
    this.approvalStatusMap = {
        'edit': ['dibuat supir'],
        'mekanik': ['dibuat supir'],
        'general_manager': ['disetujui mekanik'],
        'admin_purchasing': ['acc general manager'],
        'manager_purchasing': ['dicek admin purchasing'],
        'director': ['disetujui direktur'],
    }
}
```

### Validation sebelum Approve

```js
validateApprovalStatus: function (id, mode) {
    const allowedStatuses = this.approvalStatusMap[mode] || [];
    const currentStatus = /* get from data source */;
    
    if (!allowedStatuses.includes(currentStatus)) {
        throw new Error(`Akses ditolak, status saat ini: ${currentStatus}`);
    }
    return true;
}
```

### Shortcut Functions untuk Setiap Role

```js
accMekanik: (id) => this.f().accClicked(id, 'mekanik'),
accGeneralManager: (id) => this.f().accClicked(id, 'general_manager'),
accDirector: (id) => this.f().accClicked(id, 'director'),

accClicked: function (id, mode) {
    try {
        this.f().validateApprovalStatus(id, mode);
        this.router.navigate(['../../form', 'FormName', id], { queryParams: { mode } })
    } catch (err) {
        alert(err.message)
    }
}
```

### Conditional Buttons berdasarkan Mode

```js
{
    type: 'button',
    props: { text: 'ACC', icon: 'check', onClick: function() { this.f().clickAcc() } },
    expressions: {
        hide: 'model.mode !== "mekanik" && model.mode !== "general_manager"'
    }
},
{
    type: 'button',
    props: { text: 'Ditolak', color: "warn", onClick: function() { this.f().clickAcc('ditolak') } },
    expressions: {
        hide: 'model.mode !== "manager_purchasing"'
    }
}
```

### Logging Approval

```js
saveLog: function (model) {
    const param = {
        id: null,
        module: 'nama_module',
        status_id: this.STATUS.find(el => el.statusname.toLowerCase() === this.STATUS_MAP[model.mode]).statusid,
        request_id: model.id,
        user_id: this.storageService.getCurrentUser()
    }
    return this.dataService.sendModel(param, this.config.api, 'LOG_REQUEST')
}
```

---

## 14. Save / CRUD Pattern

### Save ke Biz-A Database (sendModel)

```js
saveData: function (model) {
    const param = {
        id: model.id,
        field1: model.field1,
        field2: model.field2,
    };
    return this.dataService.sendModel(param, this.config.api, "TABLE_NAME").pipe(
        this.map(res => {
            if (res.error) throw new Error(res.error);    // WAJIB: validasi error
            return res;
        })
    )
}
```

### Save ke FINA Database (json2fina)

```js
saveFina: function (model) {
    const param = {
        id: model.id || -1,
        dataModule: "TdmARInvoice",        // module FINA
        transType: "ARINV",                 // tipe transaksi
        userId: this.storageService.getCurrentUser(),
        dbIndex: this.config.api.finaDbIndex,
        data: {
            master: {
                id: model.id || -1,
                field1: model.field1,
                detail: model.items.map((dt, index) => ({
                    seq: index + 1,
                    itemno: dt.itemno,
                    quantity: dt.qty,
                }))
            }
        }
    };
    return this.dataService.json2fina(param, {
        ...this.config.api,
        dbIndex: this.config.api.finaDbIndex
    }).pipe(
        this.map(res => {
            if (res.result[0]?.error) throw new Error(res.result[0].error);  // WAJIB: validasi error
            return res.result[0].id;
        })
    )
}
```

### Save Master + Detail secara Sequential

```js
clickSave: function (model) {
    this.of(model.id).pipe(
        // Step 1: Generate ID jika baru
        this.mergeMap(id => {
            if (!id) return this.dataService.genId('GENERATOR_NAME', this.config.api)
            return this.of(id)
        }),
        // Step 2: Save master
        this.mergeMap(id => {
            model.id = id;
            return this.f().saveMaster(model)
        }),
        // Step 3: Save details (sequential per item)
        this.mergeMap(() => {
            return this.from(model.details).pipe(
                this.concatMap(detail => this.f().saveDetail(detail)),
                this.toArray()
            )
        }),
        // Step 4: Save log
        this.mergeMap(() => this.f().saveLog(model))
    ).subscribe({
        next: () => this.notificationService.showSuccess('Berhasil menyimpan'),
        error: (err) => this.notificationService.showError('Gagal: ' + err.message)
    })
}
```

### Update Master Only (json2fina)

```js
masterDataUpdate: function (model) {
    return {
        id: model.id,
        dataModule: "TdmARInvoice",
        transType: "ARINV",
        userId: this.storageService.getCurrentUser(),
        dbIndex: this.config.api.finaDbIndex,
        data: {
            id: model.id,
            master: { ...model }
        }
    }
}
```

### Delete Pattern (json2fina)

```js
deleteClicked: function (id) {
    const param = {
        id,
        dataModule: "TdmPurchaseOrder",
        transType: "APPO",
        userId: this.storageService.getCurrentUser(),
        dbIndex: this.config.api.finaDbIndex,
        delete: 1,                            // flag delete
    };
    this.dataService.json2fina(param, { ...this.config.api, dbIndex: this.config.api.finaDbIndex })
        .pipe(/* ... */)
        .subscribe(/* ... */)
}
```

---

## 15. Listener Pattern (valueChanges)

Pattern untuk menangani perubahan field secara reaktif.

### Setup di onInit atau Setelah Data Loaded

```js
onInit: function (id) {
    // ... load data ...
    this.f().listener()
}

// ATAU tunggu sampai data loaded
beforeLoadData: function () {
    this.intervalId = setInterval(() => {
        if (this.model.loaded) {
            this.f().listener();
            clearInterval(this.intervalId);
        }
    }, 100);
}
```

### Lookup dengan Auto-fill

```js
listener: function () {
    // Saat customer berubah, auto-fill alamat
    this.form.get('customerid').valueChanges.pipe(
        this.mergeMap(val => val ? this.f().getShipto(val) : this.rx.get.empty())
    ).subscribe(res => {
        const data = res[0] || {};
        const shipto = [data.name, data.addressline1, data.addressline2]
            .filter(Boolean).join('\n');
        this.form.get('shipto').setValue(shipto);
    });
}
```

### Auto-calculation pada Detail Changes

```js
// Total otomatis saat detail berubah
this.form.get('details').valueChanges.subscribe(res => {
    const total = res.reduce((acc, el) => acc + el.amount, 0);
    this.form.get('subtotal').setValue(total);
})

// PPN otomatis saat subtotal berubah
this.form.get('subtotal').valueChanges.subscribe(res => {
    this.f().recalculate(res);
})
```

### Cascading Value Changes

```js
// Saat discount % berubah, hitung cash discount
this.form.get('discount').valueChanges.subscribe(percentage => {
    this.fromPercentage = true;
    const discount = this.form.get('subtotal').value * (percentage / 100);
    this.form.get('cashdiscount').setValue(discount || 0);
    this.f().recalculate(this.form.get('subtotal').value);
})

// Saat cash discount berubah manual, reset percentage
this.form.get('cashdiscount').valueChanges.subscribe(val => {
    if (!this.fromPercentage) {
        this.form.get('discount').setValue(null);
    }
    this.fromPercentage = false;
    this.f().recalculate(this.form.get('subtotal').value);
})
```

---

## 16. Print Pattern

### Basic Print

```js
printClicked: function () {
    const model = { ...this.model, ...this.form.value };   // WAJIB: merge model & form
    const progressRef = this.loadingService.start('Menyusun data...', 'indeterminate');
    
    this.f().getCompanyInfo().pipe(
        this.mergeMap(companies => {
            return this.f().getCustomerData(model.customerid).pipe(
                this.map(customers => ({
                    ...model,
                    companyData: companies[0],
                    customerData: customers[0]
                }))
            )
        })
    ).subscribe({
        error: err => this.notificationService.showError(err.message),
        next: res => {
            const html = this.f().getHTMLTemplate(res);
            this.printService.print(html);
            this.loadingService.stop(progressRef);
        }
    })
}
```

### Export to Excel

```js
exportToExcel: function () {
    this.f().getTemplate(this.dayjs(), model).subscribe({
        next: html => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, "text/html");
            let table = doc.getElementById("output");
            const name = `report ${this.dayjs().format('DD MMM YYYY')}`;
            let wb = this.XLSX.utils.book_new();
            let ws = this.XLSX.utils.table_to_sheet(table);
            this.XLSX.utils.book_append_sheet(wb, ws, name);
            this.XLSX.writeFile(wb, `${name}.xlsx`);
        }
    })
}
```

---

## 17. Delete Pattern (Master-Detail)

### Delete Biz-A Data (Detail dulu, baru Master)

```js
deleteClicked: function (id) {
    const progressRef = this.loadingService.start('Menghapus...', 'indeterminate');
    return this.of(id).pipe(
        // Step 1: Delete detail
        this.mergeMap(() => this.dataService.deleteModelNonId(
            "DETAIL_TABLE", "MASTER_FK_COLUMN", id, this.config.api
        )),
        // Step 2: Validasi
        this.mergeMap(res => {
            if (res.error) throw new Error(res.error);
            // Step 3: Delete master
            return this.dataService.deleteModel(id, this.config.api, "MASTER_TABLE");
        }),
        this.map(res => {
            if (res.error) throw new Error(res.error);
            return 'success';
        }),
        // Step 4: Reload list
        this.switchMap(() => this.loadData()),
        this.catchError(err => {
            this.loadingService.stop(progressRef);
            throw err;
        }),
        this.finalize(() => this.loadingService.stop(progressRef))
    ).subscribe({
        next: () => alert("Berhasil menghapus"),
        error: (err) => alert("Gagal menghapus: " + err.message)
    });
}
```

### Delete FINA Data

```js
deleteClicked: function (id) {
    if (!confirm("Yakin mau hapus?")) return;
    const param = {
        id,
        dataModule: "TdmPurchaseOrder",
        transType: "APPO",
        userId: this.storageService.getCurrentUser(),
        dbIndex: this.config.api.finaDbIndex,
        delete: 1,
    };
    this.dataService.json2fina(param, { ...this.config.api, dbIndex: this.config.api.finaDbIndex })
        .pipe(
            this.map(res => {
                if (res.result[0].error) throw new Error(res.result[0].error);
                return 'success';
            }),
            this.switchMap(() => this.loadData()),
            this.catchError(err => { /* handle */ throw err }),
            this.finalize(() => this.loadingService.stop(progressRef))
        )
        .subscribe({ error: err => alert(err.message) });
}
```

---

## 18. Loading & Error Handling Pattern

### Loading Indicator

```js
const progressRef = this.loadingService.start('Memuat data...', 'indeterminate');

someObservable$.pipe(
    this.catchError(err => {
        this.loadingService.stop(progressRef);
        throw err;
    }),
    this.finalize(() => this.loadingService.stop(progressRef))
).subscribe({
    error: err => this.notificationService.showError(err.message),
    next: res => { /* success */ }
})
```

### Error Notification

```js
// Toast notification
this.notificationService.showError('Pesan error')
this.notificationService.showSuccess('Pesan sukses')

// Alert sederhana
alert("Pesan error: " + err.message)
```

### Validation sebelum Save

```js
validation: function (model) {
    if (!model.field1) throw new Error("Field 1 harus diisi");
    if (!model.details || model.details.length === 0) throw new Error("Detail belum diisi");
    model.details.forEach((dt, idx) => {
        if (!dt.name) throw new Error(`Nama baris ${idx + 1} kosong`);
    });
    return model;  // atau return true
}
```

### Pola try-catch di onClick

```js
onClick: function () {
    try {
        const model = { ...this.model, ...this.form.value };
        this.f().validation(model);
        this.doFunction('save', structuredClone(model));
    } catch (err) {
        this.notificationService.showError('Gagal: ' + err.message);
    }
}
```

---

## 19. Test Pattern

### File Structure

```
Proton/
├── someForm.js
├── someList.js
├── lib_utils.js
└── tests/
    ├── testUtils.js              # Shared test utilities
    ├── someForm.test.js
    ├── someList.test.js
    └── lib_utils.test.js
```

### testUtils.js

```js
function bindFunctionInObj(o, that) {
    for (let prop in o) {
        if (Object.prototype.hasOwnProperty.call(o, prop)) {
            if (typeof o[prop] === 'object' && o[prop] !== null) {
                bindFunctionInObj(o[prop], that);
            }
            if (typeof o[prop] === 'function') {
                o[prop] = o[prop].bind(that);
            }
        }
    }
}

function loadModuleFactory(relPath) {
    const mod = require(relPath);
    const factory = typeof mod === 'function' ? mod : global.get;
    return factory;
}

module.exports = { bindFunctionInObj, loadModuleFactory };
```

### Basic Test Setup

```js
const { bindFunctionInObj, loadModuleFactory } = require('./testUtils');

describe('ModuleName', () => {
    let obj;
    let app;

    beforeEach(() => {
        obj = loadModuleFactory('../moduleName.js')();
        app = obj.functions;
        
        // Load libraries jika ada useLibrary
        if (app.useLibrary) {
            app.useLibrary().map(lib => Object.assign(app, require(`../${lib}`)().functions));
        }
        
        obj.f = () => app;
        obj.config = { api: { finaDbIndex: "1", dbIndex: 2 } };
        obj.model = {};
        
        // Mock services
        obj.dataService = { queryData: jest.fn() };
        obj.storageService = { getCurrentUser: jest.fn(() => 'user-1') };
        obj.loadingService = { start: jest.fn(() => 'ref'), stop: jest.fn() };
        obj.notificationService = { showError: jest.fn(), showSuccess: jest.fn() };
        
        bindFunctionInObj(obj, obj);
    });

    // Tests...
});
```

### Test untuk Validation Function

```js
describe('validation', () => {
    test('should pass with valid data', () => {
        const model = { field1: 'value', details: [{ name: 'item1' }] };
        expect(app.validation(model)).toBe(model);
    });

    test('should throw when mandatory field is missing', () => {
        const model = { details: [] };
        expect(() => app.validation(model)).toThrow('Field 1 harus diisi');
    });
});
```

### Test dengan RxJS

```js
const { of, lastValueFrom } = require('rxjs');

test('should query data correctly', async () => {
    obj.dataService.queryData = jest.fn(() => of([{ id: 1, name: 'test' }]));
    
    await lastValueFrom(app.setAction(
        { name: 'group1', privileges: ['Edit'] }
    ));
    
    expect(obj.dataService.queryData).toHaveBeenCalledTimes(1);
});
```

### Test Categories (Best Practice dari Proton)

```js
describe('Module', () => {
    describe('Normal scenarios', () => { /* happy path */ });
    describe('Edge cases', () => { /* boundary conditions */ });
    describe('Invalid inputs', () => { /* error scenarios */ });
    describe('Deterministic behavior', () => { /* consistent results */ });
});
```

---

## 20. Menu Structure Pattern

```json
[
    {
        "menuName": "",
        "caption": "Home",
        "link": ["./main"],
        "subMenu": []
    },
    {
        "menuName": "",
        "caption": "Menu Group",
        "Link": [],
        "subMenu": [
            {
                "menuName": "",
                "caption": "Sub Menu List",
                "link": ["./list", "NamaList"]
            },
            {
                "menuName": "",
                "caption": "Sub Menu Form",
                "link": ["./form", "NamaForm", "null"]
            }
        ]
    }
]
```

---

## 21. Control Data / Data Filtering by User Group Pattern

Mengontrol data apa saja yang bisa dilihat user berdasarkan group-nya.

### Tabel `CONTROL_DATA_BY_UG`

```sql
INSERT INTO CONTROL_DATA_BY_UG (GROUP_ID, PAGE_NAME, FILTERS) 
VALUES (18, 'permohonanSparepartList', '[{"junction":"","column":"...","operator":"in","value1":"(...)"}]');
```

### Implementasi di List

```js
onPipe: function (...data) {
    if (!this.isNotFirstLoad) {
        return this.f().setControlDataList(
            this.storageService.getCurrentUser(),
            'permohonanSparepartList'
        ).pipe(
            this.tap(() => this.isNotFirstLoad = true),
            this.switchMap(() => this.loadData()),
        )
    }
    // Normal flow setelah first load
    return this.f().setAction(/* ... */)
}
```

---

## Quick Reference: Shipto Address Formatting

Pattern yang konsisten digunakan untuk format alamat pengiriman:

```js
const shipto = [
    data.name,
    data.addressline1,
    data.addressline2,
    [data.city, data.zipcode],
    [data.stateprov, data.country, data.phone]
]
    .map(val => Array.isArray(val) ? val.filter(Boolean).join(' ') : val)
    .filter(Boolean)
    .join('\n');
```

---

## Quick Reference: Data Merging Pattern

Selalu gabungkan model dan form value sebelum proses:

```js
// Sebelum save
const model = { ...this.model, ...this.form.value };

// Sebelum print
const model = { ...this.model, ...this.form.value };

// Update model setelah load data
this.model = structuredClone({ ...this.model, ...newData });
```

> **Note:** Gunakan `structuredClone()` untuk deep copy saat assign ke `this.model` agar tidak ada reference sharing.
