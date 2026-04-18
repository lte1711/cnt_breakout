from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskCheckResult:
    passed: bool
    reason: str
