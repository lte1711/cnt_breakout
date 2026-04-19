from __future__ import annotations

import time

from src.indicators import ema, extract_closes, rsi
from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal
from src.risk.exit_models import ExitModel
from src.strategies.base import BaseStrategy


class PullbackV1Strategy(BaseStrategy):
    def __init__(self, params: dict) -> None:
        self.params = dict(params)

    def validate_params(self, params: dict) -> None:
        if params["ema_fast_period"] >= params["ema_slow_period"]:
            raise ValueError("ema_fast_period must be smaller than ema_slow_period")
        if not 0 < params["pullback_rsi_min"] < 100:
            raise ValueError("pullback_rsi_min out of range")
        if not 0 < params["pullback_rsi_max"] < 100:
            raise ValueError("pullback_rsi_max out of range")
        if params["pullback_rsi_min"] >= params["pullback_rsi_max"]:
            raise ValueError("pullback_rsi_min must be smaller than pullback_rsi_max")
        if float(params["target_pct"]) <= 0:
            raise ValueError("target_pct must be positive")
        if float(params["stop_loss_pct"]) <= 0:
            raise ValueError("stop_loss_pct must be positive")
        if float(params["signal_age_limit_sec"]) < -1:
            raise ValueError("signal_age_limit_sec must be >= -1")

    def evaluate(self, context: MarketContext) -> StrategySignal:
        closes = extract_closes(context.klines_entry)
        ema_fast_series = ema(closes, self.params["ema_fast_period"])
        ema_slow_series = ema(closes, self.params["ema_slow_period"])
        rsi_series = rsi(closes, self.params["rsi_period"])

        ema_fast = ema_fast_series[-1]
        ema_slow = ema_slow_series[-1]
        rsi_value = rsi_series[-1]
        reason = "pullback_not_ready"
        entry_allowed = False
        confidence = 0.0

        if ema_fast is not None and ema_slow is not None and rsi_value is not None:
            if ema_fast > ema_slow and self.params["pullback_rsi_min"] <= rsi_value <= self.params["pullback_rsi_max"]:
                entry_allowed = True
                confidence = 0.74
                reason = "trend_pullback_reentry"
            elif ema_fast <= ema_slow:
                reason = "trend_not_up"
            else:
                reason = "pullback_rsi_not_in_range"
        else:
            reason = "insufficient_indicator_data"

        exit_model = None
        entry_price_hint = None
        if entry_allowed:
            entry_price_hint = context.last_price
            exit_model = ExitModel(
                stop_price=entry_price_hint * (1 - self.params["stop_loss_pct"]),
                target_price=entry_price_hint * (1 + self.params["target_pct"]),
            )

        return StrategySignal(
            strategy_name="pullback_v1",
            symbol=context.symbol,
            signal_timestamp=time.time(),
            signal_age_limit_sec=float(self.params["signal_age_limit_sec"]),
            entry_allowed=entry_allowed,
            side="BUY" if entry_allowed else "NONE",
            trigger="PULLBACK" if entry_allowed else "NO_SETUP",
            reason=reason,
            confidence=confidence,
            market_state="TREND_UP" if ema_fast and ema_slow and ema_fast > ema_slow else "RANGE",
            volatility_state="MEDIUM",
            entry_price_hint=entry_price_hint,
            exit_model=exit_model,
        )
