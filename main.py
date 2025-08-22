from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from huggingface_hub import InferenceClient
import os

app = FastAPI()

# ============================
# CORS setup
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Hugging Face Client Setup
# ============================
HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("❌ Error: HUGGING_FACE_TOKEN environment variable not set")

# यहां आप अपना मॉडल बदल सकते हैं
client = InferenceClient(model="google/gemma-2b", token=HF_TOKEN)

# ============================
# Simple cache
# ============================
cache = {}

# ============================
# Chat API
# ============================
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return {"reply": "कुछ तो लिखो, मैं मदद करता हूँ 🙂"}

    # Cache check
    if user_message in cache:
        return {"reply": cache[user_message]}

    try:
        # Hugging Face मॉडल से जवाब
        response = client.text_generation(
            user_message,
            max_new_tokens=150,
            temperature=0.7
        )

        # कभी string आता है, कभी dict → दोनों handle करो
        reply = response if isinstance(response, str) else str(response)

        cache[user_message] = reply
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"माफ़ करना, कुछ दिक्कत है: {e}"}

# ============================
# Serve index.html
# ============================
app.mount("/", StaticFiles(directory=".", html=True), name="static")
