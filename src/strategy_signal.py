from __future__ import annotations

# DEPRECATED:
# This module is a compatibility wrapper.
# New code must import generate_strategy_signal from src.strategy_manager.
# Planned removal target: v1.1 after all internal references are removed.

from src.strategy_manager import generate_strategy_signal as _generate_strategy_signal


def generate_strategy_signal(symbol: str) -> dict:
    """Deprecated compatibility wrapper. Use src.strategy_manager.generate_strategy_signal."""
    signal = _generate_strategy_signal(symbol)
    return {
        "strategy_name": signal.strategy_name,
        "market_state": signal.market_state,
        "volatility_state": signal.volatility_state,
        "entry_signal": signal.side if signal.entry_allowed else "NONE",
        "trigger": signal.trigger,
        "reason": signal.reason,
        "entry_allowed": signal.entry_allowed,
        "signal_timestamp": signal.signal_timestamp,
        "signal_age_limit_sec": signal.signal_age_limit_sec,
        "entry_price_hint": signal.entry_price_hint,
        "exit_model": signal.exit_model,
    }
