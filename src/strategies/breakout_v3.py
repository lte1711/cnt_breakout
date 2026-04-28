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
from src.market.feature_snapshot import build_market_feature_snapshot
from src.models.breakout_v3_eval_result import BreakoutV3Conditions
from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal
from src.risk.exit_models import ExitModel
from src.strategies.base import BaseStrategy
from src.strategies.breakout_v1 import _classify_market


def validate_breakout_v3_params(params: dict) -> None:
    if params["ema_fast_period"] >= params["ema_slow_period"]:
        raise ValueError("ema_fast_period must be smaller than ema_slow_period")
    if params["bollinger_period"] < 2:
        raise ValueError("bollinger_period must be at least 2")
    if params["vwap_period"] < 2:
        raise ValueError("vwap_period must be at least 2")
    if params["volume_avg_period"] < 2:
        raise ValueError("volume_avg_period must be at least 2")
    if params["breakout_lookback"] < 1:
        raise ValueError("breakout_lookback must be at least 1")
    if params["min_band_width_ratio"] <= 0:
        raise ValueError("min_band_width_ratio must be positive")
    if params["min_band_expansion_ratio"] <= 1.0:
        raise ValueError("min_band_expansion_ratio must be greater than 1.0")
    if params["min_vwap_distance_ratio"] <= 0:
        raise ValueError("min_vwap_distance_ratio must be positive")
    if params["min_volume_multiplier"] <= 1.0:
        raise ValueError("min_volume_multiplier must be greater than 1.0")
    if params["min_soft_pass_required"] < 1:
        raise ValueError("min_soft_pass_required must be positive")
    if params.get("relaxed_volatility_rsi_buffer", 0) < 0:
        raise ValueError("relaxed_volatility_rsi_buffer must be non-negative")


def build_breakout_v3_conditions(context: MarketContext, params: dict) -> BreakoutV3Conditions:
    validate_breakout_v3_params(params)

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
        return BreakoutV3Conditions(
            market_bias_pass=False,
            trend_up_pass=False,
            range_bias_pass=False,
            setup_ready=False,
            volatility_floor_pass=False,
            price_position_pass=False,
            breakout_confirmed=False,
            trigger_price_pass=False,
            band_width_pass=False,
            band_expansion_pass=False,
            volume_pass=False,
            vwap_distance_pass=False,
            rsi_threshold_pass=False,
            ema_pass=False,
        )

    trend_up_pass = market_state["market_state"] == "TREND_UP"
    range_bias_pass = (
        market_state["market_state"] == "RANGE"
        and market_state.get("trend_bias") == "UP"
    )
    market_bias_pass = trend_up_pass or range_bias_pass

    strict_volatility_pass = market_state["volatility_state"] == "HIGH"
    
    # Relaxed volatility pass for uptrends with stronger RSI
    relaxed_volatility_pass = (
        market_state["market_state"] == "TREND_UP"
        and rsi_value >= params["rsi_threshold"] + params.get("relaxed_volatility_rsi_buffer", 2)
        and ema_fast > ema_slow
    )
    
    volatility_floor_pass = strict_volatility_pass or relaxed_volatility_pass
    price_position_pass = current_close > vwap_value
    setup_ready = market_bias_pass and volatility_floor_pass and price_position_pass

    breakout_confirmed = False
    trigger_price_pass = False
    if len(context.klines_entry) > params["breakout_lookback"]:
        previous_highs = [
            float(item["high"])
            for item in context.klines_entry[-(params["breakout_lookback"] + 1) : -1]
        ]
        breakout_level = max(previous_highs)
        breakout_confirmed = current_close > breakout_level
        trigger_price_pass = current_close >= breakout_level * (
            1 + params["min_trigger_breakout_buffer_ratio"]
        )

    band_width_ratio = (current_upper - current_lower) / current_close
    band_width_pass = band_width_ratio >= params["min_band_width_ratio"]

    previous_band_width_ratio = (previous_upper - previous_lower) / previous_close
    band_expansion_pass = False
    if previous_band_width_ratio > 0:
        band_expansion_ratio = band_width_ratio / previous_band_width_ratio
        band_expansion_pass = band_expansion_ratio >= params["min_band_expansion_ratio"]

    vwap_distance_ratio = 0.0
    if current_close > vwap_value:
        vwap_distance_ratio = (current_close - vwap_value) / current_close
    vwap_distance_pass = vwap_distance_ratio >= params["min_vwap_distance_ratio"]

    volume_pass = False
    if len(volumes) >= params["volume_avg_period"]:
        recent_volumes = volumes[-params["volume_avg_period"] :]
        average_volume = sum(recent_volumes) / len(recent_volumes)
        if average_volume > 0:
            volume_pass = current_volume >= average_volume * params["min_volume_multiplier"]

    rsi_threshold_pass = rsi_value < params["rsi_overheat"] and rsi_value >= params["rsi_threshold"]
    ema_pass = ema_fast > ema_slow

    return BreakoutV3Conditions(
        market_bias_pass=market_bias_pass,
        trend_up_pass=trend_up_pass,
        range_bias_pass=range_bias_pass,
        setup_ready=setup_ready,
        volatility_floor_pass=volatility_floor_pass,
        price_position_pass=price_position_pass,
        breakout_confirmed=breakout_confirmed,
        trigger_price_pass=trigger_price_pass,
        band_width_pass=band_width_pass,
        band_expansion_pass=band_expansion_pass,
        volume_pass=volume_pass,
        vwap_distance_pass=vwap_distance_pass,
        rsi_threshold_pass=rsi_threshold_pass,
        ema_pass=ema_pass,
    )


class BreakoutV3Strategy(BaseStrategy):
    def __init__(self, params: dict) -> None:
        self.params = dict(params)

    def validate_params(self, params: dict) -> None:
        validate_breakout_v3_params(params)

    def evaluate(self, context: MarketContext) -> StrategySignal:
        market_features = build_market_feature_snapshot(context, self.params)
        market_state = _classify_market(context, self.params)
        conditions = build_breakout_v3_conditions(context, self.params)

        entry_allowed = conditions.setup_ready and conditions.breakout_confirmed

        soft_pass_count = sum([
            conditions.band_width_pass,
            conditions.band_expansion_pass,
            conditions.volume_pass,
            conditions.vwap_distance_pass,
            conditions.rsi_threshold_pass,
            conditions.ema_pass,
        ])

        min_soft_pass_required = self.params.get("min_soft_pass_required", 3)
        quality_gate_pass = soft_pass_count >= min_soft_pass_required

        entry_allowed = entry_allowed and quality_gate_pass

        reason = "setup_not_ready"
        if conditions.setup_ready:
            if not conditions.breakout_confirmed:
                reason = "breakout_not_confirmed"
            elif not quality_gate_pass:
                reason = f"quality_gate_fail_pass_{soft_pass_count}_required_{min_soft_pass_required}"
            else:
                reason = "breakout_v3_entry"

        confidence = 0.78 if entry_allowed else 0.0

        exit_model = None
        entry_price_hint = None
        if entry_allowed:
            entry_price_hint = context.last_price
            target_pct = self.params.get("target_pct", 0.002)
            stop_loss_pct = self.params.get("stop_loss_pct", 0.0015)
            exit_model = ExitModel(
                stop_price=entry_price_hint * (1 - stop_loss_pct),
                target_price=entry_price_hint * (1 + target_pct),
            )

        return StrategySignal(
            strategy_name="breakout_v3",
            symbol=context.symbol,
            signal_timestamp=time.time(),
            signal_age_limit_sec=float(self.params.get("signal_age_limit_sec", 15)),
            entry_allowed=entry_allowed,
            side="BUY" if entry_allowed else "NONE",
            trigger="BREAKOUT" if entry_allowed else "NO_SETUP",
            reason=reason,
            confidence=confidence,
            market_state=market_state["market_state"],
            trend_bias=market_state.get("trend_bias"),
            volatility_state=market_state["volatility_state"],
            entry_price_hint=entry_price_hint,
            exit_model=exit_model,
            market_features=market_features,
        )


def evaluate_breakout_v3(context: MarketContext, params: dict) -> StrategySignal:
    """Direct evaluation function for engine integration."""
    strategy = BreakoutV3Strategy(params)
    return strategy.evaluate(context)
