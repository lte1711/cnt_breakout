from __future__ import annotations

from dataclasses import dataclass, field

from src.models.strategy_signal import StrategySignal


@dataclass
class RankedSignalSelection:
    selected_signal: StrategySignal | None
    rank_score: float
    rank_score_components: dict
    strategy_expectancy_snapshot: dict
    total_signals: int = 0
    candidate_count: int = 0
    rejected_reasons: dict = field(default_factory=dict)
    candidate_details: list[dict] = field(default_factory=list)
    no_ranked_signal_detail: str = "none"
