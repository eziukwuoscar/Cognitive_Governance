from dataclasses import dataclass


@dataclass
class PolicyConditions:

    def _conditions_match(self, policy: dict, arguments: dict) -> bool:

        conditions = policy.get("conditions")

        # No conditions means policy always applies
        if not conditions:
            return True

        if "status_equals" in conditions:
            expected = conditions["status_equals"]
            actual = arguments.get("status")

            return actual == expected

        return False
