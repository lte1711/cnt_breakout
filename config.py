import os
from pathlib import Path


def _load_dotenv() -> None:
    dotenv_path = Path(__file__).resolve().parent / ".env"

    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"\"", "'"}:
            value = value[1:-1]

        os.environ.setdefault(key, value)


_load_dotenv()

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

# Supports both OS environment variables and repo-root .env values.
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
