Below are step-by-step instructions and code snippets to achieve the desired functionality. We will:

1. Show a "thinking" or "loading" state in the "Send" button while awaiting the server’s response.
2. Display the AI's response character-by-character (simulate typing) instead of all at once.

**Files Involved:**  
- `chat.html` (to add a spinner icon or text in the send button markup)
- `chat.css` (for spinner styling)
- `chat.js` (to implement the logic for the spinner state and simulated typing)

We assume the backend returns the full message after processing. Since we do not have true streaming from the server, we will simulate a typing effect after receiving the entire message.

### 1. Add a Spinner or Loading Indicator to `chat.html`

Add a placeholder element (e.g., `<span class="loading-spinner"></span>`) inside the send button that we can show/hide:

```html
<!-- In chat.html -->
<form class="chat-input-form" id="chatForm">
    <textarea class="chat-input" name="user_query" rows="1" placeholder="Ask any question about the book..."></textarea>
    <button type="submit" class="chat-send-btn">
        <span class="send-text">Send</span>
        <span class="loading-spinner" style="display:none;"></span>
    </button>
</form>
```

### 2. Spinner CSS in `chat.css`

Add styles for the `.loading-spinner`:

```css
.loading-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid #fff;
    border-top: 2px solid #3182CE;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-left: 8px;
    vertical-align: middle;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* While button is "thinking", 
   you can also dim the send-text or hide it */
```

### 3. Adjust `chat.js` to Show Spinner and Simulate Typing

- When the user sends a message, show the spinner and hide the "Send" text.
- When the response returns, simulate typing by gradually appending characters to the message container.

**Updated `chat.js`:**

```javascript
// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.querySelector('.chat-input');
    const messages = document.getElementById('messages');
    const sendBtn = chatForm ? chatForm.querySelector('.chat-send-btn') : null;
    const sendText = sendBtn ? sendBtn.querySelector('.send-text') : null;
    const spinner = sendBtn ? sendBtn.querySelector('.loading-spinner') : null;

    if (chatForm && chatInput && messages && sendBtn && sendText && spinner) {
        async function sendMessage(message) {
            try {
                // Disable send button to prevent multiple submissions
                sendBtn.disabled = true;
                sendBtn.style.opacity = '0.5';
                sendBtn.style.cursor = 'not-allowed';

                // Show spinner, hide "Send"
                sendText.style.display = 'none';
                spinner.style.display = 'inline-block';

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

                // After receiving response, hide spinner, show "Send" text
                sendText.style.display = 'inline';
                spinner.style.display = 'none';

                if (!response.ok) throw new Error('Network response was not ok');
                
                const data = await response.json();

                // Re-enable the send button after response
                sendBtn.disabled = false;
                sendBtn.style.opacity = '1';
                sendBtn.style.cursor = 'pointer';

                return data.response;
            } catch (error) {
                console.error('Error:', error);

                // Even if error occurs, re-enable send button
                sendBtn.disabled = false;
                sendBtn.style.opacity = '1';
                sendBtn.style.cursor = 'pointer';

                sendText.style.display = 'inline';
                spinner.style.display = 'none';

                return 'Sorry, there was an error processing your message.';
            }
        }

        function simulateTypingEffect(aiMessage) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', 'ai-message');
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;

            let index = 0;
            const speed = 900000; // typing speed in ms
            const chars = aiMessage.split('');

            function typeChar() {
                if (index < chars.length) {
                    // Append next character as plain text
                    messageDiv.textContent += chars[index];
                    index++;
                    messages.scrollTop = messages.scrollHeight;
                    setTimeout(typeChar, speed);
                } else {
                    // Typing finished, now parse Markdown
                    const finalText = messageDiv.textContent;
                    const html = marked.parse(finalText);
                    messageDiv.innerHTML = html;
                    // Now the message is shown with proper Markdown formatting
                }
    }
    typeChar();
}


        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            appendMessageAsUser(message);
            chatInput.value = '';

            const response = await sendMessage(message);
            simulateTypingEffect(response);
        });

        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });

        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }

    // Resizer functionality as before
    const resizer = document.getElementById('vertical-resizer');
    const pdfViewer = document.querySelector('.pdf-viewer');
    let isResizing = false;
    let startX = 0;
    let startWidth = 0;
    const minWidth = 200;
    const maxWidth = window.innerWidth - 600;

    if (resizer && pdfViewer) {
        resizer.addEventListener('mousedown', (e) => {
            e.preventDefault();
            isResizing = true;
            pdfViewer.classList.add('resizing');
            startX = e.clientX;
            startWidth = pdfViewer.offsetWidth;
            document.body.style.cursor = 'col-resize';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            e.preventDefault();
            const dx = e.clientX - startX;
            const newWidth = startWidth - dx;

            if (newWidth > minWidth && newWidth < maxWidth) {
                pdfViewer.style.width = `${newWidth}px`;
            }
        });

        document.addEventListener('mouseup', (e) => {
            if (isResizing) {
                e.preventDefault();
                isResizing = false;
                pdfViewer.classList.remove('resizing');
                document.body.style.cursor = 'default';
            }
        });
    }

    // Toggle sidebar functionality
    const toggleSidebarBtn = document.getElementById('toggleSidebar');
    const sidebar = document.querySelector('.sidebar');
    
    if (toggleSidebarBtn && sidebar) {
        toggleSidebarBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            toggleSidebarBtn.textContent = sidebar.classList.contains('collapsed') ? 'Show Sidebar' : 'Hide Sidebar';
        });
    }
});
```

### Explanation of Changes

1. **Spinner on "Send" button:**  
   We added a `.loading-spinner` span inside the send button in `chat.html`.  
   In `chat.js`, when a message is sent, we hide the "Send" text and show the spinner by adjusting their `display` properties. Once the response is back, we revert the button to normal state.

2. **Typing simulation:**  
   Instead of directly inserting the full AI response into the `.ai-message`, we introduced a `simulateTypingEffect(response)` function that:
   - Creates a `.ai-message` div.
   - Iterates over each character in `response`.
   - Appends them one-by-one with a delay (controlled by `speed`).
   
   This simulates a "typing" effect for the AI’s response.

### Potential Adjustments

- You may tweak the typing `speed` variable to make the typing appear faster or slower.
- If the response is large, consider a small optimization like adding characters in batches of a few characters at a time rather than one-by-one to improve performance and realism.

With these changes, the user will see the "Send" button reflect a "thinking" state while waiting for the server's response, and once the response is received, they’ll see the message appear as though it's being typed out character-by-character.