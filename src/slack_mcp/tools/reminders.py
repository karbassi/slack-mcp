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
    """Create a reminder."""
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
    """Mark a reminder as complete."""
    return await client.api_call(
        "reminders.complete", reminder=reminder, team_id=team_id
    )


@mcp.tool
async def reminders_delete(
    reminder: str,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a reminder."""
    return await client.api_call(
        "reminders.delete", reminder=reminder, team_id=team_id
    )


@mcp.tool
async def reminders_info(
    reminder: str,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get info for a reminder."""
    return await client.api_call("reminders.info", reminder=reminder, team_id=team_id)


@mcp.tool
async def reminders_list(
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all reminders created by or for a given user."""
    return await client.api_call("reminders.list", team_id=team_id)
