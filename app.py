from flask import Flask, request, jsonify, render_template
import requests
import json
import os
from dotenv import load_dotenv
from waitress import serve

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Use environment variable for the API key if available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY. Please check your .env file.")

# Load previous conversations from JSON file
def load_conversations():
    try:
        with open("conversations.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save conversations to JSON file
def save_conversations(conversations):
    with open("conversations.json", "w") as f:
        json.dump(conversations, f, indent=4)

# Function to get response from Gemini AI
def get_response_from_gemini(query):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

        headers = {
            "Content-Type": "application/json"
        }

        system_prompt = (
            "You are a friendly, caring, and expert therapist who suggests therapies "
            "based on a person's age, weight, and specific problems. Your task is to "
            "suggest the top 3 therapies tailored to the individual's age, weight, and issues. "
            "For each therapy, provide a 10-word explanation of its importance."
        )

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        { "text": f"{system_prompt}\n\nUser: {query}" }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 200
            }
        }

        print("Sending payload to Gemini:", json.dumps(payload, indent=2))

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        # Handle Gemini response
        if "candidates" in data and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            return candidate.get("content", {}).get("parts", [{}])[0].get("text", "No response text found.")
        return "No valid response from Gemini AI."

    except requests.exceptions.RequestException as e:
        print(f"Gemini AI API Error: {e}")
        return f"Gemini AI Error: {str(e)}"
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return f"Unexpected Error: {str(e)}"

# Flask route to handle queries
@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json["query"]
        response_text = get_response_from_gemini(user_input)

        conversations = load_conversations()
        conversations.append({"query": user_input, "response": response_text})
        save_conversations(conversations)

        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

# Root route
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    print("Starting server on http://0.0.0.0:8000")
    serve(app, host="0.0.0.0", port=8000)
