from __future__ import annotations

import json
from pathlib import Path


def evaluate_live_gate(snapshot: dict) -> dict:
    closed_trades = int(snapshot.get("closed_trades", 0) or 0)
    expectancy = float(snapshot.get("expectancy", 0.0) or 0.0)
    net_pnl = float(snapshot.get("net_pnl", 0.0) or 0.0)
    max_consecutive_losses = int(snapshot.get("max_consecutive_losses", 0) or 0)
    risk_trigger_stats = snapshot.get("risk_trigger_stats", {}) or {}
    cooldown_trigger = int(risk_trigger_stats.get("LOSS_COOLDOWN", 0) or 0)

    if closed_trades < 20:
        return {
            "status": "NOT_READY",
            "reason": "INSUFFICIENT_SAMPLE",
            "metrics": {
                "closed_trades": closed_trades,
                "expectancy": expectancy,
                "net_pnl": net_pnl,
            },
        }

    if expectancy <= 0:
        return {
            "status": "FAIL",
            "reason": "NON_POSITIVE_EXPECTANCY",
            "metrics": {
                "closed_trades": closed_trades,
                "expectancy": expectancy,
                "net_pnl": net_pnl,
            },
        }

    if net_pnl <= 0:
        return {
            "status": "FAIL",
            "reason": "NON_POSITIVE_NET_PNL",
            "metrics": {
                "closed_trades": closed_trades,
                "expectancy": expectancy,
                "net_pnl": net_pnl,
            },
        }

    if max_consecutive_losses > 5:
        return {
            "status": "FAIL",
            "reason": "MAX_CONSECUTIVE_LOSSES_EXCEEDED",
            "metrics": {
                "closed_trades": closed_trades,
                "expectancy": expectancy,
                "net_pnl": net_pnl,
            },
        }

    if cooldown_trigger == 0:
        return {
            "status": "FAIL",
            "reason": "COOLDOWN_NOT_OBSERVED",
            "metrics": {
                "closed_trades": closed_trades,
                "expectancy": expectancy,
                "net_pnl": net_pnl,
            },
        }

    return {
        "status": "LIVE_READY",
        "reason": "ALL_GATES_PASSED",
        "metrics": {
            "closed_trades": closed_trades,
            "expectancy": expectancy,
            "net_pnl": net_pnl,
        },
    }


def save_live_gate_decision(decision_file: Path, decision: dict) -> None:
    decision_file.parent.mkdir(parents=True, exist_ok=True)
    decision_file.write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")
