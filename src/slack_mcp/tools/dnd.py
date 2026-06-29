from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def dnd_end_dnd(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """End the current user's Do Not Disturb session."""
    return await client.api_call("dnd.endDnd")


@mcp.tool
async def dnd_end_snooze(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """End the current user's snooze mode."""
    return await client.api_call("dnd.endSnooze")


@mcp.tool
async def dnd_info(
    user: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a user's current Do Not Disturb status.

    Args:
        user: ID of the user to fetch status for; defaults to the authenticated user (e.g. ``U0123``).
        team_id: Encoded team ID to fetch the status from, required for org-wide tokens (e.g. ``T0123``).
    """
    return await client.api_call("dnd.info", user=user, team_id=team_id)


@mcp.tool
async def dnd_set_snooze(
    num_minutes: int,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Turn on Do Not Disturb mode for the current user.

    Args:
        num_minutes: Number of minutes, starting now, to snooze notifications for (e.g. ``60``).
    """
    return await client.api_call("dnd.setSnooze", num_minutes=num_minutes)


@mcp.tool
async def dnd_team_info(
    users: str,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve the Do Not Disturb status for users on a team.

    Args:
        users: Comma-separated list of user IDs to fetch Do Not Disturb status for (e.g. ``U0123,U0456``).
        team_id: Encoded team ID the users belong to, required for org-wide tokens (e.g. ``T0123``).
    """
    return await client.api_call("dnd.teamInfo", users=users, team_id=team_id)
