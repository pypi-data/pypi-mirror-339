"""
MCP plugin for Google Keep integration.
Provides tools for interacting with Google Keep notes through MCP.
"""

from mcp.server.fastmcp import FastMCP
from .keep_api import get_notes, create_note

mcp = FastMCP("keep")

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.resource("notes://all")
def get_all_notes() -> str:
    """Get all Google Keep notes as a resource"""
    return get_notes()

@mcp.tool()
def create_keep_note(title: str, text: str, pinned: bool = False) -> str:
    """
    Create a new Google Keep note.
    
    Args:
        title (str): The title of the note
        text (str): The content of the note
        pinned (bool, optional): Whether the note should be pinned. Defaults to False.
        
    Returns:
        str: JSON string containing the created note's data
    """
    return create_note(title, text, pinned)


def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
    