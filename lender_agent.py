from uagents import Agent, Context, Protocol

loan_protocol = Protocol(name="LoanMatcher")

lender = Agent(name="LenderAgent")

@loan_protocol.on_message
async def receive_request(ctx: Context, sender: str, message: str):
    ctx.logger.info(f"Lender received request: {message}")

    # Compose offer
    offer = f"I can lend {message} at 5% interest for 30 days"
    await ctx.send(sender, offer)

lender.include(loan_protocol)

if __name__ == "__main__":
    lender.run()
# This code defines a LenderAgent that listens for loan requests and sends back an offer.
# The agent uses the uagents framework to handle communication and protocol management.
# The LenderAgent can be used in a multi-agent system where it interacts with BorrowerAgents.
# The agent listens for messages on the "LoanMatcher" protocol and responds with a lending offer.
# The LenderAgent can be used in a multi-agent system where it interacts with BorrowerAgents.