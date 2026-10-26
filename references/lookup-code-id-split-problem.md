# Lookup Code and ID Split Problem

Use this reference when a master lookup table changes from using a business code as `ID` to using an internal integer `ID`, with the old code moved to a separate column such as `CODE`.

## Problem Signal

- A migration changes a lookup/master table from `ID VARCHAR` to `ID INTEGER`, and adds `CODE VARCHAR`.
- Existing child tables keep columns such as `BRANCH_ID`, but those columns now store integer IDs instead of old codes like `BA`, `BE`, or `JKT`.
- Forms still display, generate numbers, or print using `branch_id`, causing document numbers to contain `10` instead of `BA`.
- `queryData` paths still use `branch_id.id.branch.id` as the branch code.
- Lookup config still searches by `id` even though users know the business code.
- Firebird validation errors appear during migration after `RDB$RELATION_FIELDS` was updated too broadly, for example an optional column suddenly behaves as `NOT NULL`.

## Root Cause

The old schema used one field for two meanings:

- `ID` was the database key and also the business code shown to users.
- Child FK columns such as `BRANCH_ID` stored that same business code.

After the migration, those meanings are split:

- `ID` is an internal integer primary key and FK target.
- `CODE` is the old business code for display, search, print, and document numbering.
- Optional compatibility/display fields such as `BRC` may still exist, but should not replace `CODE` as the primary business-code source.

If code is only adjusted at the database layer, Biz-A forms keep mixing FK values with business codes.

## Corrected Approach

Treat the change as two separate contracts.

Database contract:

```sql
BRANCH.ID   INTEGER NOT NULL PRIMARY KEY
BRANCH.CODE VARCHAR(20) NOT NULL UNIQUE
CHILD.BRANCH_ID INTEGER REFERENCES BRANCH(ID)
```

Program contract:

```javascript
// Stored FK / navigation / delete / relation paths
branch_id: row.branch_id       // integer

// User-facing code / document number / print display
branch_brc: row.branch_code || row.branch_brc
```

Lookup config should keep `key: 'id'`, but display/search by business code:

```javascript
lookupOptions: {
    table: 'branch',
    key: 'id',
    display: `(code || ' - ' || name)`,
    searchDisplay: `(code || ' - ' || name)`,
    searchKey: ['code', 'brc', 'name'],
}
```

`queryData` paths should distinguish FK and code:

```javascript
{ data: 'spr.branch_id', key: 'branch_id' }
{ data: 'spr.branch_id.id.branch.code', key: 'branch_brc' }
{ data: 'spr.branch_id.id.branch.name', key: 'branch_name' }
```

## Migration Checklist

- Drop FK constraints and triggers that depend on the old business-code `ID`.
- Create a mapping table from old code to new integer ID before dropping the old `ID`.
- Add `CODE`, copy old `ID` into it, then replace `ID` with the integer column.
- Convert every child `BRANCH_ID` from old code to new integer through the mapping table.
- Recreate FK constraints against `BRANCH(ID)`.
- Add `UNIQUE (CODE)` and make only truly required fields `NOT NULL`.
- If using `RDB$RELATION_FIELDS` to force `NOT NULL`, always include both `RDB$RELATION_NAME` and `RDB$FIELD_NAME` in the same statement.

Do not run this without `WHERE`:

```sql
UPDATE RDB$RELATION_FIELDS
SET RDB$NULL_FLAG = 1;
```

Use a scoped update:

```sql
UPDATE RDB$RELATION_FIELDS
SET RDB$NULL_FLAG = 1
WHERE RDB$RELATION_NAME = 'BRANCH'
  AND RDB$FIELD_NAME = 'CODE';
```

If an unscoped metadata update already ran, repair optional fields before updating table rows:

```sql
UPDATE RDB$RELATION_FIELDS
SET RDB$NULL_FLAG = NULL
WHERE RDB$RELATION_NAME = 'BRANCH'
  AND RDB$FIELD_NAME NOT IN ('ID', 'CODE');
```

## Biz-A Implementation Checklist

- Add `code` to master form model, load query, and save payload.
- Do not render internal PK `id` as an editable form field.
- Keep list action columns on `table.id`, but display code columns from `table.code`.
- Change lookup `searchDisplay` and `searchKey` from `id/name` to `code/brc/name`.
- Change relation paths used as display codes from `...branch.id` or `...branch.brc` to `...branch.code`.
- Keep `branch_id` numeric in payloads and filters when the input is numeric; avoid quoting numeric FK values.
- For document numbers, print headers, and display labels, use `branch_brc` loaded from `branch.code`, not `branch_id`.
- Update any code paths that assumed `branch_id` was a string code.

## What To Avoid

- Do not use `branch_id` as a fallback for document code after the migration; it is now an integer.
- Do not change lookup `key` from `id` to `code` unless the stored FK column also changes to code.
- Do not leave `branch_id.id.branch.id` paths for display code.
- Do not blindly replace every `brc` with `code`; local fields may still be named `branch_brc`, but their source should be `branch.code`.
- Do not quote numeric FK filters as string literals.

## Related Files And Patterns

- `.agents/references/rename-used-column-rules.md`
- `.agents/references/database-standard-rules.md`
- `.agents/references/pk-field-config.md`
- `BERCA/sql/18 JUNI 2026 migrate branch id to integer code.sql`
- `BERCA/branchForm.js`
- `BERCA/branchList.js`
- `BERCA/lib_qry.js`
