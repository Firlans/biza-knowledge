# Form And Model Value Sync Problem

Use this reference when a Biz-A form loses recent user input after a dialog,
step change, lookup selection, repeat update, detail-grid refresh, or any action
that rebuilds or replaces `this.model`.

## Problem Signal

- A user finishes editing a field or detail-grid, then another action makes the
  value disappear or revert.
- `this.form.value` contains the latest value while `this.model` is stale.
- A handler spreads or clones `this.model` and unintentionally restores old
  values over controls that the user already edited.
- The failure appears only after a dialog or UI action, not during initial load.

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

- `.github/instructions/references/form-rules.md`
- `.github/instructions/references/detail-grid-state-sync-problem.md`
- `.github/instructions/references/debug-reference.md`
- Example signal: manual Payment Method rows disappearing after selecting TNC
  in `Proton/quotationForm.js`.
