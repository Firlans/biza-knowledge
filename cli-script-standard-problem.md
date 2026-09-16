# Biz-A CLI Script Standard Problem

## Problem Signal

Use this reference when a task involves `cli-script/` files, watcher scripts, callback scripts, converting a standalone Node script into Biz-A CLI format, or errors caused by a CLI script that runs immediately with `require(...)` and top-level side effects.

Common signals:

- User says "buat file ... di cli-script", "standar biza cli script", "watcher", or "callback".
- Existing source is a standalone Node script that calls its main function directly.
- Script must be callable by Biz-A through `onInit(data, socket)` and return a value instead of printing only to console.
- Script needs external packages such as `axios`, `basic-ftp`, `winston`, `crypto`, mail controller, or scheduler `datalib`.

## Root Cause

Standalone Node scripts are not the same runtime shape as Biz-A CLI scripts. A file like this is useful for manual execution but not for Biz-A CLI execution:

```javascript
const ftp = require("basic-ftp");

async function main() {
    // work
}

main();
```

Biz-A expects a module factory that returns a `functions` object. The entrypoint must be `onInit`, and framework-provided libraries come from `lib`.

## Corrected Approach

Use the Biz-A CLI script export pattern:

```javascript
get = function (lib) {
    return {
        functions: {
            onInit: async function (data, socket) {
                return {
                    success: true,
                    data: [],
                };
            },
        },
    };
};

module.exports = get;
```

Keep work inside named functions under `functions`. Use `function` syntax, not arrow functions, for methods that use `this`.

## Implementation Checklist

- Export with `get = function (lib) { return { functions: { ... } } }` and `module.exports = get`.
- Put the runtime entrypoint in `onInit`.
- Accept runtime input from `data.arguments`, `data.body`, `data.headers`, `data.query`, and `socket` as needed.
- Build a config object in a named helper such as `buildConfig` or `buildFtpConfig`.
- Validate config before opening network connections.
- Return structured success/error objects instead of relying only on `console.log`.
- Use `lib.log.info` / `lib.log.error` when available.
- Close network clients in `finally`.
- Prefer dynamic `await import(...)` inside helper functions for CLI-only dependencies when local examples use that pattern.
- For packages that are not already installed in the target folder, update the target folder's `package.json` and lockfile through normal package-manager flow.

## Watcher and Callback Notes

- Watcher scripts usually run scheduled/background work from `onInit(data, socket)`.
- Callback scripts usually validate headers/body, perform idempotency checks, then return the provider response object.
- For callback scripts, avoid direct top-level initialization that can make repeated callback calls share stale request state.
- For watcher scripts, keep long-running loops explicit and make failures loggable per iteration.

## FTP Example Notes

When converting a standalone FTP script:

- Keep the FTP credentials and remote path in `buildFtpConfig`.
- Allow overrides from `data.arguments.ftp` and `data.body.ftp`.
- Use `finally { client.close(); }`.
- If the server fails on EPSV, set `client.prepareTransfer` to `enterPassiveModeIPv4` before `client.access`.
- Return `{ success, remoteDir, total, data }` for a list operation.

## Related Files and Patterns

- `.github/doc/Watcher and Callback.pdf` for business/runtime expectations when available.
- Existing watcher examples under `*/cli-script/*watcher*.js`.
- Existing callback examples under `*/cli-script/*callback*.js` or payment gateway callback folders.
