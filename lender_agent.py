from uagents import Agent, Context, Protocol
from pyngrok import ngrok

public_url = ngrok.connect(8001)
print("🌐 Public endpoint:", public_url)

lender = Agent(name="LenderAgent", port=8001, endpoint=[public_url])
loan_protocol = Protocol(name="LoanMatcher")


@loan_protocol.on_message
async def receive_request(ctx: Context, sender: str, message: str):
    offer = f"I can lend {message} at 5% interest for 30 days"
    await ctx.send(sender, offer)

lender.include(loan_protocol)

if __name__ == "__main__":
    lender.run()