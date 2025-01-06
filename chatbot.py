# Smart Personal Chatbot using FastAPI and OpenAI API
# api AIzaSyANr0kkCj6_dnA6j7n5niYdjDeKPNBh-zI


from fastapi import FastAPI, Request
import google.generativeai as genai
import uvicorn
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

genai.configure(api_key="API")
model = genai.GenerativeModel("gemini-1.5-flash")

# Define request body schema
class ChatRequest(BaseModel):
    user_message: str

# Route for chatbot conversation
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Call OpenAI API to generate a response
        response = model.generate_content(request.user_message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
