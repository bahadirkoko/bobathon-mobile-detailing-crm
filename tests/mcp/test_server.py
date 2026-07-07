"""Smoke tests for MCP tool registration."""

from app.mcp.server import create_mcp_server


def test_create_mcp_server_returns_server() -> None:
    """The MCP server bootstrap returns a configured server instance."""
    server = create_mcp_server()
    assert server is not None
