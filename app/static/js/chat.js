// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.querySelector('.chat-input');
    const sendButton = document.querySelector('.send-button');
    const chatMessages = document.querySelector('.chat-messages');

    if (!chatInput || !sendButton || !chatMessages) return;

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
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendButton.addEventListener('click', async () => {
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
            sendButton.click();
        }
    });
});
