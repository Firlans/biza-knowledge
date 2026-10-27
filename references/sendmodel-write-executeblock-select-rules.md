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
