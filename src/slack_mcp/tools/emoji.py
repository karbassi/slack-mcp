from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import LONG_TTL, mcp, slack_client


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def emoji_list(
    include_categories: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List custom emoji for a team.

    Args:
        include_categories: Include the standard emoji categories in the response when ``True``.
    """
    return await client.api_call("emoji.list", include_categories=include_categories)
