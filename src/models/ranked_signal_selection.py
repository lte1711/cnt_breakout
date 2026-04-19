from __future__ import annotations

from dataclasses import dataclass

from src.models.strategy_signal import StrategySignal


@dataclass
class RankedSignalSelection:
    selected_signal: StrategySignal | None
    rank_score: float
    rank_score_components: dict
    strategy_expectancy_snapshot: dict
