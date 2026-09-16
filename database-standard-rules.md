# Biz-A Database Standard Rules

Use this reference when creating or changing Biz-A database tables, Firebird DDL, migrations, generators, triggers, or primary keys.

## Mandatory Naming

- Table primary key must use Table ID as the PK column: `ID`.
- Generator name must follow the table name: `<TABLE>_GEN`.
- Before-insert trigger name must follow the table name: `<TABLE>_BI`.
- After-insert trigger name must follow the table name: `<TABLE>_AI`.

Use the real table name consistently. If the database stores object names in uppercase, write the generated object names in uppercase too.

## Trigger Timing

- `<TABLE>_BI` means `BEFORE INSERT`.
- `<TABLE>_AI` means `AFTER INSERT`.
- Put ID generation in the `BEFORE INSERT` trigger unless an existing module has a stronger local pattern.

## Standard Table Skeleton

```sql
CREATE TABLE <TABLE> (
    ID INTEGER NOT NULL,
    -- other columns here
    CONSTRAINT PK_<TABLE> PRIMARY KEY (ID)
);

CREATE GENERATOR <TABLE>_GEN;

SET TERM ^ ;

CREATE OR ALTER TRIGGER <TABLE>_BI FOR <TABLE>
ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
    IF (NEW.ID IS NULL) THEN
        NEW.ID = GEN_ID(<TABLE>_GEN, 1);
END ^

SET TERM ; ^
```

Only create `<TABLE>_AI` when there is actual after-insert work to do. Do not create empty triggers.

## Implementation Checklist

- Use `ID` as the table primary key column.
- Name the primary key constraint `PK_<TABLE>` unless the target schema already has a stricter convention.
- Name the generator `<TABLE>_GEN`.
- Name insert triggers `<TABLE>_BI` and `<TABLE>_AI` according to their timing.
- Keep Biz-A JavaScript `dataService.genId(...)`, `sendModel`, relation paths, and list action keys aligned with the `ID` primary key.
- For renaming an existing generator or used primary key, also load the related dependency references below.

## Related Files

- `.github/instructions/references/firebird-generator-rename-problem.md`
- `.github/instructions/references/rename-used-column-rules.md`
- `.github/instructions/references/pk-field-config.md`
