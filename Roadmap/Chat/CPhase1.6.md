**Problem Identified:**

The logic in the `mousemove` handler calculates `newWidth` based on `const newWidth = startWidth + dx;`. Here, `dx` is `(e.clientX - startX)`:
- Moving the mouse to the right makes `dx` positive, thus increasing width.
- Moving to the left makes `dx` negative, thus decreasing width.

This is the opposite of the user’s expected behavior. The user wants:

- Moving left to **increase** the PDF viewer width.
- Moving right to **decrease** the PDF viewer width.

**How to Fix It:**

Simply invert the sign so that moving left results in a larger width and moving right a smaller width. Instead of `const newWidth = startWidth + dx;`, use:

```javascript
const newWidth = startWidth - dx;
```

**Explanation:**

- If the user moves the mouse to the left (e.g., `e.clientX < startX`), `dx` is negative. With `newWidth = startWidth - dx`, subtracting a negative number adds to `startWidth`, increasing the PDF viewer's width.
- If the user moves the mouse to the right (`dx` positive), `newWidth = startWidth - dx` decreases the width, as requested.

**Final Corrected Code Snippet:**

```javascript
document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    e.preventDefault();
    const dx = e.clientX - startX;
    const newWidth = startWidth - dx; // Inverted logic

    if (newWidth > minWidth && newWidth < maxWidth) {
        pdfViewer.style.width = `${newWidth}px`;
    }
});
```

With this change, the resizing behavior matches the user’s expectations.