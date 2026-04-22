from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.shadow_eval import append_shadow_log, evaluate_breakout_v2_shadow, update_shadow_snapshot


def _kline(
    open_price: float,
    high: float,
    low: float,
    close: float,
    volume: float,
) -> dict:
    return {
        "open": str(open_price),
        "high": str(high),
        "low": str(low),
        "close": str(close),
        "volume": str(volume),
    }


class ShadowEvalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
            "ema_fast_period": 3,
            "ema_slow_period": 5,
            "rsi_period": 3,
            "atr_period": 3,
            "ema_gap_threshold": 0.001,
            "atr_expansion_multiplier": 1.02,
            "rsi_threshold": 52,
            "rsi_overheat": 75,
            "breakout_lookback": 3,
            "target_pct": 0.002,
            "stop_loss_pct": 0.0015,
            "signal_age_limit_sec": 15,
            "bollinger_period": 5,
            "bollinger_std_multiplier": 2.0,
            "min_band_width_ratio": 0.001,
            "min_band_expansion_ratio": 1.01,
            "vwap_period": 5,
            "min_vwap_distance_ratio": 0.0005,
            "volume_avg_period": 5,
            "min_volume_multiplier": 1.1,
            "band_reentry_exit_enabled": True,
            "vwap_fail_exit_enabled": True,
            "breakout_v2_confidence": 0.78,
        }

    def test_evaluate_breakout_v2_shadow_returns_schema(self) -> None:
        klines = [
            _kline(100, 101, 99, 100.0, 100),
            _kline(100, 102, 99, 101.0, 100),
            _kline(101, 103, 100, 102.0, 100),
            _kline(102, 104, 101, 103.0, 100),
            _kline(103, 106, 102, 105.5, 200),
            _kline(105, 110, 104, 109.0, 300),
        ]

        with (
            patch("src.shadow_eval.get_recent_closed_klines", return_value=klines),
            patch("src.shadow_eval.get_price", return_value=109.0),
        ):
            result = evaluate_breakout_v2_shadow("ETHUSDT", self.params)

        expected_keys = {
            "ts",
            "symbol",
            "strategy",
            "signal_generated",
            "entry_allowed",
            "filter_reason",
            "confidence",
            "vwap",
            "band_width_ratio",
            "band_expansion_ratio",
            "volume_ratio",
            "hypothetical_entry",
        }
        self.assertEqual(result["symbol"], "ETHUSDT")
        self.assertEqual(result["strategy"], "breakout_v2_shadow")
        self.assertTrue(expected_keys.issubset(result.keys()))

    def test_append_shadow_log_writes_jsonl(self) -> None:
        event = {
            "ts": "2026-04-22T15:00:00+09:00",
            "symbol": "ETHUSDT",
            "strategy": "breakout_v2_shadow",
            "signal_generated": True,
            "entry_allowed": False,
            "filter_reason": "volume_not_confirmed",
            "confidence": 0.78,
            "vwap": 2300.0,
            "band_width_ratio": 0.01,
            "band_expansion_ratio": 1.05,
            "volume_ratio": 0.8,
            "hypothetical_entry": False,
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "logs" / "shadow_breakout_v2.jsonl"
            append_shadow_log(log_file, event)
            lines = log_file.read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["filter_reason"], "volume_not_confirmed")

    def test_update_shadow_snapshot_updates_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            snapshot_file = Path(tmpdir) / "data" / "shadow_breakout_v2_snapshot.json"
            filtered_event = {
                "ts": "2026-04-22T15:00:00+09:00",
                "entry_allowed": False,
                "filter_reason": "band_width_too_narrow",
            }
            allowed_event = {
                "ts": "2026-04-22T15:10:00+09:00",
                "entry_allowed": True,
                "filter_reason": "trend_up_vwap_boll_volume_breakout",
            }

            update_shadow_snapshot(snapshot_file, filtered_event)
            update_shadow_snapshot(snapshot_file, allowed_event)
            snapshot = json.loads(snapshot_file.read_text(encoding="utf-8"))

        self.assertEqual(snapshot["signal_count"], 2)
        self.assertEqual(snapshot["filtered_signal_count"], 1)
        self.assertEqual(snapshot["allowed_signal_count"], 1)
        self.assertEqual(snapshot["hypothetical_trades_count"], 1)
        self.assertAlmostEqual(snapshot["filtered_signal_ratio"], 0.5)
        self.assertAlmostEqual(snapshot["allowed_signal_ratio"], 0.5)
        self.assertEqual(snapshot["reason_distribution"]["band_width_too_narrow"], 1)
        self.assertEqual(snapshot["reason_distribution"]["trend_up_vwap_boll_volume_breakout"], 1)


if __name__ == "__main__":
    unittest.main()
