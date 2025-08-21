from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! 🚀 आपका AI Assistant अब चल रहा है।"

# नया route - user ka message input
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "")

    # फिलहाल simple reply logic
    if "hello" in user_message.lower():
        reply = "Hi! मैं आपका AI Assistant हूँ।"
    elif "tumhara naam" in user_message.lower():
        reply = "मेरा नाम आपका Personal AI Assistant है।"
    else:
        reply = f"आपने कहा: {user_message}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
