"""MCP server bootstrap."""

from mcp.server.fastmcp import FastMCP


def create_mcp_server() -> FastMCP:
    """Create the MCP server instance for future tool registration."""
    return FastMCP(name="mobile-detailing-crm")
