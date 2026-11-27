# FINA Customer Receipt Discount Accounts

## Problem signal

A Customer Receipt shows a discount total but the dialog cannot recover the
account for the selected invoice. In the original Proton multi-invoice flow,
the dialog collected the amount and sent `ARINVPMT.DISCTAKENAMOUNT`. The
amount field carries the invoice aggregate. The account belongs to a child
row in `ARINVPMT_DISC` linked by `INVPMTID`.
[Existing POS Sales FML and lookup](<../../MITRA SAPUTRA/posSalesList.js>)

## Payload and readback

- On the existing FML create path, give the invoice payment its own ID.
  Nest `ARINVPMT_DISC` under that invoice payment, use the parent ID in both
  `MASTERID` and `INVPMTID`, and include the child in the audit transaction
  count. Map the selected account to `DISCACCOUNT`.
- The Proton `TdmARPayment` edit path keeps the allocation ID and uses a
  nested `detail` with the existing discount `seq` for an update or removal.
  Read the stored sequence and amount before editing so an unchanged account
  can stay in place and a new value cannot overwrite a different invoice.
- For readback, join `ARINVPMT_DISC` to `ARINVPMT` by `INVPMTID` and filter
  by `PAYMENTID`. Keep the invoice ID and sequence in the result.
  [Payload](../../Proton/lib_pelunasan.js) and
  [query](../../Proton/lib_queryRaw.js)

## Biz-A metadata and legacy rows

In Proton, Kode Alat is an ITEM lookup. Persist the item code in Biz-A against
the payment and invoice. When an existing table also allows several legacy
rows identified by payment alone, use a nullable invoice ID and a unique
expression index that returns NULL for legacy rows. The expression produces
a key only for the payment and invoice pair. Keep legacy rows available for
readback. In Proton, a legacy discount can be associated with an invoice when
the payment has exactly one allocated invoice and the discount amounts agree.
[Migration](<../../Proton/migrate/27 NOVEMBER 2026 task 6631 potongan per invoice.sql>)

## Verification

The Proton regression fixtures check parent-child FML IDs, the discount
account on edit and removal, and readback by invoice. A local Firebird test
ran the generated SELECT and confirmed that the migration accepts multiple
legacy rows for one payment while rejecting a duplicate payment and invoice
pair. Confirm posting and reloading the actual discount account in the target
FINA tenant when deploying. Proton's write payloads were verified with fixtures.
[Regression tests](../../Proton/tests/pelunasanMulti.test.js)

## Related references

- [Biz-A write APIs and read-only executeBlock](sendmodel-write-executeblock-select-rules.md)
- [Biz-A database standards](database-standard-rules.md)
- [Detail-grid action button and row selection](detail-grid-manual-action-buttons-problem.md)
