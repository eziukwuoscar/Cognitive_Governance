from moko.policy import policy
from moko.tools import tool
from moko.tools.tool_call import ToolCall


class MokoGateway:

    async def execute(
        self,
        call: ToolCall
    ):

        # 1. Find the tool
        selected_tool = tool.get_tool(call.tool)

        print("Selected tool:", selected_tool)

        # 2. Stop unknown tools
        if selected_tool is None:
            return {
                "decision": "BLOCK",
                "reason": "This tool does not exist. Contact your administrator."
            }

        # 3. Check policy
        decision = policy.evaluate(
            tool_name=selected_tool.name,
            arguments=call.arguments
        )

        print("Policy decision:", decision)

        # 4. Stop blocked actions
        # if decision.decision == "BLOCK":
        #     return {
        #         "decision": "BLOCK",
        #         "reason": decision.reason
        #     }

        # # 5. Pause actions requiring approval
        # if decision.decision == "REQUIRE_APPROVAL":
        #     return {
        #         "decision": "REQUIRE_APPROVAL",
        #         "reason": decision.reason
        #     }

        # # 6. Allowed
        # return {
        #     "decision": "ALLOW",
        #     "reason": decision.reason
        # }