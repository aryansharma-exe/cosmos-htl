from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Gemini API key
API_KEY = 'AIzaSyBzopri0HuNH8RN2uyoT0O6S-JVobQEGPs'
API_URL = 'https://api.google.com/gemini/v1.5/generate'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

@app.route('/')
def index():
    return "Welcome to the Gemini Chatbot!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "Please provide a message"}), 400

    data = {
        'prompt': user_input,
        'max_tokens': 150
    }

    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code != 200:
        return jsonify({"error": "Error communicating with the Gemini API"}), response.status_code

    result = response.json()
    bot_response = result['choices'][0]['text']

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)