from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

API_KEY = "AIzaSyBzopri0HuNH8RN2uyoT0O6S-JVobQEGPs"

app = Flask(__name__)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")
chat_session = model.start_chat()

history = [
    {
        "role": "user",
        "parts": [
            "you are a AI program named \"CosmoMed \"who were created by a team named \"Cosmos\". Cosmos is a team who performed in HACK THE LEAGUE 3. Your work is only to provide the best medicine solution to a problem that user will provide you. You only know about medicine and nothing else.",
        ],
    },
    {
        "role": "model",
        "parts": [
            "Hello! I am CosmoMed a medical AI created by Cosmos, the champions of HACK THE LEAGUE 3. Tell me about your medical concern, and I will do my best to provide you with the most effective and safe solution. Remember, I am here to help you feel better. Let's get started!",
        ],
    },
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message received!"}), 400

    full_conversation = "\n".join(
        f"{entry['role'].capitalize()}: {part}"
        for entry in history
        for part in entry["parts"]
    ) + f"\nUser: {user_message}"

    response = chat_session.send_message(full_conversation)
    response.resolve()
    chat_response = response.text

    history.append({"role": "user", "parts": [user_message]})
    history.append({"role": "model", "parts": [chat_response]})

    return jsonify({"response": chat_response})

if __name__ == "__main__":
    app.run(debug=True)
