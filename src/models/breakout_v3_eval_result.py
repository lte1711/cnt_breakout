from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class BreakoutV3Conditions:
    market_bias_pass: bool
    trend_up_pass: bool
    range_bias_pass: bool
    setup_ready: bool
    volatility_floor_pass: bool
    price_position_pass: bool
    breakout_confirmed: bool
    trigger_price_pass: bool
    band_width_pass: bool
    band_expansion_pass: bool
    volume_pass: bool
    vwap_distance_pass: bool
    rsi_threshold_pass: bool
    ema_pass: bool

    def to_flags(self) -> dict[str, bool]:
        return {
            "market_bias_pass": self.market_bias_pass,
            "trend_up_pass": self.trend_up_pass,
            "range_bias_pass": self.range_bias_pass,
            "setup_ready": self.setup_ready,
            "volatility_floor_pass": self.volatility_floor_pass,
            "price_position_pass": self.price_position_pass,
            "breakout_confirmed": self.breakout_confirmed,
            "trigger_price_pass": self.trigger_price_pass,
            "band_width_pass": self.band_width_pass,
            "band_expansion_pass": self.band_expansion_pass,
            "volume_pass": self.volume_pass,
            "vwap_distance_pass": self.vwap_distance_pass,
            "rsi_threshold_pass": self.rsi_threshold_pass,
            "ema_pass": self.ema_pass,
        }


@dataclass
class StageResult:
    name: str
    passed: bool
    fail_reasons: list[str] = field(default_factory=list)
    evaluated_checks: list[str] = field(default_factory=list)


@dataclass
class BreakoutV3EvalResult:
    strategy_name: str
    allowed: bool
    first_blocker: str | None
    hard_blocker: str | None
    soft_pass_count: int
    soft_fail_count: int
    soft_total_count: int
    min_soft_pass_required: int
    stage_results: dict[str, StageResult]
    secondary_fail_reasons: list[str] = field(default_factory=list)
    condition_flags: dict[str, bool] = field(default_factory=dict)
    summary_reason: str = ""


@dataclass
class BreakoutV3ShadowEvent:
    timestamp: str
    symbol: str
    strategy_name: str
    allowed: bool
    summary_reason: str
    first_blocker: str | None
    hard_blocker: str | None
    soft_pass_count: int
    soft_fail_count: int
    soft_total_count: int
    min_soft_pass_required: int
    stage_flags: dict[str, bool]
    condition_flags: dict[str, bool]
    secondary_fail_reasons: list[str]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
