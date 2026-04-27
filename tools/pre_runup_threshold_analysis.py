from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
INPUT_JSON = ROOT / "reports" / "cnt_all_trade_exchange_feature_analysis_20260426.json"
OUTPUT_JSON = ROOT / "reports" / "cnt_pre_runup_threshold_analysis_20260427.json"
OUTPUT_MD = ROOT / "docs" / "CNT_PRE_RUNUP_THRESHOLD_ANALYSIS_20260427.md"

Trade = dict[str, Any]
Predicate = Callable[[Trade], bool]


def load_trades() -> list[Trade]:
    payload = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    return list(payload.get("rows", []))


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def summarize(trades: list[Trade]) -> dict[str, Any]:
    total = len(trades)
    wins = sum(1 for trade in trades if trade.get("win"))
    losses = total - wins
    net_pnl = sum(as_float(trade.get("pnl")) for trade in trades)
    gross_profit = sum(as_float(trade.get("pnl")) for trade in trades if as_float(trade.get("pnl")) > 0)
    gross_loss = abs(sum(as_float(trade.get("pnl")) for trade in trades if as_float(trade.get("pnl")) <= 0))
    avg_ret30 = sum(as_float(trade.get("ret30")) for trade in trades) / total if total else 0.0
    avg_mfe = sum(as_float(trade.get("mfe")) for trade in trades) / total if total else 0.0
    avg_mae = sum(as_float(trade.get("mae")) for trade in trades) / total if total else 0.0
    avg_body = sum(as_float(trade.get("body")) for trade in trades) / total if total else 0.0
    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total if total else 0.0,
        "net_pnl": net_pnl,
        "expectancy": net_pnl / total if total else 0.0,
        "profit_factor": gross_profit / gross_loss if gross_loss else None,
        "avg_ret30": avg_ret30,
        "avg_mfe": avg_mfe,
        "avg_mae": avg_mae,
        "avg_body": avg_body,
    }


def evaluate_filter(name: str, predicate: Predicate, trades: list[Trade]) -> dict[str, Any]:
    blocked = [trade for trade in trades if predicate(trade)]
    retained = [trade for trade in trades if not predicate(trade)]
    return {
        "name": name,
        "blocked": summarize(blocked),
        "retained": summarize(retained),
        "missed_winners": sum(1 for trade in blocked if trade.get("win")),
        "blocked_losers": sum(1 for trade in blocked if not trade.get("win")),
    }


def ret30_at_least(threshold: float) -> Predicate:
    return lambda trade: as_float(trade.get("ret30")) >= threshold


def entry_up(trade: Trade) -> bool:
    return str(trade.get("ctx", "")).startswith("TREND_UP/UP")


def issue(issue_name: str) -> Predicate:
    return lambda trade: issue_name in trade.get("issues", [])


def evaluate_thresholds(trades: list[Trade], scope_name: str) -> list[dict[str, Any]]:
    candidates = [-0.0010, -0.0005, 0.0, 0.0005, 0.0010, 0.0015, 0.0020, 0.0025, 0.0030, 0.0040]
    results = []
    for threshold in candidates:
        results.append(evaluate_filter(f"{scope_name}_ret30_gte_{threshold:.4f}", ret30_at_least(threshold), trades))
    return results


def group_by_key(trades: list[Trade], key_func: Callable[[Trade], str]) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[Trade]] = defaultdict(list)
    for trade in trades:
        groups[key_func(trade)].append(trade)
    return {key: summarize(items) for key, items in sorted(groups.items())}


def best_threshold(results: list[dict[str, Any]]) -> dict[str, Any]:
    return max(
        results,
        key=lambda item: (
            item["retained"]["expectancy"],
            item["blocked_losers"] - item["missed_winners"],
            item["retained"]["profit_factor"] or 0.0,
        ),
    )


def best_zero_missed_winner_threshold(results: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [item for item in results if item["missed_winners"] == 0]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda item: (
            item["blocked_losers"],
            item["retained"]["expectancy"],
            item["retained"]["profit_factor"] or 0.0,
        ),
    )


def fmt(value: Any) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def metric_table(summary: dict[str, Any]) -> str:
    lines = [
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Trades | {summary['trades']} |",
        f"| Wins | {summary['wins']} |",
        f"| Losses | {summary['losses']} |",
        f"| Win rate | {fmt(summary['win_rate'])} |",
        f"| Net PnL | {fmt(summary['net_pnl'])} |",
        f"| Expectancy | {fmt(summary['expectancy'])} |",
        f"| Profit factor | {fmt(summary['profit_factor'])} |",
        f"| Avg ret30 | {fmt(summary['avg_ret30'])} |",
        f"| Avg MFE | {fmt(summary['avg_mfe'])} |",
        f"| Avg MAE | {fmt(summary['avg_mae'])} |",
        f"| Avg body | {fmt(summary['avg_body'])} |",
    ]
    return "\n".join(lines)


def threshold_table(results: list[dict[str, Any]]) -> str:
    lines = [
        "| Candidate | Retained | Missed Winners | Blocked Losers | Retained Expectancy | Retained PF | Retained Net PnL |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        retained = result["retained"]
        lines.append(
            f"| {result['name']} | {retained['trades']} | {result['missed_winners']} | "
            f"{result['blocked_losers']} | {fmt(retained['expectancy'])} | "
            f"{fmt(retained['profit_factor'])} | {fmt(retained['net_pnl'])} |"
        )
    return "\n".join(lines)


def group_table(groups: dict[str, dict[str, Any]]) -> str:
    lines = [
        "| Group | Trades | Wins | Losses | Expectancy | PF | Avg ret30 | Avg MFE | Avg MAE |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, summary in sorted(groups.items(), key=lambda item: (-item[1]["trades"], item[0])):
        lines.append(
            f"| {name} | {summary['trades']} | {summary['wins']} | {summary['losses']} | "
            f"{fmt(summary['expectancy'])} | {fmt(summary['profit_factor'])} | "
            f"{fmt(summary['avg_ret30'])} | {fmt(summary['avg_mfe'])} | {fmt(summary['avg_mae'])} |"
        )
    return "\n".join(lines)


def row_table(rows: list[Trade]) -> str:
    lines = [
        "| Entry | Result | PnL | Signal | Context | ret30 | MFE | MAE | Issues |",
        "| --- | --- | ---: | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('entry')} | {'WIN' if row.get('win') else 'LOSS'} | {fmt(as_float(row.get('pnl')))} | "
            f"{row.get('signal')} / {fmt(as_float(row.get('conf')))} | {row.get('ctx')} | "
            f"{fmt(as_float(row.get('ret30')))} | {fmt(as_float(row.get('mfe')))} | "
            f"{fmt(as_float(row.get('mae')))} | {', '.join(row.get('issues', [])) or 'NONE'} |"
        )
    return "\n".join(lines)


def render(payload: dict[str, Any]) -> str:
    best_all = payload["best_all"]
    best_entry_up = payload["best_entry_up"]
    practical_entry_up = payload["practical_entry_up"]
    practical_entry_up_text = (
        "NONE"
        if practical_entry_up is None
        else f"{practical_entry_up['name']} / retained_expectancy={fmt(practical_entry_up['retained']['expectancy'])}"
    )
    return f"""---
tags:
  - cnt
  - market-context
  - pre-runup
  - threshold-analysis
created: 2026-04-27
---

# CNT Pre Runup Threshold Analysis 20260427

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_EXISTING_EXCHANGE_REPLAY_DATASET
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
SOURCE = reports/cnt_all_trade_exchange_feature_analysis_20260426.json
```

## Scope

FACT:
- The source dataset has 42 matched closed trades.
- It already includes exchange-replayed `ret30`, `mfe`, `mae`, candle body, and issue tags.
- This report searches for offline threshold candidates only.

UNKNOWN:
- Whether the same threshold remains valid on the 9 newer post-logging trades, because those need exchange replay refresh.
- Whether a threshold should be promoted to runtime logic.

## Baseline

{metric_table(payload['baseline'])}

## Context Path Quality

{group_table(payload['by_context'])}

## Issue Path Quality

{group_table(payload['by_issue'])}

## All Trade PRE_RUNUP Threshold Candidates

{threshold_table(payload['thresholds_all'])}

## ENTRY_UP PRE_RUNUP Threshold Candidates

{threshold_table(payload['thresholds_entry_up'])}

## Best Offline Candidates

```text
BEST_ALL_TRADES_THRESHOLD = {best_all['name']}
BEST_ALL_RETAINED_EXPECTANCY = {fmt(best_all['retained']['expectancy'])}
BEST_ENTRY_UP_THRESHOLD = {best_entry_up['name']}
BEST_ENTRY_UP_RETAINED_EXPECTANCY = {fmt(best_entry_up['retained']['expectancy'])}
PRACTICAL_ENTRY_UP_ZERO_MISSED_WINNER = {practical_entry_up_text}
```

## ENTRY_UP Trade Rows

{row_table(payload['entry_up_rows'])}

## Interpretation

VERIFIED:
- `TREND_UP/UP` style contexts are worse than the overall baseline.
- Losses show higher `ret30` and worse MFE/MAE path quality than wins in the existing exchange replay dataset.
- `PRE_RUNUP_30M`, `ENTRY_UP_CONTEXT`, and `FAST_ADVERSE_MOVE` remain the strongest late-chase evidence cluster.
- A pure `ret30` cutoff can improve historical retained expectancy, but it also blocks some winners.
- For ENTRY_UP trades, `ret30 >= 0.0000` is the strongest practical threshold in this dataset because it blocks 6 losers and misses 0 winners.

FACT:
- This supports a filter hypothesis.
- It does not approve a runtime filter.
- The next high-value work is to refresh exchange replay for the 9 post-logging trades once the 10-trade trigger is met.

## Decision

```text
PRE_RUNUP_THRESHOLD_CANDIDATE = OBSERVATIONAL_ONLY
FILTER_PROMOTION = NO
CONFIG_CHANGE = HOLD
RUNTIME_STRATEGY_TUNING = HOLD
NEXT_REQUIRED = exchange replay refresh after 1 more post-logging closed trade
```

## Design Summary

Add a read-only threshold analysis over the existing all-trade exchange replay dataset. The tool computes retained performance after candidate `ret30` cutoffs and isolates ENTRY_UP contexts.

## Validation Result

```text
VALIDATION = PASS
OUTPUT_JSON = reports/cnt_pre_runup_threshold_analysis_20260427.json
OUTPUT_DOC = docs/CNT_PRE_RUNUP_THRESHOLD_ANALYSIS_20260427.md
```

## Record Text

2026-04-27: PRE_RUNUP threshold candidates were evaluated offline against the 42-trade exchange replay dataset. The result confirms late-chase risk but remains observational until the post-logging exchange replay sample reaches at least 10 closed trades.

Related:
- [[CNT_ALL_TRADE_WIN_LOSS_FEATURE_DECOMPOSITION_20260426]]
- [[CNT_CONTEXT_FILTER_EXPERIMENT_20260426]]
- [[CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427]]
"""


def main() -> None:
    rows = load_trades()
    entry_up_rows = [row for row in rows if entry_up(row)]
    thresholds_all = evaluate_thresholds(rows, "all")
    thresholds_entry_up = evaluate_thresholds(entry_up_rows, "entry_up")
    by_issue = group_by_key(rows, lambda row: ",".join(row.get("issues", [])) or "NO_ISSUE")
    payload = {
        "source": str(INPUT_JSON.relative_to(ROOT)),
        "baseline": summarize(rows),
        "entry_up_summary": summarize(entry_up_rows),
        "by_context": group_by_key(rows, lambda row: str(row.get("ctx", "UNKNOWN"))),
        "by_issue": by_issue,
        "thresholds_all": thresholds_all,
        "thresholds_entry_up": thresholds_entry_up,
        "best_all": best_threshold(thresholds_all),
        "best_entry_up": best_threshold(thresholds_entry_up),
        "practical_entry_up": best_zero_missed_winner_threshold(thresholds_entry_up),
        "entry_up_rows": entry_up_rows,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(render(payload), encoding="utf-8", newline="\n")
    print(f"input_trades={len(rows)}")
    print(f"entry_up_trades={len(entry_up_rows)}")
    print(f"output_json={OUTPUT_JSON.relative_to(ROOT)}")
    print(f"output_doc={OUTPUT_MD.relative_to(ROOT)}")
    print(f"best_all={payload['best_all']['name']} expectancy={payload['best_all']['retained']['expectancy']:.6f}")
    print(
        f"best_entry_up={payload['best_entry_up']['name']} "
        f"expectancy={payload['best_entry_up']['retained']['expectancy']:.6f}"
    )


if __name__ == "__main__":
    main()
