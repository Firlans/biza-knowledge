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

## Related Files And Patterns

- `form-rules.md` for form save-flow responsibilities.
- `testing-rules.md` when adding or updating regression tests.
- `biz-a-query-join-depth-problem.md` only when the `queryData` failure is about join depth or `token unknown`, not BLOB content.
- Local examples: SO attachment save/load flows in `Endo Medika/SOForm.js`, `Endo Medika/lib_qry.js`, and `Endo Medika/test/SOFormAttachment.test.js`.
