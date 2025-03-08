"""Model Context Protocol (MCP) utilities."""

from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union
from dataclasses import dataclass
from enum import Enum

class MCPVersion(str, Enum):
    """Supported MCP protocol versions."""
    V1_0 = "1.0"
    V1_1 = "1.1"

@dataclass
class MCPMetadata:
    """Standard metadata structure for MCP."""
    version: MCPVersion
    interface_type: str
    interface_version: str
    supported_features: List[str]
    context_window: Optional[int] = None
    max_tokens: Optional[int] = None
    custom_metadata: Optional[Dict[str, Any]] = None

class MCPContextManager:
    """Manages MCP context information."""

    def __init__(self, metadata: MCPMetadata):
        self.metadata = metadata
        self._message_visibility = {}
        self._conversation_history = []

    def add_message(self, message_id: str, content: Any) -> None:
        """Adds a message to the conversation history."""
        self._conversation_history.append({
            "id": message_id,
            "content": content,
            "visible": True
        })
        self._message_visibility[message_id] = True

    def update_message_visibility(self, message_id: str, visible: bool) -> None:
        """Updates visibility of a specific message."""
        self._message_visibility[message_id] = visible
        for msg in self._conversation_history:
            if msg["id"] == message_id:
                msg["visible"] = visible
                break

    def get_visible_context(self) -> List[Dict[str, Any]]:
        """Returns only the visible messages from conversation history."""
        return [msg for msg in self._conversation_history 
                if self._message_visibility.get(msg["id"], True)]

    def get_metadata(self) -> Dict[str, Any]:
        """Returns current MCP metadata."""
        return {
            "version": self.metadata.version,
            "interface_type": self.metadata.interface_type,
            "interface_version": self.metadata.interface_version,
            "supported_features": self.metadata.supported_features,
            "context_window": self.metadata.context_window,
            "max_tokens": self.metadata.max_tokens,
            **(self.metadata.custom_metadata or {})
        }

def create_mcp_metadata(
    interface_type: str,
    interface_version: str,
    supported_features: List[str],
    context_window: Optional[int] = None,
    max_tokens: Optional[int] = None,
    custom_metadata: Optional[Dict[str, Any]] = None,
    version: MCPVersion = MCPVersion.V1_0
) -> MCPMetadata:
    """Creates a new MCPMetadata instance with the specified parameters."""
    return MCPMetadata(
        version=version,
        interface_type=interface_type,
        interface_version=interface_version,
        supported_features=supported_features,
        context_window=context_window,
        max_tokens=max_tokens,
        custom_metadata=custom_metadata
    ) 