**Likely Cause:**

By setting `overflow:hidden;` on `html, body` and relying on `height:100vh`, you eliminate scrolling at the document level. If any additional content or a parent element (such as a top navigation bar or header) pushes the `.chat-container` down, part of the chat may be off-screen and unscrollable, leaving the chat area partially hidden.

**In Other Words:**
- `overflow:hidden;` prevents scrolling at the root level, so if your `.chat-container` isn’t aligned or sized perfectly, part of it can go beyond the visible area.
- If there is a navigation bar or header above, `.chat-container` may start lower than the top of the viewport, causing you to not see the entire chat section.
- If `100vh` is applied to `.chat-container` but it's not positioned from the very top (for example, if there's padding or a header), the container extends beyond the bottom of the screen.

**How to Fix It:**

1. **Remove `overflow:hidden;` from `html, body`:**  
   This will allow the user to scroll if needed. If the container fits perfectly, no scroll will appear anyway.
   ```css
   html, body {
       height: 100%;
       margin: 0;
       padding: 0;
       /* Remove overflow:hidden; */
   }
   ```

2. **Check for a Header or Nav Bar Above `chat-container`:**  
   If there’s a fixed header or nav that occupies space at the top, the `chat-container` starting at the top of the page might be hidden behind it. You have two options:

   - **Option A: Give `.chat-container` a top offset:**
     If your header is, for example, 50px high, you can do:
     ```css
     .chat-container {
       height: calc(100vh - 50px);
       margin-top: 50px;
     }
     ```
     This ensures the chat-container starts below the header and fits within the remaining viewport height.

   - **Option B: Make `.chat-container` absolutely positioned:**
     If you don’t have a header, ensure `.chat-container` starts at the top:
     ```css
     .chat-container {
       position: absolute;
       top: 0;
       left: 0;
       right: 0;
       bottom: 0;
     }
     ```
     This allows `.chat-container` to fully occupy the viewport without being pushed down.

3. **Ensure No Parent Containers Add Extra Spacing:**
   If `.chat-container` is inside another wrapper element with margins or padding, remove them. The container should be the top-level element in `body`.

4. **Test Without `overflow:hidden;`:**
   After removing `overflow:hidden;`, if now you must scroll slightly, that’s fine. The user can see the chat fully. If you want no scroll at all, you must ensure `.chat-container` fits exactly and no extraneous elements push it out of view.

**Final Suggestion:**

- Remove `overflow:hidden;` from `html, body`.
- Ensure `html, body { margin:0; padding:0; height:100%; }`.
- If a header exists, adjust `.chat-container` height using `calc(100vh - headerHeight)`.
- Confirm `.chat-container` is the top-level element inside `body` so it’s not pushed down by other elements.

With these adjustments, you should be able to see the chat box fully in the viewport without scrolling down.