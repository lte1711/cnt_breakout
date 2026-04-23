from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from binance_client import get_price
from config import ENTRY_INTERVAL, KLINES_LIMIT, PRIMARY_INTERVAL
from src.indicators import (
    bollinger_bands,
    ema,
    extract_closes,
    extract_volumes,
    rolling_vwap,
    rsi,
)
from src.market_data import get_recent_closed_klines
from src.models.market_context import MarketContext
from src.strategies.breakout_v2 import BreakoutV2Strategy
from src.strategies.breakout_v1 import _classify_market


def _build_shadow_context(symbol: str) -> MarketContext:
    klines_primary = get_recent_closed_klines(
        symbol=symbol,
        interval=PRIMARY_INTERVAL,
        limit=KLINES_LIMIT,
    )
    klines_entry = get_recent_closed_klines(
        symbol=symbol,
        interval=ENTRY_INTERVAL,
        limit=KLINES_LIMIT,
    )
    last_price = get_price(symbol)
    return MarketContext(
        symbol=symbol,
        primary_interval=PRIMARY_INTERVAL,
        entry_interval=ENTRY_INTERVAL,
        klines_primary=klines_primary,
        klines_entry=klines_entry,
        last_price=last_price,
    )


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _append_stage(
    trace: list[dict],
    *,
    stage: str,
    passed: bool | None,
    reason: str | None = None,
) -> None:
    trace.append(
        {
            "stage": stage,
            "passed": passed,
            "reason": reason,
        }
    )


def _analyze_breakout_v2_stages(context: MarketContext, params: dict) -> tuple[dict, list[dict], list[str]]:
    closes = extract_closes(context.klines_entry)
    volumes = extract_volumes(context.klines_entry)
    ema_fast_series = ema(closes, params["ema_fast_period"])
    ema_slow_series = ema(closes, params["ema_slow_period"])
    rsi_series = rsi(closes, params["rsi_period"])
    upper_band, _, lower_band = bollinger_bands(
        closes,
        params["bollinger_period"],
        params["bollinger_std_multiplier"],
    )
    vwap_series = rolling_vwap(context.klines_entry, params["vwap_period"])
    market_state = _classify_market(context, params)

    trace: list[dict] = []
    secondary_fail_reasons: list[str] = []

    current_close = closes[-1]
    current_volume = volumes[-1]
    ema_fast = ema_fast_series[-1]
    ema_slow = ema_slow_series[-1]
    rsi_value = rsi_series[-1]
    current_upper = upper_band[-1]
    current_lower = lower_band[-1]
    previous_upper = upper_band[-2] if len(upper_band) >= 2 else None
    previous_lower = lower_band[-2] if len(lower_band) >= 2 else None
    previous_close = closes[-2] if len(closes) >= 2 else None
    vwap_value = vwap_series[-1]

    flags = {
        "market_bias_pass": None,
        "volatility_pass": None,
        "ema_pass": None,
        "rsi_threshold_pass": None,
        "breakout_confirmed": None,
        "vwap_distance_pass": None,
        "band_width_pass": None,
        "band_expansion_pass": None,
        "volume_pass": None,
    }

    indicator_ready = not (
        ema_fast is None
        or ema_slow is None
        or rsi_value is None
        or current_upper is None
        or current_lower is None
        or previous_upper is None
        or previous_lower is None
        or previous_close is None
        or vwap_value is None
    )

    if not indicator_ready:
        secondary_fail_reasons.append("insufficient_breakout_v2_indicator_data")
        for stage_name in flags:
            _append_stage(
                trace,
                stage=stage_name,
                passed=None,
                reason="insufficient_breakout_v2_indicator_data",
            )
        return flags, trace, secondary_fail_reasons

    market_bias_pass = market_state["market_state"] == "TREND_UP" or (
        market_state["market_state"] == "RANGE" and market_state.get("trend_bias") == "UP"
    )
    flags["market_bias_pass"] = market_bias_pass
    if not market_bias_pass:
        secondary_fail_reasons.append("range_without_upward_bias")
    _append_stage(
        trace,
        stage="market_bias",
        passed=market_bias_pass,
        reason=None if market_bias_pass else "range_without_upward_bias",
    )

    volatility_pass = market_state["volatility_state"] == "HIGH"
    flags["volatility_pass"] = volatility_pass
    if not volatility_pass:
        secondary_fail_reasons.append("volatility_not_high")
    _append_stage(
        trace,
        stage="volatility",
        passed=volatility_pass,
        reason=None if volatility_pass else "volatility_not_high",
    )

    ema_pass = ema_fast > ema_slow
    flags["ema_pass"] = ema_pass
    if not ema_pass:
        if market_state["market_state"] == "RANGE" and market_state.get("trend_bias") == "UP":
            secondary_fail_reasons.append("range_bias_up_but_entry_trend_not_up")
        else:
            secondary_fail_reasons.append("ema_fast_not_above_slow")
    _append_stage(
        trace,
        stage="ema",
        passed=ema_pass,
        reason=None
        if ema_pass
        else (
            "range_bias_up_but_entry_trend_not_up"
            if market_state["market_state"] == "RANGE" and market_state.get("trend_bias") == "UP"
            else "ema_fast_not_above_slow"
        ),
    )

    rsi_threshold_pass = rsi_value < params["rsi_overheat"] and rsi_value >= params["rsi_threshold"]
    flags["rsi_threshold_pass"] = rsi_threshold_pass
    if not rsi_threshold_pass:
        if rsi_value >= params["rsi_overheat"]:
            secondary_fail_reasons.append("rsi_overheat")
            rsi_reason = "rsi_overheat"
        else:
            secondary_fail_reasons.append("rsi_below_entry_threshold")
            rsi_reason = "rsi_below_entry_threshold"
    else:
        rsi_reason = None
    _append_stage(trace, stage="rsi_threshold", passed=rsi_threshold_pass, reason=rsi_reason)

    breakout_confirmed = False
    breakout_reason: str | None = None
    if len(context.klines_entry) <= params["breakout_lookback"]:
        breakout_reason = "not_enough_breakout_lookback"
        secondary_fail_reasons.append(breakout_reason)
    else:
        previous_highs = [
            float(item["high"])
            for item in context.klines_entry[-(params["breakout_lookback"] + 1) : -1]
        ]
        breakout_level = max(previous_highs)
        breakout_confirmed = current_close > breakout_level
        if not breakout_confirmed:
            breakout_reason = "breakout_not_confirmed"
            secondary_fail_reasons.append(breakout_reason)
    flags["breakout_confirmed"] = breakout_confirmed
    _append_stage(
        trace,
        stage="breakout_confirmation",
        passed=breakout_confirmed,
        reason=breakout_reason,
    )

    vwap_distance_pass = False
    vwap_reason: str | None = None
    if current_close <= vwap_value:
        vwap_reason = "price_not_above_vwap"
        secondary_fail_reasons.append(vwap_reason)
    else:
        vwap_distance_ratio = (current_close - vwap_value) / current_close
        vwap_distance_pass = vwap_distance_ratio >= params["min_vwap_distance_ratio"]
        if not vwap_distance_pass:
            vwap_reason = "vwap_distance_too_small"
            secondary_fail_reasons.append(vwap_reason)
    flags["vwap_distance_pass"] = vwap_distance_pass
    _append_stage(trace, stage="vwap_distance", passed=vwap_distance_pass, reason=vwap_reason)

    band_width_ratio = (current_upper - current_lower) / current_close
    band_width_pass = band_width_ratio >= params["min_band_width_ratio"]
    flags["band_width_pass"] = band_width_pass
    band_width_reason = None if band_width_pass else "band_width_too_narrow"
    if band_width_reason is not None:
        secondary_fail_reasons.append(band_width_reason)
    _append_stage(trace, stage="band_width", passed=band_width_pass, reason=band_width_reason)

    previous_band_width_ratio = (previous_upper - previous_lower) / previous_close
    band_expansion_pass = False
    band_expansion_reason: str | None = None
    if previous_band_width_ratio <= 0:
        band_expansion_reason = "band_not_expanding"
        secondary_fail_reasons.append(band_expansion_reason)
    else:
        band_expansion_ratio = band_width_ratio / previous_band_width_ratio
        band_expansion_pass = band_expansion_ratio >= params["min_band_expansion_ratio"]
        if not band_expansion_pass:
            band_expansion_reason = "band_not_expanding"
            secondary_fail_reasons.append(band_expansion_reason)
    flags["band_expansion_pass"] = band_expansion_pass
    _append_stage(
        trace,
        stage="band_expansion",
        passed=band_expansion_pass,
        reason=band_expansion_reason,
    )

    volume_pass = False
    volume_reason: str | None = None
    volume_period = int(params["volume_avg_period"])
    if len(volumes) < volume_period:
        volume_reason = "not_enough_volume_history"
        secondary_fail_reasons.append(volume_reason)
    else:
        recent_volumes = volumes[-volume_period:]
        average_volume = sum(recent_volumes) / len(recent_volumes)
        if average_volume > 0:
            volume_ratio = current_volume / average_volume
            volume_pass = volume_ratio >= params["min_volume_multiplier"]
        if not volume_pass:
            volume_reason = "volume_not_confirmed"
            secondary_fail_reasons.append(volume_reason)
    flags["volume_pass"] = volume_pass
    _append_stage(trace, stage="volume", passed=volume_pass, reason=volume_reason)

    deduped_secondary_fails: list[str] = []
    for reason in secondary_fail_reasons:
        if reason not in deduped_secondary_fails:
            deduped_secondary_fails.append(reason)

    return flags, trace, deduped_secondary_fails


def evaluate_breakout_v2_shadow(symbol: str, params: dict) -> dict:
    context = _build_shadow_context(symbol)
    strategy = BreakoutV2Strategy(dict(params))
    strategy.validate_params(params)
    signal = strategy.evaluate(context)
    stage_flags, evaluated_stage_trace, secondary_fail_reasons = _analyze_breakout_v2_stages(context, params)

    closes = extract_closes(context.klines_entry)
    volumes = extract_volumes(context.klines_entry)
    upper_band, _, lower_band = bollinger_bands(
        closes,
        params["bollinger_period"],
        params["bollinger_std_multiplier"],
    )
    vwap_series = rolling_vwap(context.klines_entry, params["vwap_period"])

    current_close = closes[-1]
    current_volume = volumes[-1]
    vwap_value = vwap_series[-1]
    current_upper = upper_band[-1]
    current_lower = lower_band[-1]
    previous_upper = upper_band[-2] if len(upper_band) >= 2 else None
    previous_lower = lower_band[-2] if len(lower_band) >= 2 else None
    previous_close = closes[-2] if len(closes) >= 2 else None

    band_width_ratio = None
    band_expansion_ratio = None
    volume_ratio = None

    if current_upper is not None and current_lower is not None and current_close > 0:
        band_width_ratio = (current_upper - current_lower) / current_close

    if (
        previous_upper is not None
        and previous_lower is not None
        and previous_close is not None
        and previous_close > 0
        and band_width_ratio is not None
    ):
        previous_band_width_ratio = (previous_upper - previous_lower) / previous_close
        if previous_band_width_ratio > 0:
            band_expansion_ratio = band_width_ratio / previous_band_width_ratio

    volume_period = int(params["volume_avg_period"])
    if len(volumes) >= volume_period:
        recent_volumes = volumes[-volume_period:]
        average_volume = sum(recent_volumes) / len(recent_volumes)
        if average_volume > 0:
            volume_ratio = current_volume / average_volume

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    filtered_reason = str(signal.reason)
    secondary_fail_reasons = [
        reason for reason in secondary_fail_reasons if reason != filtered_reason
    ]
    return {
        "ts": timestamp,
        "symbol": symbol,
        "strategy": "breakout_v2_shadow",
        "signal_generated": True,
        "entry_allowed": bool(signal.entry_allowed),
        "filter_reason": filtered_reason,
        "confidence": float(signal.confidence),
        "vwap": vwap_value,
        "band_width_ratio": band_width_ratio,
        "band_expansion_ratio": band_expansion_ratio,
        "volume_ratio": volume_ratio,
        "hypothetical_entry": bool(signal.entry_allowed),
        "secondary_fail_reasons": secondary_fail_reasons,
        "evaluated_stage_trace": evaluated_stage_trace,
        "stage_flags": stage_flags,
    }


def append_shadow_log(log_file: Path, event: dict) -> None:
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8", newline="\n") as file_handle:
            file_handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass


def update_shadow_snapshot(snapshot_file: Path, event: dict) -> None:
    try:
        snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        if snapshot_file.exists():
            loaded = json.loads(snapshot_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                snapshot = loaded
            else:
                snapshot = {}
        else:
            snapshot = {}

        signal_count = int(snapshot.get("signal_count", 0) or 0) + 1
        filtered_signal_count = int(snapshot.get("filtered_signal_count", 0) or 0)
        allowed_signal_count = int(snapshot.get("allowed_signal_count", 0) or 0)
        hypothetical_trades_count = int(snapshot.get("hypothetical_trades_count", 0) or 0)

        if event.get("entry_allowed"):
            allowed_signal_count += 1
            hypothetical_trades_count += 1
        else:
            filtered_signal_count += 1

        reason_distribution = snapshot.get("reason_distribution", {}) or {}
        reason_key = str(event.get("filter_reason") or "UNKNOWN")
        reason_distribution[reason_key] = int(reason_distribution.get(reason_key, 0) or 0) + 1

        expanded_event_count = int(snapshot.get("expanded_event_count", 0) or 0)
        secondary_fail_distribution = snapshot.get("secondary_fail_distribution", {}) or {}
        stage_false_counts = snapshot.get("stage_false_counts", {}) or {}

        has_expanded_schema = all(
            key in event for key in ("secondary_fail_reasons", "evaluated_stage_trace", "stage_flags")
        )
        if has_expanded_schema:
            expanded_event_count += 1
            for reason in event.get("secondary_fail_reasons", []) or []:
                reason_name = str(reason or "UNKNOWN")
                secondary_fail_distribution[reason_name] = (
                    int(secondary_fail_distribution.get(reason_name, 0) or 0) + 1
                )
            for stage_name, passed in (event.get("stage_flags", {}) or {}).items():
                if passed is False:
                    stage_false_counts[str(stage_name)] = (
                        int(stage_false_counts.get(str(stage_name), 0) or 0) + 1
                    )

        updated = {
            "strategy": "breakout_v2_shadow",
            "signal_count": signal_count,
            "filtered_signal_count": filtered_signal_count,
            "allowed_signal_count": allowed_signal_count,
            "filtered_signal_ratio": _safe_ratio(filtered_signal_count, signal_count),
            "allowed_signal_ratio": _safe_ratio(allowed_signal_count, signal_count),
            "hypothetical_trades_count": hypothetical_trades_count,
            "hypothetical_expectancy": float(snapshot.get("hypothetical_expectancy", 0.0) or 0.0),
            "hypothetical_profit_factor": float(snapshot.get("hypothetical_profit_factor", 0.0) or 0.0),
            "stop_exit_ratio": float(snapshot.get("stop_exit_ratio", 0.0) or 0.0),
            "reason_distribution": reason_distribution,
            "expanded_event_count": expanded_event_count,
            "secondary_fail_distribution": secondary_fail_distribution,
            "stage_false_counts": stage_false_counts,
            "last_updated": event.get("ts"),
        }
        snapshot_file.write_text(
            json.dumps(updated, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass
