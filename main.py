from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

# OpenAI key env se lo (Render settings me dala tha)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def home():
    return {"message": "🤖 Aapka AI Assistant ab chal raha hai!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    if not user_message:
        return {"reply": "Kuch likho, main madad karta hoon 🙂"}

    # OpenAI se reply
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        
        messages=[
            {"role": "system", "content": "Tum ek helpful AI ho jo simple Hindi me jawab deta hai."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    reply = response.choices[0].message["content"]
    return {"reply": reply}
    
from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

# OpenAI key env se lo (Render settings me dala tha)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def home():
    return {"message": "🤖 Aapka AI Assistant ab chal raha hai!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    if not user_message:
        return {"reply": "Kuch likho, main madad karta hoon 🙂"}

    # OpenAI se reply
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tum ek helpful AI ho jo simple Hindi me jawab deta hai."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    reply = response.choices[0].message["content"]
    return {"reply": reply}
