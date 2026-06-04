from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def bots_list(
    cursor: str | None = None,
    limit: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all bots in a workspace (legacy undocumented)."""
    return await client.session_call("bots.list", cursor=cursor, limit=limit)


@mcp.tool
async def channels_delete(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a channel (legacy undocumented)."""
    return await client.session_call("channels.delete", channel=channel)


@mcp.tool
async def chat_command(
    channel: str,
    command: str,
    text: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Execute a slash command (legacy undocumented)."""
    return await client.session_call(
        "chat.command", channel=channel, command=command, text=text
    )


@mcp.tool
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
    """Edit a file (legacy undocumented)."""
    return await client.session_call_form(
        "files.edit", file=file, title=title, filetype=filetype, content=content
    )


@mcp.tool
async def files_share_legacy(
    file: str,
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Share a file to a channel (legacy undocumented)."""
    return await client.session_call("files.share", file=file, channel=channel)


@mcp.tool
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
    """Invite a user to the workspace as admin (legacy undocumented)."""
    return await client.session_call(
        "users.admin.invite", email=email, channels=channels, real_name=real_name
    )


@mcp.tool
async def users_admin_set_inactive(
    user: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Deactivate a user (legacy undocumented)."""
    return await client.session_call("users.admin.setInactive", user=user)


@mcp.tool
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
    """Set a user preference (legacy undocumented)."""
    return await client.session_call("users.prefs.set", name=name, value=value)
