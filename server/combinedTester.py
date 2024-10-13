import os
from dotenv import load_dotenv
import google.generativeai as genai
from uagents import Agent, Model
import asyncio
# import google.cloud as speech # Import the Google Cloud Speech-to-Text library

# Load environment variables
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure the generation settings
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 50,
  "response_mime_type": "text/plain",
}

# Initialize the Gemini model
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,
)

# Create the main agent
bot_agent = Agent()

# Define the BotRequest model
class BotRequest(Model):
    message: str

# Define how the bot handles messages
@bot_agent.on_message(model=BotRequest)
async def handle_message(ctx, sender: str, msg: BotRequest):
    """Log the received message and reply to the sender"""
    print(f"[Agent] Received message from {sender}: {msg.message}")
    
    # Check if the message is from the driver
    if sender == 'agent1qggx6q8sqlkwxqupvp5h2sh9hjdnzucul9ef877gy73grud4603awnh8wpx':  # Driver's address
        # Indicate the agent is about to contact Gemini
        print("[Agent] Processing message with Gemini model for emotional response...")
        
        # Send the driver's message to Gemini for an emotional response
        response = chat_session.send_message(msg.message)
        response_message = f"[Gemini Response] {response.text}"  # Tag Gemini's response
    else:
        # Default response for other users
        response_message = "[Agent Response] Hello there! How may I help you?"

    # Print the final response being sent back for clarity
    print(f"[Agent] Sending response to {sender}: {response_message}")

    # Send the response back to the sender (print it out for this example)
    print("AI:", response_message)

# Interactive terminal loop for testing
async def main():
    print("Starting interactive session. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")  # Prompt the user for input
        
        # Check for exit condition
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Ending chat session.")
            break

        # Simulate the driver's address and call the handler
        sender = 'agent1qggx6q8sqlkwxqupvp5h2sh9hjdnzucul9ef877gy73grud4603awnh8wpx'  # Simulated driver's address
        msg = BotRequest(message=user_input)

        # Call the handle_message function asynchronously
        await handle_message(None, sender, msg)

# Start the chat session with initial context (no history)
chat_session = model.start_chat()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
