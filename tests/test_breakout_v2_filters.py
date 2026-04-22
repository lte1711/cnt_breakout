from __future__ import annotations

import unittest
from unittest.mock import patch

from src.models.market_context import MarketContext
from src.strategies import breakout_v2
from src.strategies.breakout_v2 import BreakoutV2Strategy


def _context() -> MarketContext:
    primary = []
    entry = []
    closes = [100.0, 101.0, 102.0, 103.0, 104.0, 106.0]
    volumes = [100.0, 105.0, 110.0, 120.0, 130.0, 300.0]

    for close, volume in zip(closes, volumes):
        candle = {
            "open": close - 0.5,
            "high": close,
            "low": close - 1.0,
            "close": close,
            "volume": volume,
        }
        primary.append(dict(candle))
        entry.append(dict(candle))

    return MarketContext(
        symbol="ETHUSDT",
        primary_interval="5m",
        entry_interval="1m",
        klines_primary=primary,
        klines_entry=entry,
        last_price=106.0,
    )


def _params() -> dict:
    return {
        "ema_fast_period": 9,
        "ema_slow_period": 20,
        "rsi_period": 14,
        "atr_period": 14,
        "ema_gap_threshold": 0.001,
        "atr_expansion_multiplier": 1.02,
        "rsi_threshold": 52,
        "rsi_overheat": 75,
        "breakout_lookback": 3,
        "target_pct": 0.002,
        "stop_loss_pct": 0.0015,
        "signal_age_limit_sec": 15,
        "bollinger_period": 20,
        "bollinger_std_multiplier": 2.0,
        "min_band_width_ratio": 0.006,
        "min_band_expansion_ratio": 1.03,
        "vwap_period": 20,
        "min_vwap_distance_ratio": 0.0015,
        "volume_avg_period": 3,
        "min_volume_multiplier": 1.5,
        "band_reentry_exit_enabled": True,
        "vwap_fail_exit_enabled": True,
        "breakout_v2_confidence": 0.78,
    }


class BreakoutV2FilterTests(unittest.TestCase):
    def test_narrow_band_is_filtered(self) -> None:
        strategy = BreakoutV2Strategy(_params())
        market_state = {
            "market_state": "TREND_UP",
            "volatility_state": "HIGH",
            "trend_bias": "UP",
        }

        with (
            patch("src.strategies.breakout_v2._classify_market", return_value=market_state),
            patch("src.strategies.breakout_v2.ema", side_effect=[[101.0] * 6, [100.0] * 6]),
            patch("src.strategies.breakout_v2.rsi", return_value=[60.0] * 6),
            patch(
                "src.strategies.breakout_v2.bollinger_bands",
                return_value=(
                    [100.2, 100.3, 100.4, 100.5, 100.6, 100.7],
                    [100.0] * 6,
                    [99.9, 100.0, 100.1, 100.2, 100.3, 100.35],
                ),
            ),
            patch("src.strategies.breakout_v2.rolling_vwap", return_value=[100.0] * 6),
        ):
            signal = strategy.evaluate(_context())

        self.assertFalse(signal.entry_allowed)
        self.assertEqual(signal.reason, "band_width_too_narrow")

    def test_volume_confirmation_missing_is_filtered(self) -> None:
        strategy = BreakoutV2Strategy(_params())
        market_state = {
            "market_state": "TREND_UP",
            "volatility_state": "HIGH",
            "trend_bias": "UP",
        }
        context = _context()
        context.klines_entry[-1]["volume"] = 180.0

        with (
            patch("src.strategies.breakout_v2._classify_market", return_value=market_state),
            patch("src.strategies.breakout_v2.ema", side_effect=[[101.0] * 6, [100.0] * 6]),
            patch("src.strategies.breakout_v2.rsi", return_value=[60.0] * 6),
            patch(
                "src.strategies.breakout_v2.bollinger_bands",
                return_value=(
                    [102.0, 103.0, 104.0, 105.0, 106.0, 108.0],
                    [100.0] * 6,
                    [98.0, 99.0, 100.0, 101.0, 102.0, 103.0],
                ),
            ),
            patch("src.strategies.breakout_v2.rolling_vwap", return_value=[103.0] * 6),
        ):
            signal = strategy.evaluate(context)

        self.assertFalse(signal.entry_allowed)
        self.assertEqual(signal.reason, "volume_not_confirmed")

    def test_breakout_below_vwap_is_filtered(self) -> None:
        strategy = BreakoutV2Strategy(_params())
        market_state = {
            "market_state": "TREND_UP",
            "volatility_state": "HIGH",
            "trend_bias": "UP",
        }

        with (
            patch("src.strategies.breakout_v2._classify_market", return_value=market_state),
            patch("src.strategies.breakout_v2.ema", side_effect=[[101.0] * 6, [100.0] * 6]),
            patch("src.strategies.breakout_v2.rsi", return_value=[60.0] * 6),
            patch(
                "src.strategies.breakout_v2.bollinger_bands",
                return_value=(
                    [102.0, 103.0, 104.0, 105.0, 106.0, 108.0],
                    [100.0] * 6,
                    [98.0, 99.0, 100.0, 101.0, 102.0, 103.0],
                ),
            ),
            patch("src.strategies.breakout_v2.rolling_vwap", return_value=[107.0] * 6),
        ):
            signal = strategy.evaluate(_context())

        self.assertFalse(signal.entry_allowed)
        self.assertEqual(signal.reason, "price_not_above_vwap")

    def test_valid_breakout_is_allowed(self) -> None:
        strategy = BreakoutV2Strategy(_params())
        market_state = {
            "market_state": "TREND_UP",
            "volatility_state": "HIGH",
            "trend_bias": "UP",
        }

        with (
            patch("src.strategies.breakout_v2._classify_market", return_value=market_state),
            patch("src.strategies.breakout_v2.ema", side_effect=[[101.0] * 6, [100.0] * 6]),
            patch("src.strategies.breakout_v2.rsi", return_value=[60.0] * 6),
            patch(
                "src.strategies.breakout_v2.bollinger_bands",
                return_value=(
                    [101.0, 102.0, 103.0, 104.0, 105.0, 109.0],
                    [100.0] * 6,
                    [99.0, 99.2, 99.4, 99.6, 99.8, 101.0],
                ),
            ),
            patch("src.strategies.breakout_v2.rolling_vwap", return_value=[103.0] * 6),
        ):
            signal = strategy.evaluate(_context())

        self.assertTrue(signal.entry_allowed)
        self.assertEqual(signal.reason, "trend_up_vwap_boll_volume_breakout")
        self.assertEqual(signal.confidence, 0.78)


if __name__ == "__main__":
    unittest.main()
