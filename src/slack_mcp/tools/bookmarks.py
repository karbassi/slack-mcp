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
    """Add a bookmark to a channel.

    Args:
        channel_id: ID of the channel to add the bookmark to (e.g. ``C0123``).
        title: Title (display name) for the bookmark.
        type: Type of the bookmark, e.g. ``link``.
        emoji: Emoji tag to apply to the bookmark (e.g. ``:books:``).
        entity_id: ID of the entity being bookmarked (used for non-link bookmark types).
        link: URL for the bookmark, required when ``type`` is ``link``.
        parent_id: ID of this bookmark's parent, used to nest it under a bookmark folder.
    """
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
    """Edit a bookmark in a channel.

    Args:
        bookmark_id: ID of the bookmark to edit (e.g. ``Bk0123``).
        channel_id: ID of the channel containing the bookmark (e.g. ``C0123``).
        emoji: New emoji tag for the bookmark (e.g. ``:books:``).
        link: New URL for the bookmark.
        title: New title (display name) for the bookmark.
    """
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
    """List bookmarks for a channel.

    Args:
        channel_id: ID of the channel whose bookmarks to list (e.g. ``C0123``).
    """
    return await client.api_call("bookmarks.list", channel_id=channel_id)


@mcp.tool
async def bookmarks_remove(
    bookmark_id: str,
    channel_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a bookmark from a channel.

    Args:
        bookmark_id: ID of the bookmark to remove (e.g. ``Bk0123``).
        channel_id: ID of the channel containing the bookmark (e.g. ``C0123``).
    """
    return await client.api_call(
        "bookmarks.remove", bookmark_id=bookmark_id, channel_id=channel_id
    )
