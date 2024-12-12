Below are the suggested changes to integrate Markdown rendering and maintain the current logic (including disabling the "Send" button while awaiting a response). The changes are minimal and adapted to the code you currently have.

**Key Changes:**
1. Include a Markdown parser (e.g., Marked) in `chat.html`.
2. When appending an AI message, parse it with `marked.parse()` and set `innerHTML` instead of `textContent`.
3. Ensure the `Send` button disabling logic remains intact.

### Step-by-Step Instructions

**1. Include the Marked Library**  
In `chat.html`, include the Marked.js script before your `chat.js`:

```html
{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="{{ url_for('static', filename='js/chat.js') }}"></script>
{% endblock %}
```

Place this before `chat.js`. This ensures `marked` is available by the time `chat.js` runs.

**2. Update `appendMessage` function in `chat.js`**  
In your current `appendMessage` function, you only set `textContent`. For AI messages, switch to using `marked.parse()` and `innerHTML`:

```javascript
function appendMessage(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', isUser ? 'user-message' : 'ai-message');

    if (isUser) {
        // User message: plain text is fine
        messageDiv.textContent = message;
    } else {
        // AI message: parse Markdown to HTML
        const html = marked.parse(message);
        messageDiv.innerHTML = html;
    }

    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}
```

**3. Keep Existing Button Disable/Enable Logic**  
You’ve already implemented logic to disable/enable the send button during `sendMessage`. That can remain unchanged. Just ensure you do not revert back to `textContent` for AI messages.

**4. Confirm CSS**  
No immediate changes to `chat.css` are required for Markdown. However, consider adding styles for elements like `p`, `ul`, `li`, `code` if you need a more refined look:

```css
.messages p {
    margin: 0.5rem 0;
}

.messages code {
    background: #f8f8f8;
    border-radius: 4px;
    padding: 2px 4px;
    font-family: Consolas, monospace;
    font-size: 0.9em;
}
```

**5. Test the Changes**  
- Run your application and send a query that returns Markdown (e.g., the model often returns bullet points or code blocks if asked).
- Verify that the “Send” button is disabled while the request is in flight.
- Check that the AI response shows nicely formatted Markdown.

### Summary

You only need to:

- Include a Markdown parsing library (like Marked).
- In `appendMessage`, when handling AI messages, use `marked.parse(message)` and `innerHTML` instead of `textContent`.
- Keep the existing logic for disabling the “Send” button intact.