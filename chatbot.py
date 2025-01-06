# Smart Personal Chatbot using FastAPI and OpenAI API
# api AIzaSyANr0kkCj6_dnA6j7n5niYdjDeKPNBh-zI


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import google.generativeai as genai
import uvicorn
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

genai.configure(api_key="AIzaSyANr0kkCj6_dnA6j7n5niYdjDeKPNBh-zI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Define request body schema
class ChatRequest(BaseModel):
    message: str

@app.get("/chat")
async def root():
    html_content = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #e9ecef;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        #chatbot-container {
            width: 400px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        #chatbot-header {
            background-color: #4caf50;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 1.2em;
        }

        #chatbot-messages {
            height: 300px;
            overflow-y: auto;
            padding: 10px;
            border-top: 1px solid #e0e0e0;
            border-bottom: 1px solid #e0e0e0;
            background-color: #f9f9f9;
        }

        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            max-width: 80%;
        }

        .user-message {
            background-color: #d1e7dd;
            align-self: flex-end;
            margin-left: auto;
        }

        .bot-message {
            background-color: #f1f1f1;
            align-self: flex-start;
        }

        #user-input {
            display: flex;
            padding: 10px;
            background-color: #ffffff;
            border-top: 1px solid #e0e0e0;
        }

        #message-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            margin-right: 10px;
        }

        #send-button {
            padding: 10px 15px;
            background-color: #4caf50;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        #send-button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div id="chatbot-container">
        <div id="chatbot-header">Chatbot</div>
        <div id="chatbot-messages">
            <!-- Chatbot messages will be dynamically added here -->
        </div>
        <div id="user-input">
            <input type="text" id="message-input" placeholder="Type your message..." autocomplete="off">
            <button id="send-button">Send</button>
        </div>
    </div>

    <script>
        const chatbotMessages = document.getElementById('chatbot-messages');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        function formatChatbotReply(reply) {
    // Convert Markdown bold and italics to HTML
    let formattedReply = reply
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>') // Convert **text** to <b>text</b>
        .replace(/\*(.*?)\*/g, '<i>$1</i>') // Convert *text* to <i>text</i>
        .replace(/_(.*?)_/g, '<i>$1</i>') // Convert _text_ to <i>text</i>
        .replace(/`(.*?)`/g, '<code>$1</code>') // Convert `code` to <code>code</code>
        .replace(/'''(.*?)'''/g, '<code>$1</code>') // Convert '''code''' to <code>code</code>
        .replace(/\*/g, '</br>')
        .replace(/\.\s/g, '</br>');
        
        
    // Convert Markdown links to HTML
    // try{
    //    formattedReply = new DOMParser().parseFromString(formattedReply, 'text/html').body.textContent; // Sanitize HTML
    // } catch (e) {
    //     console.error('Error formatting chatbot reply:', e);
    // }
    
    return formattedReply;
}
        sendButton.addEventListener('click', () => {
            const message = messageInput.value.trim();
            if (message === '') return;

            // Display user message
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.textContent = message;
            chatbotMessages.appendChild(userMessage);
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to bottom
            console.log(message);
            
            // Send the message to the backend for processing
            fetch('/chat', {
                method: 'POST',
                body: JSON.stringify({ message }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                chatbotMessages.innerHTML += `<div class="message bot-message">${formatChatbotReply(data.response)}</div>`;
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to bottom
            })
            .catch(error => {
                console.error('Error:', error);
            });

            messageInput.value = '';
        });

        // Optional: Allow sending message with Enter key
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendButton.click();
            }
        });
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)

# Route for chatbot conversation
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Call OpenAI API to generate a response
        response = model.generate_content(request.message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
