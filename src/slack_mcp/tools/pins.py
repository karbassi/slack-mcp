from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_items, compactable
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def pins_add(
    channel: str,
    timestamp: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Pin an item to a channel.

    Args:
        channel: ID of the channel to pin the item in (e.g. ``C0123``).
        timestamp: Timestamp of the message to pin (e.g. ``1700000000.000100``).
    """
    return await client.api_call("pins.add", channel=channel, timestamp=timestamp)


@mcp.tool
@compactable(compact_items)
async def pins_list(
    channel: str,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List items pinned to a channel. Set detailed=True for full response.

    Args:
        channel: ID of the channel whose pinned items to list (e.g. ``C0123``).
        detailed: Return the full unmodified Slack response instead of a compacted summary.
    """
    return await client.api_call("pins.list", channel=channel)


@mcp.tool
async def pins_remove(
    channel: str,
    timestamp: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Unpin an item from a channel.

    Args:
        channel: ID of the channel containing the pinned item (e.g. ``C0123``).
        timestamp: Timestamp of the pinned message to remove (e.g. ``1700000000.000100``).
    """
    return await client.api_call("pins.remove", channel=channel, timestamp=timestamp)
