from __future__ import annotations

from config import (
    ATR_EXPANSION_MULTIPLIER,
    ATR_PERIOD,
    BREAKOUT_LOOKBACK,
    EMA_FAST_PERIOD,
    EMA_GAP_THRESHOLD,
    EMA_SLOW_PERIOD,
    ENTRY_INTERVAL,
    ENTRY_RSI_OVERHEAT,
    ENTRY_RSI_THRESHOLD,
    KLINES_LIMIT,
    PRIMARY_INTERVAL,
    RSI_PERIOD,
)
from src.indicators import atr, ema, extract_closes, extract_highs, extract_lows, rsi
from src.market_data import get_recent_closed_klines


def _average_of_recent(values: list[float | None], count: int) -> float | None:
    valid_values = [v for v in values if v is not None]

    if len(valid_values) < count:
        return None

    recent = valid_values[-count:]
    return sum(recent) / count


def classify_market(klines_5m: list[dict]) -> dict:
    closes = extract_closes(klines_5m)
    highs = extract_highs(klines_5m)
    lows = extract_lows(klines_5m)

    ema_fast_series = ema(closes, EMA_FAST_PERIOD)
    ema_slow_series = ema(closes, EMA_SLOW_PERIOD)
    rsi_series = rsi(closes, RSI_PERIOD)
    atr_series = atr(highs, lows, closes, ATR_PERIOD)

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
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "atr": atr_value,
            "reason": "insufficient_indicator_data",
        }

    close_price = closes[-1]
    ema_gap_ratio = abs(ema_fast - ema_slow) / close_price

    if ema_gap_ratio < EMA_GAP_THRESHOLD:
        market_state = "RANGE"
    elif ema_fast > ema_slow:
        market_state = "TREND_UP"
    else:
        market_state = "TREND_DOWN"

    volatility_state = (
        "HIGH"
        if atr_value >= atr_average * ATR_EXPANSION_MULTIPLIER
        else "LOW"
    )

    return {
        "market_state": market_state,
        "volatility_state": volatility_state,
        "ema_fast": ema_fast,
        "ema_slow": ema_slow,
        "rsi": rsi_value,
        "atr": atr_value,
        "reason": "ok",
    }


def build_entry_signal(klines_1m: list[dict], market_state: dict) -> dict:
    closes = extract_closes(klines_1m)

    ema_fast_series = ema(closes, EMA_FAST_PERIOD)
    ema_slow_series = ema(closes, EMA_SLOW_PERIOD)
    rsi_series = rsi(closes, RSI_PERIOD)

    ema_fast = ema_fast_series[-1]
    ema_slow = ema_slow_series[-1]
    rsi_value = rsi_series[-1]
    current_close = closes[-1]

    if ema_fast is None or ema_slow is None or rsi_value is None:
        return {
            "entry_signal": "NONE",
            "trigger": "NO_SETUP",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "insufficient_indicator_data",
        }

    if market_state.get("market_state") != "TREND_UP":
        return {
            "entry_signal": "NONE",
            "trigger": "FILTERED",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "market_not_trend_up",
        }

    if market_state.get("volatility_state") != "HIGH":
        return {
            "entry_signal": "NONE",
            "trigger": "FILTERED",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "volatility_not_high",
        }

    if rsi_value >= ENTRY_RSI_OVERHEAT:
        return {
            "entry_signal": "NONE",
            "trigger": "FILTERED",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "rsi_overheat",
        }

    if ema_fast <= ema_slow:
        return {
            "entry_signal": "NONE",
            "trigger": "NO_SETUP",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "ema_fast_not_above_slow",
        }

    if rsi_value < ENTRY_RSI_THRESHOLD:
        return {
            "entry_signal": "NONE",
            "trigger": "NO_SETUP",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "rsi_below_entry_threshold",
        }

    if len(klines_1m) <= BREAKOUT_LOOKBACK:
        return {
            "entry_signal": "NONE",
            "trigger": "NO_SETUP",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "not_enough_breakout_lookback",
        }

    previous_highs = [float(item["high"]) for item in klines_1m[-(BREAKOUT_LOOKBACK + 1):-1]]
    breakout_level = max(previous_highs)

    if current_close <= breakout_level:
        return {
            "entry_signal": "NONE",
            "trigger": "NO_SETUP",
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_value,
            "reason": "breakout_not_confirmed",
        }

    return {
        "entry_signal": "BUY",
        "trigger": "BREAKOUT",
        "ema_fast": ema_fast,
        "ema_slow": ema_slow,
        "rsi": rsi_value,
        "reason": "trend_up_high_volatility_breakout",
    }


def generate_strategy_signal(symbol: str) -> dict:
    klines_5m = get_recent_closed_klines(
        symbol=symbol,
        interval=PRIMARY_INTERVAL,
        limit=KLINES_LIMIT,
    )
    market_state = classify_market(klines_5m)

    klines_1m = get_recent_closed_klines(
        symbol=symbol,
        interval=ENTRY_INTERVAL,
        limit=KLINES_LIMIT,
    )
    entry_signal = build_entry_signal(klines_1m, market_state)

    return {
        "market_state": market_state["market_state"],
        "volatility_state": market_state["volatility_state"],
        "entry_signal": entry_signal["entry_signal"],
        "trigger": entry_signal["trigger"],
        "reason": entry_signal["reason"],
    }
