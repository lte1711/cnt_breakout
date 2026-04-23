from __future__ import annotations

import unittest

from src.models.breakout_v3_eval_result import BreakoutV3Conditions
from src.shadow.breakout_v3_shadow_eval import (
    build_breakout_v3_shadow_event,
    evaluate_breakout_v3_shadow,
)


class BreakoutV3ShadowEvalTests(unittest.TestCase):
    def _conditions(self, **overrides: bool) -> BreakoutV3Conditions:
        base = {
            "market_bias_pass": True,
            "trend_up_pass": True,
            "range_bias_pass": True,
            "setup_ready": True,
            "volatility_floor_pass": True,
            "price_position_pass": True,
            "breakout_confirmed": True,
            "trigger_price_pass": True,
            "band_width_pass": True,
            "band_expansion_pass": True,
            "volume_pass": True,
            "vwap_distance_pass": True,
            "rsi_threshold_pass": True,
            "ema_pass": True,
        }
        base.update(overrides)
        return BreakoutV3Conditions(**base)

    def test_regime_fail_creates_hard_fail(self) -> None:
        result = evaluate_breakout_v3_shadow(
            self._conditions(market_bias_pass=False, trend_up_pass=False, range_bias_pass=False)
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.summary_reason, "regime_blocked")
        self.assertEqual(result.first_blocker, "market_not_trend_up")
        self.assertEqual(result.hard_blocker, "market_not_trend_up")

    def test_trigger_fail_creates_hard_fail(self) -> None:
        result = evaluate_breakout_v3_shadow(
            self._conditions(breakout_confirmed=False, trigger_price_pass=False)
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.summary_reason, "trigger_blocked")
        self.assertEqual(result.first_blocker, "breakout_not_confirmed")

    def test_hard_pass_soft_two_blocked(self) -> None:
        result = evaluate_breakout_v3_shadow(
            self._conditions(
                band_width_pass=True,
                band_expansion_pass=False,
                volume_pass=False,
                vwap_distance_pass=False,
                rsi_threshold_pass=True,
                ema_pass=False,
            ),
            min_soft_pass_required=3,
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.soft_pass_count, 2)

    def test_hard_pass_soft_three_allowed(self) -> None:
        result = evaluate_breakout_v3_shadow(
            self._conditions(
                band_width_pass=True,
                band_expansion_pass=False,
                volume_pass=False,
                vwap_distance_pass=True,
                rsi_threshold_pass=True,
                ema_pass=False,
            ),
            min_soft_pass_required=3,
        )
        self.assertTrue(result.allowed)

    def test_first_blocker_ordering_prefers_regime(self) -> None:
        result = evaluate_breakout_v3_shadow(
            self._conditions(
                market_bias_pass=False,
                trend_up_pass=False,
                range_bias_pass=False,
                breakout_confirmed=False,
                band_width_pass=False,
            )
        )
        self.assertEqual(result.first_blocker, "market_not_trend_up")

    def test_secondary_fail_reasons_and_stage_flags_present(self) -> None:
        result = evaluate_breakout_v3_shadow(
            self._conditions(
                band_width_pass=False,
                band_expansion_pass=False,
                volume_pass=True,
                vwap_distance_pass=False,
                rsi_threshold_pass=True,
                ema_pass=False,
            ),
            min_soft_pass_required=4,
        )
        self.assertIn("band_width_fail", result.secondary_fail_reasons)
        self.assertIn("band_expansion_fail", result.secondary_fail_reasons)
        self.assertIn("vwap_distance_fail", result.secondary_fail_reasons)
        self.assertIn("ema_fail", result.secondary_fail_reasons)

        event = build_breakout_v3_shadow_event(result, symbol="ETHUSDT", metadata={"timeframe": "5m"})
        event_dict = event.to_dict()
        self.assertEqual(event_dict["strategy_name"], "breakout_v3_candidate")
        self.assertIn("regime", event_dict["stage_flags"])
        self.assertIn("band_width_pass", event_dict["condition_flags"])


if __name__ == "__main__":
    unittest.main()
