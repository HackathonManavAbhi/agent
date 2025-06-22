from gettext import translation
import requests
import base64
import os
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.instruction import Instruction
from solders.system_program import transfer, TransferParams

load_dotenv()
client = Client(os.getenv("SOLANA_RPC"))

kp = Keypair()
secret_64 = kp.to_bytes()  # returns 64-byte seed + pubkey
secret_b64 = base64.b64encode(secret_64).decode()

print("📛 Public Key:", kp.pubkey())
pubkey_str = str(kp.pubkey())

try:
    airdrop = client.request_airdrop(pubkey_str, 1_000_000_000)
    print("🚰 Airdrop sent. TX:", airdrop)

    sig = airdrop["result"]
    confirm = client.confirm_transaction(sig)
    print("✅ Airdrop confirmed:", confirm)

except Exception as e:
    print("❌ Error during airdrop:", e)

# print("\n")
# print("\n")
# print("Public Key:", kp.pubkey())
# print("Base64 Secret Key:", secret_b64)

# wallet = load_wallet_from_secret(secret_b64)
# # balance = get_wallet_balance(wallet.pubkey())

# airdrop = client.request_airdrop(str(wallet.pubkey()), 1_000_000_000)  # 1 SOL
# client.confirm_transaction(airdrop["result"])

# balance = get_wallet_balance(wallet.pubkey())
# print("🔄 Updated balance:", balance, "SOL")

# print("\n")
# print("\n")
# print("Balance:", balance, "SOL")

def load_wallet_from_secret(secret_b64: str) -> Keypair:
    secret_bytes = base64.b64decode(secret_b64)
    return Keypair.from_bytes(secret_bytes)

def get_wallet_balance(pubkey: Pubkey) -> float:
    result = client.get_balance(pubkey)
    # print("Lamports:", result)
    if 'result' not in result:
        raise Exception(f"Error fetching balance: {result['error']}")
    lamports = result['result']['value']
    return lamports / 1_000_000_000

# Transfer SOL from one wallet to another
def call_solana_wallet_api(from_wallet: Keypair, to_address: str, amount_sol: float) -> dict:
    to_pubkey = Pubkey.from_string(to_address)
    lamports = int(amount_sol * 1_000_000_000)

    txn = translation()
    txn.add(
        transfer(
            TransferParams(
                from_pubkey=from_wallet.pubkey(),
                to_pubkey=to_pubkey,
                lamports=lamports
            )
        )
    )

    try:
        result = client.send_transaction(txn, from_wallet)
        return result
    except Exception as e:
        return {"error": str(e)}


def call_solana_wallet_api(from_address: str, to_address: str, amount_sol: float, api_url: str, api_key: str = None) -> dict:
    """
    Calls an external API to trigger a Solana wallet transaction.

    Args:
        from_address (str): Sender's public wallet address.
        to_address (str): Recipient's public wallet address.
        amount_sol (float): Amount in SOL to transfer.
        api_url (str): Full endpoint URL for the transfer API.
        api_key (str, optional): Optional API key for authentication.

    Returns:
        dict: Response from the API call (JSON or error).
    """
    payload = {
        "from": from_address,
        "to": to_address,
        "amount": amount_sol
    }

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}


# def load_wallet_from_secret(secret_b64: str):
#     secret_key = base64.b64decode(secret_b64)
#     keypair = Keypair.from_secret_key(secret_key)
#     return keypair

# def get_wallet_balance(pubkey_str: str):
#     return client.get_balance(pubkey_str)['result']['value'] / 1_000_000_000  # Convert lamports to SOL


def transfer_sol(sender_kp, to_pubkey_str: str, amount_sol: float):
    txn = Transaction()
    txn.add(
        transfer(
            TransferParams(
                from_pubkey=sender_kp.public_key,
                to_pubkey=PublicKey(to_pubkey_str),
                lamports=int(amount_sol * 1_000_000_000)
            )
        )
    )
    result = client.send_transaction(txn, sender_kp)
    return result

# if __name__ == "__main__":
#     import sys
#     get_wallet_balance(secret_b64)