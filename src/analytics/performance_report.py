from __future__ import annotations

from pathlib import Path


def _fmt_ratio(value: float) -> str:
    return f"{value:.4f}"


def _fmt_value(value: float) -> str:
    return f"{value:.6f}"


def _format_strategy_breakdown(strategy_breakdown: dict) -> str:
    if not strategy_breakdown:
        return "none"

    lines: list[str] = []
    for strategy_name, payload in strategy_breakdown.items():
        lines.append(
            f"{strategy_name}: trades_closed={payload.get('trades_closed', 0)}, "
            f"wins={payload.get('wins', 0)}, losses={payload.get('losses', 0)}, "
            f"win_rate={_fmt_ratio(float(payload.get('win_rate', 0.0) or 0.0))}, "
            f"expectancy={_fmt_value(float(payload.get('expectancy', 0.0) or 0.0))}, "
            f"profit_factor={_fmt_value(float(payload.get('profit_factor', 0.0) or 0.0))}"
        )
    return " | ".join(lines)


def _format_stats(stats: dict) -> str:
    if not stats:
        return "none"
    return ", ".join(f"{key}={value}" for key, value in sorted(stats.items()))


def _top_and_worst_strategy(strategy_breakdown: dict) -> tuple[str, str]:
    if not strategy_breakdown:
        return "none", "none"

    scored = []
    for strategy_name, payload in strategy_breakdown.items():
        expectancy = float(payload.get("expectancy", 0.0) or 0.0)
        trades_closed = int(payload.get("trades_closed", 0) or 0)
        scored.append((expectancy, trades_closed, strategy_name))

    scored.sort()
    worst = scored[0][2]
    top = scored[-1][2]
    return top, worst


def build_performance_report_text(snapshot: dict) -> str:
    top_strategy, worst_strategy = _top_and_worst_strategy(snapshot.get("strategy_breakdown", {}))
    return f"""# CNT v2 TESTNET PERFORMANCE REPORT

```text
DOCUMENT_NAME = cnt_v2_testnet_performance_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = {snapshot.get('timestamp', '')[:10]}
STATUS        = DATA_COLLECTION_IN_PROGRESS
LAST_UPDATED  = {snapshot.get('timestamp', '')}
```

---

# AUTO SNAPSHOT

```text
OBSERVATION_WINDOW: up to {snapshot.get('timestamp', '')}
TOTAL_SIGNALS: {snapshot.get('total_signals', 0)}
TOTAL_SELECTED_SIGNALS: {snapshot.get('selected_signals', 0)}
TOTAL_EXECUTED_TRADES: {snapshot.get('executed_trades', 0)}
TOTAL_CLOSED_TRADES: {snapshot.get('closed_trades', 0)}
WINS: {snapshot.get('wins', 0)}
LOSSES: {snapshot.get('losses', 0)}
WIN_RATE: {_fmt_ratio(float(snapshot.get('win_rate', 0.0) or 0.0))}
AVG_WIN: {_fmt_value(float(snapshot.get('avg_win', 0.0) or 0.0))}
AVG_LOSS: {_fmt_value(float(snapshot.get('avg_loss', 0.0) or 0.0))}
EXPECTANCY: {_fmt_value(float(snapshot.get('expectancy', 0.0) or 0.0))}
PROFIT_FACTOR: {_fmt_value(float(snapshot.get('profit_factor', 0.0) or 0.0))}
NET_PNL: {_fmt_value(float(snapshot.get('net_pnl', 0.0) or 0.0))}
MAX_CONSECUTIVE_LOSSES: {snapshot.get('max_consecutive_losses', 0)}
TOP_STRATEGY: {top_strategy}
WORST_STRATEGY: {worst_strategy}
BLOCKED_REASON_DISTRIBUTION: {_format_stats(snapshot.get('blocked_signal_stats', {}))}
RISK_TRIGGER_STATS: {_format_stats(snapshot.get('risk_trigger_stats', {}))}
STRATEGY_BREAKDOWN: {_format_strategy_breakdown(snapshot.get('strategy_breakdown', {}))}
NOTES: auto-generated from performance snapshot
```
"""


def generate_performance_report(report_file: Path, snapshot: dict) -> None:
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(build_performance_report_text(snapshot), encoding="utf-8")
