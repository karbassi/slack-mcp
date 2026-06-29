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
    """Save an item for later (star it).

    Args:
        channel: Channel, group, or DM to star, or the channel of a file/comment being starred (e.g. ``C0123``).
        file: File to add a star to (e.g. ``F0123``).
        file_comment: File comment to add a star to (e.g. ``Fc0123``).
        timestamp: Timestamp of the message to star; requires ``channel`` (e.g. ``1700000000.000100``).
    """
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
    """List starred items for the calling user. Set detailed=True for full response.

    Args:
        count: Number of items to return per page (legacy paging).
        cursor: Pagination cursor (``next_cursor``) from a previous response.
        limit: Maximum number of items to return per page (cursor paging).
        page: Page number of results to return (legacy paging).
        team_id: Encoded team ID to list stars for; required if the token belongs to an org-level app (e.g. ``T0123``).
        detailed: When ``True``, return the full Slack response instead of a compacted summary.
    """
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
    """Remove a star from an item.

    Args:
        channel: Channel, group, or DM to unstar, or the channel of a file/comment being unstarred (e.g. ``C0123``).
        file: File to remove a star from (e.g. ``F0123``).
        file_comment: File comment to remove a star from (e.g. ``Fc0123``).
        timestamp: Timestamp of the message to unstar; requires ``channel`` (e.g. ``1700000000.000100``).
    """
    return await client.api_call(
        "stars.remove",
        channel=channel,
        file=file,
        file_comment=file_comment,
        timestamp=timestamp,
    )
