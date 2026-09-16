---
name: biz-a-refactor
description: "Refactor existing Biz-A modules (form, list, helper) to match Firlan style. Use when: refactor form, refactor list, improve lifecycle, perbaiki structure, samakan style, ikuti style saya, normalize, pisahkan tanggung jawab, rapikan code Biz-A."
argument-hint: "Describe the file to refactor, e.g., 'refactor FormName.js ke Firlan style di project Proton', 'improve lifecycle di karyawanform.js'"
---

# Biz-A Refactor — Smart Knowledge Loading

Refactor existing Biz-A modules to match Firlan style and patterns with minimal context overhead. This skill loads **only** the knowledge base needed for your specific task.

---

## Step 1 — Detect Module Type & Target

What are you refactoring?

- **Form** (form.js) → improve lifecycle separation, field structure, save flow
- **List** (list.js) → improve authorization, filtering, button handling
- **Helper/Library** (lib_*.js) → extract common logic, improve naming, consolidate duplicate functions

---

## Step 2 — Load Relevant Knowledge Base (Smart Load)

### Refactoring a Form?
Loads: **patterns.md (Section 1, 3, 10, 14, 15, 18)**, **form-rules.md**, **refactor-checklist.md**, **biz-a.rules.instructions.md**, **pk-field-config.md**

- Lifecycle separation: `beforeLoadData`, `onInit`, `preparingData`, `setDbIndex`, `listener`, `saveClicked`
- Field and model configuration
- Save & validation orchestration
- Primary key handling
- RxJS linear flow (no nested subscribe)

### Refactoring a List?
Loads: **patterns.md (Section 1, 4, 8, 20, 21)**, **list-rules.md**, **refactor-checklist.md**, **biz-a.rules.instructions.md**

- List structure and configuration
- Authorization & data filtering via `onPipe`
- Button handlers and navigation
- Menu integration

### Refactoring a Helper/Library?
Loads: **patterns.md (Section 2, 5, 6, 7, 9)**, **helper-rules.md**, **refactor-checklist.md**, **biz-a.rules.instructions.md**

- Separation of concerns (query vs UI logic)
- Function naming and clarity
- Pure function principles
- Library reuse patterns

## Step 3 — Pre-Refactor Analysis

### Read the target file completely
Understand current structure, behavior, and edge cases.

### Identify what's working
What business logic is correct and must be preserved?

### Map the issues
Look for:
- Lifecycle hooks doing too much (mixing concerns)
- Repeated patterns that could be extracted to helpers
- Nested subscriptions (flatten with RxJS operators)
- Function parameters that read runtime state
- Primary key fields in form fields (should be in model only)
- Tight coupling

---

## Step 4 — Safe Refactoring

### For each refactoring step
1. Make one small change
2. Review the changed behavior and data flow
3. Commit if safe
4. Move to next change

Keep each refactor small enough that behavior changes are easy to inspect.

---

## Step 5 — Execute Refactoring

### For Form
1. **Separate concerns** in lifecycle hooks
2. **Move dbIndex assignments** to `setDbIndex` (via `findLuFina`)
3. **Extract helpers** for payload building and validation
4. **Flatten async** — one subscribe per flow, use mergeMap/switchMap/concatMap
5. **Cleanup field defaults** — only assign model defaults for non-trivial values
6. **Verify save flow** — check `response.error` and `json2fina` consistently

### For List
1. **Move auth logic** to `onPipe` (if not already)
2. **Simplify button handlers** — keep them short, navigation-oriented
3. **Extract filter builders** into named functions (avoid inline filter objects)
4. **Consolidate data shaping** in one place

### For Helper/Library
1. **Check useLibrary first** — can existing helpers replace your logic?
2. **Extract common patterns** (naming, validation, calculation)
3. **Improve function names** — clarity > brevity
4. **Reduce coupling** — helpers should be pure and deterministic

---

## Step 6 — Quality Gate

Before declaring complete:

- [ ] Lifecycle hooks separated by concern
- [ ] No nested function calls in parameters
- [ ] No runtime state in default parameters
- [ ] Single async chain → single `subscribe()`
- [ ] No defensive null checks on `this.form.get()`
- [ ] Primary key fields properly configured
- [ ] Code style matches `form-rules.md` / `list-rules.md` / `helper-rules.md`
- [ ] No dead code or unused functions
- [ ] Naming follows Biz-A conventions

---

## Step 7 — Summary & Next Steps

Tell me what you refactored, and I'll:
1. Review the changes against the quality gate
2. Suggest further simplifications (see `biz-a-simplify`)
3. Help debug if anything breaks

---

## Quick Reference: Knowledge Files

| Knowledge | When to Load |
|-----------|--------------|
| `patterns.md` | Always (core patterns) |
| `form-rules.md` | Refactoring form |
| `list-rules.md` | Refactoring list |
| `helper-rules.md` | Refactoring helper |
| `refactor-checklist.md` | Refactoring any module |
| `pk-field-config.md` | Form field configuration issues |
| `biz-a.rules.instructions.md` | Always (mandatory rules) |

No other knowledge loads unless you explicitly ask.

### Form
- Rapikan lifecycle sesuai `form-rules.md`:
  - `beforeLoadData` → setup only, panggil `setDbIndex`
  - `onInit` → mode detection, `preparingData`, aktifkan `listener`
  - `preparingData` → initial/reference data
  - `setDbIndex` → semua `dbIndex` assignment via `findLuFina`
  - `listener` → `valueChanges` reactive wiring only
  - `saveClicked` → payload dan save flow
- Pindahkan logic ke hook yang benar
- Extract repeated header/detail mapping ke small helpers (`build...`, `normalize...`, `apply...`)
- Gunakan `structuredClone` saat menyalin model state

### List
- Rapikan struktur sesuai `list-rules.md`
- `buttons`, `columns`, `filter`, `order` dekat module root
- Authorization + data scoping di `onPipe`
- Button handlers pendek, navigasi-oriented
- Readable filter builders > inline repeated filter objects

### Helper
- Rapikan separation dan naming sesuai `helper-rules.md`
- Query logic di query libraries, UI orchestration di form/list
- Helper functions deterministic
- Nama selaras target project

### General
- Jaga agar refactor **tidak mengubah behavior bisnis**
- Satu async chain → satu `subscribe()`
- Reuse `useLibrary` helpers sebelum buat baru
- Merge `this.model` + `this.form.value` sebelum validation/save

---

# Step 5 — Validate

Verifikasi semua poin di `.github/instructions/references/quality-gates.md` dan `.github/instructions/references/refactor-checklist.md`.

Checklist kritis:
- [ ] Behavior bisnis tidak berubah
- [ ] Lifecycle hooks sesuai Firlan style
- [ ] `dbIndex` hanya di `setDbIndex`
- [ ] `sendModel` divalidasi via `response.error`
- [ ] `json2fina` divalidasi via `res.result?.[0]?.error`
- [ ] `APL` dan `BERCA` tidak digunakan sebagai referensi
