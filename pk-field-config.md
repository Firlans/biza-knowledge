# Primary Key Field Configuration — Firlan Style

Manage primary key fields correctly to avoid "token unknown" form loading errors.

## Rule

**Primary key fields must exist in the `model` object but must NEVER appear in the `fields` or `fieldGroup` array.**

## Why

Primary key fields are auto-generated or managed by the backend database. Rendering them as form controls in Formly violates Biz-A architecture because:
1. Primary keys are read-only after creation
2. Backend manages them exclusively
3. Adding to fieldGroup instructs Formly to create editable controls → invalid form tokens → parsing error

## Primary Key Field Types

Identify primary key fields:
- `id` — single-table primary key
- `header_id`, `master_id` — parent reference for detail forms
- `record_id`, `entity_id` — any database primary key alias
- `line_number`, `item_no` — sequential/composite keys in detail grids

## Pattern: How to Handle

### Step 1: Declare in model
```javascript
model: {
    id: null,              // ✅ Required for internal use
    header_id: null,       // ✅ Parent reference for detail forms
    part_number: null,
    description: null,
    details: [],
}
```

### Step 2: Exclude from fieldGroup
```javascript
fields: [
    // { key: 'id' },  // ✅ Commented out to prevent rendering
    
    {
        fieldGroupClassName: 'row',
        fieldGroup: [
            {
                className: 'col-12 col-md-6',
                key: 'part_number',
                type: 'input',
                props: {
                    label: 'Part Number',
                    required: true,
                },
            },
            // Do NOT add id, header_id, or any primary key field here
        ],
    },
]
```

### Step 3: Manage via code
```javascript
loadData: function (id) {
    // Fetch from backend using id
    return dataService.queryData({ id }, this.config, true);
},

saveData: function (model) {
    if (!model.id) {
        // New record: generate id via genId
        model.id = dataService.genId('GEN_TABLE_ID', bizaConfig);
    }
    // Backend receives id for updates; UI never edits it
    return dataService.sendModel(buildPayload(model), this.config, 'TABLE_NAME');
},

applyToModel: function (row) {
    // Read id from database result, assign to model.id
    this.model.id = row?.id ?? null;
    // Other fields are bound via fieldGroup
    this.model.part_number = row?.part_number;
    this.model.description = row?.description;
}
```

## Error Diagnosis

### Symptom
```
SyntaxError: Invalid form control token
Form failed to load
Form not rendering
```

### Root Cause Check
```javascript
// ❌ Bad: id in fieldGroup
fields: [
    { key: 'id', type: 'input' },        // This causes the error
    { key: 'part_number', type: 'input' },
]

// ✅ Good: id commented out
fields: [
    // { key: 'id' },
    { key: 'part_number', type: 'input' },
]
```

### Fix
1. Search the form file for `{ key: 'id'` in the `fields` array
2. If found in fieldGroup, comment it out
3. Ensure `model.id` is still declared
4. Reload the form—error should be gone

## Code Review Checklist

When reviewing a Biz-A form:
- [ ] Primary key field exists in `model`
- [ ] Primary key field is **not** in `fields` or `fieldGroup`
- [ ] Primary key is commented out (if historically present)
- [ ] All other fields in `fieldGroup` are non-primary-key attributes
- [ ] Primary key is assigned in `applyToModel` or similar initialization
- [ ] Primary key is generated via `genId()` for new records before saving

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding `{ key: 'id' }` to fields | Remove or comment out the field |
| Forgetting `id` in model entirely | Add `id: null` to the model object |
| Trying to make id read-only with `readonly: true` | Remove id field entirely; manage via code |
| Nesting id inside fieldGroup array | Move outside or comment out completely |
| Rendering composite key fields | Only manage parent key in model; detail keys via hidden logic |

## Related Rules

- **biz-a-rules**: "Primary key fields must NOT be rendered in form fields"
- **Form Rules**: "key: 'id' only for hidden internal identifier"
- **Lifecycle**: Primary key assignment in `applyToModel` or `setDbIndex`

## When to Apply This Rule

- Creating a new Biz-A form
- Debugging "token unknown" form loading errors
- Code reviewing Biz-A form configurations
- Migrating forms from other patterns to Biz-A
- Training developers on Biz-A form conventions
