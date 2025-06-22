from uagents import Agent, Context, Protocol
from pyngrok import ngrok

public_url = ngrok.connect(8001)
print("🌐 Public endpoint:", public_url)

borrower = Agent(name="borrowerAgent", port=8001, endpoint=[public_url])
loan_protocol = Protocol(name="LoanMatcher")

@loan_protocol.on_message
async def handle_offer(ctx: Context, sender: str, message: str):
    ctx.logger.info(f"Borrower received offer: {message}")

borrower.include(loan_protocol)

if __name__ == "__main__":
    borrower.run()