# Rename Used Column Rules

Use this reference when a database column must be renamed after it is already used by another table, foreign key, primary key, trigger, query path, list action column, or Biz-A save payload.

## Problem Signal

- A column rename is requested for a field that appears in relation paths, for example `SO.SOID` to `SO.ID`.
- Another table still keeps a foreign key column with the old name, for example `SODET.SOID`.
- Save/update still sends the old primary key field, for example `{ soid: value }`, while the table now expects `{ id: value }`.
- Queries fail after rename with relation/field errors, constraint errors, or old Biz-A path strings.
- Firebird refuses `ALTER TABLE <TABLE> ALTER <OLD_FIELD> TO <NEW_FIELD>` with a dependency error such as `Column <OLD_FIELD> from table <TABLE> is referenced in <TRIGGER_NAME>`.
- Firebird verification queries fail with `Column unknown` because the wrong system table was used, for example selecting `RDB$TRIGGER_NAME` from `RDB$RELATION_FIELDS`.

## Root Cause

Renaming only the physical column is not enough. Biz-A uses the column in several layers:

- database constraints: primary key, foreign key, and status/reference constraints
- triggers and generators: `NEW.<field>` must match the new column
- queryData paths: header paths and header-to-detail relation paths must match the new PK
- list action rows: the action column and selected row lookup key must match the new queryData result
- save payloads: master table update payload must use the table primary key field expected by `sendModel`
- detail payloads: detail FK fields may intentionally keep the old column name if the detail table column was not renamed

## Corrected Approach

Do the rename in two layers: database first, then Biz-A code.

Database migration order:

1. Identify all constraints that depend on the column.
2. Drop dependent foreign keys first.
3. Drop or replace triggers, procedures, or computed dependencies that still reference the old field.
4. Drop or replace the primary key constraint if the renamed column is the PK.
5. Rename the column.
6. Recreate the primary key on the new column.
7. Recreate foreign keys so related tables point to the new column.
8. Recreate triggers to use `NEW.<new_column>`.
9. If the table may be rebuilt from scratch, add a separate "create ulang" section with the final schema, not only a rename patch.

Firebird 2.5 dependency order:

1. Query `RDB$REF_CONSTRAINTS`, `RDB$RELATION_CONSTRAINTS`, and `RDB$INDEX_SEGMENTS` to find all FK constraints whose parent field is the old PK.
2. Query `RDB$DEPENDENCIES` for the old field before renaming.
3. Drop all FK constraints that reference the old field.
4. Drop triggers that reference `NEW.<old_field>` or `OLD.<old_field>`; do not rely on changing them to no-op in the same migration transaction.
5. Drop the old PK constraint.
6. Rename the field.
7. Recreate PK, FK, and triggers against the new field.

Biz-A code order:

1. Change Biz-A `queryData` paths for the renamed table column.
2. Change header-to-detail relation paths to use the new PK twice when required by Biz-A relation syntax.
3. Change list action column and row lookup keys.
4. Change master `sendModel` payloads to use the renamed PK field.
5. Keep detail FK payloads unchanged when the detail table column was not renamed.
6. Do not rename FINA fields or report parameters unless the FINA database changed too.

## Implementation Checklist

- Search exact old path first:

```powershell
rg -n "SO\.SOID|SOID|soid:" "Endo Medika"
```

- For Biz-A local SO rename from `SO.SOID` to `SO.ID`, use these patterns:

```javascript
// Query Biz-A header
{ data: 'SO.ID', key: 'soid' }

// Query Biz-A header-to-detail relation
{ data: 'SO.ID.ID.SODET.ITEMNO', key: 'itemno' }

// List action column
{ title: 'Action', data: 'SO.ID' }

// Master save/update payload
{ id: model.soid || null, status: model.status }

// Detail payload stays on detail FK if SODET.SOID still exists
{ soid: model.soid, itemno: detail.itemno }
```

- For Firebird migrations, avoid renaming while constraints still depend on the old field:

```sql
ALTER TABLE SODET DROP CONSTRAINT FK_SODET_SO;
DROP TRIGGER SO_BI;
ALTER TABLE SO DROP CONSTRAINT PK_SO;
ALTER TABLE SO ALTER SOID TO ID;
ALTER TABLE SO ADD CONSTRAINT PK_SO PRIMARY KEY (ID);
ALTER TABLE SODET ADD CONSTRAINT FK_SODET_SO
FOREIGN KEY (SOID) REFERENCES SO (ID) ON DELETE CASCADE;
```

- Recreate the trigger after the column has been renamed:

```sql
CREATE OR ALTER TRIGGER SO_BI FOR SO ACTIVE BEFORE INSERT POSITION 0 AS
BEGIN
    IF (NEW.ID IS NULL) THEN
        NEW.ID = GEN_ID(SO_GEN, 1);
END
```

- For Firebird verification queries, use the correct system tables:

```sql
SELECT
    RF.RDB$FIELD_NAME AS FIELD_NAME,
    RF.RDB$FIELD_POSITION AS FIELD_POSITION
FROM RDB$RELATION_FIELDS RF
WHERE RF.RDB$RELATION_NAME = 'SO'
ORDER BY RF.RDB$FIELD_POSITION;

SELECT
    T.RDB$TRIGGER_NAME AS TRIGGER_NAME,
    T.RDB$RELATION_NAME AS TABLE_NAME,
    T.RDB$TRIGGER_INACTIVE AS TRIGGER_INACTIVE
FROM RDB$TRIGGERS T
WHERE T.RDB$RELATION_NAME = 'SO'
  AND T.RDB$TRIGGER_NAME = 'SO_BI';
```

## What To Avoid

- Do not blindly replace every `SOID` or `soid`.
- Do not change detail FK fields if the detail table column remains `SOID`.
- Do not change FINA paths such as `SO.SOID`, `ARINVDET.SOID`, FINA report `keyfield: 'SOID'`, or dictionary parameter `SOID` unless the FINA schema also changed.
- Do not send both `{ soid: value, id: value }` in the master payload unless the target table genuinely has both columns.
- Do not place the rename and "create ulang" scripts without comments; future agents must know which section is for migration and which section is for rebuild.
- Do not select trigger metadata from `RDB$RELATION_FIELDS`; trigger metadata belongs in `RDB$TRIGGERS`, while table columns belong in `RDB$RELATION_FIELDS`.
- Do not assume `CREATE OR ALTER TRIGGER` removes an old field dependency before a rename in Firebird 2.5; drop the trigger before renaming the field, then recreate it.

## Related Files And Patterns

- `Endo Medika/migrate/15 JUNI 2026 rename SO SOID to ID.sql`
- `Endo Medika/lib_qry.js`
- `Endo Medika/SOList.js`
- `Endo Medika/SOForm.js`
- `APL/migrate/17 JUNI 2026.sql`
- `.github/instructions/references/pk-field-config.md`
- `.github/instructions/references/biz-a-query-join-depth-problem.md`
