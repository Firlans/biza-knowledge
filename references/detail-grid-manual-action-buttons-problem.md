# Detail Grid Manual Action Buttons Problem

Use this reference when a Biz-A `detail-grid` Add or Delete button stays visible even after `props.addBtn.show`, `props.deleteBtn.show`, or expressions were changed.

## Problem Signal

- A form opened in view, approve, or from-bankbook mode still shows an Add button or row delete action.
- Setting `detailGrid.props.deleteBtn.show = false` does not hide the visible delete button.
- The detail-grid has a custom `Action` column with `buttons: [...]`.
- The user asks to control Add/Delete visibility manually instead of through detail-grid `props`.

## Root Cause

Biz-A detail-grid can expose two different button mechanisms:

- internal grid controls configured through `props.addBtn` and `props.deleteBtn`,
- custom row actions configured through a column such as `{ label: 'Action', buttons: [...] }`.

Changing `props.deleteBtn.show` only affects the internal delete control. It does not hide a custom row button in `columns[].buttons`.

For Add, some detail-grid implementations cache or render `props.addBtn` before later `show` changes are applied. When visibility must be predictable by mode, use a normal form `type: 'button'` and call a named handler such as `onClickAddDetail`.

## Corrected Approach

Prefer manual Add/Delete controls when visibility must follow module-specific modes.

For Add:

```javascript
{
    type: 'button',
    props: {
        text: 'Add',
        icon: 'add',
        onClick: function () {
            this.doFunction('onClickAddDetail');
        },
    },
    expressions: { hide: 'model.viewMode == true || model.approveMode == true || model.fromBankBookMode == true' },
}
```

For the handler:

```javascript
onClickAddDetail: function () {
    this.grid.newRow({});
},
```

For Delete:

```javascript
beforeLoadData: function () {
    const detailGridField = this.fields.find(field => field.type === 'detail-grid');
    const mode = this.route?.snapshot?.queryParams?.mode;
    const isFromBankBookMode = this.model.fromBankBookMode == true || mode === 'from_bankbook';
    const showDetailActions = this.model.viewMode != true && this.model.approveMode != true && isFromBankBookMode != true;
    const actionColumn = detailGridField.props.columns.find(column => column.label === 'Action');

    actionColumn.buttons = showDetailActions ? actionColumn.buttons : [];
},
```

Remove `props.addBtn` and `props.deleteBtn` from the detail-grid when the form uses manual Add/Delete controls. Mixing internal and manual controls makes visibility hard to reason about.

## Implementation Checklist

- Identify whether the visible delete control comes from `props.deleteBtn` or `columns[].buttons`.
- If delete is a custom Action column, hide it by setting that column's `buttons` to `[]`.
- If Add visibility is unreliable through `props.addBtn`, remove `props.addBtn` and create a normal form button.
- Keep the Add button's `onClick` short and route it to a named handler.
- If `beforeLoadData` runs before `onInit`, read route mode directly from `this.route?.snapshot?.queryParams?.mode` instead of trusting `this.model.fromBankBookMode`.
- Do not use `structuredClone` on fields, columns, or button configs because they contain functions.

## Related Files And Patterns

- `.agents/references/patterns.md` Section 10: Detail Grid Pattern.
- `.agents/references/detail-grid-state-sync-problem.md` for stale grid state after custom add/delete actions.
- `.agents/references/form-rules.md`.
- Example local modules: `APL/otherReceiptForm.js`, `APL/otherPaymentForm.js`.
