from __future__ import annotations

import time

from src.indicators import ema, extract_closes, rsi
from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal
from src.risk.exit_models import ExitModel
from src.strategies.base import BaseStrategy


class MeanReversionV1Strategy(BaseStrategy):
    def __init__(self, params: dict) -> None:
        self.params = dict(params)

    def validate_params(self, params: dict) -> None:
        if not 0 < params["rsi_oversold"] < 100:
            raise ValueError("rsi_oversold out of range")

    def evaluate(self, context: MarketContext) -> StrategySignal:
        closes = extract_closes(context.klines_entry)
        ema_series = ema(closes, self.params["ema_period"])
        rsi_series = rsi(closes, self.params["rsi_period"])

        ema_value = ema_series[-1]
        rsi_value = rsi_series[-1]
        last_price = context.last_price
        entry_allowed = False
        confidence = 0.0
        reason = "mean_reversion_not_ready"

        if ema_value is not None and rsi_value is not None:
            if last_price < ema_value and rsi_value <= self.params["rsi_oversold"]:
                entry_allowed = True
                confidence = 0.68
                reason = "oversold_mean_reversion_setup"
            elif last_price >= ema_value:
                reason = "price_not_below_ema"
            else:
                reason = "rsi_not_oversold"
        else:
            reason = "insufficient_indicator_data"

        exit_model = None
        entry_price_hint = None
        if entry_allowed:
            entry_price_hint = last_price
            exit_model = ExitModel(
                stop_price=entry_price_hint * (1 - self.params["stop_loss_pct"]),
                target_price=entry_price_hint * (1 + self.params["target_pct"]),
            )

        return StrategySignal(
            strategy_name="mean_reversion_v1",
            symbol=context.symbol,
            signal_timestamp=time.time(),
            signal_age_limit_sec=float(self.params["signal_age_limit_sec"]),
            entry_allowed=entry_allowed,
            side="BUY" if entry_allowed else "NONE",
            trigger="MEAN_REVERSION" if entry_allowed else "NO_SETUP",
            reason=reason,
            confidence=confidence,
            market_state="MEAN_REVERSION",
            volatility_state="MEDIUM",
            entry_price_hint=entry_price_hint,
            exit_model=exit_model,
        )
