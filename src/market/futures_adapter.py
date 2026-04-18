from __future__ import annotations


def submit_order(
    order_payload: dict,
    dry_run: bool = True,
    leverage: int = 1,
    margin_mode: str = "ISOLATED",
    reduce_only: bool = False,
) -> dict:
    payload = dict(order_payload)
    payload.update(
        {
            "leverage": leverage,
            "margin_mode": margin_mode,
            "reduce_only": reduce_only,
        }
    )
    return {
        "market": "futures",
        "dry_run": dry_run,
        "payload": payload,
    }
