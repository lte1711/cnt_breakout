from __future__ import annotations

from config import STRATEGY_ENABLED
from src.strategy_signal import generate_strategy_signal


def evaluate_entry_gate(symbol: str) -> tuple[str, str]:
    if not STRATEGY_ENABLED:
        return "ENTRY_ALLOWED", "strategy_disabled"

    strategy_result = generate_strategy_signal(symbol)
    entry_signal = str(strategy_result.get("entry_signal", "NONE")).upper()
    reason = str(strategy_result.get("reason", "no_reason"))

    if entry_signal != "BUY":
        return "NO_ENTRY_SIGNAL", reason

    return "ENTRY_ALLOWED", "strategy_buy_confirmed"