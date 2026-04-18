from __future__ import annotations

from src.models.strategy_signal import StrategySignal
from src.portfolio.signal_ranker import rank_signals
from src.strategy_manager import generate_all_signals


def get_selected_signal(symbol: str) -> StrategySignal | None:
    signals = generate_all_signals(symbol)
    return rank_signals(signals)
