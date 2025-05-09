from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from keys.env
load_dotenv("keys.env")

# Fetch the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please check your keys.env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Read system prompt from a file
with open("trustgolfprompt.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()

# Initialize conversation with system prompt
conversation = [{"role": "system", "content": system_prompt}]

@app.route('/chat', methods=['POST'])
def chat():
    global conversation
    # Get user input from the frontend
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Add the user input to the conversation
    conversation.append({"role": "user", "content": user_input})

    try:
        # Get response from OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation
        )

        # Extract the assistant's reply
        assistant_reply = completion.choices[0].message.content

        # Add the assistant's reply to the conversation
        conversation.append({"role": "assistant", "content": assistant_reply})

        # Limit conversation history to the last 10 messages
        if len(conversation) > 10:
            conversation = conversation[-10:]

        return jsonify({"reply": assistant_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Specify a different port (e.g., 5001)
    app.run(debug=True, port=5001)
