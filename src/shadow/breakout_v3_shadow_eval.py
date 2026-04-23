from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from datetime import datetime
from typing import Any

from src.models.breakout_v3_eval_result import (
    BreakoutV3Conditions,
    BreakoutV3EvalResult,
    BreakoutV3ShadowEvent,
    StageResult,
)


def _stage_result(name: str, checks: list[str], fail_reasons: list[str]) -> StageResult:
    return StageResult(
        name=name,
        passed=len(fail_reasons) == 0,
        fail_reasons=fail_reasons,
        evaluated_checks=checks,
    )


def _pick_first_blocker(stage_results: dict[str, StageResult]) -> str | None:
    for stage_name in ("regime", "setup", "trigger", "quality"):
        stage = stage_results[stage_name]
        if not stage.passed and stage.fail_reasons:
            return stage.fail_reasons[0]
    return None


def evaluate_breakout_v3_shadow(
    conditions: BreakoutV3Conditions,
    *,
    min_soft_pass_required: int = 3,
) -> BreakoutV3EvalResult:
    regime_fail_reasons: list[str] = []
    if not conditions.market_bias_pass:
        regime_fail_reasons.append("market_not_trend_up")
    if not conditions.trend_up_pass:
        regime_fail_reasons.append("trend_not_up")
    if not conditions.range_bias_pass:
        regime_fail_reasons.append("range_without_upward_bias")
    regime = _stage_result(
        "regime",
        ["market_bias_pass", "trend_up_pass", "range_bias_pass"],
        regime_fail_reasons,
    )

    setup_fail_reasons: list[str] = []
    if not conditions.setup_ready:
        setup_fail_reasons.append("setup_not_ready")
    if not conditions.volatility_floor_pass:
        setup_fail_reasons.append("volatility_floor_fail")
    if not conditions.price_position_pass:
        setup_fail_reasons.append("price_position_fail")
    setup = _stage_result(
        "setup",
        ["setup_ready", "volatility_floor_pass", "price_position_pass"],
        setup_fail_reasons,
    )

    trigger_fail_reasons: list[str] = []
    if not conditions.breakout_confirmed:
        trigger_fail_reasons.append("breakout_not_confirmed")
    if not conditions.trigger_price_pass:
        trigger_fail_reasons.append("trigger_price_fail")
    trigger = _stage_result(
        "trigger",
        ["breakout_confirmed", "trigger_price_pass"],
        trigger_fail_reasons,
    )

    soft_flags = {
        "band_width_pass": conditions.band_width_pass,
        "band_expansion_pass": conditions.band_expansion_pass,
        "volume_pass": conditions.volume_pass,
        "vwap_distance_pass": conditions.vwap_distance_pass,
        "rsi_threshold_pass": conditions.rsi_threshold_pass,
        "ema_pass": conditions.ema_pass,
    }
    soft_fail_reason_map = {
        "band_width_pass": "band_width_fail",
        "band_expansion_pass": "band_expansion_fail",
        "volume_pass": "volume_fail",
        "vwap_distance_pass": "vwap_distance_fail",
        "rsi_threshold_pass": "rsi_threshold_fail",
        "ema_pass": "ema_fail",
    }
    soft_pass_count = sum(1 for value in soft_flags.values() if value)
    soft_fail_reasons = [
        soft_fail_reason_map[name]
        for name, value in soft_flags.items()
        if not value
    ]
    quality = _stage_result(
        "quality",
        list(soft_flags.keys()),
        [] if soft_pass_count >= min_soft_pass_required else soft_fail_reasons,
    )

    stage_results = {
        "regime": regime,
        "setup": setup,
        "trigger": trigger,
        "quality": quality,
    }

    hard_pass = regime.passed and trigger.passed
    quality_pass = quality.passed
    allowed = hard_pass and quality_pass
    first_blocker = _pick_first_blocker(stage_results)
    hard_blocker = None if hard_pass else first_blocker

    if allowed:
        summary_reason = "allowed_by_hard_and_soft_gates"
    elif not regime.passed:
        summary_reason = "regime_blocked"
    elif not trigger.passed:
        summary_reason = "trigger_blocked"
    else:
        summary_reason = "hard_pass_but_soft_count_insufficient"

    return BreakoutV3EvalResult(
        strategy_name="breakout_v3_candidate",
        allowed=allowed,
        first_blocker=first_blocker,
        hard_blocker=hard_blocker,
        soft_pass_count=soft_pass_count,
        soft_fail_count=len(soft_flags) - soft_pass_count,
        soft_total_count=len(soft_flags),
        min_soft_pass_required=min_soft_pass_required,
        stage_results=stage_results,
        secondary_fail_reasons=soft_fail_reasons,
        condition_flags=conditions.to_flags(),
        summary_reason=summary_reason,
    )


def build_breakout_v3_shadow_event(
    result: BreakoutV3EvalResult,
    *,
    symbol: str,
    metadata: dict[str, Any] | None = None,
) -> BreakoutV3ShadowEvent:
    stage_flags = {
        stage_name: stage_result.passed
        for stage_name, stage_result in result.stage_results.items()
    }
    return BreakoutV3ShadowEvent(
        timestamp=datetime.now().astimezone().isoformat(timespec="seconds"),
        symbol=symbol,
        strategy_name=result.strategy_name,
        allowed=result.allowed,
        summary_reason=result.summary_reason,
        first_blocker=result.first_blocker,
        hard_blocker=result.hard_blocker,
        soft_pass_count=result.soft_pass_count,
        soft_fail_count=result.soft_fail_count,
        soft_total_count=result.soft_total_count,
        min_soft_pass_required=result.min_soft_pass_required,
        stage_flags=stage_flags,
        condition_flags=dict(result.condition_flags),
        secondary_fail_reasons=list(result.secondary_fail_reasons),
        metadata=metadata or {},
    )


def aggregate_breakout_v3_shadow_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    signal_count = len(events)
    allowed_count = sum(1 for event in events if event["allowed"])
    first_blockers = Counter(
        event["first_blocker"] for event in events if event.get("first_blocker")
    )
    hard_blockers = Counter(
        event["hard_blocker"] for event in events if event.get("hard_blocker")
    )
    secondary = Counter()
    soft_pass_dist = Counter()
    stage_pass_counts = Counter()
    stage_fail_counts = Counter()

    for event in events:
        soft_pass_dist[event["soft_pass_count"]] += 1
        for reason in event.get("secondary_fail_reasons", []):
            secondary[reason] += 1
        for stage_name, passed in event.get("stage_flags", {}).items():
            if passed:
                stage_pass_counts[stage_name] += 1
            else:
                stage_fail_counts[stage_name] += 1

    min_soft_pass_required = events[0]["min_soft_pass_required"] if events else 0
    soft_total_count = events[0]["soft_total_count"] if events else 0

    return {
        "signal_count": signal_count,
        "allowed_signal_count": allowed_count,
        "allowed_signal_ratio": allowed_count / signal_count if signal_count else 0.0,
        "expanded_event_count": signal_count,
        "first_blocker_distribution": dict(first_blockers),
        "hard_blocker_distribution": dict(hard_blockers),
        "secondary_blocker_distribution": dict(secondary),
        "soft_pass_count_distribution": dict(soft_pass_dist),
        "stage_pass_counts": dict(stage_pass_counts),
        "stage_fail_counts": dict(stage_fail_counts),
        "min_soft_pass_required": min_soft_pass_required,
        "soft_total_count": soft_total_count,
        "aggregation_scope": "all_breakout_v3_shadow_events",
    }


def breakout_v3_shadow_event_to_dict(event: BreakoutV3ShadowEvent) -> dict[str, Any]:
    return asdict(event)
