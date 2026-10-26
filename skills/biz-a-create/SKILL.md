---
name: biz-a-create
description: "Create new Biz-A modules (form, list, helper) from scratch. Use when: buat form baru, buat list baru, create helper, scaffold module, generate Biz-A, new form/list/helper structure."
---

# Biz-A Create — Smart Knowledge Loading

Create new Biz-A modules (form, list, helper) with minimal context overhead. This skill loads **only** the knowledge base needed for your specific task.

---

## Step 1 — Detect Module Type

What are you creating?

- **Form** (form.js) → create a new form module with fields, model, lifecycle
- **List** (list.js) → create a new list module with columns, filters, buttons
- **Helper/Library** (lib_*.js) → create a utility/query/calculation helper

---

## Step 2 — Load Relevant Knowledge Base (Smart Load)

Depending on your module type, the appropriate reference docs will load:

### Creating a Form?
Loads: **patterns.md (Section 1, 3, 10, 14, 15, 18)**, **form-rules.md**, **creation-checklist.md**, **biz-a.rules.instructions.md**, **pk-field-config.md**

- Standard Biz-A module export (`get = function () { return { ... } }`)
- Form structure with `model`, `tableName`, `fields`, `functions`
- Lifecycle pattern: `beforeLoadData`, `onInit`, `preparingData`, `setDbIndex`, `listener`, `saveClicked`
- Detail grid pattern (if applicable)
- Save & validation orchestration
- Primary key field configuration

### Creating a List?
Loads: **patterns.md (Section 1, 4, 8, 20, 21)**, **list-rules.md**, **creation-checklist.md**, **biz-a.rules.instructions.md**

- Standard Biz-A module export
- List structure with `buttons`, `columns`, `filter`, `order`
- Authorization & data scoping via `onPipe`
- Menu integration

### Creating a Helper/Library?
Loads: **patterns.md (Section 2, 5, 6, 7, 9)**, **helper-rules.md**, **creation-checklist.md**, **biz-a.rules.instructions.md**

- Library pattern (`useLibrary` reuse before creating)
- Query pattern (`lib_qry`, `lib_queryRaw`)
- Utility functions deterministic and pure
- Separation of concerns

## Step 3 — Follow the Creation Workflow

### For Form
1. Start with `model` object (initial state)
2. Define `tableName` (backend table/view name)
3. Build `fields` array with Formly config + expressions
4. Implement `functions` lifecycle: `beforeLoadData`, `onInit`, `preparingData`, `setDbIndex`, `listener`, `saveClicked`
5. Add named helpers: `buildPayload`, `applyToModel`, `validation`
6. Handle detail grids if needed (Section 10)
7. Validate save flow (Section 14) — check `response.error` and `json2fina`

### For List
1. Define top-level: `buttons`, `columns`, `filter`, `order`
2. Implement lifecycle: `beforeLoadData`, `onPipe` (auth + filtering)
3. Add button handlers (short, navigation-oriented)
4. Shape data for display

### For Helper/Library
1. Check `useLibrary` first — reuse existing helpers before creating new
2. Name functions with clear intent: `build...`, `calculate...`, `normalize...`, `validate...`
3. Keep functions pure and deterministic
4. Export via `module.exports` or as object methods
5. Document parameters and return type
6. Keep critical logic deterministic and easy to inspect

---

## Step 4 — Quality Gate

Before declaring complete:

- [ ] Module export follows standard pattern (Section 1)
- [ ] No hardcoded defaults in function parameters (use `undefined` + function body fallback)
- [ ] No nested function calls in parameters (extract to named variables)
- [ ] Primary key fields in `model` but NOT in `fields`
- [ ] All lifecycle hooks in correct sections
- [ ] Single async chain → single `subscribe()` (RxJS linear flow)
- [ ] No defensive null checks on `this.form.get()` (use early return instead)
- [ ] Code style matches `form-rules.md` / `list-rules.md` / `helper-rules.md`

---

## Step 5 — Summary & Next Steps

Tell me what you created, and I'll:
1. Verify it against the quality gate
2. Suggest refactoring or quality improvements
3. Point out related patterns to apply (e.g., running number, approval workflow)
4. Help with debug if anything isn't working

---

## Quick Reference: Knowledge Files

| Knowledge | When to Load |
|-----------|--------------|
| `patterns.md` | Always (core patterns) |
| `form-rules.md` | Creating/updating form |
| `list-rules.md` | Creating/updating list |
| `helper-rules.md` | Creating/updating helper |
| `creation-checklist.md` | Creating new module |
| `pk-field-config.md` | Setting up form fields |
| `biz-a.rules.instructions.md` | Always (mandatory rules) |

No other knowledge loads unless you explicitly ask.

---

# Step 4 — Generate Module

Gunakan aturan dari doc yang sudah dibaca:

- **Form**: ikuti lifecycle dan style targets dari `form-rules.md`
  - `beforeLoadData` → setup only, panggil `setDbIndex`
  - `onInit` → mode detection, `preparingData`, aktifkan `listener`
  - `preparingData` → initial/reference data
  - `setDbIndex` → semua `dbIndex` assignment
  - `listener` → `valueChanges` reactive wiring
  - `saveClicked` → payload dan save flow
- **List**: ikuti struktur dari `list-rules.md`
  - `beforeLoadData` → db index, flags
  - `onPipe` → authorization, data scoping, button shaping
  - Action handlers → pendek, navigasi-oriented
- **Helper**: ikuti separation dan naming dari `helper-rules.md`
  - Query logic → `lib_qry`
  - Raw SQL → `lib_queryRaw`
  - Utility → `lib_utils`
  - Authorization → `lib_authorization`
- **Naming**: `build...`, `apply...`, `normalize...`, `set...`, `load...`, `validation`

---

# Step 5 — Validate

Verifikasi semua poin di `.agents/references/quality-gates.md` dan `.agents/references/creation-checklist.md`.

Checklist kritis:
- [ ] Standard Biz-A export: `get = function () { return { ... } }` + `module.exports = get`
- [ ] `fields.key` lowercase, prefer `snake_case`
- [ ] `dbIndex` hanya di `setDbIndex` via `findLuFina`
- [ ] Satu async chain → satu `subscribe()`
- [ ] `sendModel` divalidasi via `response.error`
- [ ] `json2fina` divalidasi via `res.result?.[0]?.error`
- [ ] Merge `this.model` + `this.form.value` sebelum validation/save
- [ ] `APL` dan `BERCA` tidak digunakan sebagai referensi

## Invocation hint

Describe the module to create, e.g., 'buat form untuk input karyawan', 'create helper untuk calculate gaji'
