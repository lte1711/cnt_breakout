from __future__ import annotations

from binance_client import get_signed


def get_account_info() -> dict:
    return get_signed("/api/v3/account", {"omitZeroBalances": "true"})


def get_open_orders(symbol: str) -> list:
    response = get_signed("/api/v3/openOrders", {"symbol": symbol})
    if isinstance(response, list):
        return response
    return []


def get_order_info(symbol: str, order_id: int) -> dict:
    return get_signed(
        "/api/v3/order",
        {
            "symbol": symbol,
            "orderId": order_id,
        },
    )