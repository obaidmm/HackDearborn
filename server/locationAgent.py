import requests
from uagents import Agent, Context
import time
import math

# Initialize the Location-Based Agent
agent = Agent()

MY_WALLET_ADDRESS = "fetch1___"  # Replace with your actual Fetch.ai wallet address
DECELERATION_THRESHOLD = -5  # Threshold for sudden deceleration (m/s^2); adjust as needed

initial_speed = 20  # Initial speed in m/s
initial_location = (40.7128, -74.0060)  # Example starting coordinates (latitude, longitude)
initial_time = time.time()  # Current time in seconds

def get_current_location():
    """Simulate getting current location data; replace with actual GPS location data in real application"""
    return (40.7129, -74.0059)  # Adjusted coordinates for testing

def calculate_speed(prev_location, current_location, time_interval):
    """Calculate speed based on change in location over time interval"""
    lat1, lon1 = prev_location
    lat2, lon2 = current_location
    R = 6371000  # Radius of the Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distance in meters

    return distance / time_interval if time_interval > 0 else 0

@agent.on_interval(period=60)
async def monitor_speed(ctx: Context):
    """Check for rapid deceleration and alert another agent if detected"""
    global initial_speed, initial_location, initial_time

    current_location = get_current_location()
    current_time = time.time()
    time_interval = current_time - initial_time

    current_speed = calculate_speed(initial_location, current_location, time_interval)
    deceleration = current_speed - initial_speed  # Change in speed

    if deceleration < DECELERATION_THRESHOLD:
        ctx.logger.info(f"Sudden deceleration detected: {deceleration} m/s^2")

        alert_message = f"Rapid deceleration detected! Current speed: {current_speed} m/s"
        if MY_WALLET_ADDRESS != "fetch1___":
            await ctx.send_wallet_message(MY_WALLET_ADDRESS, alert_message)
        else:
            ctx.logger.info("Set 'MY_WALLET_ADDRESS' to your actual wallet address to receive alerts.")
        
    else:
        ctx.logger.info("No rapid deceleration detected.")

    initial_speed = current_speed
    initial_location = current_location
    initial_time = current_time

    ctx.logger.info("Simulating a sudden deceleration for testing.")
    initial_speed = 100 
    current_speed = 5
    deceleration = current_speed - initial_speed
    if deceleration < DECELERATION_THRESHOLD:
        ctx.logger.info(f"Test Deceleration: {deceleration} m/s^2 - Alert should trigger.")
        alert_message = f"Test: Rapid deceleration detected! Current speed: {current_speed} m/s"
        await ctx.send_wallet_message(MY_WALLET_ADDRESS, alert_message)

if __name__ == "__main__":
    agent.run()
