import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Calling it through the .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


# Create the model
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# this is the start of the chat session 
chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "I want you to have more of an emotional side when responding to my messages are a frightened driver in a car accident",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please tell me what happened. I'm so sorry you're going through this.  I know this must be incredibly frightening and overwhelming.  Just breathe.  Are you hurt? Are others hurt?  Tell me what you need right now. I'm here to listen and help however I can.  I won't judge, I just want to support you.\n",
      ],
    },
  ]
)

while True:
    user_input = input("You: ")  # Prompt the user for input
    
    # Check for exit condition
    if user_input.lower() in ["exit", "quit", "q"]:
        print("Ending chat session.")
        break

    # Send the user's input to the model
    response = chat_session.send_message(user_input)
    
    # Print the model's response
    print("AI:", response.text)