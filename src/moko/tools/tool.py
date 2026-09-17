from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    server: str
    description: str


TOOLS = {
    "update_ticket": Tool(
        name="update_ticket",
        server="jira",
        description="Update a Jira ticket"
    ),

    "delete_ticket": Tool(
        name="delete_ticket",
        server="jira",
        description="Delete a Jira ticket"
    ),

    "send_email": Tool(
        name="send_email",
        server="outlook",
        description="Send an email"
    )
}


def get_tool(tool_name: str) -> Tool | None:

    tool = TOOLS.get(tool_name)

    if tool is None:
        print("no tool found")
        return None

    return tool