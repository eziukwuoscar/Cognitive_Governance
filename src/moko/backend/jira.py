from moko.tools.tool_call import ToolCall


def register_jira_tools(mcp, gateway):
    @mcp.tool()
    async def update_ticket(ticket_id: str, new_status: str):
        """Update the status of a Jira ticket."""
        return await gateway.execute(
            ToolCall(
                tool="update_ticket",
                arguments={
                    "ticket_id": ticket_id,
                    "new_status": new_status,
                },
            )
        )