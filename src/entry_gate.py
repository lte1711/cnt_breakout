from __future__ import annotations

import time

from config import STRATEGY_ENABLED
from src.models.strategy_signal import StrategySignal
from src.strategy_manager import generate_strategy_signal


def get_entry_signal(symbol: str) -> StrategySignal:
    return generate_strategy_signal(symbol)


def evaluate_entry_gate_from_signal(signal: StrategySignal) -> tuple[str, str]:
    if not STRATEGY_ENABLED:
        return "NO_ENTRY_SIGNAL", "strategy_disabled"

    if not signal.entry_allowed:
        return "NO_ENTRY_SIGNAL", signal.reason

    if signal.side.upper() != "BUY":
        return "NO_ENTRY_SIGNAL", signal.reason

    if signal.signal_age_limit_sec > 0:
        signal_age = time.time() - signal.signal_timestamp
        if signal_age > signal.signal_age_limit_sec:
            return "NO_ENTRY_SIGNAL", "stale_signal"

    return "ENTRY_ALLOWED", signal.reason


def evaluate_entry_gate(symbol: str) -> tuple[str, str]:
    signal = get_entry_signal(symbol)
    return evaluate_entry_gate_from_signal(signal)
