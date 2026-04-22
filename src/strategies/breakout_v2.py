from __future__ import annotations

import time

from src.indicators import (
    bollinger_bands,
    ema,
    extract_closes,
    extract_volumes,
    rolling_vwap,
    rsi,
)
from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal
from src.risk.exit_models import ExitModel
from src.strategies.base import BaseStrategy
from src.strategies.breakout_v1 import _classify_market


def _filtered_signal(reason: str) -> dict:
    return {
        "entry_allowed": False,
        "side": "NONE",
        "trigger": "FILTERED",
        "reason": reason,
        "confidence": 0.0,
    }


def _no_setup_signal(reason: str) -> dict:
    return {
        "entry_allowed": False,
        "side": "NONE",
        "trigger": "NO_SETUP",
        "reason": reason,
        "confidence": 0.0,
    }


def _build_entry_signal(context: MarketContext, params: dict, market_state: dict) -> dict:
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

    if (
        ema_fast is None
        or ema_slow is None
        or rsi_value is None
        or current_upper is None
        or current_lower is None
        or previous_upper is None
        or previous_lower is None
        or previous_close is None
        or vwap_value is None
    ):
        return _filtered_signal("insufficient_breakout_v2_indicator_data")

    if market_state["market_state"] == "TREND_UP":
        trend_gate_pass = True
    elif market_state["market_state"] == "RANGE":
        if market_state.get("trend_bias") != "UP":
            return _filtered_signal("range_without_upward_bias")
        if ema_fast <= ema_slow:
            return _filtered_signal("range_bias_up_but_entry_trend_not_up")
        trend_gate_pass = True
    else:
        trend_gate_pass = False

    if not trend_gate_pass:
        return _filtered_signal("market_not_trend_up")

    if rsi_value >= params["rsi_overheat"]:
        return _filtered_signal("rsi_overheat")

    if market_state["volatility_state"] != "HIGH":
        return _filtered_signal("volatility_not_high")

    if ema_fast <= ema_slow:
        return _no_setup_signal("ema_fast_not_above_slow")

    if rsi_value < params["rsi_threshold"]:
        return _no_setup_signal("rsi_below_entry_threshold")

    if len(context.klines_entry) <= params["breakout_lookback"]:
        return _no_setup_signal("not_enough_breakout_lookback")

    previous_highs = [
        float(item["high"])
        for item in context.klines_entry[-(params["breakout_lookback"] + 1) : -1]
    ]
    breakout_level = max(previous_highs)
    if current_close <= breakout_level:
        return _no_setup_signal("breakout_not_confirmed")

    if current_close <= vwap_value:
        return _filtered_signal("price_not_above_vwap")

    vwap_distance_ratio = (current_close - vwap_value) / current_close
    if vwap_distance_ratio < params["min_vwap_distance_ratio"]:
        return _filtered_signal("vwap_distance_too_small")

    band_width_ratio = (current_upper - current_lower) / current_close
    if band_width_ratio < params["min_band_width_ratio"]:
        return _filtered_signal("band_width_too_narrow")

    previous_band_width_ratio = (previous_upper - previous_lower) / previous_close
    if band_width_ratio < previous_band_width_ratio * params["min_band_expansion_ratio"]:
        return _filtered_signal("band_not_expanding")

    volume_avg_period = params["volume_avg_period"]
    if len(volumes) < volume_avg_period:
        return _filtered_signal("not_enough_volume_history")
    recent_volumes = volumes[-volume_avg_period:]
    average_volume = sum(recent_volumes) / len(recent_volumes)
    if current_volume < average_volume * params["min_volume_multiplier"]:
        return _filtered_signal("volume_not_confirmed")

    return {
        "entry_allowed": True,
        "side": "BUY",
        "trigger": "BREAKOUT",
        "reason": "trend_up_vwap_boll_volume_breakout",
        "confidence": params["breakout_v2_confidence"],
    }


class BreakoutV2Strategy(BaseStrategy):
    def __init__(self, params: dict) -> None:
        self.params = dict(params)

    def validate_params(self, params: dict) -> None:
        if params["ema_fast_period"] >= params["ema_slow_period"]:
            raise ValueError("ema_fast_period must be smaller than ema_slow_period")
        if not 0 < params["rsi_threshold"] < params["rsi_overheat"] < 100:
            raise ValueError("rsi thresholds must satisfy 0 < threshold < overheat < 100")
        if params["atr_expansion_multiplier"] <= 1.0:
            raise ValueError("atr_expansion_multiplier must be greater than 1.0")
        if params["breakout_lookback"] < 1:
            raise ValueError("breakout_lookback must be at least 1")
        if params["bollinger_period"] < 2:
            raise ValueError("bollinger_period must be at least 2")
        if params["bollinger_std_multiplier"] <= 0:
            raise ValueError("bollinger_std_multiplier must be positive")
        if params["min_band_width_ratio"] <= 0:
            raise ValueError("min_band_width_ratio must be positive")
        if params["min_band_expansion_ratio"] <= 1.0:
            raise ValueError("min_band_expansion_ratio must be greater than 1.0")
        if params["vwap_period"] < 2:
            raise ValueError("vwap_period must be at least 2")
        if params["min_vwap_distance_ratio"] <= 0:
            raise ValueError("min_vwap_distance_ratio must be positive")
        if params["volume_avg_period"] < 2:
            raise ValueError("volume_avg_period must be at least 2")
        if params["min_volume_multiplier"] <= 1.0:
            raise ValueError("min_volume_multiplier must be greater than 1.0")
        if not 0 < params["breakout_v2_confidence"] <= 1:
            raise ValueError("breakout_v2_confidence must be in (0, 1]")
        if params["target_pct"] <= 0 or params["stop_loss_pct"] <= 0:
            raise ValueError("target_pct and stop_loss_pct must be positive")
        if float(params["signal_age_limit_sec"]) == 0:
            raise ValueError("signal_age_limit_sec must be -1 or > 0")
        if float(params["signal_age_limit_sec"]) < -1:
            raise ValueError("signal_age_limit_sec must be >= -1")

    def evaluate(self, context: MarketContext) -> StrategySignal:
        market_state = _classify_market(context, self.params)
        entry_state = _build_entry_signal(context, self.params, market_state)

        exit_model = None
        entry_price_hint = None
        if entry_state["entry_allowed"]:
            entry_price_hint = context.last_price
            exit_model = ExitModel(
                stop_price=entry_price_hint * (1 - self.params["stop_loss_pct"]),
                target_price=entry_price_hint * (1 + self.params["target_pct"]),
            )

        return StrategySignal(
            strategy_name="breakout_v2",
            symbol=context.symbol,
            signal_timestamp=time.time(),
            signal_age_limit_sec=float(self.params["signal_age_limit_sec"]),
            entry_allowed=entry_state["entry_allowed"],
            side=entry_state["side"],
            trigger=entry_state["trigger"],
            reason=entry_state["reason"],
            confidence=entry_state["confidence"],
            market_state=market_state["market_state"],
            trend_bias=market_state.get("trend_bias"),
            volatility_state=market_state["volatility_state"],
            entry_price_hint=entry_price_hint,
            exit_model=exit_model,
        )
