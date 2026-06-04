from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_items, compact_single_item, compactable
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
@compactable(compact_single_item)
async def reactions_get(
    channel: str | None = None,
    file: str | None = None,
    file_comment: str | None = None,
    full: bool | None = None,
    timestamp: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get reactions for an item. Set detailed=True for full response."""
    return await client.api_call(
        "reactions.get",
        channel=channel,
        file=file,
        file_comment=file_comment,
        full=full,
        timestamp=timestamp,
    )


@mcp.tool
@compactable(compact_items)
async def reactions_list(
    count: int | None = None,
    cursor: str | None = None,
    full: bool | None = None,
    limit: int | None = None,
    page: int | None = None,
    team_id: str | None = None,
    user: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List reactions made by a user. Set detailed=True for full response."""
    return await client.api_call(
        "reactions.list",
        count=count,
        cursor=cursor,
        full=full,
        limit=limit,
        page=page,
        team_id=team_id,
        user=user,
    )


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
    return await client.api_call(
        "reactions.remove",
        name=name,
        channel=channel,
        file=file,
        file_comment=file_comment,
        timestamp=timestamp,
    )
