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
SIGNAL_LOG_FILE = "logs/signal.log"
STRATEGY_METRICS_FILE = "data/strategy_metrics.json"
PERFORMANCE_SNAPSHOT_FILE = "data/performance_snapshot.json"
LIVE_GATE_DECISION_FILE = "data/live_gate_decision.json"

# =========================
# STRATEGY ENABLE SWITCH
# =========================

STRATEGY_ENABLED = True
ACTIVE_STRATEGY = "breakout_v1"
ACTIVE_STRATEGIES = [
    "breakout_v1",
    "pullback_v1",
]
# mean_reversion_v1 is registered and parameterized, but remains inactive by default
# until separate activation validation is completed.

STRATEGY_PARAMS = {
    "breakout_v1": {
        "ema_fast_period": 9,
        "ema_slow_period": 20,
        "rsi_period": 14,
        "atr_period": 14,
        "ema_gap_threshold": 0.001,
        "atr_expansion_multiplier": 1.05,
        "rsi_threshold": 53,
        "rsi_overheat": 75,
        "breakout_lookback": 3,
        "target_pct": 0.002,
        "stop_loss_pct": 0.0015,
        "signal_age_limit_sec": 15,
    },
    "pullback_v1": {
        "ema_fast_period": 9,
        "ema_slow_period": 20,
        "rsi_period": 14,
        "pullback_rsi_max": 52,
        "pullback_rsi_min": 40,
        "target_pct": 0.0018,
        "stop_loss_pct": 0.0015,
        "signal_age_limit_sec": 15,
    },
    "mean_reversion_v1": {
        "ema_period": 20,
        "rsi_period": 14,
        "rsi_oversold": 35,
        "target_pct": 0.0015,
        "stop_loss_pct": 0.0015,
        "signal_age_limit_sec": 15,
    },
}

# =========================
# MARKET DATA CONFIG
# =========================

KLINES_LIMIT = 200
PRIMARY_INTERVAL = "5m"
ENTRY_INTERVAL = "1m"

# =========================
# RISK CONFIG
# =========================

MAX_DAILY_LOSS_COUNT = 3
MAX_CONSECUTIVE_LOSSES = 3
LOSS_COOLDOWN_MINUTES = 60

# =========================
# STAGE 2 EXIT CONFIG
# =========================

TRAILING_STOP_PCT = 0.01
TIME_EXIT_MINUTES = 240
ENABLE_PARTIAL_EXIT = True

# =========================
# V2 PORTFOLIO CONFIG
# =========================

PORTFOLIO_STATE_FILE = "data/portfolio_state.json"
PORTFOLIO_LOG_FILE = "logs/portfolio.log"
PORTFOLIO_STATE_SCHEMA_VERSION = "2.0"
MAX_PORTFOLIO_EXPOSURE = 1000.0
ONE_PER_SYMBOL_POLICY = True

# =========================
# PERFORMANCE TUNING CONFIG
# =========================

RANKER_MINIMUM_SAMPLE = 5
RANKER_EXPECTANCY_WEIGHT = 1.5
RANKER_TREND_ALIGNMENT_BONUS = 0.08
RANKER_VOLATILITY_PENALTY = 0.05
RANKER_RECENT_LOSS_PENALTY = 0.12
STRATEGY_STATIC_BASE_SCORES = {
    "breakout_v1": 1.0,
    "pullback_v1": 0.95,
    "mean_reversion_v1": 0.9,
}
AUTO_VALIDATION_MINUTES = 5
