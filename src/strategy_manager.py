from __future__ import annotations

import time

from binance_client import get_price
from config import ACTIVE_STRATEGY, ENTRY_INTERVAL, KLINES_LIMIT, PRIMARY_INTERVAL, STRATEGY_PARAMS
from src.market_data import get_recent_closed_klines
from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal
from src.strategy_registry import STRATEGY_REGISTRY


def _build_error_signal(symbol: str, strategy_name: str, message: str) -> StrategySignal:
    return StrategySignal(
        strategy_name=strategy_name,
        symbol=symbol,
        signal_timestamp=time.time(),
        signal_age_limit_sec=0,
        entry_allowed=False,
        side="NONE",
        trigger="ERROR",
        reason=f"strategy_error:{message}",
        confidence=0.0,
        market_state="UNKNOWN",
        volatility_state="UNKNOWN",
        entry_price_hint=None,
        exit_model=None,
    )


def generate_strategy_signal(symbol: str) -> StrategySignal:
    active_strategy = ACTIVE_STRATEGY

    try:
        strategy_class = STRATEGY_REGISTRY[active_strategy]
        params = dict(STRATEGY_PARAMS[active_strategy])
        strategy = strategy_class(params)
        strategy.validate_params(params)

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

        context = MarketContext(
            symbol=symbol,
            primary_interval=PRIMARY_INTERVAL,
            entry_interval=ENTRY_INTERVAL,
            klines_primary=klines_primary,
            klines_entry=klines_entry,
            last_price=last_price,
        )

        return strategy.evaluate(context)
    except Exception as error:
        return _build_error_signal(symbol, active_strategy, str(error))
