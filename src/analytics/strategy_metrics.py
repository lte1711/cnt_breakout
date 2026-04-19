from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from config import ACTIVE_STRATEGIES, RANKER_MINIMUM_SAMPLE
from src.models.strategy_performance import StrategyPerformance


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _default_performance(strategy_name: str) -> StrategyPerformance:
    return StrategyPerformance(strategy_name=strategy_name, last_updated=_timestamp())


def _recalculate(perf: StrategyPerformance) -> StrategyPerformance:
    perf.win_rate = (perf.wins / perf.trades_closed) if perf.trades_closed > 0 else 0.0
    perf.avg_win = (perf.gross_profit / perf.wins) if perf.wins > 0 else 0.0
    perf.avg_loss = (perf.gross_loss / perf.losses) if perf.losses > 0 else 0.0
    perf.expectancy = (perf.win_rate * perf.avg_win) - ((1 - perf.win_rate) * perf.avg_loss)
    perf.profit_factor = (perf.gross_profit / perf.gross_loss) if perf.gross_loss > 0 else 0.0
    perf.confidence_multiplier = min(1.0, perf.trades_closed / float(RANKER_MINIMUM_SAMPLE))
    perf.last_updated = _timestamp()
    return perf


def load_strategy_metrics(metrics_file: Path) -> dict[str, StrategyPerformance]:
    base = {name: _default_performance(name) for name in ACTIVE_STRATEGIES}
    if not metrics_file.exists():
        return base

    try:
        loaded = json.loads(metrics_file.read_text(encoding="utf-8"))
    except Exception:
        return base

    if not isinstance(loaded, dict):
        return base

    for strategy_name, payload in loaded.items():
        if not isinstance(payload, dict):
            continue
        base[strategy_name] = _recalculate(
            StrategyPerformance(
                strategy_name=strategy_name,
                signals_generated=int(payload.get("signals_generated", 0) or 0),
                signals_selected=int(payload.get("signals_selected", 0) or 0),
                trades_closed=int(payload.get("trades_closed", 0) or 0),
                wins=int(payload.get("wins", 0) or 0),
                losses=int(payload.get("losses", 0) or 0),
                gross_profit=float(payload.get("gross_profit", 0.0) or 0.0),
                gross_loss=float(payload.get("gross_loss", 0.0) or 0.0),
                avg_win=float(payload.get("avg_win", 0.0) or 0.0),
                avg_loss=float(payload.get("avg_loss", 0.0) or 0.0),
                win_rate=float(payload.get("win_rate", 0.0) or 0.0),
                expectancy=float(payload.get("expectancy", 0.0) or 0.0),
                profit_factor=float(payload.get("profit_factor", 0.0) or 0.0),
                confidence_multiplier=float(payload.get("confidence_multiplier", 0.0) or 0.0),
                last_updated=payload.get("last_updated"),
            )
        )

    return base


def save_strategy_metrics(metrics_file: Path, metrics: dict[str, StrategyPerformance]) -> None:
    metrics_file.parent.mkdir(parents=True, exist_ok=True)
    serializable = {name: asdict(perf) for name, perf in metrics.items()}
    metrics_file.write_text(json.dumps(serializable, indent=2, ensure_ascii=False), encoding="utf-8")


def increment_signals_generated(metrics: dict[str, StrategyPerformance], strategy_name: str) -> None:
    perf = metrics.setdefault(strategy_name, _default_performance(strategy_name))
    perf.signals_generated += 1
    _recalculate(perf)


def increment_signals_selected(metrics: dict[str, StrategyPerformance], strategy_name: str) -> None:
    perf = metrics.setdefault(strategy_name, _default_performance(strategy_name))
    perf.signals_selected += 1
    _recalculate(perf)


def record_closed_trade(metrics: dict[str, StrategyPerformance], strategy_name: str, pnl: float) -> None:
    perf = metrics.setdefault(strategy_name, _default_performance(strategy_name))
    perf.trades_closed += 1
    if pnl >= 0:
        perf.wins += 1
        perf.gross_profit += float(pnl)
    else:
        perf.losses += 1
        perf.gross_loss += abs(float(pnl))
    _recalculate(perf)


def build_expectancy_snapshot(metrics: dict[str, StrategyPerformance], strategy_name: str) -> dict:
    perf = metrics.get(strategy_name) or _default_performance(strategy_name)
    return {
        "trades_closed": perf.trades_closed,
        "win_rate": perf.win_rate,
        "expectancy": perf.expectancy,
        "confidence_multiplier": perf.confidence_multiplier,
        "profit_factor": perf.profit_factor,
    }
