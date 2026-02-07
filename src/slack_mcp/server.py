from dotenv import load_dotenv

load_dotenv()

from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient, get_client

mcp = FastMCP(name="Slack MCP")


def slack_client() -> SlackClient:
    """Dependency provider for SlackClient."""
    return get_client()


if __name__ == "__main__":
    mcp.run()
