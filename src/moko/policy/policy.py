# src/moko/policy.py

from policy.policyDecision import PolicyDecision
from policy.conditions import PolicyConditions

COMPANY_POLICIES = [
    {
        "policy_id": "POL-007",
        "name": "Jira Ticket Delete Policy",
        "reason": "Deleting tickets isn't permited by Pjt partners",

        "applies_to": {
            "identity_types": ["human", "agent"],
            "actions": ["ticket.delete"]
        },

        "effect": "BLOCK"
    },

    {
        "policy_id": "POL-002",
        "name": "Jira Ticket Close Policy",
        "reason": "Closing tickets requires senior approval",

        "applies_to": {
            "identity_types": ["human", "agent"],
            "actions": ["ticket.update"]
        },

        "conditions": {
            "status_equals": "closed"
        },

        "effect": "REQUIRE_APPROVAL",

        "approval": {
            "required_role": "Managing Director"
        }
    },

    {
        "policy_id": "POL-003",
        "name": "Jira Ticket Read Policy",
        "reason": "Closing tickets requires senior approval",

        "applies_to": {
            "identity_types": ["human", "agent"],
            "actions": ["ticket.read"]
        },

        "effect": "ALLOW"
    }
]


class PolicyEngine:
  
  def __init__(self, policies: list[dict]):
    self.policies = policies
    
    
  def _find_matching_policies(
    self,
    action: str,
    identity_type: str
  ):

    matches = []

    for policy in self.policies:

        applies_to = policy["applies_to"]

        action_matches = (
            action in applies_to["actions"]
        )

        identity_matches = (
            identity_type
            in applies_to["identity_types"]
        )

        if action_matches and identity_matches:
            matches.append(policy)

    return matches
  
  
  def evaluate(
    self,
    action: str,
    arguments: dict,
    identity_type: str
  ) -> PolicyDecision:
    
    matching_policies = self._find_matching_policies(
      action=action,
      identity_type=identity_type
    )
    
    if not matching_policies:
            return PolicyDecision(
                decision="ALLOW",
                reason="No matching policy."
            )
    
    for policy in matching_policies:

            if not PolicyConditions(
                policy,
                arguments
            ):
                continue

            effect = policy["effect"].upper()

            if effect == "BLOCK":
                return PolicyDecision(
                    decision="BLOCK",
                    reason=policy["reason"],
                    policy_id=policy["policy_id"]
                )

            if effect == "REQUIRE_APPROVAL":
                return PolicyDecision(
                    decision="REQUIRE_APPROVAL",
                    reason=policy["reason"],
                    policy_id=policy["policy_id"],
                    required_role=policy.get(
                        "approval", {}
                    ).get("required_role")
                )

    return PolicyDecision(
        decision="ALLOW",
        reason="No policy violation detected."
    )