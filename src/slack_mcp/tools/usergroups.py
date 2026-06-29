from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import SHORT_TTL, mcp, slack_client


@mcp.tool
async def usergroups_create(
    name: str,
    channels: str | None = None,
    description: str | None = None,
    handle: str | None = None,
    include_count: bool | None = None,
    team_id: str | None = None,
    additional_channels: str | None = None,
    enable_section: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a User Group.

    Args:
        name: A name for the User Group (must be unique among User Groups).
        channels: Comma-separated string of default channel IDs for the User Group (e.g. ``C0123,C0456``).
        description: A short description of the User Group.
        handle: A mention handle (must be unique among channels, users, and User Groups).
        include_count: Include the number of users in each User Group in the response.
        team_id: Encoded team ID where the User Group exists, required if org token is used (e.g. ``T0123``).
        additional_channels: Comma-separated additional default channel IDs to add beyond ``channels`` (e.g. ``C0789``).
        enable_section: Whether to enable a section for the User Group.
    """
    return await client.api_call(
        "usergroups.create",
        name=name,
        channels=channels,
        description=description,
        handle=handle,
        include_count=include_count,
        team_id=team_id,
        additional_channels=additional_channels,
        enable_section=enable_section,
    )


@mcp.tool
async def usergroups_disable(
    usergroup: str,
    include_count: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Disable an existing User Group.

    Args:
        usergroup: The encoded ID of the User Group to disable (e.g. ``S0123``).
        include_count: Include the number of users in the User Group in the response.
        team_id: Encoded team ID where the User Group exists, required if org token is used (e.g. ``T0123``).
    """
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
    """Enable a User Group.

    Args:
        usergroup: The encoded ID of the User Group to enable (e.g. ``S0123``).
        include_count: Include the number of users in the User Group in the response.
        team_id: Encoded team ID where the User Group exists, required if org token is used (e.g. ``T0123``).
    """
    return await client.api_call(
        "usergroups.enable",
        usergroup=usergroup,
        include_count=include_count,
        team_id=team_id,
    )


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def usergroups_list(
    include_count: bool | None = None,
    include_disabled: bool | None = None,
    include_users: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all User Groups for a team.

    Args:
        include_count: Include the number of users in each User Group in the response.
        include_disabled: Include disabled User Groups in the response.
        include_users: Include the list of users for each User Group in the response.
        team_id: Encoded team ID where the User Group exists, required if org token is used (e.g. ``T0123``).
    """
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
    additional_channels: str | None = None,
    enable_section: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an existing User Group.

    Args:
        usergroup: The encoded ID of the User Group to update (e.g. ``S0123``).
        channels: Comma-separated string of default channel IDs for the User Group (e.g. ``C0123,C0456``).
        description: A short description of the User Group.
        handle: A mention handle (must be unique among channels, users, and User Groups).
        include_count: Include the number of users in the User Group in the response.
        name: A name for the User Group (must be unique among User Groups).
        team_id: Encoded team ID where the User Group exists, required if org token is used (e.g. ``T0123``).
        additional_channels: Comma-separated additional default channel IDs to add beyond ``channels`` (e.g. ``C0789``).
        enable_section: Whether to enable a section for the User Group.
    """
    return await client.api_call(
        "usergroups.update",
        usergroup=usergroup,
        channels=channels,
        description=description,
        handle=handle,
        include_count=include_count,
        name=name,
        team_id=team_id,
        additional_channels=additional_channels,
        enable_section=enable_section,
    )


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def usergroups_users_list(
    usergroup: str,
    include_disabled: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all users in a User Group.

    Args:
        usergroup: The encoded ID of the User Group to list users for (e.g. ``S0123``).
        include_disabled: Include disabled User Group users in the response.
        team_id: Encoded team ID where the User Group exists, required if org token is used (e.g. ``T0123``).
    """
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
    is_shared: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update the list of users for a User Group.

    Args:
        usergroup: The encoded ID of the User Group to update (e.g. ``S0123``).
        users: Comma-separated user IDs representing the entire list of users for the User Group (e.g. ``U0123,U0456``).
        include_count: Include the number of users in the User Group in the response.
        team_id: Encoded team ID where the User Group exists, required if org token is used (e.g. ``T0123``).
        is_shared: Whether the User Group is shared across an org/Enterprise Grid.
    """
    return await client.api_call(
        "usergroups.users.update",
        usergroup=usergroup,
        users=users,
        is_shared=is_shared,
        include_count=include_count,
        team_id=team_id,
    )
