# Creation Checklist — Firlan Style

## Form

- [ ] Standard Biz-A export: `get = function () { return { ... } }` + `module.exports = get` (Section 1)
- [ ] Mulai dengan `model`, `tableName`, `fields`, `functions`
- [ ] `fields.key` lowercase, prefer `snake_case`
- [ ] Setup di `beforeLoadData`
- [ ] Mode detection + new/edit flow di `onInit` (Section 3)
- [ ] Initial/reference data loading di `preparingData`
- [ ] Setiap `dbIndex` assignment di `setDbIndex` via `findLuFina` (Section 7)
- [ ] `valueChanges` subscriptions di `listener` (Section 15)
- [ ] Button actions di named handlers: `saveClicked`, `printClicked`, business-specific
- [ ] Detail-grid di focused helpers: `assignDetail`, `apply...`, `build...` (Section 10)
- [ ] Save orchestration: satu linear observable flow, validasi response (Section 14)
- [ ] Running number jika ada → Section 12
- [ ] Approval workflow jika ada → Section 13 (`STATUS_MAP`)

## List

- [ ] `buttons`, `columns`, `filter`, `order` dekat module root (Section 4)
- [ ] Setup + default indexes di `beforeLoadData`
- [ ] Authorization, filter shaping, button shaping di `onPipe` (Section 8, 21)
- [ ] Action handlers pendek, navigasi-oriented

## Lookup

- [ ] FINA lookups: `className: '... lu-fina'` (Section 3)
- [ ] Form lookup `dbIndex` di `setDbIndex`
- [ ] Detail-grid lookup `dbIndex` di `setDbIndex`
- [ ] Jangan duplikasi `dbIndex` di `beforeLoadData`, `onInit`, atau listeners

## Separation

- [ ] Query dan DB access di query libraries (`lib_qry`, `lib_queryRaw`)
- [ ] UI orchestration di form/list modules
- [ ] Reuse shared helpers sebelum buat baru (Section 2)
- [ ] Calculations dan mappers deterministic
- [ ] Merge `this.model` + `this.form.value` sebelum validation/save mapping
- [ ] Dialog pattern >1 module → dedicated dialog library (Section 11)

## Validation

- [ ] Satu async chain → satu `subscribe()`
- [ ] Cek `response.error` setelah `sendModel` (Section 14)
- [ ] Cek `res.result?.[0]?.error` setelah `json2fina` (Section 14)
- [ ] `loadingService.start`/`stop` mengelilingi async flow (Section 18)
