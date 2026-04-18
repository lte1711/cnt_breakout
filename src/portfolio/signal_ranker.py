from __future__ import annotations

from src.models.strategy_signal import StrategySignal


def rank_signals(signals: list[StrategySignal]) -> StrategySignal | None:
    valid = [signal for signal in signals if signal.entry_allowed]

    if not valid:
        return None

    ranked = sorted(valid, key=lambda signal: signal.confidence, reverse=True)
    return ranked[0]
