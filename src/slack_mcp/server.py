from dotenv import load_dotenv

load_dotenv()

from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient, get_client

mcp = FastMCP(name="Slack MCP")


def slack_client() -> SlackClient:
    """Dependency provider for SlackClient."""
    return get_client()


# Import all tool modules so @mcp.tool decorators register the tools
import slack_mcp.tools.api
import slack_mcp.tools.apps
import slack_mcp.tools.assistant
import slack_mcp.tools.auth
import slack_mcp.tools.bookmarks
import slack_mcp.tools.bots
import slack_mcp.tools.calls
import slack_mcp.tools.canvases
import slack_mcp.tools.chat
import slack_mcp.tools.conversations
import slack_mcp.tools.dialog
import slack_mcp.tools.dnd
import slack_mcp.tools.emoji
import slack_mcp.tools.entity
import slack_mcp.tools.files
import slack_mcp.tools.functions
import slack_mcp.tools.migration
import slack_mcp.tools.oauth
import slack_mcp.tools.openid
import slack_mcp.tools.pins
import slack_mcp.tools.reactions
import slack_mcp.tools.reminders
import slack_mcp.tools.rtm
import slack_mcp.tools.search
import slack_mcp.tools.slack_lists
import slack_mcp.tools.stars
import slack_mcp.tools.team
import slack_mcp.tools.tooling
import slack_mcp.tools.usergroups
import slack_mcp.tools.users
import slack_mcp.tools.views
import slack_mcp.tools.workflows
import slack_mcp.tools.undocumented
import slack_mcp.tools.legacy


if __name__ == "__main__":
    mcp.run()
