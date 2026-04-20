from __future__ import annotations

import unittest
from unittest.mock import patch

from src.models.market_context import MarketContext
from src.strategies import breakout_v1


def _context() -> MarketContext:
    primary = []
    entry = []
    for idx, close in enumerate([100.0, 101.0, 102.0, 103.0, 104.0, 105.0]):
        candle = {
            "open": close - 0.5,
            "high": close,
            "low": close - 1.0,
            "close": close,
        }
        primary.append(dict(candle))
        entry.append(dict(candle))

    return MarketContext(
        symbol="ETHUSDT",
        primary_interval="5m",
        entry_interval="1m",
        klines_primary=primary,
        klines_entry=entry,
        last_price=105.0,
    )


class BreakoutTrendFilterTests(unittest.TestCase):
    def test_classify_market_keeps_upward_bias_inside_range(self) -> None:
        context = _context()
        params = {
            "ema_fast_period": 9,
            "ema_slow_period": 20,
            "rsi_period": 14,
            "atr_period": 14,
            "ema_gap_threshold": 0.05,
            "atr_expansion_multiplier": 1.05,
        }

        with (
            patch("src.strategies.breakout_v1.ema", side_effect=[[100.0, 101.0], [99.0, 100.0]]),
            patch("src.strategies.breakout_v1.rsi", return_value=[60.0, 61.0]),
            patch("src.strategies.breakout_v1.atr", return_value=[1.0] * 25),
        ):
            result = breakout_v1._classify_market(context, params)

        self.assertEqual(result["market_state"], "RANGE")
        self.assertEqual(result["trend_bias"], "UP")

    def test_range_with_upward_bias_can_reach_breakout_setup(self) -> None:
        context = _context()
        params = {
            "ema_fast_period": 9,
            "ema_slow_period": 20,
            "rsi_period": 14,
            "rsi_threshold": 53,
            "rsi_overheat": 75,
            "breakout_lookback": 3,
        }
        market_state = {
            "market_state": "RANGE",
            "volatility_state": "HIGH",
            "trend_bias": "UP",
        }

        with (
            patch("src.strategies.breakout_v1.ema", side_effect=[[100.0] * 6, [99.0] * 6]),
            patch("src.strategies.breakout_v1.rsi", return_value=[60.0] * 6),
        ):
            result = breakout_v1._build_entry_signal(context, params, market_state)

        self.assertTrue(result["entry_allowed"])
        self.assertEqual(result["trigger"], "BREAKOUT")

    def test_range_without_upward_bias_stays_blocked(self) -> None:
        context = _context()
        params = {
            "ema_fast_period": 9,
            "ema_slow_period": 20,
            "rsi_period": 14,
            "rsi_threshold": 53,
            "rsi_overheat": 75,
            "breakout_lookback": 3,
        }
        market_state = {
            "market_state": "RANGE",
            "volatility_state": "HIGH",
            "trend_bias": "DOWN",
        }

        with (
            patch("src.strategies.breakout_v1.ema", side_effect=[[100.0] * 6, [99.0] * 6]),
            patch("src.strategies.breakout_v1.rsi", return_value=[60.0] * 6),
        ):
            result = breakout_v1._build_entry_signal(context, params, market_state)

        self.assertFalse(result["entry_allowed"])
        self.assertEqual(result["reason"], "market_not_trend_up")


if __name__ == "__main__":
    unittest.main()
