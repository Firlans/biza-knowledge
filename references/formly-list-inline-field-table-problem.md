# Formly List Inline Field Table Problem

Use this reference when a Biz-A list needs an input or other helper field beside the rendered list table, especially when the user mentions a Formly list, `fields`, `body > app-root > app-list > div > table`, or keeping other siblings in their original position.

## Problem Signal

- A user asks to add a field beside a Biz-A list table.
- A field inserted with DOM APIs appears below the table instead of beside it.
- Setting `display: flex` on `body > app-root > app-list > div` moves unrelated siblings.
- The requested container is the rendered table, such as `body > app-root > app-list > div > table`.
- The user asks whether a built-in component from `fields` can be used in the list.

## Root Cause

Biz-A list table markup is rendered by Angular. A manual DOM node can be placed beside the table, but a Formly field config in `fields` is rendered only by the Biz-A/Formly renderer. A Formly component cannot be created by `document.createElement()` and manually inserted beside a table.

The list body wrapper often contains more than the table. If `display: flex` is applied to the outer body wrapper, every sibling in that wrapper is affected. To keep unrelated siblings stable, create a narrow wrapper around only the table and the adjacent helper input.

## Correct Pattern

Keep the responsibilities separate:

- For exact beside-table placement, use a narrow DOM fallback around the rendered table.
- For a built-in Formly component, add `model` and `fields` at the list root and let the Biz-A list renderer place it.
- Do not assume the Formly `fields` component can be mounted inside the manual table wrapper.

Use a selector helper for the table, not a broad body wrapper:

```javascript
getListTableSelector: function () {
    return 'body > app-root > app-list > div > table'
}
```

Wrap only the table before applying flex:

```javascript
ensureListTableWrapper: function (table) {
    const parentElement = table.parentElement

    if (!parentElement) {
        return null
    }

    if (parentElement.dataset.listTableWrapper === '1') {
        return parentElement
    }

    const wrapper = document.createElement('div')
    wrapper.dataset.listTableWrapper = '1'
    table.insertAdjacentElement('beforebegin', wrapper)
    wrapper.appendChild(table)

    return wrapper
}
```

Then insert the adjacent native input into that wrapper:

```javascript
const wrapper = this.f().ensureListTableWrapper(table)
const input = this.f().createListHelperInput()
table.insertAdjacentElement('beforebegin', input)
wrapper.style.display = 'flex'
wrapper.style.alignItems = 'flex-start'
wrapper.style.gap = '8px'
```

For the built-in Formly component, add root config separately:

```javascript
model: {
    test_component: null,
},
fields: [
    {
        key: 'test_component',
        type: 'input',
        props: {
            label: 'Sample',
            placeholder: 'Sample',
        },
    },
],
```

## Implementation Checklist

- Read the list file completely before changing DOM behavior.
- Put selectors in named helpers.
- Use `typeof document === 'undefined'` guard for non-browser flows.
- Select the rendered table with `body > app-root > app-list > div > table` when the user targets the table.
- Create an idempotent wrapper around only the table before applying flex.
- Mark the wrapper with a dataset flag so repeated scheduling does not nest wrappers.
- Move an existing helper input into the wrapper if it already exists.
- Do not set `display: flex` on `body > app-root > app-list > div` unless the user explicitly wants all siblings affected.
- If the user asks for a built-in component, add `model` and `fields` at the list root, but keep exact beside-table placement as a separate DOM concern.
- Do not use `structuredClone` on `fields` or other Biz-A config objects.

## Related Files And Patterns

- `.agents/references/list-rules.md`
- `.agents/references/list-row-action-dom-state-problem.md` for rendered list table selector patterns.
- `Endo Medika/DOList.js` shows an inline helper input beside a rendered list table plus a root `fields` input config.
