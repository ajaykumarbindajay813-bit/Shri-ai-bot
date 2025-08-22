from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()

# CORS allow all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Serve index.html and static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    if not user_message:
        return {"reply": "Kuch likho, main madad karta hoon 🙂"}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tum ek helpful AI ho jo simple Hindi me jawab deta hai."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Error: {str(e)}"

    return {"reply": reply}
