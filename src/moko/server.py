import sys
from mcp.server import MCPServer
from moko.gateway.gateway import MokoGateway
from moko.mcp_tools.jira import register_jira_tools

mcp = MCPServer("Moko")
mokogateway = MokoGateway()

print(f"Moko received:", file=sys.stderr, flush=True)
register_jira_tools(mcp, mokogateway)

if __name__ == "__main__":
    mcp.run()