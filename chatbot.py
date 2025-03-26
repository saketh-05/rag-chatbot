# Smart Personal Chatbot using FastAPI and Gemini API
# api AIzaSyANr0kkCj6_dnA6j7n5niYdjDeKPNBh-zI

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for CORS
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

genai.configure(api_key="AIzaSyANr0kkCj6_dnA6j7n5niYdjDeKPNBh-zI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Define request body schema
class ChatRequest(BaseModel):
    message: str

# Route for chatbot conversation
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Call OpenAI API to generate a response
        response = model.generate_content(request.message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
