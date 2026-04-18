from __future__ import annotations

from binance_client import post_signed


def send_test_order(order_payload: dict) -> dict:
    return post_signed("/api/v3/order/test", order_payload)


def send_live_testnet_order(order_payload: dict) -> dict:
    return post_signed("/api/v3/order", order_payload)