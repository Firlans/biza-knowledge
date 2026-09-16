# Bank Book Source Navigation Mode Problem

## Problem Signal

Use this reference when a Bank Book row opens a source form, but the target form does not behave like it was opened from Bank Book.

Common signals:
- A source form opened from `bankBookForm.js` should be read-only or show only a Back/Kembali button, but it behaves like normal edit mode.
- The target form already supports `mode=from_bankbook`, `fromBankBookMode`, or `applyFromBankBookMode`, but the behavior is not active.
- The first attempted fix adds read-only logic directly inside the target form, even though the navigation did not pass Bank Book mode.
- The issue appears only for some sources, such as FINA rows, Biz-A rows, Ctrl Pusat approved rows, or fallback lookups without `source_id`.

## Root Cause

The source form detects Bank Book context from route query params, usually:

```javascript
{ queryParams: { mode: 'from_bankbook' } }
```

If `bankBookForm.js` navigates without that query param, the target form cannot reliably know it came from Bank Book. Fixing only the target form can create duplicated mode handling and still miss other source forms.

## Corrected Approach

Fix the navigation source first.

In `bankBookForm.js`, centralize Bank Book route params in `buildSourceFormQueryParams` and use it for every `router.navigate` path from `openSourceForm`:

```javascript
buildSourceFormQueryParams: function (nav) {
    return this.f().getFromBankBookQueryParams();
},
```

Then every path should pass the result:

```javascript
const sourceFormParams = this.f().buildSourceFormQueryParams(nav);
this.router.navigate(['../../form', nav.formName, nav.source_id], sourceFormParams);
```

This applies to:
- Direct navigation when `nav.source_id` exists.
- Vendor payment fallback lookup by sequence number.
- JV fallback lookup by voucher/reference number.
- FINA and Biz-A source rows.
- Approved and unapproved rows, when the user requirement is "from Bank Book from anywhere".

## What To Avoid

- Do not patch each target form with extra read-only helpers before confirming the navigation sends `mode=from_bankbook`.
- Do not condition Bank Book params on only `source_db === 'FINA'` or `approved_by_ctrl_pusat` unless the user explicitly asks for that limited behavior.
- Do not leave one `router.navigate` branch using `{}` while another branch uses Bank Book params; that creates inconsistent target form behavior.
- Do not pass nested function calls directly into `router.navigate`; assign the params to a named variable first.

## Implementation Checklist

- Find `bankBookForm.js`.
- Inspect `resolveSourceForm`, `buildOpenSourceNavigation`, `buildSourceFormQueryParams`, and `openSourceForm`.
- Confirm target forms already detect `mode=from_bankbook` through `applyFromBankBookMode` or equivalent.
- Update `buildSourceFormQueryParams` to match the requested scope.
- Ensure all `openSourceForm` navigation branches use `buildSourceFormQueryParams`.
- Preserve `markBankBookStateForReturn()` before navigating.

## Related Files

- `APL/bankBookForm.js`
- Target source forms that already use `applyFromBankBookMode`, for example Other Payment, Other Receipt, Journal Voucher, and Vendor Payment flows.
