from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)
client.API_URL = "https://testnet.binance.vision/api"

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