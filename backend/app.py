from google import genai
from google.genai import types
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyAcncs1Zq_2dqOPVLFaARlssaEYpjw1kHo"
client = genai.Client(api_key=API_KEY)

@app.route("/chat", methods=["POST"])
def chat():
    print("--- MESSAGE RECEIVED ---")
    data = request.get_json()
    user_message = data.get("message", "")
    print(f"User said: {user_message}")

    model_options = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-8b"]
    for model_name in model_options:
        try:
            print(f"Trying model: {model_name}...")
            response = client.models.generate_content(
                model=model_name, 
                contents=user_message
            )
            print(f"Success with {model_name}!")
            return jsonify({"reply": response.text})
        except Exception as e:
            print(f"Failed {model_name}: {e}")
            continue 

    # If all fail, send a friendly local response to Harsh
    return jsonify({"reply": "I'm right here, Harsh. I'm just organizing my thoughts. How can I help you feel better?"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)