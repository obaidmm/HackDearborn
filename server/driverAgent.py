from uagents import Agent, Context, Model

driver_agent = Agent()

class DriverRequest(Model):
    message: str

@driver_agent.on_message(model=DriverRequest)
async def handle_message(ctx: Context, sender: str, msg: DriverRequest):
    """Log the received message along with its sender"""
    ctx.logger.info(f"Driver received message from {sender}: {msg.message}")

@driver_agent.on_event("startup")
async def send_message(ctx: Context):
    """Send a message to the Bot agent by specifying its address"""
    ctx.logger.info("Driver is about to send a message to the Bot")
    await ctx.send('agent1q0yd9yafuts5pnztzjgz7pwfl4em9dadwnqrrmaqrtamej3k4udd2jac22l', DriverRequest(message="Hello, I need assistance"))
    ctx.logger.info("Message has been sent to the Bot")

if __name__ == "__main__":
    driver_agent.run()
