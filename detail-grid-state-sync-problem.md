# Detail Grid State Sync Problem

Use this reference when a Biz-A form detail-grid shows stale rows after the model or form value already changed, especially after add/delete actions or when several conditional grids share the same `detailKey`.

## Problem Signal

- User deletes a detail-grid row and no runtime error appears, but the row remains visible.
- Console inspection shows `model.<detailKey>` or `form.value.<detailKey>` is empty or already updated, while the grid still renders old rows.
- Clicking a custom grid delete button throws `Cannot read properties of undefined (reading 'map')`, `removeAt`, `controls`, or `dataSubject`.
- A form has several `detail-grid` fields with the same `props.detailKey` and conditional `expressions.hide`.
- A cached grid reference such as `this.gridItems` is assigned before mode, status, category, or loaded data has selected the visible grid.

## Root Cause

Biz-A `detail-grid` maintains its own rendered datasource. Updating `this.model.<detailKey>` alone does not always refresh the rendered grid rows after the grid instance has been created.

This becomes more likely when a form declares multiple conditional grids for the same detail data. A cached reference can point to a hidden or stale grid instance, while the user is interacting with another grid that has the same `detailKey`.

Directly mutating internal datasource structures such as `grid.datasource.controls.removeAt(...)` or reading `grid.datasource.dataSubject.getValue().map(...)` couples the form to implementation details that are not stable across grid states.

## Correct Pattern

Keep the model as the source of truth, then push the updated array into the active detail-grid instance with `assignData`.

For forms with multiple conditional grids for the same detail data:

- collect grid instances from `this.fields` by matching `type: 'detail-grid'` and `props.detailKey`,
- include the cached grid reference only as one candidate,
- de-duplicate grid instances,
- call `grid.assignData({ data: rows })` for every matching grid instance,
- avoid `datasource.controls.removeAt(...)` for custom delete buttons.

Short example:

```javascript
getDetailGridsByKey: function (detailKey) {
    const grids = [];
    const addGrid = (grid) => {
        if (grid?.assignData && !grids.includes(grid)) {
            grids.push(grid);
        }
    };

    addGrid(this.gridItems);

    const fields = Array.isArray(this.fields) ? this.fields : [];
    fields.forEach((field) => {
        if (field?.type !== 'detail-grid') return;
        if (field?.props?.detailKey !== detailKey) return;

        const refs = Array.isArray(field._componentRefs) ? field._componentRefs : [];
        const grid = refs[0]?.instance?.grid;
        addGrid(grid);
    });

    return grids;
},
```

## Implementation Checklist

- Identify the detail key that owns the rows, for example `unit_items`, `details`, or `sidet`.
- Normalize the source rows with `Array.isArray(...) ? rows : []` before calling `.filter`, `.map`, or `.some`.
- Update the model array first, for example `this.model.unit_items = nextRows`.
- Preserve delete metadata used by save flow, such as marking the original row with `{ delete: 1 }` when existing detail rows must be deleted later.
- Refresh the rendered grid through `assignData({ data: nextRows })`.
- If multiple conditional grids share the same `detailKey`, sync every matching grid instance instead of trusting one cached reference.
- Do not update repeat/detail data by `this.form.get(detailKey).setValue(...)`.
- Do not depend on `grid.datasource.controls`, `grid.datasource.dataSubject`, or `removeAt` for form-owned custom row actions.

## Related Files And Patterns

- `.github/doc/patterns.md` Section 10: Detail Grid Pattern.
- `.github/instructions/references/form-rules.md`.
- `.github/instructions/references/error-reference.md` for repeat/detail data assignment pitfalls.
- Example fixed module: `BERCA/contractForm.js` custom `unit_items` delete flow.
