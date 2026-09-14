from moko.policy.policy import PolicyDecision as policy

class MokoGateway:

    async def execute(
        self,
        server: str,
        tool: str,
        arguments: dict
    ):

        # 1. Check policy
        decision = await policy.evaluate(
            server=server,
            tool_name=tool,
            arguments=arguments
        )

        # 2. Stop blocked actions
        if decision.action == "BLOCK":
            return {
                "decision": "BLOCK",
                "reason": decision.reason
            }

        # 3. Forward allowed actions
        result = await connector.call_tool(
            server=server,
            tool=tool,
            arguments=arguments
        )

        # 4. Record what happened
        await audit.record(
            server=server,
            tool=tool,
            arguments=arguments,
            result=result
        )

        # 5. Return result
        return {
            "decision": "ALLOW",
            "result": result
        }