# Attachment BLOB QueryData Problem

Use this reference when a Biz-A form saves or loads file attachments, especially PDF/image BLOB columns, and the failure appears around `queryData`, `updateImg`, `input-file`, or JSON parsing.

## Problem Signal

- `queryData` fails with `n.map is not a function` while loading an attachment column.
- `JSON.parse` fails with `Bad control character in string literal` on a response that contains PDF text such as `%PDF-1.4`.
- A BLOB/PDF attachment appears inside a JSON string response with raw newlines or binary content.
- Loading a form breaks only after an attachment was saved.
- Attachment works for new file upload but breaks after edit/reopen.

## Root Cause

BLOB content is not safe to send or store as raw JSON string data.

PDF and image files contain binary bytes and control characters. If the raw content is saved through `sendModel` or embedded directly into a JSON response, the response can stop being valid JSON. The visible runtime error can be misleading, because the failure may happen inside the Biz-A query/response mapper before the form code receives normal rows.

Do not treat a BLOB column like normal model text.

## Corrected Approach

- Do not include file attachment values in the master `sendModel` payload.
- Save the master/detail rows first.
- Save the file content through the attachment/image API, normally `dataService.updateImg`.
- Convert the uploaded file to a Data URL with `FileReader.readAsDataURL`.
- Extract the base64 part after the comma.
- Encode the base64 string with `btoa(...)` when the target API expects the stored BLOB-safe representation.
- Load attachment separately from normal master/detail queries when the BLOB column can destabilize the main query response.
- Ignore loaded attachment strings when saving unless the user selected a new file.

## Implementation Checklist

1. Keep `attachment` out of JSON master payloads:

```javascript
const { sodet, ...masterBiza } = this.f().JSONBIZASO(saveModel)
// JSONBIZASO should not include attachment in masterBiza.
```

2. Save uploaded file only after the SO/record id exists:

```javascript
const rawFile = this.f().getAttachmentUploadFile(saveModel.attachment)
if (!rawFile) return this.of('success')
return this.f().saveAttachment(saveModel.soid, rawFile)
```

3. Build the `updateImg` body from a file, not from a loaded base64 string:

```javascript
const splitted = String(dataUrl || '').split(',')
const base64Image = splitted[1]
const encodedImage = btoa(base64Image)

return this.dataService.updateImg(this.config.api, {
    tableName: 'SO',
    keyCol: 'ID',
    keyValue: soid,
    imgCol: 'ATTACHMENT',
    img: encodedImage,
    dbIndex: this.config.api.dbIndex
}, false)
```

4. Guard against re-saving loaded attachment strings:

```javascript
const file = Array.isArray(files) ? files[0] : files
if (!file || typeof file === 'string') {
    return null
}
```

5. Query attachments separately when needed:

```javascript
getSOAttachmentBiza: function (soid) {
    const param = {
        columns: [
            { data: 'SO.ATTACHMENT', key: 'attachment' }
        ],
        filter: [
            { junction: '', column: 'SO.ID', operator: '=', value1: soid }
        ],
        length: 1
    }

    return this.dataService.queryData(param, this.config.api, true, true)
}
```

## What To Avoid

- Do not parse your way around corrupted raw BLOB JSON responses as the primary fix.
- Do not add raw `File`, `Blob`, Data URL, PDF text, or loaded attachment strings into `sendModel` payloads.
- Do not re-save an existing loaded attachment string when the user did not upload a new file.
- Do not put large BLOB columns in broad master/detail `queryData` calls if they destabilize query result mapping.
- Do not assume `n.map is not a function` always means the final subscriber received a non-array; it may be a response mapper failure caused by invalid attachment content.

## Test Expectations

Add focused tests that prove:

- Master payload builders do not include `attachment`.
- `saveAttachment` sends `updateImg` with `img: btoa(base64Image)` when a new `File` or `Blob` is uploaded.
- `saveAttachment` skips `updateImg` for empty input and loaded attachment strings.
- Edit mode can load attachment from a separate query and map it into the form model.
- The normal module test suite still passes after attachment changes.

## Linking an uploaded row to its document

When the upload has already created a child row and its parent key is still
null, check which keys the save uses to find that row. In the Spiritia
Document Bank, Firebird 2.5 reproduced `validation error for column
"SP_BANK_DOC_FILE"."FILE_NAME"` when a test upsert matched both attachment ID
and the new parent ID. The staged row missed the match, so the statement tried
to insert it. Supplying the name in that test exposed a duplicate primary key.

- If the error names an unknown parent column instead, compare the ORM's
  expected `<MASTER_TABLE>_ID` column with the child schema. Spiritia needed
  `SP_BANK_DOCUMENT_ID`. Keep the read filter, save keys, foreign key, triggers,
  and list view aligned when migrating an existing database.
- Use the attachment's existing primary key for a direct `sendModel` call
  to the child table. Pass its name and parent key as metadata. Keep the
  content in the BLOB saved via `updateImg`.
- Save the parent revision before applying the changes to attachments. Track
  the confirmed revision and uploaded IDs in the form. If linking fails,
  report partial completion and retry the pending changes with those IDs.
- Test the transition from a null parent key to the saved parent and verify
  that the existing BLOB bytes are preserved. Cover a failure after one of
  several links succeeds, then verify the retry skips that link and reuses the
  upload for the remaining rows.

See the [Spiritia save flow](../../Spiritia/v2/lib_documentBank.js) and
[attachment regressions](../../Spiritia/v2/tests/documentBank.test.js).

## Picker and preview with a separate attachment grid

- Subscribe to the native `attachments` control's `valueChanges` in its field
  hook. If the detail grid owns both pending and saved rows, move valid entries
  from `uploads` into that grid and clear the picker value once. Test selection
  twice in a row and mixed valid and invalid files. Stage the files until the
  user clicks Save.
- For preview in a new tab, open the tab during the Preview click and then
  fetch a saved file. Render the resulting Blob in the new tab. A delayed
  response should replace the loading state with the image, PDF, or an error.
  Keep the Download handler separate and verify in a browser that Preview
  displays the bytes without starting a download.

See the [Spiritia attachment picker](../../Spiritia/v2/documentBankForm.js).

## Related Files And Patterns

- `form-rules.md` for form save-flow responsibilities.
- `testing-rules.md` when adding or updating regression tests.
- `biz-a-query-join-depth-problem.md` only when the `queryData` failure is about join depth or `token unknown`, not BLOB content.
- Local examples: SO attachment save/load flows in `Endo Medika/SOForm.js`, `Endo Medika/lib_qry.js`, and `Endo Medika/test/SOFormAttachment.test.js`.
