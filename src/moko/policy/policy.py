# src/moko/policy.py

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


def evaluate(
    tool_name: str,
    arguments: dict
) -> PolicyDecision:

    # Dangerous action
    if tool_name == "delete_ticket":
        return PolicyDecision(
            decision="BLOCK",
            reason="Deleting Jira tickets is prohibited."
        )

    # Example sensitive transition
    if (
        tool_name == "update_ticket"
        and arguments.get("status", "").lower() == "closed"
    ):
        return PolicyDecision(
            decision="REQUIRE_APPROVAL",
            reason=(
                "Closing tickets requires "
                "human approval."
            )
        )

    return PolicyDecision(
        decision="ALLOW",
        reason="No policy violation detected."
    )