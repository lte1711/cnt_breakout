from binance.client import Client
import os
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

if not api_key or not api_secret:
    print("ERROR: BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env file")
    sys.exit(1)

try:
    client = Client(api_key, api_secret, testnet=True)
    account = client.get_account()

    print("=== TESTNET ACCOUNT OK ===")
    print("canTrade:", account.get("canTrade"))
    print("accountType:", account.get("accountType"))

    print("=== BALANCES ===")
    for b in account.get("balances", []):
        free = float(b.get("free", 0))
        locked = float(b.get("locked", 0))
        if free > 0 or locked > 0:
            print(b["asset"], "free=", b["free"], "locked=", b["locked"])
except Exception as e:
    print(f"ERROR: Failed to connect to testnet: {e}")
    sys.exit(1)