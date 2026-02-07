from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def users_conversations(
    cursor: str | None = None,
    exclude_archived: bool | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    types: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List conversations the calling user may access."""
    kwargs = {}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if exclude_archived is not None:
        kwargs["exclude_archived"] = exclude_archived
    if limit is not None:
        kwargs["limit"] = limit
    if team_id is not None:
        kwargs["team_id"] = team_id
    if types is not None:
        kwargs["types"] = types
    if user is not None:
        kwargs["user"] = user
    return await client.api_call("users.conversations", **kwargs)


@mcp.tool
async def users_delete_photo(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete the user profile photo."""
    return await client.api_call("users.deletePhoto")


@mcp.tool
async def users_discoverable_contacts_lookup(
    email: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Look up a user by their email address for Slack Connect discovery."""
    return await client.api_call("users.discoverableContacts.lookup", email=email)


@mcp.tool
async def users_get_presence(
    user: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get user presence information."""
    return await client.api_call("users.getPresence", user=user)


@mcp.tool
async def users_identity(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get a user's identity."""
    return await client.api_call("users.identity")


@mcp.tool
async def users_info(
    user: str,
    include_locale: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a user."""
    kwargs = {"user": user}
    if include_locale is not None:
        kwargs["include_locale"] = include_locale
    return await client.api_call("users.info", **kwargs)


@mcp.tool
async def users_list(
    cursor: str | None = None,
    include_locale: bool | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all users in a Slack team."""
    kwargs = {}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if include_locale is not None:
        kwargs["include_locale"] = include_locale
    if limit is not None:
        kwargs["limit"] = limit
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("users.list", **kwargs)


@mcp.tool
async def users_lookup_by_email(
    email: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Find a user with an email address."""
    return await client.api_call("users.lookupByEmail", email=email)


@mcp.tool
async def users_profile_get(
    include_labels: bool | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a user's profile information."""
    kwargs = {}
    if include_labels is not None:
        kwargs["include_labels"] = include_labels
    if user is not None:
        kwargs["user"] = user
    return await client.api_call("users.profile.get", **kwargs)


@mcp.tool
async def users_profile_set(
    name: str | None = None,
    profile: dict | None = None,
    user: str | None = None,
    value: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the profile information for a user."""
    kwargs = {}
    if name is not None:
        kwargs["name"] = name
    if profile is not None:
        kwargs["profile"] = profile
    if user is not None:
        kwargs["user"] = user
    if value is not None:
        kwargs["value"] = value
    return await client.api_call("users.profile.set", **kwargs)


@mcp.tool
async def users_set_photo(
    image: str,
    crop_w: int | None = None,
    crop_x: int | None = None,
    crop_y: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the user profile photo."""
    kwargs = {"image": image}
    if crop_w is not None:
        kwargs["crop_w"] = crop_w
    if crop_x is not None:
        kwargs["crop_x"] = crop_x
    if crop_y is not None:
        kwargs["crop_y"] = crop_y
    return await client.api_call("users.setPhoto", **kwargs)


@mcp.tool
async def users_set_presence(
    presence: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Manually set user presence."""
    return await client.api_call("users.setPresence", presence=presence)
