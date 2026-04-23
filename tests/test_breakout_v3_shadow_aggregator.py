from __future__ import annotations

import unittest

from src.shadow.breakout_v3_shadow_eval import aggregate_breakout_v3_shadow_events


class BreakoutV3ShadowAggregatorTests(unittest.TestCase):
    def test_aggregate_breakout_v3_shadow_events(self) -> None:
        events = [
            {
                "allowed": False,
                "first_blocker": "market_not_trend_up",
                "hard_blocker": "market_not_trend_up",
                "secondary_fail_reasons": ["band_width_fail", "volume_fail"],
                "soft_pass_count": 2,
                "soft_total_count": 6,
                "min_soft_pass_required": 3,
                "stage_flags": {"regime": False, "setup": False, "trigger": False, "quality": False},
            },
            {
                "allowed": True,
                "first_blocker": None,
                "hard_blocker": None,
                "secondary_fail_reasons": [],
                "soft_pass_count": 4,
                "soft_total_count": 6,
                "min_soft_pass_required": 3,
                "stage_flags": {"regime": True, "setup": True, "trigger": True, "quality": True},
            },
        ]

        snapshot = aggregate_breakout_v3_shadow_events(events)

        self.assertEqual(snapshot["signal_count"], 2)
        self.assertEqual(snapshot["allowed_signal_count"], 1)
        self.assertAlmostEqual(snapshot["allowed_signal_ratio"], 0.5)
        self.assertEqual(snapshot["expanded_event_count"], 2)
        self.assertEqual(snapshot["first_blocker_distribution"]["market_not_trend_up"], 1)
        self.assertEqual(snapshot["hard_blocker_distribution"]["market_not_trend_up"], 1)
        self.assertEqual(snapshot["secondary_blocker_distribution"]["band_width_fail"], 1)
        self.assertEqual(snapshot["secondary_blocker_distribution"]["volume_fail"], 1)
        self.assertEqual(snapshot["soft_pass_count_distribution"][2], 1)
        self.assertEqual(snapshot["soft_pass_count_distribution"][4], 1)
        self.assertEqual(snapshot["stage_fail_counts"]["regime"], 1)
        self.assertEqual(snapshot["stage_pass_counts"]["quality"], 1)


if __name__ == "__main__":
    unittest.main()
