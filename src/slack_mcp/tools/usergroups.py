from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def usergroups_create(
    name: str,
    channels: Optional[str] = None,
    description: Optional[str] = None,
    handle: Optional[str] = None,
    include_count: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a User Group."""
    kwargs = {"name": name}
    if channels is not None:
        kwargs["channels"] = channels
    if description is not None:
        kwargs["description"] = description
    if handle is not None:
        kwargs["handle"] = handle
    if include_count is not None:
        kwargs["include_count"] = include_count
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("usergroups.create", **kwargs)


@mcp.tool
async def usergroups_disable(
    usergroup: str,
    include_count: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Disable an existing User Group."""
    kwargs = {"usergroup": usergroup}
    if include_count is not None:
        kwargs["include_count"] = include_count
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("usergroups.disable", **kwargs)


@mcp.tool
async def usergroups_enable(
    usergroup: str,
    include_count: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Enable a User Group."""
    kwargs = {"usergroup": usergroup}
    if include_count is not None:
        kwargs["include_count"] = include_count
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("usergroups.enable", **kwargs)


@mcp.tool
async def usergroups_list(
    include_count: Optional[bool] = None,
    include_disabled: Optional[bool] = None,
    include_users: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all User Groups for a team."""
    kwargs = {}
    if include_count is not None:
        kwargs["include_count"] = include_count
    if include_disabled is not None:
        kwargs["include_disabled"] = include_disabled
    if include_users is not None:
        kwargs["include_users"] = include_users
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("usergroups.list", **kwargs)


@mcp.tool
async def usergroups_update(
    usergroup: str,
    channels: Optional[str] = None,
    description: Optional[str] = None,
    handle: Optional[str] = None,
    include_count: Optional[bool] = None,
    name: Optional[str] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an existing User Group."""
    kwargs = {"usergroup": usergroup}
    if channels is not None:
        kwargs["channels"] = channels
    if description is not None:
        kwargs["description"] = description
    if handle is not None:
        kwargs["handle"] = handle
    if include_count is not None:
        kwargs["include_count"] = include_count
    if name is not None:
        kwargs["name"] = name
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("usergroups.update", **kwargs)


@mcp.tool
async def usergroups_users_list(
    usergroup: str,
    include_disabled: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all users in a User Group."""
    kwargs = {"usergroup": usergroup}
    if include_disabled is not None:
        kwargs["include_disabled"] = include_disabled
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("usergroups.users.list", **kwargs)


@mcp.tool
async def usergroups_users_update(
    usergroup: str,
    users: str,
    include_count: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update the list of users for a User Group."""
    kwargs = {"usergroup": usergroup, "users": users}
    if include_count is not None:
        kwargs["include_count"] = include_count
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("usergroups.users.update", **kwargs)
