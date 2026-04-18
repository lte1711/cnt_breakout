from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionState:
    position_id: str
    symbol: str
    market_type: str
    strategy_name: str
    entry_price: float
    entry_qty: float
    entry_time: str
    stop_price: float | None
    target_price: float | None
    status: str
