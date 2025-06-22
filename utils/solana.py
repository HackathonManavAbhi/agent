import requests
import base64
import os
from dotenv import load_dotenv
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey

load_dotenv()
client = Client(os.getenv("SOLANA_RPC"))

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


def load_wallet_from_secret(secret_b64: str):
    secret_key = base64.b64decode(secret_b64)
    keypair = Keypair.from_secret_key(secret_key)
    return keypair

def get_wallet_balance(pubkey_str: str):
    return client.get_balance(pubkey_str)['result']['value'] / 1_000_000_000  # Convert lamports to SOL


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