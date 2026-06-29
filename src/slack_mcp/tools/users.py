from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_users, compactable
from slack_mcp.server import LONG_TTL, SHORT_TTL, mcp, slack_client


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def users_conversations(
    cursor: str | None = None,
    exclude_archived: bool | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    types: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List conversations the calling user may access.

    Args:
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor`` to fetch the next page.
        exclude_archived: Set to ``True`` to exclude archived channels from the list.
        limit: Maximum number of items to return per page (1-1000, default 100).
        team_id: Encoded team ID to list conversations in, required for org-wide app tokens (e.g. ``T0123``).
        types: Comma-separated conversation types to include: ``public_channel``, ``private_channel``, ``mpim``, ``im``.
        user: Browse conversations by a specific user ID rather than the calling user (e.g. ``U0123``).
    """
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
    """Look up a user by their email address for Slack Connect discovery.

    Args:
        email: The email address of the user to look up (e.g. ``user@example.com``).
    """
    return await client.api_call("users.discoverableContacts.lookup", email=email)


@mcp.tool
async def users_get_presence(
    user: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get user presence information.

    Args:
        user: ID of the user to get presence info for (e.g. ``U0123``).
    """
    return await client.api_call("users.getPresence", user=user)


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def users_identity(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get a user's identity."""
    return await client.api_call("users.identity")


@mcp.tool(meta={"cache_ttl": LONG_TTL})
@compactable(compact_users)
async def users_info(
    user: str,
    include_locale: bool | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a user. Set detailed=True for full response.

    Args:
        user: ID of the user to get info about (e.g. ``U0123``).
        include_locale: Set to ``True`` to receive the locale for the user in the response.
        detailed: Set to ``True`` to return the full, uncompacted Slack response.
    """
    return await client.api_call(
        "users.info", user=user, include_locale=include_locale
    )


@mcp.tool(meta={"cache_ttl": LONG_TTL})
@compactable(compact_users)
async def users_list(
    cursor: str | None = None,
    include_locale: bool | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all users in a Slack team. Set detailed=True for full response.

    Args:
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor`` to fetch the next page.
        include_locale: Set to ``True`` to receive the locale for users in the response.
        limit: Maximum number of users to return per page (0-1000, default 0 for no limit).
        team_id: Encoded team ID to list users in, required if the token belongs to an org-wide app (e.g. ``T0123``).
        detailed: Set to ``True`` to return the full, uncompacted Slack response.
    """
    return await client.api_call(
        "users.list",
        cursor=cursor,
        include_locale=include_locale,
        limit=limit,
        team_id=team_id,
    )


@mcp.tool(meta={"cache_ttl": LONG_TTL})
@compactable(compact_users)
async def users_lookup_by_email(
    email: str,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Find a user with an email address. Set detailed=True for full response.

    Args:
        email: An email address belonging to a user in the workspace (e.g. ``user@example.com``).
        detailed: Set to ``True`` to return the full, uncompacted Slack response.
    """
    return await client.api_call("users.lookupByEmail", email=email)


@mcp.tool(meta={"cache_ttl": LONG_TTL})
@compactable(compact_users)
async def users_profile_get(
    include_labels: bool | None = None,
    user: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a user's profile information. Set detailed=True for full response.

    Args:
        include_labels: Set to ``True`` to include labels for each ID in custom profile fields.
        user: ID of user to retrieve profile info for; defaults to the authenticated user if omitted (e.g. ``U0123``).
        detailed: Set to ``True`` to return the full, uncompacted Slack response.
    """
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
    """Set the profile information for a user.

    Args:
        name: Name of a single profile field to set (e.g. ``first_name``); use with ``value``.
        profile: Map of profile fields to set, as key-value pairs (alternative to ``name``/``value``).
        user: ID of user to change; requires admin scope, defaults to the authenticated user (e.g. ``U0123``).
        value: Value to set on a single profile field named by ``name``.
    """
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
    """Set the user profile photo.

    Args:
        image: Path to the image file to set as the profile photo.
        crop_w: Width/height of the square crop box, in pixels (the crop is always square).
        crop_x: X coordinate of the top-left corner of the crop box, in pixels.
        crop_y: Y coordinate of the top-left corner of the crop box, in pixels.
    """
    return await client.api_call(
        "users.setPhoto", image=image, crop_w=crop_w, crop_x=crop_x, crop_y=crop_y
    )


@mcp.tool
async def users_set_presence(
    presence: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Manually set user presence.

    Args:
        presence: Presence to set, either ``auto`` or ``away``.
    """
    return await client.api_call("users.setPresence", presence=presence)
