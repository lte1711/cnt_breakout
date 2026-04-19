from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.analytics.performance_snapshot import build_performance_snapshot


def _write(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


class PerformanceSnapshotTests(unittest.TestCase):
    def _metrics_payload(self) -> dict:
        return {
            "breakout_v1": {
                "strategy_name": "breakout_v1",
                "signals_generated": 10,
                "signals_selected": 0,
                "trades_closed": 0,
                "wins": 0,
                "losses": 0,
                "gross_profit": 0.0,
                "gross_loss": 0.0,
                "win_rate": 0.0,
                "expectancy": 0.0,
                "profit_factor": 0.0,
            },
            "pullback_v1": {
                "strategy_name": "pullback_v1",
                "signals_generated": 10,
                "signals_selected": 2,
                "trades_closed": 1,
                "wins": 1,
                "losses": 0,
                "gross_profit": 0.01,
                "gross_loss": 0.0,
                "win_rate": 1.0,
                "expectancy": 0.01,
                "profit_factor": 0.0,
            },
        }

    def test_legacy_no_ranked_signal_log_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            metrics_file = root / "strategy_metrics.json"
            portfolio_log = root / "portfolio.log"
            _write(metrics_file, json.dumps(self._metrics_payload()))
            _write(
                portfolio_log,
                "[2026-04-20 00:00:00] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal rank_score=0.0 rank_score_components={} blocked_by_policy=no_ranked_signal\n",
            )

            snapshot = build_performance_snapshot(metrics_file, portfolio_log)

            self.assertEqual(snapshot["blocked_signal_stats"]["no_ranked_signal"], 1)
            self.assertEqual(snapshot["selected_strategy_counts"], {})

    def test_new_no_ranked_signal_detail_is_grouped_as_nested_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            metrics_file = root / "strategy_metrics.json"
            portfolio_log = root / "portfolio.log"
            _write(metrics_file, json.dumps(self._metrics_payload()))
            _write(
                portfolio_log,
                "[2026-04-20 00:00:00] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal rank_score=0.0 rank_score_components={} blocked_by_policy=no_ranked_signal blocked_detail=all_filtered total_signals=2 candidate_count=0 rejected_reasons={'volatility_not_high': 2}\n",
            )

            snapshot = build_performance_snapshot(metrics_file, portfolio_log)

            self.assertEqual(snapshot["blocked_signal_stats"]["no_ranked_signal"], {"all_filtered": 1})

    def test_mixed_legacy_and_new_no_ranked_signal_logs_are_both_counted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            metrics_file = root / "strategy_metrics.json"
            portfolio_log = root / "portfolio.log"
            _write(metrics_file, json.dumps(self._metrics_payload()))
            _write(
                portfolio_log,
                "\n".join(
                    [
                        "[2026-04-20 00:00:00] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal rank_score=0.0 rank_score_components={} blocked_by_policy=no_ranked_signal",
                        "[2026-04-20 00:10:00] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal rank_score=0.0 rank_score_components={} blocked_by_policy=no_ranked_signal blocked_detail=no_candidate total_signals=2 candidate_count=0 rejected_reasons={'market_not_trend_up': 2}",
                    ]
                )
                + "\n",
            )

            snapshot = build_performance_snapshot(metrics_file, portfolio_log)

            self.assertEqual(
                snapshot["blocked_signal_stats"]["no_ranked_signal"],
                {"no_candidate": 1, "legacy": 1},
            )

    def test_selected_strategy_counts_only_selection_reason_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            metrics_file = root / "strategy_metrics.json"
            portfolio_log = root / "portfolio.log"
            _write(metrics_file, json.dumps(self._metrics_payload()))
            _write(
                portfolio_log,
                "\n".join(
                    [
                        "[2026-04-20 00:00:00] symbol=ETHUSDT selected_strategy=pullback_v1 confidence=0.74 selection_reason=highest_score reason=trend_pullback_reentry rank_score=1.77 rank_score_components={'score': 1.77} strategy_expectancy_snapshot={'trades_closed': 1} rank_candidates=[{'strategy': 'pullback_v1', 'score': 1.77}]",
                        "[2026-04-20 00:10:00] symbol=ETHUSDT selected_strategy=pullback_v1 close_action=SELL_FILLED close_pnl_estimate=0.01 strategy_expectancy_snapshot={'trades_closed': 2}",
                    ]
                )
                + "\n",
            )

            snapshot = build_performance_snapshot(metrics_file, portfolio_log)

            self.assertEqual(snapshot["selected_strategy_counts"], {"pullback_v1": 1})

    def test_entry_gate_block_details_are_grouped(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            metrics_file = root / "strategy_metrics.json"
            portfolio_log = root / "portfolio.log"
            _write(metrics_file, json.dumps(self._metrics_payload()))
            _write(
                portfolio_log,
                "[2026-04-20 00:00:00] symbol=ETHUSDT selected_strategy=breakout_v1 blocked_by_policy=entry_gate blocked_detail=stale_signal total_signals=2 candidate_count=1 rejected_reasons={'market_not_trend_up': 1}\n",
            )

            snapshot = build_performance_snapshot(metrics_file, portfolio_log)

            self.assertEqual(snapshot["blocked_signal_stats"]["entry_gate"], {"stale_signal": 1})


if __name__ == "__main__":
    unittest.main()
