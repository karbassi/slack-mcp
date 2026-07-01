from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import SHORT_TTL, mcp, slack_client


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def calendar_get_installed_calendars(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List the calendar integrations connected to the user (undocumented session endpoint).

    Answers "which calendars are linked to my Slack". Returns:
        gcal: Google Calendar integration state for the user.
        ocal: Outlook Calendar integration state for the user.
    """
    return await client.session_call("calendar.getInstalledCalendars")


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def calendar_user_status(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get the user's current calendar status (undocumented session endpoint).

    Surfaces the user's in-meeting / calendar availability. Returns:
        status: The user's calendar status (e.g. current or upcoming event info).
    """
    return await client.session_call("calendar.user.status")
