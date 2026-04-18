from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExitSignal:
    should_exit: bool
    exit_type: str
    reason: str
    target_price: float | None
    stop_price: float | None
    partial_qty: float | None
