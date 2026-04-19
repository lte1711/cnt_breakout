from __future__ import annotations

from config import (
    RANKER_EXPECTANCY_WEIGHT,
    RANKER_MINIMUM_SAMPLE,
    RANKER_RECENT_LOSS_PENALTY,
    RANKER_TREND_ALIGNMENT_BONUS,
    RANKER_VOLATILITY_PENALTY,
    STRATEGY_STATIC_BASE_SCORES,
)
from src.models.ranked_signal_selection import RankedSignalSelection
from src.models.strategy_performance import StrategyPerformance
from src.models.strategy_signal import StrategySignal


def _normalize_expectancy(expectancy: float, confidence_multiplier: float) -> float:
    return expectancy * confidence_multiplier


def _build_score_components(
    signal: StrategySignal,
    performance: StrategyPerformance | None,
) -> dict:
    base_signal_score = float(signal.confidence)
    static_priority_score = float(STRATEGY_STATIC_BASE_SCORES.get(signal.strategy_name, 0.8))
    trend_alignment_bonus = (
        RANKER_TREND_ALIGNMENT_BONUS
        if signal.market_state in {"TREND_UP", "MEAN_REVERSION"}
        else 0.0
    )
    volatility_penalty = RANKER_VOLATILITY_PENALTY if signal.volatility_state == "LOW" else 0.0

    if performance is None or performance.trades_closed < RANKER_MINIMUM_SAMPLE:
        expectancy_weighted_score = 0.0
        recent_loss_penalty = 0.0
        fallback_static_only = True
        expectancy_snapshot = {
            "trades_closed": 0 if performance is None else performance.trades_closed,
            "expectancy": 0.0 if performance is None else performance.expectancy,
            "confidence_multiplier": 0.0 if performance is None else performance.confidence_multiplier,
        }
    else:
        expectancy_weighted_score = (
            _normalize_expectancy(performance.expectancy, performance.confidence_multiplier)
            * RANKER_EXPECTANCY_WEIGHT
        )
        recent_loss_penalty = (
            RANKER_RECENT_LOSS_PENALTY if performance.losses > 0 and performance.losses >= performance.wins else 0.0
        )
        fallback_static_only = False
        expectancy_snapshot = {
            "trades_closed": performance.trades_closed,
            "expectancy": performance.expectancy,
            "confidence_multiplier": performance.confidence_multiplier,
        }

    score = (
        static_priority_score
        + base_signal_score
        + expectancy_weighted_score
        + trend_alignment_bonus
        - volatility_penalty
        - recent_loss_penalty
    )
    return {
        "static_priority_score": static_priority_score,
        "base_signal_score": base_signal_score,
        "expectancy_weighted_score": expectancy_weighted_score,
        "trend_alignment_bonus": trend_alignment_bonus,
        "volatility_penalty": volatility_penalty,
        "recent_loss_penalty": recent_loss_penalty,
        "fallback_static_only": fallback_static_only,
        "score": score,
        "expectancy_snapshot": expectancy_snapshot,
    }


def rank_signals(
    signals: list[StrategySignal],
    strategy_metrics: dict[str, StrategyPerformance] | None = None,
) -> RankedSignalSelection:
    rejected_reasons: dict[str, int] = {}
    for signal in signals:
        if signal.entry_allowed:
            continue
        rejected_reasons[signal.reason] = rejected_reasons.get(signal.reason, 0) + 1

    valid = [signal for signal in signals if signal.entry_allowed]

    if not valid:
        return RankedSignalSelection(
            selected_signal=None,
            rank_score=0.0,
            rank_score_components={},
            strategy_expectancy_snapshot={},
            total_signals=len(signals),
            candidate_count=0,
            rejected_reasons=rejected_reasons,
            candidate_details=[],
            no_ranked_signal_detail="no_candidate" if not signals else "all_filtered",
        )

    scored: list[tuple[float, StrategySignal, dict]] = []
    for signal in valid:
        performance = (strategy_metrics or {}).get(signal.strategy_name)
        components = _build_score_components(signal, performance)
        scored.append((float(components["score"]), signal, components))

    ranked = sorted(scored, key=lambda item: item[0], reverse=True)
    top_score, top_signal, top_components = ranked[0]
    candidate_details = [
        {
            "strategy": signal.strategy_name,
            "score": float(score),
            "components": {
                key: value for key, value in components.items() if key != "expectancy_snapshot"
            },
        }
        for score, signal, components in ranked
    ]
    return RankedSignalSelection(
        selected_signal=top_signal,
        rank_score=top_score,
        rank_score_components={
            key: value for key, value in top_components.items() if key != "expectancy_snapshot"
        },
        strategy_expectancy_snapshot=dict(top_components["expectancy_snapshot"]),
        total_signals=len(signals),
        candidate_count=len(valid),
        rejected_reasons=rejected_reasons,
        candidate_details=candidate_details,
        no_ranked_signal_detail="none",
    )
