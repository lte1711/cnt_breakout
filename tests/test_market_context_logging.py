from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.analytics.performance_report import build_performance_report_text
from src.analytics.performance_snapshot import build_performance_snapshot
from src.models.strategy_signal import StrategySignal
from src.risk.exit_models import ExitModel
from src.signal_logger import append_signal_log


class MarketContextLoggingTests(unittest.TestCase):
    def test_signal_log_includes_decision_id_and_market_features(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "signal.log"
            signal = StrategySignal(
                strategy_name="pullback_v1",
                symbol="ETHUSDT",
                signal_timestamp=1.0,
                signal_age_limit_sec=-1,
                entry_allowed=True,
                side="BUY",
                trigger="PULLBACK",
                reason="trend_pullback_reentry",
                confidence=0.74,
                market_state="TREND_UP",
                volatility_state="MEDIUM",
                entry_price_hint=2300.0,
                exit_model=ExitModel(stop_price=2290.0, target_price=2310.0),
                trend_bias="UP",
                decision_id="ETHUSDT-pullback_v1-1000",
                market_features={
                    "multi_timeframe_trend": "PRIMARY_UP_ENTRY_UP",
                    "entry": {"rsi": 48.0, "atr_pct": 0.001},
                },
            )

            append_signal_log(log_file, signal)
            content = log_file.read_text(encoding="utf-8")

        self.assertIn("decision_id=ETHUSDT-pullback_v1-1000", content)
        self.assertIn("market_features=", content)
        self.assertIn("multi_timeframe_trend", content)

    def test_performance_report_includes_market_context_split(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            metrics_file = root / "strategy_metrics.json"
            portfolio_log_file = root / "portfolio.log"
            runtime_log_file = root / "runtime.log"
            portfolio_state_file = root / "portfolio_state.json"

            metrics_file.write_text("{}", encoding="utf-8")
            runtime_log_file.write_text("", encoding="utf-8")
            portfolio_state_file.write_text('{"open_positions":[]}', encoding="utf-8")
            portfolio_log_file.write_text(
                "[2026-04-26 00:00:00] symbol=ETHUSDT selected_strategy=pullback_v1 "
                "close_action=SELL_FILLED close_pnl_estimate=0.01 "
                "decision_id=ETHUSDT-pullback_v1-1 market_context=PRIMARY_UP_ENTRY_UP "
                "market_features={}\n",
                encoding="utf-8",
            )

            snapshot = build_performance_snapshot(
                metrics_file=metrics_file,
                portfolio_log_file=portfolio_log_file,
                runtime_log_file=runtime_log_file,
                portfolio_state_file=portfolio_state_file,
            )
            report_text = build_performance_report_text(snapshot)

        self.assertIn("pullback_v1:PRIMARY_UP_ENTRY_UP", snapshot["market_context_performance"])
        self.assertIn("MARKET_CONTEXT_PERFORMANCE:", report_text)
        self.assertIn("PRIMARY_UP_ENTRY_UP", report_text)


if __name__ == "__main__":
    unittest.main()
