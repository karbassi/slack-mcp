from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def stars_add(
    channel: str | None = None,
    file: str | None = None,
    file_comment: str | None = None,
    timestamp: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Save an item for later (star it)."""
    kwargs = {}
    if channel is not None:
        kwargs["channel"] = channel
    if file is not None:
        kwargs["file"] = file
    if file_comment is not None:
        kwargs["file_comment"] = file_comment
    if timestamp is not None:
        kwargs["timestamp"] = timestamp
    return await client.api_call("stars.add", **kwargs)


@mcp.tool
async def stars_list(
    count: int | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    page: int | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List starred items for the calling user."""
    kwargs = {}
    if count is not None:
        kwargs["count"] = count
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    if page is not None:
        kwargs["page"] = page
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("stars.list", **kwargs)


@mcp.tool
async def stars_remove(
    channel: str | None = None,
    file: str | None = None,
    file_comment: str | None = None,
    timestamp: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a star from an item."""
    kwargs = {}
    if channel is not None:
        kwargs["channel"] = channel
    if file is not None:
        kwargs["file"] = file
    if file_comment is not None:
        kwargs["file_comment"] = file_comment
    if timestamp is not None:
        kwargs["timestamp"] = timestamp
    return await client.api_call("stars.remove", **kwargs)
