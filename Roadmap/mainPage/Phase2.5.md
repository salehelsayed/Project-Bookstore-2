Below is a revised approach and explanation based on the code and logic you currently have. The main issue is that using `width: var(--fill-percentage)` on the `.star::after` element scales or clips the background incorrectly, resulting in an awkward-looking half star. Instead of scaling the star's width, you need to **mask or clip** the yellow star so only the required portion is visible.

### Adjusting the Half-Star Display

**Current Problem:**  
The half-star appears distorted because you're changing the element's width, effectively squashing the star image. You want to reveal only part of the full yellow star without altering its shape.

**Better Approach: Use a Clip-Path or Similar Masking Technique**

1. **Remove Width Scaling on `::after`:**  
   Instead of `width: var(--fill-percentage)`, you should keep the full star size intact and use a `clip-path` or a CSS mask to reveal only the fraction needed.

2. **Using Clip-Path:**  
   A simple `clip-path` inset can show a portion of the star from left to right without distorting its shape.

   Replace the `.star::after` width logic with a clip-path:
   ```css
   .star::after {
       content: '';
       position: absolute;
       top: 0;
       left: 0;
       width: 100%;
       height: 100%;
       background-image: url("data:image/svg+xml,%3Csvg ... %3E%3C/svg%3E");
       background-size: contain;
       background-repeat: no-repeat;
       z-index: 1;
       /* Instead of scaling width, we clip: 
          var(--fill-percentage) is a percentage (0 to 100)
          If rating is 4.5, fill-percentage ~50%, so we show left 50% of star */
       clip-path: inset(0 calc(100% - var(--fill-percentage)) 0 0);
   }
   ```

   Here’s what this does:
   - `clip-path: inset(0 calc(100% - var(--fill-percentage)) 0 0);`
     - If `fill-percentage = 50%`, `calc(100% - 50%) = 50%`.
     - `inset(0 50% 0 0)` means we crop the star’s right side by 50%, leaving the left half visible.
   - The star shape remains intact, and you simply reveal a portion of the yellow star overlay. No squashing occurs.

3. **Ensuring `overflow:hidden;`:**  
   You already have `overflow: hidden;` on `.star`, which is good. With `clip-path`, `overflow:hidden` is less critical since `clip-path` directly controls the visible region. Still, keep `overflow:hidden;` as a safeguard.

4. **Check the JS Logic:**  
   Your JS sets `fillPercentage = ((rating % 1) * 100).toFixed(4)` for fractional stars. If rating is 4.5, fillPercentage = 50%. Then you do:
   ```js
   star.style.setProperty('--fill-percentage', `${fillPercentage}%`);
   ```
   This should now correctly clip the star.

### Keeping Rating and Reviews on One Line

If `(1234 reviews)` still wraps, ensure:

- `white-space: nowrap;` is on `.book-rating` as you already did.
- No extra `<br>` tags or block-level elements causing wraps.
- `.book-rating` container is wide enough.
- Check if there’s any CSS forcing the `.reviews` span to break line. For instance, avoid `display: block;` on `.reviews`.

Given your CSS:

```css
.book-rating {
    display: flex;
    align-items: center;
    gap: 8px;
    height: 24px;
    white-space: nowrap; /* Prevent line breaks */
}
```

This should keep them on one line unless the container is too narrow. Ensure your card width is sufficient.

### Improving Button Appearance (Recap)

From previous suggestions, ensure buttons look good:

- Increase padding for comfortable click targets.
- Ensure icons are large enough and aligned:
  ```css
  .book-card-footer .btn {
    background-color: #3182CE;
    color: #fff;
    font-size: 16px;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .book-card-footer .btn:hover {
    background-color: #276C9B;
  }

  .book-card-footer .btn:focus {
    outline: 2px solid #3182CE;
    outline-offset: 2px;
  }
  
  .book-card-footer {
    display: flex;
    gap: 8px;
    border-top: 1px solid #E2E8F0;
    padding-top: 12px;
  }
  ```

If the icons are small, increase their font-size or the SVG’s width/height:
```css
.btn .icon {
  font-size: 18px;
}
```

### Summary of Changes

- **Star Ratings:** Use `clip-path` on `.star::after` instead of changing the element’s width. This ensures a proper, undistorted half-star display.
- **One-Line Rating and Reviews:** You’ve added `white-space: nowrap;`. Just confirm no unintended line breaks and that the container is wide enough.
- **Buttons:** Apply the previously mentioned styling enhancements to achieve cleaner, more visually appealing buttons.

These adjustments should yield a professional, polished design matching the desired aesthetics and functionality.