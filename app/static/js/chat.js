// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    // Chat elements
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.querySelector('.chat-input');
    const messages = document.getElementById('messages');
    const sendBtn = chatForm ? chatForm.querySelector('.chat-send-btn') : null;
    const sendText = sendBtn ? sendBtn.querySelector('.send-text') : null;
    const spinner = sendBtn ? sendBtn.querySelector('.loading-spinner') : null;

    if (chatForm && chatInput && messages && sendBtn && sendText && spinner) {
        async function sendMessage(message) {
            try {
                // Show loading state
                sendBtn.disabled = true;
                sendBtn.style.opacity = '0.5';
                sendBtn.style.cursor = 'not-allowed';
                sendText.style.display = 'none';
                spinner.style.display = 'inline-block';

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();

                // Reset button state
                sendBtn.disabled = false;
                sendBtn.style.opacity = '1';
                sendBtn.style.cursor = 'pointer';
                sendText.style.display = 'inline';
                spinner.style.display = 'none';

                // Return both response and pages
                return {
                    response: data.response,
                    pages: data.pages || []
                };
            } catch (error) {
                console.error('Error:', error);
                // Reset button state on error
                sendBtn.disabled = false;
                sendBtn.style.opacity = '1';
                sendBtn.style.cursor = 'pointer';
                sendText.style.display = 'inline';
                spinner.style.display = 'none';

                return {
                    response: 'Sorry, there was an error processing your message.',
                    pages: []
                };
            }
        }

        function simulateTypingEffect(aiMessage, pages = [], options = {speed: 1, batchSize: 10}) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', 'ai-message');
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;

            // Extract options with defaults
            const {
                speed = 1,
                batchSize = 500,
                instant = false
            } = options;

            if (instant) {
                const html = marked.parse(aiMessage);
                messageDiv.innerHTML = html;
                
                // Add references if available
                if (pages && pages.length > 0) {
                    const refsDiv = document.createElement('div');
                    refsDiv.classList.add('references');
                    refsDiv.innerHTML = "<strong>References:</strong> " + 
                        pages.map(page => 
                            `<a href="#" class="ref-link" data-page="${page}">Page ${page}</a>`
                        ).join(", ");
                    messageDiv.appendChild(refsDiv);
                }
                
                messages.scrollTop = messages.scrollHeight;
                return;
            }

            let index = 0;
            const chars = aiMessage.split('');

            function typeChar() {
                if (index < chars.length) {
                    const nextChunk = chars.slice(index, index + batchSize).join('');
                    messageDiv.textContent += nextChunk;
                    index += batchSize;
                    messages.scrollTop = messages.scrollHeight;
                    setTimeout(typeChar, speed);
                } else {
                    // Typing finished, now parse Markdown and add references
                    const finalText = messageDiv.textContent;
                    const html = marked.parse(finalText);
                    messageDiv.innerHTML = html;

                    // Add references if available
                    if (pages && pages.length > 0) {
                        const refsDiv = document.createElement('div');
                        refsDiv.classList.add('references');
                        refsDiv.innerHTML = "<strong>References:</strong> " + 
                            pages.map(page => 
                                `<a href="#" class="ref-link" data-page="${page}">Page ${page}</a>`
                            ).join(", ");
                        messageDiv.appendChild(refsDiv);
                    }
                }
            }
            typeChar();
        }
        

        function appendMessageAsUser(message) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', 'user-message');
            messageDiv.textContent = message;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            appendMessageAsUser(message);
            chatInput.value = '';

            const response = await sendMessage(message);
            simulateTypingEffect(response.response, response.pages);
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

        // Add event delegation for reference clicks
        messages.addEventListener('click', (e) => {
            if (e.target.classList.contains('ref-link')) {
                e.preventDefault();
                const page = parseInt(e.target.dataset.page);
                if (!isNaN(page)) {
                    const pdfFrame = document.querySelector('.pdf-frame');
                    if (pdfFrame) {
                        // Update PDF viewer to show the referenced page
                        const currentSrc = pdfFrame.src;
                        const baseUrl = currentSrc.split('#')[0];
                        pdfFrame.src = `${baseUrl}#page=${page}&view=Fit`;
                    }
                }
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

