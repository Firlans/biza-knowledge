# FINA json2fina, Biz-A sendModel, And executeBlock SELECT Only

## Problem signal

Adding master records or saving table rows through an `executeBlock` containing INSERT, UPDATE, DELETE, or a procedure with write side effects. Also applies to FINA writes incorrectly routed through `sendModel`, including `Column unknown ID` when adding a driver to `EXTENDEDDET`.

## Root cause

A SQL block can execute successfully while still violating the Biz-A application standard. A passing database fixture does not establish that the write mechanism is correct. The Biz-A ORM assumes an `ID` column; FINA tables can use different keys such as `EXTENDEDDETID`. Sending FINA records through `sendModel` can therefore produce `Column unknown ID`.

## Correct approach

- Use `dataService.sendModel(payload, api, tableName)` for adding/saving records in the Biz-A database. Validate `response.error` before reporting success.
- Use `dataService.json2fina(payload, api)` for adding/saving FINA data, including master lookups. Validate both `response.error` and `response.result?.[0]?.error` before success. Never use `sendModel` to write to FINA.
- For new FINA records, use the correct dataset, `id: -1`, `userId`, `dbIndex: finaDbIndex`, and `data.master`. Let the FINA dataset manage native IDs and GUIDs. Validate the returned ID if subsequent behavior needs a saved record.
- Allocate Biz-A IDs with `dataService.genId(generatorName, api)` when required by the existing table.
- Use `queryData` for ordinary reads and duplicate checks. Use `executeBlock` only for SELECT/read-only queries.
- Do not hide data changes or generator increments inside a SELECT or a stored procedure called by `executeBlock`.
- Use the established delete API for deletion. Existing FINA integrations using `fml2fina` keep their native API. Do not replace them with SQL mutations.

## Successful SELECT with no rows

A Biz-A `dataService.executeBlock` SELECT can return `{"success":"OK"}` without
`data` when the query finds no rows. A guard that requires an array before
checking the success marker will report a false query failure.

- Check for a response error before using the result. Treat the observed
  success response with an omitted `data` field as an empty row list.
  Preserve arrays as returned. Keep reporting unexpected shapes and errors.
- Apply the business default after reading the rows. In the Spiritia Journal
  Voucher budget check, an empty budget result gives the selected project and
  department a zero budget.
- Test the exact success response without `data`, an ordinary result with
  rows, and a response with `error` even when it also reports success.

The API trace and Submit regression were verified in
[Spiritia's budget query](../../Spiritia/Trunk/lib_qry.js) and
[its working-day and budget tests](../../Spiritia/Trunk/tests/journalVoucherWorkingDays.test.js).

## Local FINA report transport

For a report that posts read-only SQL directly to the FINA block URL and needs
to use a local FINA service, pass the SQL to `dataService.executeBlock` with a
request-scoped copy of `this.config.api`. Override `url` with the deployment's
FINA endpoint, such as `http://localhost:212`, set `subdomain` to an empty
string for the direct endpoint, and set `dbIndex` to the application's FINA
index. Keep using the original Biz-A configuration for audit writes and
Biz-A budget reads. See the [ASATA query helper](../../Asata/trunk/lib_qry.js)
and [Spiritia TB USD](../../Spiritia/v2/reportTBUSD2.js).

For a report built from several blocks, pair each SQL statement with the result
key the renderer expects. Follow the existing sequential pipeline with
`concatMap` and check each response before running the next block. Spiritia
Forex uses distinct keys for `saldousd` and `total2`, which come from different
SQL statements. Check View and Export, the order and names of the result sets,
loading cleanup, and the connection used for the audit or budget. Update the
expected endpoint in the tests when a deployment changes the report endpoint.
See [Spiritia Forex](../../Spiritia/v2/reportForex2.js) and
[the local variance report tests](../../Spiritia/v2/tests/report5Local.test.js).

In Spiritia #6812, the report had a recorded HTTP 408 and direct browser POST
was flagged as a CORS risk. Read-only requests to the local API returned data.
Some blocks exceeded the test time limit when run concurrently, while the
first Forex and SUF blocks returned rows on sequential retries. When a block
times out, replay the same SQL individually to measure its execution. Verify
browser access from the target tenant separately.

## Driver lookup example

`Proton/SOForm.js` calls `saveJobOrderDriver` in `Proton/lib_qry.js`. Read duplicates from FINA `EXTENDEDDET` with `EXTENDEDTYPEID = 3`, then save through `json2fina` with `dataModule: 'TExtendedDetDataset'`, `transType: ''`, and `data.master: { extendedtypeid: 3, info1: driverName, info2: driverName }`. The lookup and JO `ITEMRESERVED4` continue to use the driver name from `INFO2`.

## Implementation checklist

- Separate duplicate lookup, payload mapping, and the appropriate save API for the target database.
- Point all calls at the intended database configuration.
- Keep user text unchanged in JSON payloads; escape only SQL filter text.
- Test duplicate reuse, payload/target, error propagation, and absence of executeBlock writes. For FINA saves, verify `json2fina` is called and `sendModel` is not.
- Distinguish mocked service verification from a live API save.

## Related files

- `patterns.md`, sections 5, 6, and 14.
- `helper-rules.md`.
- `Proton/lib_qry.js`: `saveJobOrderDriver`.
