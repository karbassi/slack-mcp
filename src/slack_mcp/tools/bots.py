from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def bots_info(
    bot: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get info for a bot user."""
    return await client.api_call("bots.info", bot=bot, team_id=team_id)
