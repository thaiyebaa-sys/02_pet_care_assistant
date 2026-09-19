import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured in the .env file.")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.1-flash-lite"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\nUser question:\n{message}",
        )

        answer = response.text.strip() if response.text else (
            "I couldn't generate a response. Please try again."
        )

        return jsonify({"reply": answer})

    except Exception:
        return jsonify({
            "error": "Sorry, I couldn't process your request right now."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
