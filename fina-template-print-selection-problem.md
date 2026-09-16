# FINA Template Print Selection Problem

Use this reference when a Biz-A form or list prints through FINA report templates with `previewTemplateFina`, especially when the user asks to select and remember a template, restrict template names, control paper size/orientation, or skip the Biz-A print preview.

## Problem Signal

- The print button uses generated HTML even though the user asks for `previewTemplateFina`.
- Print always uses the first template from `getTemplates(templatetype)` and the user later asks that the template can be selected.
- A FINA-backed form opens in `view` or `print` mode and needs a `templateid` lookup filtered by `TEMPLATETYPE`.
- Existing checks only assert custom HTML output and miss the selected-template payload sent to `previewTemplateFina`.
- A selected template saves successfully but reopening the print form shows the first/default template.
- A lookup intended for two named templates still shows other FINA templates.
- `printService.print()` creates a Biz-A Print/Close preview before the browser print dialog.
- CSS `@page` does not reliably lock Letter, Half Letter, orientation, or image scaling across browsers/printers.

## Root Cause

FINA template print has several separate concerns:

- Selecting the template (`TEMPLATE.TEMPLATEID`, filtered by `TEMPLATE.TEMPLATETYPE`).
- Persisting the selection to the correct Biz-A and FINA records.
- Loading the saved `TEMPLATEID` and applying it to the Formly lookup after the default-template query.
- Rendering the selected FINA report through `dataService.previewTemplateFina`.
- Sending the rendered pages to the desired print path.

If the implementation jumps directly to `getTemplates(type)[0]`, the print works but users cannot choose among multiple templates of the same type.

Common secondary causes are:

- The FINA document query does not include `SO.TEMPLATEID` (or the equivalent document field).
- `preparingData` assigns `templates[0]`, but the loaded model never reassigns the lookup control afterward.
- A compound lookup filter is supplied in a string shape that the lookup runtime does not apply consistently.
- Calling `printService.print(html)` intentionally creates the Biz-A preview; it is not a direct browser-print API.

## Corrected Approach

1. Add a `templateid` lookup field on the form when selection is required.
2. Filter the lookup with the exact requested template type, for example `TEMPLATETYPE = 0`.
3. Show the lookup only in the mode where printing happens, usually `model.mode === "view"` or `model.mode === "print"`.
4. Restrict both the lookup and the default-template query when only specific names are valid. Prefer structured filters (`TEMPLATETYPE`, then `NAME in (...)`).
5. Persist the selected template before rendering. If Biz-A and FINA both store the field, save Biz-A, then update FINA through the document's established `json2fina` mapper.
6. Validate `sendModel` with `response.error` / success state and `json2fina` with `response.result?.[0]?.error`. A failed save must stop printing.
7. Include the document `TEMPLATEID` in edit/load queries. After data load, validate the saved ID against the allowed template rows and explicitly set the lookup control. This must happen after any `templates[0]` default assignment.
8. Pass the selected ID as `templateid` to `previewTemplateFina`. The word `preview` here describes FINA report generation; it does not require showing a Biz-A UI preview.
9. For the standard Biz-A preview, convert the binary response to image HTML and call `printService.print`.
10. To skip the Biz-A Print/Close preview and require exact paper geometry, build a jsPDF document from the generated JPEG pages, load its Blob URL in a hidden iframe, and call the iframe's `print()`. Do not also call `doc.autoPrint()` or two print dialogs may be triggered.
11. Keep the flow linear: save Biz-A -> save FINA -> generate report -> build/print PDF, with one final `subscribe()`.

## Implementation Checklist

- [ ] `useLibrary` includes the library that provides `getTemplates`, usually `lib_qry`.
- [ ] `templateid` lookup uses `table: 'TEMPLATE'`, `key: 'TEMPLATEID'`, `display: 'NAME'`, and `searchKey: ['NAME']`.
- [ ] Lookup filter uses the requested `TEMPLATETYPE`, not a copied value from another document type.
- [ ] When names are restricted, the lookup filter and `getTemplates` query use the same allowed names.
- [ ] The FINA/Biz-A load query selects `TEMPLATEID`, and the load mapper returns `templateid`.
- [ ] A loaded allowed template overrides the first-template default; an invalid legacy ID falls back to the first allowed template.
- [ ] Template persistence runs before `previewTemplateFina` and updates every required data store.
- [ ] Print param includes `dbIndex`, `id`, `table`, `keyfield`, `imageQuality`, `templateid`, and the required `dictionary`.
- [ ] `apiConfig` passed to `previewTemplateFina` uses the FINA db index, for example `{ ...this.config.api, dbIndex: this.config.api.finaDbIndex }`.
- [ ] Error handling stops loading and shows `notificationService.showError(err.message)`.
- [ ] Any after-print update, such as marking a FINA invoice as printed, remains in the `printService.print` callback.
- [ ] If jsPDF is used, load it before printing and set the page format/orientation explicitly.
- [ ] Half Letter landscape uses 139.7 x 215.9 mm with `orientation: 'landscape'`; Letter portrait uses 215.9 x 279.4 mm with `orientation: 'portrait'`.
- [ ] Fit report images with `min(pageWidth/imageWidth, pageHeight/imageHeight)`, preserve aspect ratio, and center them.
- [ ] A hidden PDF iframe revokes its Blob URL and removes itself after printing; no `window.open` tab is created.

## Example

```javascript
{
    className: 'col-3 lu-fina',
    key: 'templateid',
    type: 'lookup',
    props: {
        label: 'Template',
        placeholder: 'Pilih Template',
        lookupOptions: {
            table: 'TEMPLATE',
            key: 'TEMPLATEID',
            display: 'NAME',
            dbIndex: '',
            searchKey: ['NAME'],
            filter: 'TEMPLATETYPE = 0',
        },
    },
    expressions: {
        hide: 'model.mode !== "view"',
    },
}
```

```javascript
const selectedTemplateId = this.form.get('templateid').value
const templateId$ = selectedTemplateId
    ? this.of(selectedTemplateId)
    : this.f().getTemplates(0).pipe(this.map(templates => templates[0]?.id))
```

For direct PDF printing without a Biz-A preview, keep sizing and placement explicit:

```javascript
const scale = Math.min(pageWidth / imageWidth, pageHeight / imageHeight)
const width = imageWidth * scale
const height = imageHeight * scale
const x = (pageWidth - width) / 2
const y = (pageHeight - height) / 2

doc.addImage(imageSource, 'JPEG', x, y, width, height)
```

## Related Patterns

- `.github/instructions/references/form-rules.md`
- `Endo Medika/DOForm.js` for a selectable FINA template lookup pattern.
- `Endo Medika/SIForm.js` for a Sales Invoice `templatetype = 0` print flow.
- `Endo Medika/SOForm.js` for persisted template selection, exact jsPDF paper sizing, fit-to-paper images, and hidden-iframe browser printing.
- `CAR/reportRekapMuatBarang.js` for the local jsPDF loading and Blob generation pattern.
