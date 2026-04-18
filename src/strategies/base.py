from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal


class BaseStrategy(ABC):
    @abstractmethod
    def validate_params(self, params: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, context: MarketContext) -> StrategySignal:
        raise NotImplementedError
