from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def emoji_list(
    include_categories: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List custom emoji for a team."""
    kwargs = {}
    if include_categories is not None:
        kwargs["include_categories"] = include_categories
    return await client.api_call("emoji.list", **kwargs)
