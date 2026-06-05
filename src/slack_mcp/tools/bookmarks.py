from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import SHORT_TTL, mcp, slack_client


@mcp.tool
async def bookmarks_add(
    channel_id: str,
    title: str,
    type: str,
    emoji: str | None = None,
    entity_id: str | None = None,
    link: str | None = None,
    parent_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add a bookmark to a channel."""
    return await client.api_call(
        "bookmarks.add",
        channel_id=channel_id,
        title=title,
        type=type,
        emoji=emoji,
        entity_id=entity_id,
        link=link,
        parent_id=parent_id,
    )


@mcp.tool
async def bookmarks_edit(
    bookmark_id: str,
    channel_id: str,
    emoji: str | None = None,
    link: str | None = None,
    title: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Edit a bookmark in a channel."""
    return await client.api_call(
        "bookmarks.edit",
        bookmark_id=bookmark_id,
        channel_id=channel_id,
        emoji=emoji,
        link=link,
        title=title,
    )


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
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
