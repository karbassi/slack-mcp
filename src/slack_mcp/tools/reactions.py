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
    """Add a reaction to an item.

    Args:
        channel: Channel where the target message was posted (e.g. ``C0123``).
        name: Reaction (emoji) name, without surrounding colons (e.g. ``thumbsup``).
        timestamp: Timestamp of the message to react to (e.g. ``1700000000.000100``).
    """
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
    """Get reactions for an item. Set detailed=True for full response.

    Args:
        channel: Channel of the target message (e.g. ``C0123``). Required when getting reactions for a message.
        file: File to get reactions for (e.g. ``F0123``).
        file_comment: File comment to get reactions for (e.g. ``Fc0123``).
        full: Return the complete reaction list, not a truncated one.
        timestamp: Timestamp of the message (e.g. ``1700000000.000100``). Used together with ``channel``.
        detailed: Return the full Slack response instead of a compacted summary.
    """
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
    """List reactions made by a user. Set detailed=True for full response.

    Args:
        count: Number of items to return per page (deprecated; prefer ``limit`` with ``cursor``).
        cursor: Pagination cursor from the previous response's ``response_metadata.next_cursor`` (e.g. ``dXNlcjpV``).
        full: Return the complete reaction list for each item, not a truncated one.
        limit: Maximum number of items to return per page.
        page: Page number of results to return (deprecated; prefer ``limit`` with ``cursor``).
        team_id: Encoded team ID to list reactions in, required for org-wide app tokens (e.g. ``T0123``).
        user: User whose reactions to list; defaults to the authenticated user (e.g. ``U0123``).
        detailed: Return the full Slack response instead of a compacted summary.
    """
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
    """Remove a reaction from an item.

    Args:
        name: Reaction (emoji) name to remove, without surrounding colons (e.g. ``thumbsup``).
        channel: Channel where the message to remove the reaction from was posted (e.g. ``C0123``).
        file: File to remove the reaction from (e.g. ``F0123``).
        file_comment: File comment to remove the reaction from (e.g. ``Fc0123``).
        timestamp: Timestamp of the message (e.g. ``1700000000.000100``). Used together with ``channel``.
    """
    return await client.api_call(
        "reactions.remove",
        name=name,
        channel=channel,
        file=file,
        file_comment=file_comment,
        timestamp=timestamp,
    )
