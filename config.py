import os

USE_TESTNET = True

if USE_TESTNET:
    BINANCE_BASE_URL = "https://testnet.binance.vision"
else:
    BINANCE_BASE_URL = "https://api.binance.com"

REQUEST_TIMEOUT = 5
SYMBOL = "ETHUSDT"

STATE_FILE = "data/state.json"
LOG_FILE = "logs/runtime.log"

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

RECV_WINDOW = 5000

ENABLE_TEST_ORDER_VALIDATION = False