from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def conversations_accept_shared_invite(
    channel_name: str,
    channel_id: Optional[str] = None,
    free_trial_accepted: Optional[bool] = None,
    invite_id: Optional[str] = None,
    is_private: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Accept an invitation to a Slack Connect channel."""
    kwargs = {"channel_name": channel_name}
    if channel_id is not None:
        kwargs["channel_id"] = channel_id
    if free_trial_accepted is not None:
        kwargs["free_trial_accepted"] = free_trial_accepted
    if invite_id is not None:
        kwargs["invite_id"] = invite_id
    if is_private is not None:
        kwargs["is_private"] = is_private
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("conversations.acceptSharedInvite", **kwargs)


@mcp.tool
async def conversations_approve_shared_invite(
    invite_id: str,
    target_team: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Approve an invitation to a Slack Connect channel."""
    kwargs = {"invite_id": invite_id}
    if target_team is not None:
        kwargs["target_team"] = target_team
    return await client.api_call("conversations.approveSharedInvite", **kwargs)


@mcp.tool
async def conversations_archive(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Archive a conversation."""
    return await client.api_call("conversations.archive", channel=channel)


@mcp.tool
async def conversations_canvases_create(
    channel_id: str,
    document_content: Optional[dict] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a canvas in a channel."""
    kwargs = {"channel_id": channel_id}
    if document_content is not None:
        kwargs["document_content"] = document_content
    return await client.api_call("conversations.canvases.create", **kwargs)


@mcp.tool
async def conversations_close(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Close a direct message or multi-party direct message."""
    return await client.api_call("conversations.close", channel=channel)


@mcp.tool
async def conversations_create(
    name: str,
    is_private: Optional[bool] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new channel."""
    kwargs = {"name": name}
    if is_private is not None:
        kwargs["is_private"] = is_private
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("conversations.create", **kwargs)


@mcp.tool
async def conversations_decline_shared_invite(
    invite_id: str,
    target_team: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Decline an invitation to a Slack Connect channel."""
    kwargs = {"invite_id": invite_id}
    if target_team is not None:
        kwargs["target_team"] = target_team
    return await client.api_call("conversations.declineSharedInvite", **kwargs)


@mcp.tool
async def conversations_external_invite_permissions_set(
    channel: str,
    action: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set external invite permissions for a Slack Connect channel."""
    return await client.api_call(
        "conversations.externalInvitePermissions.set", channel=channel, action=action
    )


@mcp.tool
async def conversations_history(
    channel: str,
    cursor: Optional[str] = None,
    inclusive: Optional[bool] = None,
    latest: Optional[str] = None,
    limit: Optional[int] = None,
    oldest: Optional[str] = None,
    include_all_metadata: Optional[bool] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Fetch a conversation's history of messages and events."""
    kwargs = {"channel": channel}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if inclusive is not None:
        kwargs["inclusive"] = inclusive
    if latest is not None:
        kwargs["latest"] = latest
    if limit is not None:
        kwargs["limit"] = limit
    if oldest is not None:
        kwargs["oldest"] = oldest
    if include_all_metadata is not None:
        kwargs["include_all_metadata"] = include_all_metadata
    return await client.api_call("conversations.history", **kwargs)


@mcp.tool
async def conversations_info(
    channel: str,
    include_locale: Optional[bool] = None,
    include_num_members: Optional[bool] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve information about a conversation."""
    kwargs = {"channel": channel}
    if include_locale is not None:
        kwargs["include_locale"] = include_locale
    if include_num_members is not None:
        kwargs["include_num_members"] = include_num_members
    return await client.api_call("conversations.info", **kwargs)


@mcp.tool
async def conversations_invite(
    channel: str,
    users: str,
    force: Optional[bool] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Invite users to a channel."""
    kwargs = {"channel": channel, "users": users}
    if force is not None:
        kwargs["force"] = force
    return await client.api_call("conversations.invite", **kwargs)


@mcp.tool
async def conversations_invite_shared(
    channel: str,
    emails: Optional[list] = None,
    external_limited: Optional[bool] = None,
    user_ids: Optional[list] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Send a shared channel invite."""
    kwargs = {"channel": channel}
    if emails is not None:
        kwargs["emails"] = emails
    if external_limited is not None:
        kwargs["external_limited"] = external_limited
    if user_ids is not None:
        kwargs["user_ids"] = user_ids
    return await client.api_call("conversations.inviteShared", **kwargs)


@mcp.tool
async def conversations_join(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Join an existing conversation."""
    return await client.api_call("conversations.join", channel=channel)


@mcp.tool
async def conversations_kick(
    channel: str,
    user: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a user from a conversation."""
    return await client.api_call("conversations.kick", channel=channel, user=user)


@mcp.tool
async def conversations_leave(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Leave a conversation."""
    return await client.api_call("conversations.leave", channel=channel)


@mcp.tool
async def conversations_list(
    cursor: Optional[str] = None,
    exclude_archived: Optional[bool] = None,
    limit: Optional[int] = None,
    team_id: Optional[str] = None,
    types: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all channels in a Slack team."""
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
    return await client.api_call("conversations.list", **kwargs)


@mcp.tool
async def conversations_list_connect_invites(
    count: Optional[int] = None,
    cursor: Optional[str] = None,
    team_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List shared channel invites."""
    kwargs = {}
    if count is not None:
        kwargs["count"] = count
    if cursor is not None:
        kwargs["cursor"] = cursor
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("conversations.listConnectInvites", **kwargs)


@mcp.tool
async def conversations_mark(
    channel: str,
    ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the read cursor in a channel."""
    return await client.api_call("conversations.mark", channel=channel, ts=ts)


@mcp.tool
async def conversations_members(
    channel: str,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve members of a conversation."""
    kwargs = {"channel": channel}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    return await client.api_call("conversations.members", **kwargs)


@mcp.tool
async def conversations_open(
    channel: Optional[str] = None,
    prevent_creation: Optional[bool] = None,
    return_im: Optional[bool] = None,
    users: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Open or resume a direct message or multi-party DM."""
    kwargs = {}
    if channel is not None:
        kwargs["channel"] = channel
    if prevent_creation is not None:
        kwargs["prevent_creation"] = prevent_creation
    if return_im is not None:
        kwargs["return_im"] = return_im
    if users is not None:
        kwargs["users"] = users
    return await client.api_call("conversations.open", **kwargs)


@mcp.tool
async def conversations_rename(
    channel: str,
    name: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Rename a conversation."""
    return await client.api_call("conversations.rename", channel=channel, name=name)


@mcp.tool
async def conversations_replies(
    channel: str,
    ts: str,
    cursor: Optional[str] = None,
    inclusive: Optional[bool] = None,
    latest: Optional[str] = None,
    limit: Optional[int] = None,
    oldest: Optional[str] = None,
    include_all_metadata: Optional[bool] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a thread of messages from a conversation."""
    kwargs = {"channel": channel, "ts": ts}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if inclusive is not None:
        kwargs["inclusive"] = inclusive
    if latest is not None:
        kwargs["latest"] = latest
    if limit is not None:
        kwargs["limit"] = limit
    if oldest is not None:
        kwargs["oldest"] = oldest
    if include_all_metadata is not None:
        kwargs["include_all_metadata"] = include_all_metadata
    return await client.api_call("conversations.replies", **kwargs)


@mcp.tool
async def conversations_request_shared_invite_approve(
    invite_id: str,
    channel_id: Optional[str] = None,
    is_approved: Optional[bool] = None,
    message: Optional[dict] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Approve a shared channel invite request."""
    kwargs = {"invite_id": invite_id}
    if channel_id is not None:
        kwargs["channel_id"] = channel_id
    if is_approved is not None:
        kwargs["is_approved"] = is_approved
    if message is not None:
        kwargs["message"] = message
    return await client.api_call("conversations.requestSharedInvite.approve", **kwargs)


@mcp.tool
async def conversations_request_shared_invite_deny(
    invite_id: str,
    message: Optional[dict] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Deny a shared channel invite request."""
    kwargs = {"invite_id": invite_id}
    if message is not None:
        kwargs["message"] = message
    return await client.api_call("conversations.requestSharedInvite.deny", **kwargs)


@mcp.tool
async def conversations_request_shared_invite_list(
    cursor: Optional[str] = None,
    include_approved: Optional[bool] = None,
    include_denied: Optional[bool] = None,
    include_expired: Optional[bool] = None,
    invite_ids: Optional[list] = None,
    limit: Optional[int] = None,
    user_id: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List shared channel invite requests."""
    kwargs = {}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if include_approved is not None:
        kwargs["include_approved"] = include_approved
    if include_denied is not None:
        kwargs["include_denied"] = include_denied
    if include_expired is not None:
        kwargs["include_expired"] = include_expired
    if invite_ids is not None:
        kwargs["invite_ids"] = invite_ids
    if limit is not None:
        kwargs["limit"] = limit
    if user_id is not None:
        kwargs["user_id"] = user_id
    return await client.api_call("conversations.requestSharedInvite.list", **kwargs)


@mcp.tool
async def conversations_set_purpose(
    channel: str,
    purpose: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the purpose for a conversation."""
    return await client.api_call(
        "conversations.setPurpose", channel=channel, purpose=purpose
    )


@mcp.tool
async def conversations_set_topic(
    channel: str,
    topic: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the topic for a conversation."""
    return await client.api_call(
        "conversations.setTopic", channel=channel, topic=topic
    )


@mcp.tool
async def conversations_unarchive(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Reverse a conversation archive."""
    return await client.api_call("conversations.unarchive", channel=channel)
