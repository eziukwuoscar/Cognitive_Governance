# src/moko/policy.py
import sys
from moko.policy.policyDecision import PolicyDecision
from moko.policy.conditions import PolicyConditions


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
    
    print(f"matching policies: {matching_policies}", file=sys.stderr, flush=True)
    
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