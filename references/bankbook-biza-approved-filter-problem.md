# Bank Book Biz-A Approved Filter Problem

## Problem Signal

Use this reference when Bank Book Biz-A rows should show only unapproved data, but approved rows still appear.

Common signals:
- `bankBookForm.js` Biz-A grid still shows approved VP, OP, OR, or JV rows.
- Vendor Payment rows with `chequeid_fina` already filled still appear in Biz-A Bank Book.
- Other Payment, Other Receipt, or JV rows with `isfinasend` / `jvid_fina` still appear in the unapproved Biz-A section.
- Opening a row from Bank Book behaves readonly/editable incorrectly because the row approval flag was mapped incorrectly.

## Root Cause

Bank Book Biz-A rows are assembled from `APL/lib_qry.js` and then mapped in `APL/bankBookForm.js`.

Approved filtering fails when the source row does not expose a normalized approval marker. For JV-backed rows the marker usually comes from:

```javascript
APPROVED_BY_CTRL_PUSAT: header.isfinasend === true
    || header.isfinasend === 1
    || header.isfinasend === '1'
    || Boolean(header.jvid_fina)
```

Vendor Payment rows are different. They are approved when `APCHEQ.CHEQUEID_FINA` / `chequeid_fina` is filled. If `buildBizaVendorPaymentRows` does not map that into `APPROVED_BY_CTRL_PUSAT`, `bankBookForm.js` treats approved VP rows as unapproved and keeps them visible.

## Corrected Approach

Normalize approved state at the data source row before `bankBookForm.js` filters it.

In `APL/lib_qry.js`, `buildBizaVendorPaymentQueryParam` must select the FINA id:

```javascript
{ data: 'APCHEQ.CHEQUEID_FINA', key: 'chequeid_fina' }
```

Then `buildBizaVendorPaymentRows` must map it:

```javascript
const finaChequeId = payment?.chequeid_fina ?? payment?.CHEQUEID_FINA;
const approvedByCtrlPusat = finaChequeId !== null
    && finaChequeId !== undefined
    && finaChequeId !== ''
    && finaChequeId !== 0
    && finaChequeId !== '0';

APPROVED_BY_CTRL_PUSAT: approvedByCtrlPusat,
```

In `APL/bankBookForm.js`, centralize row approval detection in `isApprovedByCtrlPusat(row)` and let it recognize:

- `approved_by_ctrl_pusat` / `APPROVED_BY_CTRL_PUSAT`
- `isfinasend` / `ISFINASEND`
- `jvid_fina` / `JVID_FINA`
- `chequeid_fina` / `CHEQUEID_FINA`

Then filter Biz-A rows before mapping them into the Biz-A grid:

```javascript
const bizaSourceRows = Array.isArray(sourceData.biza) ? sourceData.biza : [];
const unapprovedBizaRows = bizaSourceRows.filter(row => !this.f().isApprovedByCtrlPusat(row));
const bizaRows = this.f().mapBankBookRows(unapprovedBizaRows, glaccount);
```

## What To Avoid

- Do not filter only by `APPROVED_BY_CTRL_PUSAT` if some sources expose approval through `chequeid_fina`, `jvid_fina`, or `isfinasend`.
- Do not fix only `bankBookForm.js` when `lib_qry.js` never maps Vendor Payment approval status.
- Do not assume Vendor Payment follows the same JV approval fields. VP uses `APCHEQ.CHEQUEID_FINA`.
- Do not change FINA Bank Book rows when the request is only for Biz-A Bank Book unapproved data.

## Implementation Checklist

- Inspect `APL/lib_qry.js`:
  - `buildBizaVendorPaymentQueryParam`
  - `buildBizaVendorPaymentRows`
  - `buildBizaJvBankBookRows`
- Inspect `APL/bankBookForm.js`:
  - `mapBankBookDataSources`
  - `mapBankBookRows`
  - `isApprovedByCtrlPusat`
  - `buildOpenSourceNavigation`
- Confirm `Vendor Payment` approved state is based on `chequeid_fina`.
- Confirm JV/OP/OR approved state is based on `isfinasend` or `jvid_fina`.
- Filter only `sourceData.biza`; leave `sourceData.fina` unchanged.
- Preserve row navigation behavior by using the same normalized approval helper.

## Related Files

- `APL/bankBookForm.js`
- `APL/lib_qry.js`
- `APL/vendorPaymentForm.js`
- `APL/vendorPaymentListBiza.js`

## Related References

- `.agents/references/bankbook-source-navigation-mode-problem.md`
- `.agents/references/fina-biza-jv-key-mismatch-problem.md`
