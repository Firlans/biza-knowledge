---
name: biz-a-simplify
description: "Simplify existing Biz-A modules — remove dead code, replace functions with library helpers, inline unnecessary wrappers, flatten nested structures. Use when: simplify code, sederhanakan, inline function, hapus function tidak terpakai, unused functions, dead code, terlalu banyak function, ganti dengan library helper, flatten subscribe, rapikan code."
---

# Biz-A Simplify — Smart Knowledge Loading

Simplify existing Biz-A modules by removing unnecessary complexity, dead code, and improving clarity. This skill loads **only** the knowledge base needed for your specific task.

This skill **complements** `biz-a-refactor` (which handles lifecycle separation). This skill focuses on **code structure simplification** — removing dead code, replacing functions with library helpers, eliminating unnecessary indirection, flattening nested async calls, and moving dialog logic to shared libraries.

---

## Step 1 — Detect Simplification Target

What are you simplifying?

- **Remove dead/unused code** → functions with zero callers
- **Replace with library helpers** → inline logic already exists in a library
- **Flatten async calls** → nested subscribe → RxJS operators (mergeMap, switchMap)
- **Inline small wrappers** → single-call functions that add no clarity
- **Extract to shared library** → dialog logic, complex calculations used by multiple modules

---

## Step 2 — Load Relevant Knowledge Base (Smart Load)

### Simplifying Any Module?
Always loads: **patterns.md (Section 2, 8, 11, 14, 15)**, **helper-rules.md**, **biz-a.rules.instructions.md**

Additional loads based on target:
- **Form simplification**: **form-rules.md**
- **List simplification**: **list-rules.md**
- **Async/RxJS issues**: **patterns.md (Section 14, 15)**
- **Dialog extraction**: **patterns.md (Section 11)**

---

## Step 3 — Code Analysis

### Step 3a — Read the target file completely
Understand structure and all functions.

### Step 3b — Function Inventory
For each function in the target file, document:
- **Name**: function identifier
- **Lines**: total lines of code
- **Callers**: how many places call this function
- **Implicit callers**: called via lifecycle, config, or callback reference?
- **Wrapper**: does it only call one operation or simple native method?
- **Library match**: does a library (lib_utility, lib_helper, lib_qry) have equivalent?

### Step 3c — Identify 7 Anti-patterns

#### 1. Dead Code — Zero Callers
Function exists but is **never called**.
```js
// ❌ Dead: nobody calls getOldValue()
getOldValue: function () { return this.oldValue; },

// ✅ Fix: delete it
```

#### 2. Function Within Function — Single Caller Chain
Function A calls function B, and **B is only called from A**.
```js
// ❌ Anti-pattern:
saveData: function () {
    const payload = this.f().buildPayload();
    return this.f().sendPayload(payload);
},
buildPayload: function () { /* ... */ },
sendPayload: function (p) { /* ... */ },

// ✅ Better: inline buildPayload into saveData
saveData: function () {
    const payload = { /* ... */ };
    return this.f().sendPayload(payload);
},
sendPayload: function (p) { /* ... */ },
```

#### 3. Small Wrapper — Adds No Clarity
Function only wraps one native operation or library call.
```js
// ❌ Wrapper adds nothing:
getCustomerId: function () {
    return this.form.get('customer_id').value;
},

// ✅ Just call directly:
// in saveData: const customerId = this.form.get('customer_id').value;
```

#### 4. Library Replacement — Logic Already in Helper
Function duplicates logic that exists in a library.
```js
// ❌ Duplicates lib_gaji.normalizePointRows():
normalizePoints: function (points) {
    return points.map((p, i) => ({
        id: p.id || `p${i}`,
        text: p.text || `Point ${i + 1}`
    }));
},

// ✅ Use library instead:
// In preparingData: const points = this.f().normalizePointRows(raw.points);
```

#### 5. Nested Subscribe — RxJS Anti-pattern
Subscribe inside a subscribe.
```js
// ❌ Nested subscribe:
listener: function () {
    this.form.get('location_id').valueChanges.subscribe((loc) => {
        this.dataService.getServicePeriods(loc).subscribe((periods) => {
            this.form.get('service_period_id').patchValue(null);
        });
    });
},

// ✅ Flatten with switchMap:
listener: function () {
    this.form.get('location_id').valueChanges
        .pipe(
            switchMap(loc => this.dataService.getServicePeriods(loc))
        )
        .subscribe(() => {
            this.form.get('service_period_id').patchValue(null);
        });
},
```

#### 6. Dialog Logic in Module — Extract to lib_dialog
Form-specific dialog code that could be shared.
```js
// ❌ Dialog logic scattered in form:
confirmDelete: function (itemId) {
    return this.notify.confirm('Delete item?')
        .pipe(
            switchMap(ok => this.api.deleteItem(itemId))
        )
        .toPromise();
},

// ✅ Move to lib_dialog_confirmDelete:
// In form: const lib = this.f().useLibrary('lib_dialog');
//          lib.confirmDeleteItem(itemId).toPromise();
```

#### 7. Repeated Pattern — Consolidate Logic
Same logic pattern repeated multiple times.
```js
// ❌ Repeated filtering:
const activeItems = items.filter(i => i.status === 'ACTIVE');
const activeCount = activeItems.length;
const activeSummary = activeItems.reduce((sum, i) => sum + i.qty, 0);

const pendingItems = items.filter(i => i.status === 'PENDING');
const pendingCount = pendingItems.length;
const pendingSummary = pendingItems.reduce((sum, i) => sum + i.qty, 0);

// ✅ Extract helper:
const getStatusGroup = (status) => {
    const filtered = items.filter(i => i.status === status);
    return {
        count: filtered.length,
        summary: filtered.reduce((sum, i) => sum + i.qty, 0)
    };
};
const active = getStatusGroup('ACTIVE');
const pending = getStatusGroup('PENDING');
```

---

## Step 4 — Simplification Workflow

### For Each Anti-pattern Found

1. **Verify** the function is safe to remove/inline/replace
2. **Check callers** — no implicit dependencies?
3. **Update call sites** if replacing with library
4. **Verify** code is clearer after change

### Priority Order

1. **Dead code** (zero callers) — delete
2. **Nested subscribe** — flatten immediately
3. **Library replacement** — reduce duplication
4. **Function within function** — inline
5. **Small wrappers** — remove if no clarity gain
6. **Repeated patterns** — consolidate

---

## Step 5 — Safety Checks

Before each simplification:
- [ ] No implicit callers (lifecycle, config, callback references)
- [ ] Replacement is clearer (not just shorter)
- [ ] Library helpers are available and maintained

---

## Step 6 — Quality Gate

After simplification:

- [ ] No dead code remains
- [ ] No nested subscribe
- [ ] No unnecessary wrappers
- [ ] Functions with clear purpose and naming
- [ ] Code is more readable, not just shorter
- [ ] All library helpers used instead of duplicates
- [ ] Async flows are linear (one subscribe per flow)

---

## Step 7 — Summary & Next Steps

Tell me what you simplified, and I'll:
1. Review changes for correctness
2. Identify any remaining anti-patterns
3. Suggest related refactors (see `biz-a-refactor`)
4. Help debug if regressions appear

---

## Quick Reference: Knowledge Files

| Knowledge | When to Load |
|-----------|--------------|
| `patterns.md (Section 2, 8, 11, 14, 15)` | Always (core patterns) |
| `form-rules.md` | Simplifying form |
| `list-rules.md` | Simplifying list |
| `helper-rules.md` | Simplifying helper |
| `biz-a.rules.instructions.md` | Always (mandatory rules) |

No other knowledge loads unless you explicitly ask.
// ❌ BAD — function dalam function, B hanya dipanggil dari A
syncSalesReturnNumber: function () {
    return this.f().refreshSalesReturnNumber().pipe(
        this.tap(sr_no => this.f().applySalesReturnNumber(sr_no))
    )
},

applySalesReturnNumber: function (sr_no) {
    this.form.get('sr_no')?.setValue(sr_no || null)
},

// ✅ GOOD — inline langsung, hapus function B
syncSalesReturnNumber: function () {
    return this.f().refreshSalesReturnNumber().pipe(
        this.tap(sr_no => this.form.get('sr_no')?.setValue(sr_no || null))
    )
},
```

**Pengecualian — JANGAN inline jika:**
- Function B dipanggil dari **≥2 tempat berbeda** (itu reusable, bukan wrapper)
- Function B punya **>5 baris logic non-trivial** dengan business name jelas (misal `buildPayload`, `validation`)
- Function B ada di **`useLibrary`** (shared across modules)

## Aturan 2: Function Terlalu Kecil (Trivial Wrapper)

Function ≤3 baris yang **hanya membungkus satu operasi native** tanpa menambah business meaning → inline langsung di caller.

```js
// ❌ BAD — wrapper terlalu kecil, tidak ada business logic
getToday: function () {
    return this.dayjs().format('YYYY-MM-DD')
},

getSelectedWarehouseId: function () {
    return this.form.get('warehouseid')?.value
},

// ✅ GOOD — tulis langsung di tempat dipanggil
const today = this.dayjs().format('YYYY-MM-DD')
const warehouseId = this.form.get('warehouseid')?.value
```

**Pengecualian — JANGAN inline jika:**
- Function kecil tapi dipanggil dari **≥3 tempat** (DRY principle masih berlaku)
- Function kecil tapi punya **business name yang memperjelas intent** dan dipakai di banyak tempat (misal `toNumber()` di `lib_utils`)
- Function ada di **`useLibrary`** (shared)

## Aturan 3: Nested Subscribe (Subscribe dalam Subscribe)

Subscribe di dalam callback subscribe → flatten ke **satu pipe chain linear** dengan satu `subscribe()` di akhir.

```js
// ❌ BAD — nested subscribe, sulit di-trace, rawan memory leak
watchSourceInvoiceChange: function () {
    this.form.get('arinvoiceid')?.valueChanges.subscribe(arinvoiceid => {
        if (!arinvoiceid) { return }
        this.f().getSourceInvoice(arinvoiceid).subscribe({
            next: data => this.f().applySourceInvoice(data),
            error: err => this.f().resetSourceInvoiceControl(),
        })
    })
},

// ✅ GOOD — flat pipe chain, satu subscribe
watchSourceInvoiceChange: function () {
    this.form.get('arinvoiceid')?.valueChanges.pipe(
        this.filter(arinvoiceid => !!arinvoiceid),
        this.switchMap(arinvoiceid => this.f().getSourceInvoice(arinvoiceid).pipe(
            this.catchError(err => {
                this.f().resetSourceInvoiceControl()
                return this.EMPTY
            })
        ))
    ).subscribe(data => this.f().applySourceInvoice(data))
},
```

**Teknik flatten:**
- `switchMap` / `mergeMap` / `concatMap` untuk async chain
- `from()` + `concatMap()` + `toArray()` untuk sequential array processing
- `catchError` + `EMPTY` untuk error handling tanpa break chain
- `filter()` untuk guard clause di awal pipe
- Satu `subscribe()` di paling akhir — **tidak boleh nested**

## Aturan 4a: Function Bisa Diganti Library Helper (Library Replacement)

Function yang duplicate atau partial-duplicate logic dari library helper — ganti dengan call ke library helper, atau refactor function untuk menggunakan library helper.

```js
// ❌ BAD — duplicate logic dari lib_utility.toNumber()
toNumber: function (val) {
    return val ? Number(val) : 0
},

parseAmount: function (str) {
    const num = str ? Number(str) : 0
    return num < 0 ? 0 : num
},

// ✅ GOOD — ganti dengan lib_utility
useLibrary: function () {
    return ['lib_utility']
},

parseAmount: function (str) {
    const num = this.f().toNumber(str)
    return num < 0 ? 0 : num
},
```

**Checklist fungsi umum yang sering ada di library:**
- `toNumber(val)` — string ke number, null → 0
- `toString(val)` — any to string
- `toUpperCase(val)` / `toLowerCase(val)` — case conversion
- `trim(val)` — string trimming
- `capitalize(str)` — first letter uppercase
- `normalizePhone(phone)` — phone number formatting
- `normalizeCurrency(val)` — currency parsing/formatting
- `calculateTax(amount, rate)` — tax calculation
- `calculateDiscount(amount, pct)` — discount calculation
- `isValidEmail(email)` — email validation
- `isValidPhone(phone)` — phone validation
- `isValidDate(date)` — date validation
- `formatDate(date, fmt)` — date formatting
- `addDays(date, days)` — date arithmetic
- `getMonthName(month)` — month name lookup
- `getStatusLabel(status)` — status label mapping
- `buildQueryString(params)` — query building
- `parseQueryString(qs)` — query parsing
- `deepClone(obj)` — object cloning
- `mergeDeep(target, source)` — object merging
- `flattenObject(obj)` — flatten nested object
- `pickKeys(obj, keys)` — select specific keys dari object
- `omitKeys(obj, keys)` — exclude specific keys dari object

**Proses replacement:**
1. Identifikasi function di target yang logic-nya sudah ada di library
2. **Cek signature & behavior** — apakah library helper bisa langsung dipakai atau perlu composition/wrapping
3. **Replace call site** — ganti function di target dengan call ke library helper
4. **Hapus function lama** — jika setelah replacement function lama tidak punya caller lagi, hapus (Aturan 5)
5. **Update `useLibrary`** — pastikan library yang menyediakan helper sudah di-load

**Pengecualian — JANGAN replace jika:**
- Library helper memiliki **signature berbeda** dan refactoring sangat kompleks
- Library helper ada di **external npm package** yang belum di-trust di module ini
- Function lama punya **side effect khusus** yang tidak terdapat di library helper (misal logging, state mutation yang unik)
- Library helper masih dalam **development** atau tidak stabil

## Aturan 4b: Generic Wrapper (Wrapper Tanpa Business Meaning)

Wrapper function yang hanya meneruskan ke API native tanpa menambah logic atau business meaning → hapus, gunakan API langsung.

```js
// ❌ BAD — generic wrapper yang tidak menambah apapun
getFormValue: function (key) {
    return this.form.get(key)?.value
},

setFormValue: function (key, val) {
    this.form.get(key)?.setValue(val)
},

watchControl: function (key) {
    return this.form.get(key)?.valueChanges
},

loadLookupOptions: function (key) {
    return this.f().getLookupComponent(key)?.loadOptions()
},

// ✅ GOOD — gunakan API langsung, lebih explicit
const val = this.form.get('customer_name')?.value
this.form.get('customer_name')?.setValue('PT ABC')
this.form.get('customer_name')?.valueChanges.subscribe(...)
```

**Pengecualian — JANGAN hapus jika:**
- Wrapper menambah **side effect** atau **transformation** (misal logging, normalization)
- Wrapper menjadi **facade** untuk operasi multi-step (misal `refreshWarehouseLookup()` yang clear + reload + filter)

## Aturan 5: Function Tidak Terpakai (Zero Caller)

Function yang **tidak punya caller di module** dan **bukan** entrypoint lifecycle/config/framework → hapus.

```js
// ❌ BAD — function mati, tidak pernah dipanggil
resetDraftSummary: function () {
    this.form.get('draft_summary')?.setValue(null)
},

save: function () {
    return this.f().submit()
},

// ✅ GOOD — function mati dihapus, sisakan flow yang benar-benar dipakai
save: function () {
    return this.f().submit()
},
```

**Pengecualian — JANGAN hapus jika:**
- Function direferensikan oleh lifecycle Biz-A, config object, listener map, action/renderer, atau callback yang dipassing sebagai reference
- Function adalah contract/public surface yang memang dipanggil dari luar file dan sudah terverifikasi lewat grep workspace
- Masih ada keraguan apakah function dipanggil implicit oleh framework; verifikasi dulu sebelum hapus

## Aturan 6: Function Dialog Harus Dipindah ke `lib_dialog`

Jika ada function di form/list yang fokus pada dialog orchestration — misalnya membangun `fields` atau `config`, lalu memanggil `this.dialog.open(...)`, `this.f().openDialog(...)`, atau menangani hasil dialog — pindahkan function itu ke `lib_dialog`.

```js
// ❌ BAD — function dialog tetap hidup di form
openManualNumberDialog: function () {
    const fields = [/* ... */]
    return this.f().openDialog('Manual Quotation Number', { quotno: null }, fields)
},

// ✅ GOOD — dialog dipindah ke lib_dialog, form hanya memanggil helper
useLibrary: function () {
    return ['lib_qry', 'lib_utils', 'lib_dialog']
},

openManualNumberDialog: function () {
    return this.f().dialogManualNumber()
},
```

**Prinsipnya:** dialog helper adalah concern terpisah. Saat simplify menemukan dialog-specific function, jangan hanya di-inline atau dibiarkan di module; ekstrak ke `lib_dialog`.

**Cek saat extract:**
- Pastikan `useLibrary()` memuat `lib_dialog`
- Reuse dialog helper yang sudah ada di `lib_dialog` jika behavior-nya sama atau sangat dekat
- Sisakan orchestration tipis di form/list hanya jika memang perlu menghubungkan hasil dialog ke state module

---

# Step 4 — Simplify

Lakukan simplifikasi secara **incremental** — satu function per satu, pastikan behavior tidak berubah.

### Urutan Eksekusi

1. **Ganti dengan library helper** (Aturan 4a) — early pass, efisiensi tertinggi
2. **Hapus function tidak terpakai** (Aturan 5) — zero-caller yang jelas bukan entrypoint
3. **Pindahkan function dialog ke `lib_dialog`** (Aturan 6) — separation paling jelas, jangan di-inline di form/list
4. **Hapus generic wrapper** (Aturan 4b) — paling aman, tidak mengubah flow
5. **Inline function terlalu kecil** (Aturan 2) — replace call site dengan body
6. **Inline single-caller chain** (Aturan 1) — gabungkan function A dan B
7. **Flatten nested subscribe** (Aturan 3) — paling kompleks, lakukan terakhir

Setelah setiap langkah simplify, **rerun caller count**. Jika ada function yang berubah menjadi zero-caller dan bukan entrypoint, hapus pada pass yang sama.

### Guard Rails

Sebelum meng-inline atau menghapus function, **SELALU verifikasi**:

1. **Hitung caller** — grep nama function di seluruh file. Jika 0 caller, treat sebagai kandidat hapus; jika ≥2 caller, pertimbangkan ulang.
2. **Cek entrypoint implicit** — untuk function 0 caller, verifikasi dulu apakah ia dipakai dari lifecycle/config/framework atau callback reference. Jika ragu, lakukan grep workspace cepat sebelum hapus.
3. **Cek library helper dulu** — sebelum hapus atau inline function, cek apakah logic-nya sudah ada di library (Aturan 4a).
4. **Cek `useLibrary`** — jangan sentuh function dari library external.
5. **Cek side effect** — jika function punya side effect yang perlu di-isolate, biarkan terpisah.
6. **Cek `lib_dialog` lebih dulu** — jangan membuat helper dialog baru jika helper yang setara sudah ada.
7. **Jangan over-simplify** — jika hasil inline membuat parent function >30 baris, pertimbangkan untuk tetap terpisah tapi rename agar lebih jelas.

### Penamaan Setelah Simplify

Jika setelah inline, function parent menjadi lebih besar dan butuh nama yang lebih descriptif:

- Gunakan konvensi Firlan: `build...`, `apply...`, `normalize...`, `set...`, `load...`, `validation`
- Nama harus **spesifik ke domain**, bukan generic (`processData` ❌, `buildSalesReturnPayload` ✅)

---

# Step 5 — Validate

Setelah simplifikasi selesai, verifikasi:

- [ ] **Behavior tidak berubah** — output dan side effect identik dengan sebelum simplify
- [ ] **Library helper dipakai maksimal** — semua function yang logic-nya ada di library sudah di-replace atau direuse dari library
- [ ] **`useLibrary()` up-to-date** — semua library yang dipakai helper sudah di-load, tidak ada unused library
- [ ] **Tidak ada nested subscribe** — semua observable chain linear dengan satu `subscribe()`
- [ ] **Tidak ada single-caller wrapper** — setiap function punya ≥2 caller atau punya business logic non-trivial
- [ ] **Tidak ada trivial wrapper ≤3 baris** tanpa business meaning yang dipanggil dari <3 tempat
- [ ] **Tidak ada generic wrapper** — semua form/API access langsung, kecuali ada side effect
- [ ] **Tidak ada function zero-caller yang tertinggal** kecuali lifecycle/framework/public contract yang sudah terverifikasi
- [ ] **Tidak ada function dialog tertinggal di form/list** — dialog helper sudah dipindahkan atau direuse dari `lib_dialog`
- [ ] **Guard rails dipatuhi** — `useLibrary` functions tidak disentuh, functions ≥3 callers tetap ada
- [ ] **`useLibrary()` memuat `lib_dialog`** jika module masih memanggil dialog helper
- [ ] **Naming sesuai Firlan** — `build...`, `apply...`, `normalize...`, `set...`, `load...`, `validation`
- [ ] **`sendModel` divalidasi** via `response.error`
- [ ] **`json2fina` divalidasi** via `res.result?.[0]?.error`

## Invocation hint

Describe the file to simplify, e.g., 'simplify salesReturnForm.js di project CAR', 'hapus dead code dan inline small functions'
