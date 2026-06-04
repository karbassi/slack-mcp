from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def usergroups_create(
    name: str,
    channels: str | None = None,
    description: str | None = None,
    handle: str | None = None,
    include_count: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a User Group."""
    return await client.api_call(
        "usergroups.create",
        name=name,
        channels=channels,
        description=description,
        handle=handle,
        include_count=include_count,
        team_id=team_id,
    )


@mcp.tool
async def usergroups_disable(
    usergroup: str,
    include_count: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Disable an existing User Group."""
    return await client.api_call(
        "usergroups.disable",
        usergroup=usergroup,
        include_count=include_count,
        team_id=team_id,
    )


@mcp.tool
async def usergroups_enable(
    usergroup: str,
    include_count: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Enable a User Group."""
    return await client.api_call(
        "usergroups.enable",
        usergroup=usergroup,
        include_count=include_count,
        team_id=team_id,
    )


@mcp.tool
async def usergroups_list(
    include_count: bool | None = None,
    include_disabled: bool | None = None,
    include_users: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all User Groups for a team."""
    return await client.api_call(
        "usergroups.list",
        include_count=include_count,
        include_disabled=include_disabled,
        include_users=include_users,
        team_id=team_id,
    )


@mcp.tool
async def usergroups_update(
    usergroup: str,
    channels: str | None = None,
    description: str | None = None,
    handle: str | None = None,
    include_count: bool | None = None,
    name: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an existing User Group."""
    return await client.api_call(
        "usergroups.update",
        usergroup=usergroup,
        channels=channels,
        description=description,
        handle=handle,
        include_count=include_count,
        name=name,
        team_id=team_id,
    )


@mcp.tool
async def usergroups_users_list(
    usergroup: str,
    include_disabled: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all users in a User Group."""
    return await client.api_call(
        "usergroups.users.list",
        usergroup=usergroup,
        include_disabled=include_disabled,
        team_id=team_id,
    )


@mcp.tool
async def usergroups_users_update(
    usergroup: str,
    users: str,
    include_count: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update the list of users for a User Group."""
    return await client.api_call(
        "usergroups.users.update",
        usergroup=usergroup,
        users=users,
        include_count=include_count,
        team_id=team_id,
    )
