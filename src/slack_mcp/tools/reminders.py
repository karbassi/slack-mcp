from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def reminders_add(
    text: str,
    time: str,
    recurrence: Optional[dict] = None,
    team_id: Optional[str] = None,
    user: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a reminder."""
    kwargs = {"text": text, "time": time}
    if recurrence is not None:
        kwargs["recurrence"] = recurrence
    if team_id is not None:
        kwargs["team_id"] = team_id
    if user is not None:
        kwargs["user"] = user
    return await client.api_call("reminders.add", **kwargs)


@mcp.tool
async def reminders_complete(
    reminder: str,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Mark a reminder as complete."""
    kwargs = {"reminder": reminder}
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("reminders.complete", **kwargs)


@mcp.tool
async def reminders_delete(
    reminder: str,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a reminder."""
    kwargs = {"reminder": reminder}
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("reminders.delete", **kwargs)


@mcp.tool
async def reminders_info(
    reminder: str,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get info for a reminder."""
    kwargs = {"reminder": reminder}
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("reminders.info", **kwargs)


@mcp.tool
async def reminders_list(
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all reminders created by or for a given user."""
    kwargs = {}
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("reminders.list", **kwargs)
