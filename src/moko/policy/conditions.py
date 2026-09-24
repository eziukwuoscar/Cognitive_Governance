from dataclasses import dataclass


@dataclass
class PolicyConditions:
    
    def __init__(self, policies, arguments):
        self.policies = policies
        self.arguments = arguments

    def _conditions_match(self, policies: dict, arguments: dict) -> bool:

        conditions = policies.get("conditions")

        # No conditions means policy always applies
        if not conditions:
            return True

        if "status_equals" in conditions:
            expected = conditions["status_equals"]
            actual = arguments.get("status")

            return actual == expected

        return False
