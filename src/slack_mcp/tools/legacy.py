from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import LONG_TTL, mcp, slack_client


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def bots_list(
    cursor: str | None = None,
    limit: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all bots in a workspace (legacy undocumented).

    Args:
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Maximum number of items to return per page.
    """
    return await client.session_call("bots.list", cursor=cursor, limit=limit)


@mcp.tool
async def channels_delete(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a channel (legacy undocumented).

    Args:
        channel: ID of the channel to delete (e.g. ``C0123``).
    """
    return await client.session_call("channels.delete", channel=channel)


@mcp.tool
async def chat_command(
    channel: str,
    command: str,
    text: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Execute a slash command (legacy undocumented).

    Args:
        channel: ID of the channel in which to run the command (e.g. ``C0123``).
        command: The slash command to execute, including the leading slash (e.g. ``/remind``).
        text: Arguments passed to the slash command.
    """
    return await client.session_call(
        "chat.command", channel=channel, command=command, text=text
    )


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def commands_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List available slash commands (legacy undocumented)."""
    return await client.session_call("commands.list")


@mcp.tool
async def files_edit(
    file: str,
    title: str | None = None,
    filetype: str | None = None,
    content: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Edit a file (legacy undocumented).

    Args:
        file: ID of the file to edit (e.g. ``F0123``).
        title: New title for the file.
        filetype: New file type (Slack-internal file type identifier, e.g. ``text``).
        content: New body content of the file.
    """
    return await client.session_call_form(
        "files.edit", file=file, title=title, filetype=filetype, content=content
    )


@mcp.tool
async def files_share_legacy(
    file: str,
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Share a file to a channel (legacy undocumented).

    Args:
        file: ID of the file to share (e.g. ``F0123``).
        channel: ID of the channel to share the file into (e.g. ``C0123``).
    """
    return await client.session_call("files.share", file=file, channel=channel)


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def team_prefs_get(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get team preferences (legacy undocumented)."""
    return await client.session_call("team.prefs.get")


@mcp.tool
async def users_admin_invite(
    email: str,
    channels: str | None = None,
    real_name: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Invite a user to the workspace as admin (legacy undocumented).

    Args:
        email: Email address of the person to invite.
        channels: Comma-separated list of channel IDs to add the invitee to (e.g. ``C0123,C0456``).
        real_name: Full name to assign to the invited user.
    """
    return await client.session_call(
        "users.admin.invite", email=email, channels=channels, real_name=real_name
    )


@mcp.tool
async def users_admin_set_inactive(
    user: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Deactivate a user (legacy undocumented).

    Args:
        user: ID of the user to deactivate (e.g. ``U0123``).
    """
    return await client.session_call("users.admin.setInactive", user=user)


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def users_prefs_get(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get user preferences (legacy undocumented)."""
    return await client.session_call("users.prefs.get")


@mcp.tool
async def users_prefs_set(
    name: str,
    value: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set a user preference (legacy undocumented).

    Args:
        name: Name of the preference to set.
        value: Value to assign to the preference.
    """
    return await client.session_call("users.prefs.set", name=name, value=value)
