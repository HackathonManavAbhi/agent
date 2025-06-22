from uagents import Agent, Context, Protocol

loan_protocol = Protocol(name="LoanMatcher")

borrower = Agent(name="BorrowerAgent")

@loan_protocol.on_message
async def handle_offer(ctx: Context, sender: str, message: str):
    ctx.logger.info(f"Borrower received offer: {message}")

borrower.include(loan_protocol)

if __name__ == "__main__":
    borrower.run()