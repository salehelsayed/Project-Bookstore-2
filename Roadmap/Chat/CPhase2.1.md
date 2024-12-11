**Summary of Required Changes:**

1. Replace the single-line input with a `<textarea>` in `chat.html` so the user can type multiple lines.
2. In `chat.css`, add rules to allow the textarea to expand up to a certain max height, then show a scrollbar.
3. In `chat.js`, add a small JavaScript snippet to automatically adjust the textarea's height as the user types, stopping at the max height and showing scrollbars beyond that limit.

**Detailed Steps:**

### 1. Update `chat.html` to Use a `<textarea>`

Originally, `chat.html` uses an `<input type="text">` for the chat input. Change it to a `<textarea>` that can grow:

```html
<form class="chat-input-form" id="chatForm">
    <!-- Use textarea instead of input -->
    <textarea class="chat-input" name="user_query" rows="1" placeholder="Ask any question about the book..."></textarea>
    <button type="submit" class="chat-send-btn">Send</button>
</form>
```

By using `<textarea>`, the user can enter multiple lines.

### 2. Add CSS for Auto-Growing Until Max Height

In `chat.css`, modify the `.chat-input` class for the textarea:

```css
.chat-input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    font-size: 1rem;
    resize: none; /* Prevent user from manually resizing */
    line-height: 1.5;

    /* Max height and overflow: */
    max-height: 150px; /* Example max height */
    overflow-y: auto;  /* Show scrollbar if content exceeds max-height */
}
```

What this does:
- `resize: none;` stops manual drag-resizing.
- `max-height: 150px;` sets a limit after which a scrollbar appears.
- `overflow-y: auto;` ensures that once the text is too long, the user can scroll inside the textarea.

### 3. Add JavaScript for Auto-Expanding Textarea

In `chat.js`, after defining `chatInput`, add an event listener on `input` to auto-adjust the height based on the content. This ensures that as the user types more lines (up to `max-height`), the textarea grows until it reaches that limit:

```javascript
const chatInput = document.querySelector('.chat-input');
if (chatInput) {
    chatInput.addEventListener('input', function() {
        // Reset height to 'auto' to correctly measure the new scrollHeight
        this.style.height = 'auto';
        
        // Set the textarea's height to its scrollHeight (or maxed at max-height by CSS)
        this.style.height = this.scrollHeight + 'px';
    });
}
```

**How It Works:**
- On each keystroke (`input` event), the textarea resets its height to auto, then sets it to `this.scrollHeight`.
- If the content would exceed `max-height`, the CSS rules cause the textarea to stop growing and show a scrollbar instead.
- The `line-height` and `font-size` ensure the textarea grows smoothly line by line.

**No Changes to the Enter-to-Submit Logic:**
Your existing logic for `Enter` key submission still works. Users press Enter (without shift) to submit, or shift+Enter to add a new line. The textarea expands as needed.

---

With these changes:
- Users can enter multiple lines.
- The input area auto-expands until a certain height, then scrolls.
- The rest of the chat functionality, resizer, and sidebar toggle remain unchanged.