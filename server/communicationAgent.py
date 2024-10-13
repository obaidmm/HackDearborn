from uagents import Agent, Model
import asyncio
import time

# Define the Combined Communication Agent
communication_agent = Agent(
    name="communication_agent",
    port=8000,
    seed="YOUR_COMMUNICATION_AGENT_SECRET_PHRASE",  # Replace with your unique secret phrase
    endpoint=["http://127.0.0.1:8000"]  # Update <127.0.0.1> with the server IP if needed
)

communication_agent_address = "http://127.0.0.1:8000"

class Heartbeat(Model):
    message: str

class TranscriptionMessage(Model):
    transcription: str

# Track the last heartbeat time
last_heartbeat = time.time()
HEARTBEAT_TIMEOUT = 120
emergency_service_address = "fetch1g88yj3wtmjlzyqlwrwx7nl7fxknuzu9cf9wgrj"  # Update with actual address if necessary

@communication_agent.on_message(model=Heartbeat)
async def receive_heartbeat(sender: str, msg: Heartbeat):
    print("Attempting to send transcription message to communication agent")
    global last_heartbeat
    last_heartbeat = time.time()
    print(f"Heartbeat received from {sender}: {msg.message}")

@communication_agent.on_message(model=TranscriptionMessage)
async def receive_transcription(sender: str, msg: TranscriptionMessage):
    print(f"Transcription received from {sender}: {msg.transcription}")
    if "No response, possible emergency." in msg.transcription or not msg.transcription.strip():
        print("No response or empty transcription. Triggering emergency.")
        await trigger_emergency()
    else:
        # Process transcription, for example:
        print(f"Communicating with driver: {msg.transcription}")

async def monitor_heartbeat():
    global last_heartbeat
    try:
        while True:
            if time.time() - last_heartbeat > HEARTBEAT_TIMEOUT:
                await trigger_emergency()
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("Heartbeat monitoring stopped.")

async def trigger_emergency():
    emergency_message = "Driver is unresponsive. Immediate assistance required."
    print(emergency_message)
    # Replace send_message with an existing or simulated function
    await send_emergency_message(emergency_service_address, emergency_message)

# Custom function to send messages (if send_message does not exist)
async def send_emergency_message(address: str, message: str):
    print(f"Sending emergency message to {address}: {message}")
    # Implement actual sending logic if the library supports it, or simulate

async def main():
    # Run the agent's asynchronous loop
    agent_task = asyncio.create_task(communication_agent.run_async())
    try:
        await asyncio.gather(agent_task, monitor_heartbeat())
    except asyncio.CancelledError:
        print("Communication agent shutting down.")
        agent_task.cancel()
        await agent_task

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted and stopped.")
