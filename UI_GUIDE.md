# UI Guide

## Filters Form (`filters-form`)

- **Description:** The form containing all filter inputs.
- **ID:** `filters-form`
- **Behavior:** Listens for `change` events to trigger AJAX updates.

## Book Grid (`book-grid`)

- **Description:** The main container for book cards.
- **ID:** `book-grid`
- **Behavior:** Content is dynamically replaced based on filter selections.

## New CSS Classes

- **`.filters-form`**
  - Styles for the filters form.
  - Should support proper spacing and alignment of inputs.

- **Responsive Behavior:**
  - On smaller screens, the filter column may stack above the book grid.
  - Ensure that `book-grid` and `filters-form` adjust appropriately for mobile devices.

## JavaScript Interactions

- The JavaScript in `main.js` handles dynamic updating of the `book-grid`.

---

Ensure these elements are styled consistently with the rest of the application.
