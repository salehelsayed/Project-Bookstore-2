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
