from __future__ import annotations

from src.analytics.strategy_metrics import increment_signals_generated
from src.models.ranked_signal_selection import RankedSignalSelection
from src.portfolio.signal_ranker import rank_signals
from src.strategy_manager import generate_all_signals


def get_ranked_signal_selection(
    symbol: str,
    strategy_metrics: dict | None = None,
) -> RankedSignalSelection:
    signals = generate_all_signals(symbol)
    if strategy_metrics is not None:
        for signal in signals:
            increment_signals_generated(strategy_metrics, signal.strategy_name)
    return rank_signals(signals, strategy_metrics=strategy_metrics)
