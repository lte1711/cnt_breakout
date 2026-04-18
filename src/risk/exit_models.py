from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExitModel:
    stop_price: float | None
    target_price: float | None
    trailing_stop_pct: float | None = None
    partial_exit_levels: list[dict] | None = None
    time_based_exit_minutes: int | None = None
