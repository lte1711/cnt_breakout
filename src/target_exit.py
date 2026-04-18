from __future__ import annotations


def calculate_target_price(entry_price: float, target_pct: float) -> float:
    return entry_price * (1.0 + target_pct)


def should_exit_long(current_price: float, target_price: float) -> bool:
    return current_price >= target_price