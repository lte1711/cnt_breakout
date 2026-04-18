from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartialExitLevel:
    qty_ratio: float
    target_price: float


@dataclass
class ExitModel:
    stop_price: float | None
    target_price: float | None
    trailing_stop_pct: float | None = None
    partial_exit_levels: list[PartialExitLevel] | None = None
    time_based_exit_minutes: int | None = None
