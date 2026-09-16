# Firebird Generator Rename Problem

Use this reference when changing Biz-A generator/sequence names, especially from non-standard names like `GEN_<TABLE>_ID` or `<TABLE>_ID_GEN` to `<TABLE>_GEN`.

## Problem Signal

- Firebird returns:

```text
SQL Message : -607
This operation is not defined for system tables.
unsuccessful metadata update
cannot delete
GENERATOR <OLD_GENERATOR>
there are 1 dependencies
```

- A rename script creates the new generator and updates a trigger, but `DROP GENERATOR <OLD_GENERATOR>` still fails.
- The table still inserts with the old generator or both old and new triggers exist.

## Root Cause

Firebird does not rename generators directly. Migration usually creates a new generator, copies the current value, updates dependent triggers, then drops the old generator.

The drop fails when an existing database object still references the old generator. The most common mistake is using a guessed trigger name in `CREATE OR ALTER TRIGGER`. If the real trigger has a different name, Firebird creates or alters the wrong trigger and keeps the original trigger dependency on the old generator.

## Corrected Approach

Always inspect dependencies before dropping the old generator.

```sql
SELECT
    TRIM(RDB$DEPENDENT_NAME) AS DEPENDENT_NAME,
    RDB$DEPENDENT_TYPE
FROM RDB$DEPENDENCIES
WHERE TRIM(RDB$DEPENDED_ON_NAME) = '<OLD_GENERATOR>';
```

Use the returned `DEPENDENT_NAME` as the trigger name in the migration script. Do not assume names like `TRG_<TABLE>_BI` or `<TABLE>_BI`.

## Migration Template

```sql
SET TERM ^ ;

CREATE GENERATOR <TABLE>_GEN ^

EXECUTE BLOCK AS
DECLARE OLD_VAL BIGINT;
BEGIN
    OLD_VAL = GEN_ID(<OLD_GENERATOR>, 0);
    OLD_VAL = GEN_ID(<TABLE>_GEN, :OLD_VAL);
END ^

CREATE OR ALTER TRIGGER <DEPENDENT_TRIGGER_NAME> FOR <TABLE>
ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
    IF (NEW.ID IS NULL) THEN
        NEW.ID = GEN_ID(<TABLE>_GEN, 1);
END ^

DROP GENERATOR <OLD_GENERATOR> ^

SET TERM ; ^
```

If the existing trigger has other defaults or business logic, copy the full trigger body and only replace the generator expression. Do not reduce the trigger to ID assignment only.

## Implementation Checklist

- Query `RDB$DEPENDENCIES` for the old generator before writing the final `DROP GENERATOR`.
- Use the exact dependent trigger name from the database.
- Preserve the old generator value with `GEN_ID(<OLD>, 0)` before changing inserts.
- Preserve all existing trigger behavior, including timestamps, status defaults, quantity defaults, and update-side logic.
- Run the dependency query again after altering the trigger; it should return no rows for the old generator.
- Only then run `DROP GENERATOR <OLD_GENERATOR>`.
- Update Biz-A JavaScript `dataService.genId(...)` calls to the new `<TABLE>_GEN` name if the app prefetches IDs.

## Related Files

- `.github/instructions/references/rename-used-column-rules.md`
- `.github/instructions/references/error-reference.md`
