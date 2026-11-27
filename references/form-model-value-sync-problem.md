# Form And Model Value Sync Problem

Use this reference when a Biz-A form loses recent user input after a dialog,
step change, lookup selection, repeat update, or detail-grid refresh. It also
covers a form that loses saved values while opening an existing record.

## Problem Signal

- A user finishes editing a field or detail-grid, then another action makes the
  value disappear or revert.
- `this.form.value` contains the latest value while `this.model` is stale.
- A handler spreads or clones `this.model` and unintentionally restores old
  values over controls that the user already edited.
- View or Edit opens with blank fields or detail rows even though the initial
  query returned the saved record.

## Root Cause

In an active Biz-A form, Formly controls can hold newer values than
`this.model`. Treating `this.model` alone as the current form state discards
those control values when the model is replaced or cloned.

The spread order is significant. Current form values must override stale model
values, while model-only and disabled-field values must still be preserved.

## Correct Pattern

Before validating, mapping, cloning, or replacing active form state, build one
synchronized snapshot in this order:

```javascript
const currentModel = {
    ...this.model,
    ...this.form.value,
};
```

Apply the intended change to that snapshot:

```javascript
this.model = structuredClone({
    ...currentModel,
    tnc_points: nextTncPoints,
});
```

Do not reverse the spread order:

```javascript
// Wrong: stale model values overwrite current form values.
const currentModel = {
    ...this.form.value,
    ...this.model,
};
```

`this.form.value` may omit disabled controls, so always spread `this.model`
first. This retains model-only values and lets active form controls override
only the keys they currently own.

## Initial load of an existing record

While controls still hold their initial values, build the model from the query
result and include derived rows such as the attachment list in the same
assignment. A refresh helper that snapshots `this.form.value` at this point can
copy `null` or `[]` over saved header fields and detail rows. Apply the loaded
lookup values and use `assignData` on the detail-grid before installing listeners
that react to these fields. Use the active-form snapshot once the controls hold
the current edits.

In the Missi Idea PO Client regression tests, both View and Edit start with
empty control values while the mocked query returns saved data. The tests check
the loaded header, selected lookup IDs, grid rows, and attachment list.
[PO Client form](<../../Missi Idea/poClientForm.js>)
[Regression tests](<../../Missi Idea/tests/poClientAttachments.test.js>)

## Refresh derived fields after an async response

If a loading message stays visible after a read has populated the model, check
when Formly evaluates the expressions for the affected fields. The Biz-A build
observed in Spiritia uses `checkExpressionOn: "modelChange"`. Changes emitted by
form controls trigger evaluation. Direct model mutations from a separate API
callback can leave `hide` and `props.url` expressions showing their old values.

Update the existing model properties, then call `field.options.detectChanges(field)`
on the populated Formly field or group that owns those expressions. Handle both
the success and failure displays. This preserves the active controls and their
unsaved values. A response that arrives before Formly builds the fields supplies
their initial model state.

Test a delayed response after the loading state has rendered. Verify the image
or error appears before any click, keystroke, or control change. A fixture that
automatically renders every model assignment can hide this regression.
[Profile photo refresh](../../Spiritia/v2/lib_employeeDialogs.js)

## Implementation Checklist

- Before any active-form model replacement, merge
  `{ ...this.model, ...this.form.value }`.
- Use the merged snapshot for validation, payload mapping, `structuredClone`,
  dialog results, step changes, and repeat/detail updates.
- Keep the spread order: model first, form value second.
- After changing detail rows, also refresh the active grid with `assignData`
  when required by `detail-grid-state-sync-problem.md`.
- Do not use `form.setValue` on repeat fields merely to force synchronization.
- Add a regression test where the form value is newer than the model, trigger
  the secondary action, and verify the latest value survives.

## Related Files And Patterns

- `.agents/references/form-rules.md`
- `.agents/references/detail-grid-state-sync-problem.md`
- `.agents/references/debug-reference.md`
- Example signal: manual Payment Method rows disappearing after selecting TNC
  in `Proton/quotationForm.js`.
