let chatMessages = [];

function addMessage(role, content) {
    chatMessages.push({ role, content });
    const chatMessagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', role);
    messageDiv.textContent = content;
    chatMessagesDiv.appendChild(messageDiv);
    chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const question = userInput.value.trim();
    
    if (question) {
        addMessage('user', question);
        userInput.value = '';

        try {
            const response = await fetch('http://localhost:8000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: question }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            addMessage('bot', data.response);
        } catch (error) {
            console.error('Error:', error);
            addMessage('bot', 'Sorry, I encountered an error while processing your request.');
        }
    }
}

document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
