from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_items, compactable
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
    return await client.api_call(
        "stars.add",
        channel=channel,
        file=file,
        file_comment=file_comment,
        timestamp=timestamp,
    )


@mcp.tool
@compactable(compact_items)
async def stars_list(
    count: int | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    page: int | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List starred items for the calling user. Set detailed=True for full response."""
    return await client.api_call(
        "stars.list",
        count=count,
        cursor=cursor,
        limit=limit,
        page=page,
        team_id=team_id,
    )


@mcp.tool
async def stars_remove(
    channel: str | None = None,
    file: str | None = None,
    file_comment: str | None = None,
    timestamp: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a star from an item."""
    return await client.api_call(
        "stars.remove",
        channel=channel,
        file=file,
        file_comment=file_comment,
        timestamp=timestamp,
    )
