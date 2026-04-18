from __future__ import annotations

from src.market.futures_adapter import submit_order as submit_futures_order
from src.market.spot_adapter import submit_order as submit_spot_order


def route_order(decision, order_payload: dict, market: str = "spot", dry_run: bool = True) -> dict:
    del decision

    if market.lower() == "futures":
        return submit_futures_order(order_payload, dry_run=dry_run)

    return submit_spot_order(order_payload, dry_run=dry_run)
