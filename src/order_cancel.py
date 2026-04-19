from __future__ import annotations

from binance_client import delete_signed


def cancel_order(symbol: str, order_id: int) -> dict:
    response = delete_signed(
        "/api/v3/order",
        {
            "symbol": symbol,
            "orderId": order_id,
        },
    )

    if isinstance(response, dict):
        return response

    return {}
