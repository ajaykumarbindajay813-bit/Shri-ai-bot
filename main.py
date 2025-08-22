from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from huggingface_hub import InferenceClient
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

# Hugging Face Access Token - इसे सीधे कोड में न डालें
# बल्कि environment variable का उपयोग करें
HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

# Hugging Face Inference Client - यहाँ अपने मॉडल का नाम डालें
client = InferenceClient(model="google/gemma-2b", token=HF_TOKEN)

# Simple cache
cache = {}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return {"reply": "कुछ तो लिखो, मैं मदद करता हूँ 🙂"}

    # Cache check
    if user_message in cache:
        return {"reply": cache[user_message]}
    
    # यदि टोकन नहीं मिला तो एरर भेजें
    if not HF_TOKEN:
        return {"reply": "Error: Hugging Face Token is not set. Please set the HUGGING_FACE_TOKEN environment variable."}

    try:
        # Hugging Face मॉडल से जवाब प्राप्त करना
        response = client.text_generation(
            prompt=user_message,
            max_new_tokens=150,
            temperature=0.7,
            truncate=True
        )

        reply = response.strip()
        cache[user_message] = reply
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"माफ़ करना, कुछ दिक्कत है: {e}"}

# Serve index.html - इसे सबसे अंत में रखें
app.mount("/", StaticFiles(directory=".", html=True), name="static")
