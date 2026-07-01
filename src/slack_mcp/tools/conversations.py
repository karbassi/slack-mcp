from fastmcp.dependencies import Depends
from slack_sdk.errors import SlackApiError

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_channel_list, compact_message_list, compactable
from slack_mcp.errors import is_missing_scope
from slack_mcp.server import SHORT_TTL, SLOW_CALL_TIMEOUT, mcp, slack_client


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
    """Accept an invitation to a Slack Connect channel.

    Args:
        channel_name: Name for the channel once accepted.
        channel_id: ID of the channel the invite is for, if already known.
        free_trial_accepted: Accept a paid-feature free trial as part of accepting the invite.
        invite_id: ID of the invite to accept. Required unless ``channel_id`` is given.
        is_private: Create the accepted channel as private.
        team_id: Encoded team ID accepting the invite (for org-wide tokens).
    """
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
    """Approve an invitation to a Slack Connect channel.

    Args:
        invite_id: ID of the shared-channel invite to approve.
        target_team: Encoded team ID the invite is directed to (for org-wide approvals).
    """
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
    """Archive a conversation.

    Args:
        channel: ID of the conversation to archive (e.g. C0123).
    """
    return await client.api_call("conversations.archive", channel=channel)


@mcp.tool
async def conversations_canvases_create(
    channel_id: str,
    document_content: dict | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a canvas in a channel.

    Args:
        channel_id: ID of the channel the canvas belongs to (e.g. C0123).
        document_content: Canvas body as a structured document object (e.g. a markdown document).
    """
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
    """Close a direct message or multi-party direct message.

    Args:
        channel: ID of the DM or multi-party DM to close (e.g. D0123).
    """
    return await client.api_call("conversations.close", channel=channel)


@mcp.tool
async def conversations_create(
    name: str,
    is_private: bool | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new channel.

    Args:
        name: Channel name (lowercase, no spaces or periods, max 80 chars).
        is_private: Create a private channel instead of a public one.
        team_id: Encoded team ID to create the channel in (for org-wide tokens).
    """
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
    """Decline an invitation to a Slack Connect channel.

    Args:
        invite_id: ID of the shared-channel invite to decline.
        target_team: Encoded team ID the invite is directed to (for org-wide tokens).
    """
    return await client.api_call(
        "conversations.declineSharedInvite",
        invite_id=invite_id,
        target_team=target_team,
    )


@mcp.tool
async def conversations_external_invite_permissions_set(
    channel: str,
    action: str,
    target_team: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set external invite permissions for a Slack Connect channel.

    Args:
        channel: ID of the Slack Connect channel (e.g. ``C0123``).
        action: Permission to apply — ``upgrade`` to allow external write access or ``downgrade`` to restrict it.
        target_team: Encoded team ID of the target team to change permissions for (e.g. ``T0123``).
    """
    return await client.api_call(
        "conversations.externalInvitePermissions.set",
        channel=channel,
        action=action,
        target_team=target_team,
    )


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
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
    """Fetch a conversation's history.

    Args:
        channel: ID of the conversation to read (e.g. C0123).
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        inclusive: Include messages with ``latest`` or ``oldest`` timestamps in the results.
        latest: Only include messages at or before this timestamp (e.g. 1700000000.000100). Defaults to now.
        limit: Maximum number of messages to return per page (default 100).
        oldest: Only include messages at or after this timestamp.
        include_all_metadata: Include all message metadata in the response.
        detailed: Return the full, uncompacted Slack response when True.
    """
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


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def conversations_info(
    channel: str,
    include_locale: bool | None = None,
    include_num_members: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve information about a conversation.

    Args:
        channel: ID of the conversation to look up (e.g. C0123).
        include_locale: Include the channel's locale in the response.
        include_num_members: Include the channel's member count in the response.
    """
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
    """Invite users to a channel.

    Args:
        channel: ID of the channel to invite users into (e.g. C0123).
        users: Comma-separated list of user IDs to invite (e.g. ``U0123,U0456``), up to 1000.
        force: Continue inviting valid users even if some IDs fail, rather than failing the whole call.
    """
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
    """Send a shared channel invite.

    Args:
        channel: ID of the channel to share (e.g. C0123).
        emails: Email addresses to invite. Provide ``emails`` or ``user_ids``.
        external_limited: Invite the external party as a limited (single-channel) guest.
        user_ids: User IDs to invite. Provide ``emails`` or ``user_ids``.
    """
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
    """Join an existing conversation.

    Args:
        channel: ID of the channel to join (e.g. C0123).
    """
    return await client.api_call("conversations.join", channel=channel)


@mcp.tool
async def conversations_kick(
    channel: str,
    user: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a user from a conversation.

    Args:
        channel: ID of the channel to remove the user from (e.g. C0123).
        user: ID of the user to remove (e.g. U0123).
    """
    return await client.api_call("conversations.kick", channel=channel, user=user)


@mcp.tool
async def conversations_leave(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Leave a conversation.

    Args:
        channel: ID of the conversation to leave (e.g. C0123).
    """
    return await client.api_call("conversations.leave", channel=channel)


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
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
    """List all channels.

    Args:
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        exclude_archived: Omit archived channels from the results.
        limit: Maximum number of channels to return per page (default 100).
        team_id: Encoded team ID to list channels for (for org-wide tokens).
        types: Comma-separated conversation types to include, e.g. ``public_channel,private_channel,mpim,im``.
        detailed: Return the full, uncompacted Slack response when True.
    """
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
    """List shared channel invites.

    Args:
        count: Maximum number of invites to return (default 100).
        cursor: Pagination cursor from ``response_metadata.next_cursor`` in a prior response.
        team_id: Encoded team ID to list invites for (for org-wide tokens).
    """
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
    """Set the read cursor in a channel.

    Args:
        channel: ID of the channel to mark (e.g. C0123).
        ts: Timestamp of the most recently seen message (e.g. 1700000000.000100); everything up to it is marked read.
    """
    try:
        return await client.api_call("conversations.mark", channel=channel, ts=ts)
    except SlackApiError as e:
        if is_missing_scope(e.response.get("error")):
            return await client.session_call_form(
                "conversations.mark", channel=channel, ts=ts
            )
        raise


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def conversations_members(
    channel: str,
    cursor: str | None = None,
    limit: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve members of a conversation.

    Args:
        channel: ID of the conversation to list members for (e.g. C0123).
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Maximum number of member IDs to return per page (default 100).
    """
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
    """Open or resume a direct message or multi-party DM.

    Args:
        channel: ID of an existing DM/MPIM to resume. Provide ``channel`` or ``users``.
        prevent_creation: For 1:1 DMs, don't create a new conversation if one doesn't already exist.
        return_im: Return the full IM/MPIM channel object rather than just its ID.
        users: Comma-separated user IDs to open a DM/MPIM with (e.g. ``U0123,U0456``).
    """
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
    """Rename a conversation.

    Args:
        channel: ID of the channel to rename (e.g. C0123).
        name: New channel name (lowercase, no spaces or periods, max 80 chars).
    """
    return await client.api_call("conversations.rename", channel=channel, name=name)


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
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
    """Retrieve a thread of messages.

    Args:
        channel: ID of the conversation containing the thread (e.g. C0123).
        ts: Timestamp of the thread's parent message (e.g. 1700000000.000100).
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        inclusive: Include messages with ``latest`` or ``oldest`` timestamps in the results.
        latest: Only include messages at or before this timestamp. Defaults to now.
        limit: Maximum number of messages to return per page (default 100).
        oldest: Only include messages at or after this timestamp.
        include_all_metadata: Include all message metadata in the response.
        detailed: Return the full, uncompacted Slack response when True.
    """
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
    is_external_limited: bool | None = None,
    message: dict | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Approve a shared channel invite request.

    Args:
        invite_id: ID of the shared-invite request to approve.
        channel_id: ID of the channel to override the requested invite destination.
        is_external_limited: Restrict the invited team to post-only (limited) access.
        message: Optional message object (``{"text": ..., "is_override": ...}``) to attach to the approval.
    """
    return await client.api_call(
        "conversations.requestSharedInvite.approve",
        invite_id=invite_id,
        channel_id=channel_id,
        is_external_limited=is_external_limited,
        message=message,
    )


@mcp.tool
async def conversations_request_shared_invite_deny(
    invite_id: str,
    message: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Deny a shared channel invite request.

    Args:
        invite_id: ID of the shared-invite request to deny.
        message: Optional message explaining why the request was denied.
    """
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
    """List shared channel invite requests.

    Args:
        cursor: Pagination cursor from ``response_metadata.next_cursor`` in a prior response.
        include_approved: Include already-approved requests in the results.
        include_denied: Include denied requests in the results.
        include_expired: Include expired requests in the results.
        invite_ids: Restrict results to these specific invite request IDs.
        limit: Maximum number of requests to return per page.
        user_id: Only return requests made by this user ID.
    """
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
    """Set the purpose for a conversation.

    Args:
        channel: ID of the conversation to update (e.g. C0123).
        purpose: New purpose text (max 250 chars).
    """
    return await client.api_call(
        "conversations.setPurpose", channel=channel, purpose=purpose
    )


@mcp.tool
async def conversations_set_topic(
    channel: str,
    topic: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the topic for a conversation.

    Args:
        channel: ID of the conversation to update (e.g. C0123).
        topic: New topic text (max 250 chars).
    """
    return await client.api_call("conversations.setTopic", channel=channel, topic=topic)


@mcp.tool
async def conversations_unarchive(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Reverse a conversation archive.

    Args:
        channel: ID of the archived conversation to restore (e.g. C0123).
    """
    return await client.api_call("conversations.unarchive", channel=channel)


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def conversations_bulk_reacji_triggers(
    channel_ids: list,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get reacji (emoji-reaction workflow) triggers for multiple channels.

    Undocumented session endpoint (requires xoxc/xoxd tokens).

    Args:
        channel_ids: List of channel IDs to fetch reacji triggers for (e.g. ``["C0123", "C0456"]``).

    Returns:
        A dict with:
        - ``ok``: Whether the call succeeded.
        - ``channel_triggers``: Per-channel reacji trigger definitions (empty when no triggers are configured).
    """
    return await client.session_call(
        "conversations.bulkReacjiTriggers", channel_ids=channel_ids
    )


@mcp.tool
async def conversations_suggestions(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get suggested channels for the current user to join.

    Undocumented session endpoint (requires xoxc/xoxd tokens). Takes no arguments.

    Returns:
        A dict with:
        - ``ok``: Whether the call succeeded.
        - ``status``: Status of the suggestion computation (e.g. ``complete``).
        - ``suggestion_types_tried``: The suggestion strategies Slack attempted.
    """
    return await client.session_call("conversations.suggestions")


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def conversations_team_connections(
    channel: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get the Slack Connect team connections for a channel.

    Undocumented session endpoint (requires xoxc/xoxd tokens). Uses form-encoded
    transport — the JSON transport rejects the ``channel`` argument with
    ``invalid_arguments``.

    Args:
        channel: ID of the channel to fetch team connections for (e.g. C0123).

    Returns:
        A dict with:
        - ``ok``: Whether the call succeeded.
        - ``connections``: Teams currently connected to the channel (empty when none).
        - ``pending_connections``: Teams with a pending connection.
        - ``previous_connections``: Teams previously connected to the channel.
    """
    return await client.session_call_form(
        "conversations.teamConnections", channel=channel
    )
