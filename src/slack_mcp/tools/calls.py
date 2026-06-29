from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def calls_add(
    external_unique_id: str,
    join_url: str,
    created_by: str | None = None,
    date_start: int | None = None,
    desktop_app_join_url: str | None = None,
    external_display_id: str | None = None,
    title: str | None = None,
    users: list[dict[str, str]] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Register a new call.

    Args:
        external_unique_id: Unique ID for the Call supplied by the third-party Call provider.
        join_url: URL required for a client to join the Call (e.g. ``https://example.com/calls/1234``).
        created_by: ID of the user who created the Call; required when called with a bot token (e.g. ``U0123``).
        date_start: Unix timestamp of when the Call started (e.g. ``1562002086``).
        desktop_app_join_url: Alternate join URL used by Slack clients that have the provider's desktop app installed.
        external_display_id: Human-readable ID supplied by the third-party Call provider, displayed to users.
        title: Display name for the Call.
        users: Participants to register; each entry uses ``slack_id`` and/or external_id, display_name, avatar_url.
    """
    return await client.api_call(
        "calls.add",
        external_unique_id=external_unique_id,
        join_url=join_url,
        created_by=created_by,
        date_start=date_start,
        desktop_app_join_url=desktop_app_join_url,
        external_display_id=external_display_id,
        title=title,
        users=users,
    )


@mcp.tool
async def calls_end(
    id: str,
    duration: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """End a call.

    Args:
        id: ID of the Call returned by ``calls.add`` (e.g. ``R0E69JAID``).
        duration: Call duration in seconds.
    """
    return await client.api_call("calls.end", id=id, duration=duration)


@mcp.tool
async def calls_info(
    id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a call.

    Args:
        id: ID of the Call returned by ``calls.add`` (e.g. ``R0E69JAID``).
    """
    return await client.api_call("calls.info", id=id)


@mcp.tool
async def calls_participants_add(
    id: str,
    users: list[dict[str, str]],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Register new participants added to a call.

    Args:
        id: ID of the Call returned by ``calls.add`` (e.g. ``R0E69JAID``).
        users: Users added to the Call; each entry uses ``slack_id`` and/or external_id, display_name, avatar_url.
    """
    return await client.api_call("calls.participants.add", id=id, users=users)


@mcp.tool
async def calls_participants_remove(
    id: str,
    users: list[dict[str, str]],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Register participants removed from a call.

    Args:
        id: ID of the Call returned by ``calls.add`` (e.g. ``R0E69JAID``).
        users: Users removed from the Call; each entry uses ``slack_id`` and/or external_id, display_name, avatar_url.
    """
    return await client.api_call("calls.participants.remove", id=id, users=users)


@mcp.tool
async def calls_update(
    id: str,
    desktop_app_join_url: str | None = None,
    join_url: str | None = None,
    title: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update information about a call.

    Args:
        id: ID of the Call returned by ``calls.add`` (e.g. ``R0E69JAID``).
        desktop_app_join_url: Alternate URL used by Slack clients with the Call provider's desktop app installed.
        join_url: URL required for a client to join the Call (e.g. ``https://example.com/calls/1234567890``).
        title: Display name for the Call.
    """
    return await client.api_call(
        "calls.update",
        id=id,
        desktop_app_join_url=desktop_app_join_url,
        join_url=join_url,
        title=title,
    )
