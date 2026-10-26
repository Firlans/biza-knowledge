# FINA Biz-A JV Key Mismatch Problem

Use this reference when a JV-backed Biz-A module loads, opens, approves, or edits FINA journal voucher data and an error mentions `JV.ID`, `JV.JVID`, `jvid_fina`, or `Column unknown JV.ID`.

## Problem Signal

- A FINA-backed form/list fails with an error like `Column unknown JV.ID`.
- An approved Other Payment, Other Receipt, or Journal Voucher flow opens a row from FINA but queries it with `JV.ID`.
- A list action column passes the wrong identifier into an approved form.
- The same module reads both the local Biz-A JV table and the FINA JV table.
- A previous migration changed the local Biz-A JV primary key to `ID`, but the FINA database still uses `JVID`.

## Root Cause

Biz-A and FINA can expose similar JV entities with different primary keys:

- Local Biz-A JV table: use `JV.ID` when querying the Biz-A database.
- FINA JV table: use `JV.JVID` when querying `config.api.finaDbIndex`.
- Mapping from local Biz-A JV to FINA JV: use a dedicated mapping field such as `JV.jvid_fina`.

The bug usually appears when a local Biz-A rename from `JVID` to `ID` is applied too broadly and accidentally changes FINA paths. In FINA, `JV.ID` may not exist, so `queryData` fails before the form can load.

## Corrected Approach

Trace the database boundary before changing any JV path.

For FINA-backed list rows:

```javascript
{
    title: '',
    data: 'jv.jvid',
    button: [{ onClick: 'editOnClick' }],
}
```

For FINA `queryData` calls:

```javascript
const param = {
    filter: [
        { junction: '', column: 'JV.jvid', operator: '=', value1: jvid },
    ],
    columns: [
        { data: 'JV.jvid', key: 'jvid' },
        { data: 'JV.jvid.jvid.JVDET.seq', key: 'seq' },
    ],
    dbIndex: this.config.api.finaDbIndex,
};
```

For local Biz-A lookup by FINA JV id:

```javascript
const param = {
    filter: [
        { junction: '', column: 'JV.jvid_fina', operator: '=', value1: jvid },
    ],
    columns: [
        { data: 'JV.id', key: 'jvid' },
        { data: 'JV.pembayaran_ke', key: 'pembayaran_ke' },
    ],
};
```

## Implementation Checklist

1. Identify whether each query targets Biz-A or FINA by checking `dbIndex`, `finaDbIndex`, `beforeLoadData`, and the `queryData` call.
2. In FINA lists, use row action data from `jv.jvid`, not `jv.id`.
3. In approved FINA forms, filter FINA JV by `JV.jvid`.
4. In FINA JV header-to-detail paths, use `JV.jvid.jvid.JVDET.<field>`.
5. In local Biz-A cross-reference queries, use `JV.jvid_fina` to find the local row and use `JV.id` only for Biz-A columns.
6. Avoid broad replace operations for `JV.ID` or `jv.id`; change only the path whose database boundary is known.

## What To Avoid

- Do not use `JV.ID` in a `queryData` call whose `dbIndex` is `config.api.finaDbIndex`.
- Do not change local Biz-A `JV.ID` paths to `JV.JVID` just because the target flow is FINA-backed.
- Do not pass a local Biz-A `id` from a FINA approved list into a form that loads by FINA `JVID`.
- Do not rely on casing differences (`JV.ID` vs `JV.id`) to decide the database; check the actual `dbIndex`.

## Related Files And Patterns

- `APL/otherPaymentListApproved.js`
- `APL/otherPaymentFormApproved.js`
- `APL/otherReceiptListApproved.js`
- `APL/otherReceiptFormApproved.js`
- `.agents/references/rename-used-column-rules.md`
- `.agents/references/biz-a-query-join-depth-problem.md`
