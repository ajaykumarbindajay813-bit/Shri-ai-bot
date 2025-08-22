from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple cache
cache = {}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return {"reply": "Kuch likho, main madad karta hoon 🙂"}

    # Cache check
    if user_message in cache:
        return {"reply": cache[user_message]}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tum ek helpful AI ho jo simple Hindi me jawab deta ho."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=150
        )

        # ✅ Updated line
        reply = response.choices[0].message.content
        cache[user_message] = reply
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Error: API key ya network issue. {str(e)}"}

