Below is a modified version of your **current `chat.js`** code that integrates the button disabling logic. This ensures that once the user sends a message, the "Send" button becomes disabled until a response is received. The rest of the code remains consistent with what you currently have, just adding the necessary changes to disable and re-enable the send button.

**Modified `chat.js`:**

```javascript
// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    // Chat elements
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.querySelector('.chat-input');
    const messages = document.getElementById('messages');
    const sendBtn = chatForm ? chatForm.querySelector('.chat-send-btn') : null;

    if (chatForm && chatInput && messages && sendBtn) {
        async function sendMessage(message) {
            try {
                // Disable send button to prevent multiple submissions
                sendBtn.disabled = true;
                sendBtn.style.opacity = '0.5';
                sendBtn.style.cursor = 'not-allowed';

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

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

                return 'Sorry, there was an error processing your message.';
            }
        }

        function appendMessage(message, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', isUser ? 'user-message' : 'ai-message');
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

        chatInput.addEventListener('input', function() {
            // Reset height to 'auto' to correctly measure the new scrollHeight
            this.style.height = 'auto';
            
            // Set the textarea's height to its scrollHeight (or maxed at max-height by CSS)
            this.style.height = this.scrollHeight + 'px';
        });
    }

    // Resizer functionality
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
            // Invert logic so moving left increases width:
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

**What Changed?**

- Added a reference to the `.chat-send-btn` from the `chatForm`.
- Disabled the send button upon sending a message.
- Re-enabled the send button after receiving a response or encountering an error.
- Added some styling changes (opacity, cursor) for visual feedback while disabled.

This ensures the user cannot send another message until a response returns, providing a better user experience.