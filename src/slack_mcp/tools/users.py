from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_users, compactable
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
    return await client.api_call(
        "users.conversations",
        cursor=cursor,
        exclude_archived=exclude_archived,
        limit=limit,
        team_id=team_id,
        types=types,
        user=user,
    )


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
@compactable(compact_users)
async def users_info(
    user: str,
    include_locale: bool | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a user. Set detailed=True for full response."""
    return await client.api_call(
        "users.info", user=user, include_locale=include_locale
    )


@mcp.tool
@compactable(compact_users)
async def users_list(
    cursor: str | None = None,
    include_locale: bool | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all users in a Slack team. Set detailed=True for full response."""
    return await client.api_call(
        "users.list",
        cursor=cursor,
        include_locale=include_locale,
        limit=limit,
        team_id=team_id,
    )


@mcp.tool
@compactable(compact_users)
async def users_lookup_by_email(
    email: str,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Find a user with an email address. Set detailed=True for full response."""
    return await client.api_call("users.lookupByEmail", email=email)


@mcp.tool
@compactable(compact_users)
async def users_profile_get(
    include_labels: bool | None = None,
    user: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a user's profile information. Set detailed=True for full response."""
    return await client.api_call(
        "users.profile.get", include_labels=include_labels, user=user
    )


@mcp.tool
async def users_profile_set(
    name: str | None = None,
    profile: dict | None = None,
    user: str | None = None,
    value: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the profile information for a user."""
    return await client.api_call(
        "users.profile.set", name=name, profile=profile, user=user, value=value
    )


@mcp.tool
async def users_set_photo(
    image: str,
    crop_w: int | None = None,
    crop_x: int | None = None,
    crop_y: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the user profile photo."""
    return await client.api_call(
        "users.setPhoto", image=image, crop_w=crop_w, crop_x=crop_x, crop_y=crop_y
    )


@mcp.tool
async def users_set_presence(
    presence: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Manually set user presence."""
    return await client.api_call("users.setPresence", presence=presence)
