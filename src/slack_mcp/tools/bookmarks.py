from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def bookmarks_add(
    channel_id: str,
    title: str,
    type: str,
    emoji: Optional[str] = None,
    entity_id: Optional[str] = None,
    link: Optional[str] = None,
    parent_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add a bookmark to a channel."""
    kwargs = {"channel_id": channel_id, "title": title, "type": type}
    if emoji is not None:
        kwargs["emoji"] = emoji
    if entity_id is not None:
        kwargs["entity_id"] = entity_id
    if link is not None:
        kwargs["link"] = link
    if parent_id is not None:
        kwargs["parent_id"] = parent_id
    return await client.api_call("bookmarks.add", **kwargs)


@mcp.tool
async def bookmarks_edit(
    bookmark_id: str,
    channel_id: str,
    emoji: Optional[str] = None,
    link: Optional[str] = None,
    title: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Edit a bookmark in a channel."""
    kwargs = {"bookmark_id": bookmark_id, "channel_id": channel_id}
    if emoji is not None:
        kwargs["emoji"] = emoji
    if link is not None:
        kwargs["link"] = link
    if title is not None:
        kwargs["title"] = title
    return await client.api_call("bookmarks.edit", **kwargs)


@mcp.tool
async def bookmarks_list(
    channel_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List bookmarks for a channel."""
    return await client.api_call("bookmarks.list", channel_id=channel_id)


@mcp.tool
async def bookmarks_remove(
    bookmark_id: str,
    channel_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a bookmark from a channel."""
    return await client.api_call(
        "bookmarks.remove", bookmark_id=bookmark_id, channel_id=channel_id
    )
