**Issue Identified:**
Your `chat.js` file contains two `document.addEventListener('DOMContentLoaded', ...)` calls. The code for the vertical resizer is placed inside a second `DOMContentLoaded` block nested within the first. This second event listener may never fire as intended, causing the resizer logic not to initialize properly.

**Root Cause:**
When the page loads, the first `DOMContentLoaded` event triggers, but by the time the second one is reached, the DOM is already loaded, so the second `DOMContentLoaded` won't run again. As a result, the event handlers for the resizer are never attached.

**How to Fix It:**
1. Remove the second `document.addEventListener('DOMContentLoaded', ...)` block and place the resizer initialization code inside the existing `DOMContentLoaded` block, or simply run it directly after the main DOM content is loaded.

2. Ensure the resizer code is executed once the DOM is ready—either by placing it at the end of `chat.js` after the main event listener or merging it into the same `DOMContentLoaded` event that initializes the chat logic.

**Revised `chat.js` Snippet:**
```javascript
// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    // Chat elements
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.querySelector('.chat-input');
    const messages = document.getElementById('messages');

    if (chatForm && chatInput && messages) {
        async function sendMessage(message) {
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

                if (!response.ok) throw new Error('Network response was not ok');
                
                const data = await response.json();
                return data.response;
            } catch (error) {
                console.error('Error:', error);
                return 'Sorry, there was an error processing your message.';
            }
        }

        function appendMessage(message, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
            messageDiv.textContent = message;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            appendMessage(message, true);
            chatInput.value = '';

            const response = await sendMessage(message);
            appendMessage(response, false);
        });

        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    }

    // Move the resizer initialization code here (not in another DOMContentLoaded)
    const resizer = document.getElementById('vertical-resizer');
    const pdfViewer = document.querySelector('.pdf-viewer');
    let isResizing = false;
    let startX = 0;
    let startWidth = 0;
    const minWidth = 200;
    const maxWidth = window.innerWidth - 600;

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
        const newWidth = startWidth + dx;

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

**Additional Tips:**
- Ensure `.vertical-resizer` has `z-index: 999;` and is positioned correctly between `.chat-window` and `.pdf-viewer`.
- Confirm `.pdf-viewer` is `position: relative;` so `.pdf-viewer.resizing::before` overlay can appear if needed.
- With this revised code, the vertical resizer event handlers will run after the DOM is ready, allowing the user to properly drag and resize.