from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def reactions_add(
    channel: str,
    name: str,
    timestamp: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add a reaction to an item."""
    return await client.api_call(
        "reactions.add", channel=channel, name=name, timestamp=timestamp
    )


@mcp.tool
async def reactions_get(
    channel: str | None = None,
    file: str | None = None,
    file_comment: str | None = None,
    full: bool | None = None,
    timestamp: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get reactions for an item."""
    kwargs = {}
    if channel is not None:
        kwargs["channel"] = channel
    if file is not None:
        kwargs["file"] = file
    if file_comment is not None:
        kwargs["file_comment"] = file_comment
    if full is not None:
        kwargs["full"] = full
    if timestamp is not None:
        kwargs["timestamp"] = timestamp
    return await client.api_call("reactions.get", **kwargs)


@mcp.tool
async def reactions_list(
    count: int | None = None,
    cursor: str | None = None,
    full: bool | None = None,
    limit: int | None = None,
    page: int | None = None,
    team_id: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List reactions made by a user."""
    kwargs = {}
    if count is not None:
        kwargs["count"] = count
    if cursor is not None:
        kwargs["cursor"] = cursor
    if full is not None:
        kwargs["full"] = full
    if limit is not None:
        kwargs["limit"] = limit
    if page is not None:
        kwargs["page"] = page
    if team_id is not None:
        kwargs["team_id"] = team_id
    if user is not None:
        kwargs["user"] = user
    return await client.api_call("reactions.list", **kwargs)


@mcp.tool
async def reactions_remove(
    name: str,
    channel: str | None = None,
    file: str | None = None,
    file_comment: str | None = None,
    timestamp: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a reaction from an item."""
    kwargs = {"name": name}
    if channel is not None:
        kwargs["channel"] = channel
    if file is not None:
        kwargs["file"] = file
    if file_comment is not None:
        kwargs["file_comment"] = file_comment
    if timestamp is not None:
        kwargs["timestamp"] = timestamp
    return await client.api_call("reactions.remove", **kwargs)
