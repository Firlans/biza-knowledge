---
name: biz-a-rules
description: "Use when editing Biz-A JavaScript form, list, or helper files. Enforces mandatory cross-cutting rules: load the relevant Biz-A reference docs, keep runtime-safe parameter defaults, and avoid unsafe primary-key rendering."
applyTo: "**/*.js"
---

# Biz-A Rules

## Required reference loading

- Sebelum mengubah kode Biz-A, baca `.agents/references/INDEX.md`
  (tabel trigger → file) untuk menentukan reference mana yang relevan dengan
  task, error, atau pattern yang sedang dikerjakan. Load hanya file yang match.
- Jika task menyentuh Biz-A Control Center, App Config, metadata aplikasi/domain,
  penamaan source domain yang diunggah, atau analisis wiring script domain, baca
  `.agents/references/biz-a-control-center-config-rules.md`.
  Pisahkan temuan konfigurasi dari penyebab error runtime yang belum terbukti.
- Jika task membuat atau menganalisis workflow approval BPM, `PR_BPM.json`,
  state/transisi, role approver, atau assignment task, baca
  `.agents/references/biz-a-control-center-approval-workflow-rules.md`.
  Bedakan ID header/detail dari ID instance dan validasi lokal dari hasil runtime.
- Jika task meminta tampilan lebih baik, theming, visual consistency, spacing,
  typography, alignment, density, responsivitas profile, light/dark, migrasi
  Material 3, atau pemeriksaan kontras, load
  `.agents/references/visual-design-theming-index.md`.
- Jika task membuat mobile layout dari prototipe, menata header/filter,
  memasangkan tanggal, membuat kartu master/list, atau memperbaiki kartu kosong
  dan tombol yang hilang pada mobile, load
  `.agents/references/mobile-layout-rules.md` sebelum pencarian
  repo yang lebih luas. Pertahankan kontrol/authorization asli, verifikasi
  pemetaan kolom serta ID baris, dan bedakan hasil fixture dari runtime target.
- Jika task menyentuh file form, load `form-rules.md` dan `pk-field-config.md`.
- Jika input terbaru hilang setelah dialog/action, `this.form.value` berbeda
  dari `this.model`, atau kode akan clone/replace model pada form aktif, load
  `.agents/references/form-model-value-sync-problem.md`.
- Jika detail-grid tanggal kosong menampilkan `Invalid Date` atau `sendModel`
  gagal dengan Firebird `conversion error from string` pada kolom `DATE`, load
  `.agents/references/biz-a-date-conversion-invalid-date-problem.md`.
- Jika task menyentuh file list, load `list-rules.md`.
- Jika task menyentuh custom table columns, print table columns, atau field
  seperti `visible_column`, load
  `.agents/references/table-custom-column-flexible-rules.md`.
- Jika task menyentuh horizontal scroll detail-grid, tabel keluar frame,
  kolom nowrap, angka/money terpotong, sizing kolom dengan `rem`, atau
  centering isi kolom flex, load
  `.agents/references/detail-grid-scroll-sizing-alignment-problem.md`.
- Jika task menyentuh field inline di samping table Formly/Biz-A list,
  wrapper table list, selector `body > app-root > app-list > div > table`,
  atau root `fields` pada list, load
  `.agents/references/formly-list-inline-field-table-problem.md`.
- Jika task menyentuh attachment file, kolom BLOB PDF/image, `input-file`,
  `updateImg`, `btoa`, atau error attachment seperti `n.map is not a function`
  dan `Bad control character in string literal`, load
  `.agents/references/attachment-blob-querydata-problem.md`.
- Jika task menyentuh `previewTemplateFina`, template print yang dipilih/disimpan,
  `templateid`, preview Print/Close Biz-A, jsPDF, ukuran Letter/Half Letter,
  orientasi atau fit-to-paper, load
  `.agents/references/fina-template-print-selection-problem.md`.
- Jika unduhan Excel meminta recovery, muncul `We found a problem with some
  content`, atau ekspor memakai SheetJS/ExcelJS untuk pewarnaan header, load
  `.agents/references/excel-export-ooxml-recovery-problem.md`
  sebelum pencarian repo yang lebih luas. Periksa XML file akhir dan bedakan
  round trip library dari pembukaan normal di Microsoft Excel.
- Jika tidak ada reference yang cocok di INDEX.md, cari contoh lokal di repo
  dulu sebelum mempertimbangkan sumber eksternal.
- Load hanya reference yang relevan dengan file dan task saat ini agar context
  tetap efisien.

## Runtime-safe parameter defaults

- Never read runtime state in a default parameter expression.
- Forbidden sources include `this.f()`, `this.form`, `this.model`, services, optional-chained control reads, and any fallback that depends on the form already being ready.
- The following pattern is forbidden because it can throw before the function body runs:

```javascript
hydrateUnitsLookups: function (units = [], locationId = this.f().getSelectedLocationId()) {
    // ...
}
```

- Another forbidden example is:

```javascript
refreshData: function (customerId = this.form?.get?.('customerid')?.value) {
    // ...
}
```

- If a fallback depends on runtime state, accept `undefined` in the signature and resolve the fallback inside the function body.

```javascript
hydrateUnitsLookups: function (units, locationId) {
    const sourceUnits = Array.isArray(units) ? units : [];
    const selectedLocationId = typeof locationId === 'undefined'
        ? this.f().getSelectedLocationId()
        : locationId;

    // ...
}
```

- This is a hard rule for Biz-A JavaScript because default parameter expressions are evaluated before the function body and can cause runtime errors in Keres or embed flows when `this`, form controls, or injected services are not ready yet.

## Biz-A query join depth limit

- Query join-depth details are documented in `.agents/references/biz-a-query-join-depth-problem.md`.
- Keep `columns[].data` and `filter[].column` paths short, split long joins into smaller queries, and never introduce queries against tables that do not exist in the deployed schema.

## structuredClone only for model data

- Use `structuredClone` only for plain model/payload data.
- Never use `structuredClone` on Biz-A configuration objects such as `fields`, `props`, detail-grid `columns`, dialog configs, lookup configs, or button configs.
- Biz-A configuration often contains functions (`onClick`, callbacks, native handlers) that cannot be cloned by `structuredClone` and will throw `DataCloneError`.
- If a configuration copy is needed, copy only the required plain properties or use a local helper that preserves function references.

## Form-specific model and primary-key rules

- Detail rule untuk `model` / `initModel` defaults pada form ada di `.agents/references/form-rules.md`.
- Detail rule untuk primary key rendering pada form ada di `.agents/references/form-rules.md` dan `.agents/references/pk-field-config.md`.
- Untuk list files, tetap pakai prinsip yang sama: hindari `model` / `initModel` assignment yang tidak memberi meaningful default.

## Synchronize active form values before model replacement

- Before validation, payload mapping, cloning, or replacing an active form
  model, synchronize the latest controls with this exact precedence:

```javascript
const currentModel = {
    ...this.model,
    ...this.form.value,
};
```

- Model values come first and form values second. Never reverse this order.
- Use the synchronized snapshot as the source for the next model state so a
  dialog, step change, lookup, repeat update, or detail-grid refresh cannot
  restore stale model values over recent user input.
- See `.agents/references/form-model-value-sync-problem.md` for
  the full checklist and regression-test pattern.

## No nested function calls in parameters

- Never pass the result of a function call directly as a parameter to another function call.
- Nested function calls make code harder to debug because intermediate values cannot be inspected during execution.
- Extract the inner function call result to a named variable first, then pass the variable as the parameter.

**Forbidden — nested function calls:**

```javascript
// ❌ Hard to debug: which function failed? What was the intermediate value?
this.f().saveRecord(this.f().getFormData());

// ❌ Same issue with method chains
this.f().validateData(this.form.get('customerId').value);

// ❌ Multiple levels of nesting
this.f().func1(this.f().func2(this.f().func3()));
```

**Correct — extract to named variables:**

```javascript
// ✅ Easy to debug: can inspect formData in debugger
const formData = this.f().getFormData();
this.f().saveRecord(formData);

// ✅ Clear intention: shows what value is being passed
const customerId = this.form.get('customerId').value;
this.f().validateData(customerId);

// ✅ Each step is clear and debuggable
const innerResult = this.f().func3();
const middleResult = this.f().func2(innerResult);
this.f().func1(middleResult);
```

- This rule applies to all Biz-A JavaScript files (forms, lists, helpers).
- Exception: Single-level method calls on stable objects (e.g., `obj.method().anotherMethod()`) are acceptable if they are fluent chains on the same object instance.
- The reasoning: when debugging stack traces and using console inspection, nested function calls make it impossible to see which intermediate value caused an error or behaved unexpectedly.
