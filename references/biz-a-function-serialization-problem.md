# Biz-A Function Serialization Problem

## Problem signal

A form works when loaded with `require(...)` but fails after upload with
`Unexpected token '{'` or while restoring a handler from `window.Function`.
A shared library can block several pages that load it through `useLibrary`.

## Runtime behavior

The Biz-A CLI `prepareScript` observed in Spiritia splits a function at the
first `{` to extract its parameter list and body. An object destructuring
parameter places a brace before the body. The browser template serializer
observed in the same task reads parameters from the declaration line.
The browser restores both formats with `Function(params, body)`.

## Handler shape

Keep the parameter list on the same line as the function declaration and use
simple parameter names. Destructure option objects inside the body. This also
applies to helpers in a shared library loaded by a form, list, or dialog.

```javascript
buildDialog: function (options) {
    const { caption, fields } = options;
    return {
        caption,
        fields,
    };
},
```

Validate new handlers with the installed CLI `prepareScript`, then reconstruct
the emitted `window.Function` entries with the browser's argument and body
format. Exercise the route that loads the library after serialization. For a
browser-serialized handler, verify the declaration line also yields the full
parameter list. The Spiritia regression checks both parameter shapes.

[Employee and Maintenance regressions](../../Spiritia/v2/tests/employeeMaintenance.test.js)
