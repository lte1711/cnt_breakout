from __future__ import annotations


def _to_float(value: str | float | int | None) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def extract_asset_balance(account_info: dict, asset: str) -> dict:
    balances = account_info.get("balances", [])

    for item in balances:
        if item.get("asset") == asset:
            free_value = _to_float(item.get("free"))
            locked_value = _to_float(item.get("locked"))

            return {
                "asset": asset,
                "free": free_value,
                "locked": locked_value,
                "total": free_value + locked_value,
            }

    return {
        "asset": asset,
        "free": 0.0,
        "locked": 0.0,
        "total": 0.0,
    }


def calculate_balance_change(previous_balance: dict | None, current_balance: dict) -> dict:
    previous_total = 0.0
    previous_free = 0.0
    previous_locked = 0.0

    if isinstance(previous_balance, dict):
        previous_total = _to_float(previous_balance.get("total"))
        previous_free = _to_float(previous_balance.get("free"))
        previous_locked = _to_float(previous_balance.get("locked"))

    current_total = _to_float(current_balance.get("total"))
    current_free = _to_float(current_balance.get("free"))
    current_locked = _to_float(current_balance.get("locked"))

    return {
        "asset": current_balance.get("asset"),
        "previous_total": previous_total,
        "current_total": current_total,
        "delta_total": current_total - previous_total,
        "previous_free": previous_free,
        "current_free": current_free,
        "delta_free": current_free - previous_free,
        "previous_locked": previous_locked,
        "current_locked": current_locked,
        "delta_locked": current_locked - previous_locked,
    }