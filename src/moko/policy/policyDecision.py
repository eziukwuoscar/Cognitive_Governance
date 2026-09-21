from dataclasses import dataclass
from typing import Literal


Decision = Literal[
    "ALLOW",
    "BLOCK",
    "REQUIRE_APPROVAL"
]



@dataclass
class PolicyDecision:
    decision: Decision
    reason: str
    policy_id: str | None = None
    required_role: str | None = None