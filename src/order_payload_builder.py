from __future__ import annotations


def build_limit_order_payload(
    symbol: str,
    side: str,
    price: float,
    quantity: float,
) -> dict:
    return {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "timeInForce": "GTC",
        "price": str(price),
        "quantity": str(quantity),
    }