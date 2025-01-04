from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from keys.env
load_dotenv("keys.env")

# Fetch the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please check your keys.env file.")

# Initialize the OpenAI client
client = OpenAI()

# Conversation history
conversation = [{"role": "system", "content": "Act like a therapist and have a session with me. Start by asking me typically therapist questions."}]

print("Start chatting with the assistant. Type 'exit' to end the conversation.\n")

while True:
    # Get user input
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    
    # Add user input to conversation history
    conversation.append({"role": "user", "content": user_input})
    
    # Get response from OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    
    # Extract the assistant's reply
    assistant_reply = completion.choices[0].message.content  # Accessing the `content` attribute
    
    # Add the assistant's reply to the conversation history
    conversation.append({"role": "assistant", "content": assistant_reply})
    
    # Print the assistant's reply
    print(f"Assistant: {assistant_reply}\n")
