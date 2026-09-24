from dataclasses import dataclass


LIST_TOOLS = {
    "update_ticket",
    "delete_ticket",
    "read_ticket"
}

@dataclass
class ToolRegistry:
    exposed_tools: exposed_tools()
    
def exposed_tools() -> ToolRegistry | None:
    
    return LIST_TOOLS
        
        
    