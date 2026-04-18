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
REQUEST_TIMEOUT = 5

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
ACTIVE_STRATEGY = "breakout_v1"

STRATEGY_PARAMS = {
    "breakout_v1": {
        "ema_fast_period": 9,
        "ema_slow_period": 20,
        "rsi_period": 14,
        "atr_period": 14,
        "ema_gap_threshold": 0.001,
        "atr_expansion_multiplier": 1.2,
        "rsi_threshold": 55,
        "rsi_overheat": 75,
        "breakout_lookback": 3,
        "target_pct": 0.002,
        "stop_loss_pct": 0.0015,
        "signal_age_limit_sec": 15,
    }
}

# =========================
# MARKET DATA CONFIG
# =========================

KLINES_LIMIT = 200
PRIMARY_INTERVAL = "5m"
ENTRY_INTERVAL = "1m"
