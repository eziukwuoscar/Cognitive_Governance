import sys
from moko.policy.policy import PolicyEngine
from moko.tools import tool
from moko.tools.tool_call import ToolCall


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

class MokoGateway:
    
    def __init__(self):
        self.policy_engine = PolicyEngine(COMPANY_POLICIES)

    async def execute(
        self,
        call: ToolCall
    ):

        # 1. Find the tool
        selected_tool = tool.get_tool(call.tool)

        print("Selected tool:", selected_tool)
        print(f"Selected tool: {selected_tool}", file=sys.stderr, flush=True)

        # 2. Stop unknown tools
        if selected_tool is None:
            return {
                "decision": "BLOCK",
                "reason": "This tool does not exist. Contact your administrator."
            }

        # 3. Check policy
        decision = self.policy_engine.evaluate(
            action="ticket.update",
            arguments=call.arguments,
            identity_type="human",
        )

        print("Policy decision:", decision)
        print(f"Policy decision: {decision}", file=sys.stderr, flush=True)
        
        if decision.decision == "BLOCK":
            return {
                "status": "blocked",
                "tool": call.tool,
                "reason": decision.reason,
            }

        if decision.decision == "REQUIRE_APPROVAL":
            return {
                "status": "pending_approval",
                "tool": call.tool,
                "reason": decision.reason,
                "required_role": decision.required_role,
            }

        # 4. Stop blocked actions