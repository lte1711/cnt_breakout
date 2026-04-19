from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StrategyPerformance:
    strategy_name: str
    signals_generated: int = 0
    signals_selected: int = 0
    trades_closed: int = 0
    wins: int = 0
    losses: int = 0
    gross_profit: float = 0.0
    gross_loss: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    win_rate: float = 0.0
    expectancy: float = 0.0
    profit_factor: float = 0.0
    confidence_multiplier: float = 0.0
    last_updated: str | None = None
