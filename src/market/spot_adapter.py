from __future__ import annotations


def submit_order(order_payload: dict, dry_run: bool = True) -> dict:
    return {
        "market": "spot",
        "dry_run": dry_run,
        "payload": dict(order_payload),
    }
