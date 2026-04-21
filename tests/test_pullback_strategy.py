from __future__ import annotations

import unittest
from unittest.mock import patch

from src.models.market_context import MarketContext
from src.strategies.pullback_v1 import PullbackV1Strategy


def _context() -> MarketContext:
    candles = []
    for close in [100.0, 100.5, 101.0, 101.5, 102.0, 102.5]:
        candles.append(
            {
                "open": close - 0.3,
                "high": close + 0.2,
                "low": close - 0.5,
                "close": close,
            }
        )

    return MarketContext(
        symbol="ETHUSDT",
        primary_interval="5m",
        entry_interval="1m",
        klines_primary=list(candles),
        klines_entry=list(candles),
        last_price=102.5,
    )


def _params() -> dict:
    return {
        "ema_fast_period": 9,
        "ema_slow_period": 20,
        "rsi_period": 14,
        "pullback_rsi_min": 40,
        "pullback_rsi_max": 52,
        "relaxed_pullback_rsi_min": 38,
        "relaxed_pullback_rsi_max": 56,
        "ema_near_trend_tolerance": 0.0008,
        "relaxed_pullback_confidence": 0.64,
        "near_trend_pullback_confidence": 0.58,
        "target_pct": 0.0018,
        "stop_loss_pct": 0.0015,
        "signal_age_limit_sec": 15,
    }


class PullbackStrategyTests(unittest.TestCase):
    def test_core_pullback_keeps_existing_confidence(self) -> None:
        strategy = PullbackV1Strategy(_params())

        with (
            patch("src.strategies.pullback_v1.ema", side_effect=[[100.0] * 6, [99.0] * 6]),
            patch("src.strategies.pullback_v1.rsi", return_value=[45.0] * 6),
        ):
            signal = strategy.evaluate(_context())

        self.assertTrue(signal.entry_allowed)
        self.assertEqual(signal.reason, "trend_pullback_reentry")
        self.assertEqual(signal.confidence, 0.74)

    def test_relaxed_rsi_band_creates_lower_confidence_candidate(self) -> None:
        strategy = PullbackV1Strategy(_params())

        with (
            patch("src.strategies.pullback_v1.ema", side_effect=[[100.0] * 6, [99.0] * 6]),
            patch("src.strategies.pullback_v1.rsi", return_value=[55.0] * 6),
        ):
            signal = strategy.evaluate(_context())

        self.assertTrue(signal.entry_allowed)
        self.assertEqual(signal.reason, "trend_pullback_reentry_relaxed_rsi")
        self.assertEqual(signal.confidence, 0.64)

    def test_near_trend_tolerance_creates_candidate(self) -> None:
        strategy = PullbackV1Strategy(_params())

        with (
            patch("src.strategies.pullback_v1.ema", side_effect=[[99.96] * 6, [100.0] * 6]),
            patch("src.strategies.pullback_v1.rsi", return_value=[46.0] * 6),
        ):
            signal = strategy.evaluate(_context())

        self.assertTrue(signal.entry_allowed)
        self.assertEqual(signal.reason, "near_trend_pullback_reentry")
        self.assertEqual(signal.confidence, 0.58)

    def test_trend_not_up_stays_blocked_when_gap_exceeds_tolerance(self) -> None:
        strategy = PullbackV1Strategy(_params())

        with (
            patch("src.strategies.pullback_v1.ema", side_effect=[[99.0] * 6, [100.0] * 6]),
            patch("src.strategies.pullback_v1.rsi", return_value=[46.0] * 6),
        ):
            signal = strategy.evaluate(_context())

        self.assertFalse(signal.entry_allowed)
        self.assertEqual(signal.reason, "trend_not_up")


if __name__ == "__main__":
    unittest.main()
