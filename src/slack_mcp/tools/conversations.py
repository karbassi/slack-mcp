from fastmcp.dependencies import Depends
from slack_sdk.errors import SlackApiError

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_channel_list, compact_message_list, compactable
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def conversations_accept_shared_invite(
    channel_name: str,
    channel_id: str | None = None,
    free_trial_accepted: bool | None = None,
    invite_id: str | None = None,
    is_private: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Accept an invitation to a Slack Connect channel."""
    return await client.api_call(
        "conversations.acceptSharedInvite",
        channel_name=channel_name,
        channel_id=channel_id,
        free_trial_accepted=free_trial_accepted,
        invite_id=invite_id,
        is_private=is_private,
        team_id=team_id,
    )


@mcp.tool
async def conversations_approve_shared_invite(
    invite_id: str,
    target_team: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Approve an invitation to a Slack Connect channel."""
    return await client.api_call(
        "conversations.approveSharedInvite",
        invite_id=invite_id,
        target_team=target_team,
    )


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
    document_content: dict | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a canvas in a channel."""
    return await client.api_call(
        "conversations.canvases.create",
        channel_id=channel_id,
        document_content=document_content,
    )


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
    is_private: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new channel."""
    return await client.api_call(
        "conversations.create",
        name=name,
        is_private=is_private,
        team_id=team_id,
    )


@mcp.tool
async def conversations_decline_shared_invite(
    invite_id: str,
    target_team: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Decline an invitation to a Slack Connect channel."""
    return await client.api_call(
        "conversations.declineSharedInvite",
        invite_id=invite_id,
        target_team=target_team,
    )


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
@compactable(compact_message_list)
async def conversations_history(
    channel: str,
    cursor: str | None = None,
    inclusive: bool | None = None,
    latest: str | None = None,
    limit: int | None = None,
    oldest: str | None = None,
    include_all_metadata: bool | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Fetch a conversation's history. Set detailed=True for full response."""
    return await client.api_call(
        "conversations.history",
        channel=channel,
        cursor=cursor,
        inclusive=inclusive,
        latest=latest,
        limit=limit,
        oldest=oldest,
        include_all_metadata=include_all_metadata,
    )


@mcp.tool
async def conversations_info(
    channel: str,
    include_locale: bool | None = None,
    include_num_members: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve information about a conversation."""
    return await client.api_call(
        "conversations.info",
        channel=channel,
        include_locale=include_locale,
        include_num_members=include_num_members,
    )


@mcp.tool
async def conversations_invite(
    channel: str,
    users: str,
    force: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Invite users to a channel."""
    return await client.api_call(
        "conversations.invite", channel=channel, users=users, force=force
    )


@mcp.tool
async def conversations_invite_shared(
    channel: str,
    emails: list | None = None,
    external_limited: bool | None = None,
    user_ids: list | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Send a shared channel invite."""
    return await client.api_call(
        "conversations.inviteShared",
        channel=channel,
        emails=emails,
        external_limited=external_limited,
        user_ids=user_ids,
    )


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
@compactable(compact_channel_list)
async def conversations_list(
    cursor: str | None = None,
    exclude_archived: bool | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    types: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all channels. Set detailed=True for the full response."""
    return await client.api_call(
        "conversations.list",
        cursor=cursor,
        exclude_archived=exclude_archived,
        limit=limit,
        team_id=team_id,
        types=types,
    )


@mcp.tool
async def conversations_list_connect_invites(
    count: int | None = None,
    cursor: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List shared channel invites."""
    return await client.api_call(
        "conversations.listConnectInvites",
        count=count,
        cursor=cursor,
        team_id=team_id,
    )


@mcp.tool
async def conversations_mark(
    channel: str,
    ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the read cursor in a channel."""
    try:
        return await client.api_call("conversations.mark", channel=channel, ts=ts)
    except SlackApiError as e:
        if e.response.get("error") == "missing_scope":
            return await client.session_call_form(
                "conversations.mark", channel=channel, ts=ts
            )
        raise


@mcp.tool
async def conversations_members(
    channel: str,
    cursor: str | None = None,
    limit: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve members of a conversation."""
    return await client.api_call(
        "conversations.members", channel=channel, cursor=cursor, limit=limit
    )


@mcp.tool
async def conversations_open(
    channel: str | None = None,
    prevent_creation: bool | None = None,
    return_im: bool | None = None,
    users: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Open or resume a direct message or multi-party DM."""
    return await client.api_call(
        "conversations.open",
        channel=channel,
        prevent_creation=prevent_creation,
        return_im=return_im,
        users=users,
    )


@mcp.tool
async def conversations_rename(
    channel: str,
    name: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Rename a conversation."""
    return await client.api_call("conversations.rename", channel=channel, name=name)


@mcp.tool
@compactable(compact_message_list)
async def conversations_replies(
    channel: str,
    ts: str,
    cursor: str | None = None,
    inclusive: bool | None = None,
    latest: str | None = None,
    limit: int | None = None,
    oldest: str | None = None,
    include_all_metadata: bool | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a thread of messages. Set detailed=True for full response."""
    return await client.api_call(
        "conversations.replies",
        channel=channel,
        ts=ts,
        cursor=cursor,
        inclusive=inclusive,
        latest=latest,
        limit=limit,
        oldest=oldest,
        include_all_metadata=include_all_metadata,
    )


@mcp.tool
async def conversations_request_shared_invite_approve(
    invite_id: str,
    channel_id: str | None = None,
    is_approved: bool | None = None,
    message: dict | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Approve a shared channel invite request."""
    return await client.api_call(
        "conversations.requestSharedInvite.approve",
        invite_id=invite_id,
        channel_id=channel_id,
        is_approved=is_approved,
        message=message,
    )


@mcp.tool
async def conversations_request_shared_invite_deny(
    invite_id: str,
    message: dict | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Deny a shared channel invite request."""
    return await client.api_call(
        "conversations.requestSharedInvite.deny",
        invite_id=invite_id,
        message=message,
    )


@mcp.tool
async def conversations_request_shared_invite_list(
    cursor: str | None = None,
    include_approved: bool | None = None,
    include_denied: bool | None = None,
    include_expired: bool | None = None,
    invite_ids: list | None = None,
    limit: int | None = None,
    user_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List shared channel invite requests."""
    return await client.api_call(
        "conversations.requestSharedInvite.list",
        cursor=cursor,
        include_approved=include_approved,
        include_denied=include_denied,
        include_expired=include_expired,
        invite_ids=invite_ids,
        limit=limit,
        user_id=user_id,
    )


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
    return await client.api_call("conversations.setTopic", channel=channel, topic=topic)


@mcp.tool
async def conversations_unarchive(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Reverse a conversation archive."""
    return await client.api_call("conversations.unarchive", channel=channel)
