# List Action Button Wrap Problem

Use this reference when a Biz-A list has many row action buttons and the user reports that the buttons overlap, collide, clip, or "tumpang tindih".

## Problem Signal

- A list column titled `Action` contains several buttons with long captions.
- The user asks to fix button layout, not to change the action grouping or authorization model.
- The list uses `lib_authorization.setActionByCustomPrivilege`, `setAction`, or `setActionUsingKey`.
- Code expects `this.columns.find(col => col.title === 'Action').button` to contain all action buttons.

## Root Cause

Dense action buttons can exceed the default cell width. A tempting fix is to split buttons into multiple action columns such as `Action`, `Print`, and `Approval Print`, but that changes the list contract.

Biz-A authorization helpers commonly locate only the `Action` or `Otorisasi` column. Splitting buttons into new columns can silently bypass or break privilege filtering, and it changes the UI shape when the user only asked for layout wrapping.

## Correct Pattern

Keep all existing action buttons in the original action column unless the user explicitly asks for separate columns.

For layout-only overlap fixes:

- Add local wrapping style on the existing `Action` column.
- Add button-level style for wrapping and small spacing if the renderer supports per-button style.
- Preserve button `id`, `caption`, `icon`, `color`, and `onClick`.
- Preserve the existing authorization path; do not add custom privilege filtering helpers just because of a visual issue.

Example:

```javascript
{
    title: 'Action',
    data: 'workshop_sales.id',
    style: {
        'white-space': 'normal',
        'min-width': '360px',
    },
    button: [
        {
            id: 'print picklist',
            caption: 'Print Picklist',
            icon: 'print',
            color: 'accent',
            onClick: 'printPicklistClicked',
            style: {
                'white-space': 'normal',
                margin: '2px',
            },
        },
    ],
}
```

## Implementation Checklist

- Confirm whether the user wants a visual wrap fix or a structural regrouping of actions.
- Search for existing code that reads the `Action` column directly.
- Keep the action buttons in one `Action` column for wrap-only requests.
- Add style locally to the column and buttons; avoid broad CSS or global renderer changes.
- Do not alter navigation handlers, print handlers, approval handlers, or payload logic.
- Do not add custom privilege filtering if the standard helper already filters the single `Action` column.

## Related Files And Patterns

- `.agents/references/list-rules.md`
- `BERCA/workshopSalesList.js` shows the corrected pattern for dense Workshop Sales row actions.
