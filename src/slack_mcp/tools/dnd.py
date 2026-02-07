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
    """Retrieve a user's current Do Not Disturb status."""
    kwargs = {}
    if user is not None:
        kwargs["user"] = user
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("dnd.info", **kwargs)


@mcp.tool
async def dnd_set_snooze(
    num_minutes: int,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Turn on Do Not Disturb mode for the current user."""
    return await client.api_call("dnd.setSnooze", num_minutes=num_minutes)


@mcp.tool
async def dnd_team_info(
    users: str,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve the Do Not Disturb status for users on a team."""
    kwargs = {"users": users}
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("dnd.teamInfo", **kwargs)
