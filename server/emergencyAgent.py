from uagents import Agent, Model
import asyncio
import time

# Initialize the bot agent
bot_agent = Agent(name="bot_agent")

class BotRequest(Model):
    message: str

# Simulate driver activity by sending regular messages to the Bot Agent
async def simulate_driver_activity():
    while True:
        driver_message = "Driver is checking in."
        print("Simulated Driver: Sending message to Bot Agent.")
        
        # Use a generic event emitter function; replace it with the actual method.
        await emit_event_to_agent(bot_agent, "simulated_driver", BotRequest(message=driver_message))
        
        # Wait for a specified interval before sending the next simulated message
        await asyncio.sleep(60)  # Sends a message every 60 seconds to simulate driver check-ins

# Placeholder for emitting events to another agent; replace with actual function
async def emit_event_to_agent(agent, recipient, message):
    # Placeholder method; replace this with actual message or event emitter
    print(f"Sending message to {recipient}: {message.message}")

@bot_agent.on_message(model=BotRequest)
async def handle_message(sender: str, msg: BotRequest):
    """Log the received message and reply to the sender"""
    print(f"Bot received message from {sender}: {msg.message}")
    
    # Respond based on the sender's address
    if sender == 'simulated_driver':  # Simulated driver's address
        response_message = "Hello, Driver! How can I assist you today?"
    else:
        response_message = "Hello there! How may I help you?"

    # Log and print the response
    print(f"Response to Driver: {response_message}")

    # Send a heartbeat to the Emergency Monitor Agent
    emergency_monitor_address = "agent1qdg79kh8srwwly0dp9zcn2r240nnfcs4s4rj2wwk7rh438mncefsucj0c7c"  # Replace with Emergency Monitor Agent's address
    await emit_event_to_agent(bot_agent, emergency_monitor_address, BotRequest(message="Driver is responsive"))
    print("Heartbeat message sent to Emergency Monitor Agent")

if __name__ == "__main__":
    # Run the bot agent and start simulating driver activity
    bot_agent.run()
    asyncio.run(simulate_driver_activity())
