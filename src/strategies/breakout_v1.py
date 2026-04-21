from __future__ import annotations

import time

from src.indicators import atr, ema, extract_closes, extract_highs, extract_lows, rsi
from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal
from src.risk.exit_models import ExitModel
from src.strategies.base import BaseStrategy


def _average_of_recent(values: list[float | None], count: int) -> float | None:
    valid_values = [value for value in values if value is not None]

    if len(valid_values) < count:
        return None

    recent = valid_values[-count:]
    return sum(recent) / count


def _classify_market(context: MarketContext, params: dict) -> dict:
    closes = extract_closes(context.klines_primary)
    highs = extract_highs(context.klines_primary)
    lows = extract_lows(context.klines_primary)

    ema_fast_series = ema(closes, params["ema_fast_period"])
    ema_slow_series = ema(closes, params["ema_slow_period"])
    rsi_series = rsi(closes, params["rsi_period"])
    atr_series = atr(highs, lows, closes, params["atr_period"])

    ema_fast = ema_fast_series[-1]
    ema_slow = ema_slow_series[-1]
    rsi_value = rsi_series[-1]
    atr_value = atr_series[-1]
    atr_average = _average_of_recent(atr_series, 20)

    if (
        ema_fast is None
        or ema_slow is None
        or rsi_value is None
        or atr_value is None
        or atr_average is None
    ):
        return {
            "market_state": "RANGE",
            "volatility_state": "LOW",
            "reason": "insufficient_indicator_data",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
        }

    close_price = closes[-1]
    ema_gap_ratio = abs(ema_fast - ema_slow) / close_price
    trend_bias = "UP" if ema_fast > ema_slow else "DOWN"

    if ema_gap_ratio < params["ema_gap_threshold"]:
        market_state = "RANGE"
    elif ema_fast > ema_slow:
        market_state = "TREND_UP"
    else:
        market_state = "TREND_DOWN"

    volatility_state = (
        "HIGH"
        if atr_value >= atr_average * params["atr_expansion_multiplier"]
        else "LOW"
    )

    return {
        "market_state": market_state,
        "volatility_state": volatility_state,
        "reason": "ok",
        "ema_fast": ema_fast,
        "ema_slow": ema_slow,
        "ema_gap_ratio": ema_gap_ratio,
        "trend_bias": trend_bias,
        "rsi": rsi_value,
    }


def _build_entry_signal(context: MarketContext, params: dict, market_state: dict) -> dict:
    closes = extract_closes(context.klines_entry)

    ema_fast_series = ema(closes, params["ema_fast_period"])
    ema_slow_series = ema(closes, params["ema_slow_period"])
    rsi_series = rsi(closes, params["rsi_period"])

    ema_fast = ema_fast_series[-1]
    ema_slow = ema_slow_series[-1]
    rsi_value = rsi_series[-1]
    current_close = closes[-1]

    if ema_fast is None or ema_slow is None or rsi_value is None:
        return {
            "entry_allowed": False,
            "side": "NONE",
            "trigger": "NO_SETUP",
            "reason": "insufficient_indicator_data",
            "confidence": 0.0,
        }

    if market_state["market_state"] == "TREND_UP":
        trend_gate_pass = True
    elif market_state["market_state"] == "RANGE":
        if market_state.get("trend_bias") != "UP":
            return {
                "entry_allowed": False,
                "side": "NONE",
                "trigger": "FILTERED",
                "reason": "range_without_upward_bias",
                "confidence": 0.0,
            }

        if ema_fast <= ema_slow:
            return {
                "entry_allowed": False,
                "side": "NONE",
                "trigger": "FILTERED",
                "reason": "range_bias_up_but_entry_trend_not_up",
                "confidence": 0.0,
            }

        trend_gate_pass = True
    else:
        trend_gate_pass = False

    if not trend_gate_pass:
        return {
            "entry_allowed": False,
            "side": "NONE",
            "trigger": "FILTERED",
            "reason": "market_not_trend_up",
            "confidence": 0.0,
        }

    if rsi_value >= params["rsi_overheat"]:
        return {
            "entry_allowed": False,
            "side": "NONE",
            "trigger": "FILTERED",
            "reason": "rsi_overheat",
            "confidence": 0.0,
        }

    relaxed_low_volatility = False
    if market_state["volatility_state"] != "HIGH":
        relaxed_threshold = (
            params["rsi_threshold"] + params["relaxed_volatility_rsi_buffer"]
        )
        if market_state["market_state"] == "TREND_UP" and rsi_value >= relaxed_threshold:
            relaxed_low_volatility = True
        else:
            return {
                "entry_allowed": False,
                "side": "NONE",
                "trigger": "FILTERED",
                "reason": "volatility_not_high",
                "confidence": 0.0,
            }

    if ema_fast <= ema_slow:
        return {
            "entry_allowed": False,
            "side": "NONE",
            "trigger": "NO_SETUP",
            "reason": "ema_fast_not_above_slow",
            "confidence": 0.0,
        }

    if rsi_value < params["rsi_threshold"]:
        return {
            "entry_allowed": False,
            "side": "NONE",
            "trigger": "NO_SETUP",
            "reason": "rsi_below_entry_threshold",
            "confidence": 0.0,
        }

    if len(context.klines_entry) <= params["breakout_lookback"]:
        return {
            "entry_allowed": False,
            "side": "NONE",
            "trigger": "NO_SETUP",
            "reason": "not_enough_breakout_lookback",
            "confidence": 0.0,
        }

    previous_highs = [
        float(item["high"])
        for item in context.klines_entry[-(params["breakout_lookback"] + 1) : -1]
    ]
    breakout_level = max(previous_highs)

    if current_close <= breakout_level:
        return {
            "entry_allowed": False,
            "side": "NONE",
            "trigger": "NO_SETUP",
            "reason": "breakout_not_confirmed",
            "confidence": 0.0,
        }

    return {
        "entry_allowed": True,
        "side": "BUY",
        "trigger": "BREAKOUT",
        "reason": (
            "trend_up_relaxed_volatility_breakout"
            if relaxed_low_volatility
            else "trend_up_high_volatility_breakout"
        ),
        "confidence": (
            params["relaxed_breakout_confidence"] if relaxed_low_volatility else 0.82
        ),
    }


class BreakoutV1Strategy(BaseStrategy):
    def __init__(self, params: dict) -> None:
        self.params = dict(params)

    def validate_params(self, params: dict) -> None:
        if params["ema_fast_period"] >= params["ema_slow_period"]:
            raise ValueError("ema_fast_period must be smaller than ema_slow_period")

        if not 0 < params["rsi_threshold"] < 100:
            raise ValueError("rsi_threshold out of range")

        if not 0 < params["rsi_overheat"] < 100:
            raise ValueError("rsi_overheat out of range")

        if params["rsi_threshold"] >= params["rsi_overheat"]:
            raise ValueError("rsi_threshold must be smaller than rsi_overheat")

        if params["atr_expansion_multiplier"] <= 1.0:
            raise ValueError("atr_expansion_multiplier must be greater than 1.0")

        if params["relaxed_volatility_rsi_buffer"] < 0:
            raise ValueError("relaxed_volatility_rsi_buffer must be >= 0")

        if not 0 < params["relaxed_breakout_confidence"] <= 1:
            raise ValueError("relaxed_breakout_confidence must be in (0, 1]")

        if params["breakout_lookback"] < 1:
            raise ValueError("breakout_lookback must be at least 1")

        if params["target_pct"] <= 0:
            raise ValueError("target_pct must be positive")

        if params["stop_loss_pct"] <= 0:
            raise ValueError("stop_loss_pct must be positive")

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
            strategy_name="breakout_v1",
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
