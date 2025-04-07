# src/wiz_mcp/__init__.py

from .server import start_server


def main() -> None:
    """Main function to run the MCP server"""
    start_server()
