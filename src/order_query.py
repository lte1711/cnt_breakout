from __future__ import annotations

from binance_client import get_signed


def get_open_orders(symbol: str, base_url: str | None = None) -> list:
    response = get_signed("/api/v3/openOrders", {"symbol": symbol})

    if isinstance(response, list):
        return response

    return []


def get_order(symbol: str, order_id: int, base_url: str | None = None) -> dict:
    response = get_signed(
        "/api/v3/order",
        {
            "symbol": symbol,
            "orderId": order_id,
        },
    )

    if isinstance(response, dict):
        return response

    return {}