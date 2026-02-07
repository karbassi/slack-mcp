from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def pins_add(
    channel: str,
    timestamp: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Pin an item to a channel."""
    return await client.api_call("pins.add", channel=channel, timestamp=timestamp)


@mcp.tool
async def pins_list(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List items pinned to a channel."""
    return await client.api_call("pins.list", channel=channel)


@mcp.tool
async def pins_remove(
    channel: str,
    timestamp: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Unpin an item from a channel."""
    return await client.api_call("pins.remove", channel=channel, timestamp=timestamp)
