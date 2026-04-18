import os

# =========================
# BINANCE CONFIG
# =========================

BINANCE_BASE_URL = "https://testnet.binance.vision"
REQUEST_TIMEOUT = 10

# Binance timing protection
RECV_WINDOW = 5000  # ms

# =========================
# API KEY (binance_client 호환 필수)
# =========================

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# (호환 alias)
API_KEY = BINANCE_API_KEY
API_SECRET = BINANCE_API_SECRET

# =========================
# ENGINE CONFIG
# =========================

SYMBOL = "ETHUSDT"

ENABLE_TEST_ORDER_VALIDATION = True

LOG_FILE = "logs/runtime.log"
STATE_FILE = "data/state.json"

# =========================
# STRATEGY ENABLE SWITCH
# =========================

STRATEGY_ENABLED = True

# =========================
# TEST OVERRIDE
# =========================

FORCE_BUY_FOR_TEST = False
FORCE_TARGET_EXIT_TEST = False

# =========================
# MARKET DATA CONFIG
# =========================

KLINES_LIMIT = 200
PRIMARY_INTERVAL = "5m"
ENTRY_INTERVAL = "1m"

# =========================
# INDICATOR CONFIG
# =========================

EMA_FAST_PERIOD = 9
EMA_SLOW_PERIOD = 20
RSI_PERIOD = 14
ATR_PERIOD = 14

# =========================
# STRATEGY THRESHOLDS
# =========================

EMA_GAP_THRESHOLD = 0.001
ATR_EXPANSION_MULTIPLIER = 1.2

ENTRY_RSI_THRESHOLD = 55
ENTRY_RSI_OVERHEAT = 75

BREAKOUT_LOOKBACK = 3

FORCE_PRICE_FOR_TEST = None
