# Biz-A CLI FTP Data Sync Problem

## Problem Signal

Use this reference when a task involves a Biz-A `cli-script/` watcher that reads files from FTP, saves pulled file names to a Biz-A table, parses CSV content, or logs downloaded CSV rows as JSON.

Common signals:

- Script logs FTP file names but `totalSaved` stays `0`.
- `sendModel` is never reached or a debug log after `sendModel` never appears.
- Runtime data has `data.arguments.hostname`, `dbindex`, `finaDbIndex`, or `subdomain`, but no `data.body` and no explicit `url`.
- Errors include `Missing API config: url/dbindex`.
- Firebird rejects date values with messages like `conversion error from string "2026-06-29T04:34:12.992Z"`.
- User asks to show CSV data in logs as JSON.
- User asks to remove large logs and keep only error logs plus summaries.

## Root Cause

Biz-A CLI watcher input is not always shaped like form/list code or callback body input. Scheduler input commonly arrives in `data.arguments`, and `data.body` may be `null`.

For local scheduler runs, `hostname` can already include a path such as `server.biz-a.id/hub`, and `port` can be `null`. Requiring both `url` and `port` makes `apiConfig` fail even though `dbindex` and `subdomain` are present.

Do not silently skip persistence when `apiConfig` is missing. Returning `[]` from save helpers hides the real problem as a false success with `totalSaved: 0`.

Firebird-backed saves also should not receive raw JavaScript `Date` objects if the transport serializes them as ISO strings. Use a database-friendly date-time string.

## Corrected Approach

Build separate configs for FTP and Biz-A API:

- `buildFtpConfig(data)` reads FTP host/user/password/remoteDir from defaults plus optional overrides.
- `buildApiConfig(data)` reads scheduler data from `data.arguments` first.
- Accept `args.url` when present.
- If `url` is absent, build it from `args.hostname`, even when `args.port` is `null`.
- If a local endpoint is required, use an explicit fallback such as `http://localhost:212`.
- Use `dbindex` for Biz-A `sendModel` / `queryData`; only fall back to `finaDbIndex` when that is the intended database.
- Validate API config before saving and throw a clear error if it is missing.

For FTP CSV content:

- Download files through `basic-ftp` after `client.access`.
- Close the FTP client in `finally`.
- Parse CSV using the first row as headers.
- Default to summary-only logs such as `lib.log.info({ message: "FTP CSV summary", file_name, totalRows })`.
- Do not log full CSV rows, raw lookup rows, raw scheduler input, raw FINA payloads, or `JSON.stringify(payload)` unless the user explicitly asks for that diagnostic output.
- When the user asks for temporary diagnostic CSV content, keep the log scoped to the failing file or a short sample, then remove it before finalizing if they ask for summary-only logs.
- Avoid logging full `data` objects because scheduler arguments can include SMTP credentials.

For date fields:

- Format values as `YYYY-MM-DD HH:mm:ss` before `sendModel`.
- Do not rely on automatic `Date` serialization for Firebird date/time fields.

## Implementation Checklist

- Add a pure `normalizeApiUrl(url, hostname, port)` helper.
- Add a pure `buildApiConfig(data)` helper and keep it separate from FTP config.
- Log sanitized `apiConfig` only: `url`, `dbindex`, `subdomain`, `timeout`.
- Keep routine logs summary-only. Preserve `lib.log.error` blocks with message/code/stack because those are needed for scheduler failures.
- Throw on missing `apiConfig` in save flow instead of returning an empty saved list.
- Save pulled file names with `sendModel(model, apiConfig, "vendis_data")` or the target table name.
- Format date payloads with a helper such as `formatDateTime(new Date())`.
- When reading CSV content, download only the files that need processing unless the user asks for all files.
- Log CSV summaries before or after persistence depending on the business requirement, but keep the order explicit.
- Keep FTP credentials out of logs.
- For FINA `json2fina` imports, log SO summaries (`file_name`, `order_key`, `userId`, `dbIndex`, master IDs, `detailCount`) instead of the whole payload. If unit or mapping errors recur, log only targeted fields such as `itemno`, `itemunit`, and quantity for a small sample.

## Related Files and Patterns

- `.github/instructions/references/cli-script-standard-problem.md` for the base Biz-A CLI script shape.
- `*/cli-script/*.js` watcher scripts that use `get = function (lib) { return { functions: { onInit } } }`.
- `CAR/cli-script/ftpScript.js` as a concrete FTP CSV pull example when present.
