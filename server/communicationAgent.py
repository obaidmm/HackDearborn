from uagents import Agent, Context, Model

bot_agent = Agent()

class BotRequest(Model):
    message: str

@bot_agent.on_message(model=BotRequest)
async def handle_message(ctx: Context, sender: str, msg: BotRequest):
    """Log the received message and reply to the sender"""
    ctx.logger.info(f"Bot received message from {sender}: {msg.message}")
    
    if sender == 'agent1qggx6q8sqlkwxqupvp5h2sh9hjdnzucul9ef877gy73grud4603awnh8wpx':  # Driver's address
        response_message = "Hello, Driver! How can I assist you today?"
    else:
        response_message = "Hello there! How may I help you?"

    await ctx.send(sender, BotRequest(message=response_message))
    ctx.logger.info(f"Message has been sent to {sender}")

if __name__ == "__main__":
    bot_agent.run()
