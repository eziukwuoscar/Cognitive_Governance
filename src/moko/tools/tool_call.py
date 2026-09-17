from dataclasses import dataclass


@dataclass
class ToolCall:
    tool: str
    arguments: dict