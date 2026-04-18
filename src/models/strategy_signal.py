from __future__ import annotations

from dataclasses import dataclass

from src.risk.exit_models import ExitModel


@dataclass
class StrategySignal:
    strategy_name: str
    symbol: str
    signal_timestamp: float
    signal_age_limit_sec: float
    entry_allowed: bool
    side: str
    trigger: str
    reason: str
    confidence: float
    market_state: str
    volatility_state: str
    entry_price_hint: float | None
    exit_model: ExitModel | None
