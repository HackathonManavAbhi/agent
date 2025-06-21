from uagents import Agent, Context, Protocol

# Define a protocol for matching offers
loan_protocol = Protocol(name="LoanMatcher")

# Agent representing the borrower
borrower = Agent(name="BorrowerAgent")

@loan_protocol.on_message
async def handle_offer(ctx: Context, sender: str, message: str):
    ctx.logger.info(f"Borrower received offer from {sender}: {message}")
    # Future: logic to accept or decline offer based on interest rate or duration

# Attach protocol to agent
borrower.include(loan_protocol)

if __name__ == "__main__":
    borrower.run()
