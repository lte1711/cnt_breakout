from __future__ import annotations

from dataclasses import dataclass, field

from src.models.position_state import PositionState


@dataclass
class PortfolioState:
    schema_version: str
    total_exposure: float
    open_positions: list[PositionState] = field(default_factory=list)
    cash_balance: float = 0.0
    daily_loss_count: int = 0
    consecutive_losses: int = 0
