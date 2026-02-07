from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def bots_list(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all bots in a workspace (legacy undocumented)."""
    kwargs = {}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    return await client.session_call("bots.list", **kwargs)


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
    text: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Execute a slash command (legacy undocumented)."""
    kwargs = {"channel": channel, "command": command}
    if text is not None:
        kwargs["text"] = text
    return await client.session_call("chat.command", **kwargs)


@mcp.tool
async def commands_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List available slash commands (legacy undocumented)."""
    return await client.session_call("commands.list")


@mcp.tool
async def files_edit(
    file: str,
    title: Optional[str] = None,
    filetype: Optional[str] = None,
    content: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Edit a file (legacy undocumented)."""
    kwargs = {"file": file}
    if title is not None:
        kwargs["title"] = title
    if filetype is not None:
        kwargs["filetype"] = filetype
    if content is not None:
        kwargs["content"] = content
    return await client.session_call("files.edit", **kwargs)


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
    channels: Optional[str] = None,
    real_name: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Invite a user to the workspace as admin (legacy undocumented)."""
    kwargs = {"email": email}
    if channels is not None:
        kwargs["channels"] = channels
    if real_name is not None:
        kwargs["real_name"] = real_name
    return await client.session_call("users.admin.invite", **kwargs)


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
