# Spiritia Report Menu Lifecycle Problem

Use this reference when a Biz-A menu change works on Home but disappears after
navigation, or when adding a shared script through `useLibrary` breaks a page's
`onInit`.

## Problem signal

- Report submenu captions are numbered in `menu.json`, leaving gaps when user
  group permissions hide some reports.
- A DOM numbering script runs on Home only, or appears not to run on any page.
- Importing `main` through every page's `useLibrary` replaces page-specific
  lifecycle functions such as `onInit`.
- Re-entering pages creates multiple DOM observers.

## Root cause

`menu.json` is static, while the visible submenu depends on permissions and
Angular Material's rendered overlay. A library factory call is not a reliable
DOM lifecycle trigger. A module exported as a shared library can also contribute
functions with the same names as the consuming page's lifecycle functions;
`main.onInit` therefore collided with page-specific `onInit` functions. A guard
stored only on `this` is page-instance scoped and does not prevent another page
from installing a second observer.

## Corrected pattern

1. Keep Report captions unnumbered in `menu.json`.
2. Put the reusable DOM helper in `lib_utility.js`, without an `onInit` hook in
   that library.
3. Declare `lib_utility` in each page's `useLibrary` and call
   `this.f().installReportMenuNumbering()` from that page's own `onInit`. Home's
   `main.js` follows the same pattern. Do not import `main` into other pages.
4. Mark the calling instance with `this.spiritiaReportMenuNumberingInstalled`.
   Also keep the observer on `document.body.spiritiaReportMenuObserver`, since
   `document.body` survives normal route changes while page instances change.
5. Observe `aria-expanded`, `aria-controls`, and child-list changes. Number only
   the rendered items of the currently expanded Report menu. Remove any old
   numeric prefix before writing the current sequence, so reopening the menu
   does not stack prefixes.

## Verification checklist

- Confirm each page retains its original `onInit` behavior after library merge.
- Confirm Home and other pages load `lib_utility` and call the helper once from
  their own `onInit`.
- Open Report with different permission-filtered item sets and verify visible
  numbering starts at 1 and has no gaps.
- Navigate between pages and reopen Report; verify numbering persists and only
  one observer is attached to the current body.
- Run the relevant Jest tests, then verify the deployed Biz-A UI. Local tests
  do not prove the actual Angular overlay behavior after upload.

## Related files

- [Spiritia main](../../Spiritia/main.js)
- [Spiritia utility](../../Spiritia/lib_utility.js)
- [Spiritia menu](../../Spiritia/menu.json)
- [Report numbering tests](../../Spiritia/tests/reportMenuNumbering.test.js)
- [Library and lifecycle patterns](patterns.md)
