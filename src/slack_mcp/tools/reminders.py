from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def reminders_add(
    text: str,
    time: str,
    recurrence: dict[str, str] | None = None,
    team_id: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a reminder.

    Args:
        text: The content of the reminder (e.g. ``eat a banana``).
        time: When to trigger — a Unix timestamp, seconds from now, or natural language (e.g. ``in 15 minutes``).
        recurrence: Recurring schedule, e.g. ``{"frequency": "weekly", "weekdays": ["monday"]}``.
        team_id: Encoded team ID the reminder belongs to, required for org-wide app tokens (e.g. ``T0123``).
        user: User who will receive the reminder; defaults to the authenticated user (e.g. ``U0123``).
    """
    return await client.api_call(
        "reminders.add",
        text=text,
        time=time,
        recurrence=recurrence,
        team_id=team_id,
        user=user,
    )


@mcp.tool
async def reminders_complete(
    reminder: str,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Mark a reminder as complete.

    Args:
        reminder: The ID of the reminder to mark complete (e.g. ``Rm0123``).
        team_id: Encoded team ID the reminder belongs to, required for org-wide app tokens (e.g. ``T0123``).
    """
    return await client.api_call(
        "reminders.complete", reminder=reminder, team_id=team_id
    )


@mcp.tool
async def reminders_delete(
    reminder: str,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a reminder.

    Args:
        reminder: The ID of the reminder to delete (e.g. ``Rm0123``).
        team_id: Encoded team ID the reminder belongs to, required for org-wide app tokens (e.g. ``T0123``).
    """
    return await client.api_call(
        "reminders.delete", reminder=reminder, team_id=team_id
    )


@mcp.tool
async def reminders_info(
    reminder: str,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get info for a reminder.

    Args:
        reminder: The ID of the reminder to get info for (e.g. ``Rm0123``).
        team_id: Encoded team ID the reminder belongs to, required for org-wide app tokens (e.g. ``T0123``).
    """
    return await client.api_call("reminders.info", reminder=reminder, team_id=team_id)


@mcp.tool
async def reminders_list(
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all reminders created by or for a given user.

    Args:
        team_id: Encoded team ID to list reminders for, required for org-wide app tokens (e.g. ``T0123``).
    """
    return await client.api_call("reminders.list", team_id=team_id)
