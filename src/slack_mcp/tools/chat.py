from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import SHORT_TTL, mcp, slack_client


@mcp.tool
async def chat_append_stream(
    channel: str,
    thread_ts: str,
    text: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Append text to an AI assistant streaming message.

    Args:
        channel: ID of the channel containing the stream (e.g. ``C0123``).
        thread_ts: Timestamp of the parent thread that owns the stream (e.g. ``1700000000.000100``).
        text: Text chunk to append to the streaming message.
    """
    return await client.api_call(
        "chat.appendStream", channel=channel, thread_ts=thread_ts, text=text
    )


@mcp.tool
async def chat_delete(
    channel: str,
    ts: str,
    as_user: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a message.

    Args:
        channel: ID of the channel containing the message to delete (e.g. ``C0123``).
        ts: Timestamp of the message to delete (e.g. ``1700000000.000100``).
        as_user: Delete as the authenticated user rather than as the bot (legacy; ignored for workspace apps).
    """
    return await client.api_call(
        "chat.delete", channel=channel, ts=ts, as_user=as_user
    )


@mcp.tool
async def chat_delete_scheduled_message(
    channel: str,
    scheduled_message_id: str,
    as_user: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a pending scheduled message from the queue.

    Args:
        channel: ID of the channel the scheduled message targets (e.g. ``C0123``).
        scheduled_message_id: ID of the scheduled message to delete (from ``chat.scheduleMessage`` or the list tool).
        as_user: Delete as the authenticated user rather than as the bot (legacy; ignored for workspace apps).
    """
    return await client.api_call(
        "chat.deleteScheduledMessage",
        channel=channel,
        scheduled_message_id=scheduled_message_id,
        as_user=as_user,
    )


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def chat_get_permalink(
    channel: str,
    message_ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a permalink URL for a specific message.

    Args:
        channel: ID of the channel containing the message (e.g. ``C0123``).
        message_ts: Timestamp of the message to link to (e.g. ``1700000000.000100``).
    """
    return await client.api_call(
        "chat.getPermalink", channel=channel, message_ts=message_ts
    )


@mcp.tool
async def chat_me_message(
    channel: str,
    text: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Send a /me message to a channel.

    Args:
        channel: ID of the channel to post the /me message in (e.g. ``C0123``).
        text: Message text displayed as an action (e.g. "waves hello").
    """
    return await client.api_call("chat.meMessage", channel=channel, text=text)


@mcp.tool
async def chat_post_ephemeral(
    channel: str,
    user: str,
    text: str | None = None,
    attachments: list | None = None,
    blocks: list | None = None,
    as_user: bool | None = None,
    thread_ts: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Send an ephemeral message to a user in a channel.

    Args:
        channel: ID of the channel to post the ephemeral message in (e.g. ``C0123``).
        user: ID of the user who will see the ephemeral message (e.g. ``U0123``).
        text: Message text or fallback text when ``blocks`` are provided. Supports Slack mrkdwn.
        attachments: Legacy attachment array. Prefer ``blocks`` for new messages.
        blocks: Block Kit block array defining the message layout.
        as_user: Post as the authenticated user rather than as the bot (legacy; ignored for workspace apps).
        thread_ts: Parent message timestamp to post the ephemeral reply inside a thread (e.g. ``1700000000.000100``).
    """
    return await client.api_call(
        "chat.postEphemeral",
        channel=channel,
        user=user,
        text=text,
        attachments=attachments,
        blocks=blocks,
        as_user=as_user,
        thread_ts=thread_ts,
    )


@mcp.tool
async def chat_post_message(
    channel: str,
    text: str | None = None,
    attachments: list | None = None,
    blocks: list | None = None,
    as_user: bool | None = None,
    icon_emoji: str | None = None,
    icon_url: str | None = None,
    link_names: bool | None = None,
    metadata: dict | None = None,
    mrkdwn: bool | None = None,
    parse: str | None = None,
    reply_broadcast: bool | None = None,
    thread_ts: str | None = None,
    unfurl_links: bool | None = None,
    unfurl_media: bool | None = None,
    username: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Send a message to a channel.

    Args:
        channel: ID of the channel to post to (e.g. ``C0123``), or a DM ID (``D0123``) or user ID for a DM.
        text: Message text or fallback text when ``blocks`` are provided. Supports Slack mrkdwn.
        attachments: Legacy attachment array. Prefer ``blocks`` for new messages.
        blocks: Block Kit block array defining the message layout.
        as_user: Post as the authenticated user rather than as the bot (legacy; ignored for workspace apps).
        icon_emoji: Emoji to use as the bot icon, overrides the app default (e.g. ``:robot_face:``); needs ``username``.
        icon_url: URL of an image to use as the bot's icon. Requires ``username``.
        link_names: Find and link channel names and usernames in ``text`` (e.g. ``#general`` → hyperlink).
        metadata: Structured metadata object attached to the message (``event_type`` + ``event_payload``).
        mrkdwn: Render Slack mrkdwn formatting in ``text`` (default True).
        parse: How to handle message text: ``full`` (linkify everything) or ``none`` (pass text as-is).
        reply_broadcast: Also post the threaded reply to the channel when ``thread_ts`` is set.
        thread_ts: Timestamp of the parent message to reply to, forming a thread (e.g. ``1700000000.000100``).
        unfurl_links: Automatically unfurl URL links in the message.
        unfurl_media: Automatically unfurl media URLs (images, video) in the message.
        username: Override the bot's display name for this message.
    """
    return await client.api_call(
        "chat.postMessage",
        channel=channel,
        text=text,
        attachments=attachments,
        blocks=blocks,
        as_user=as_user,
        icon_emoji=icon_emoji,
        icon_url=icon_url,
        link_names=link_names,
        metadata=metadata,
        mrkdwn=mrkdwn,
        parse=parse,
        reply_broadcast=reply_broadcast,
        thread_ts=thread_ts,
        unfurl_links=unfurl_links,
        unfurl_media=unfurl_media,
        username=username,
    )


@mcp.tool
async def chat_schedule_message(
    channel: str,
    post_at: int,
    text: str | None = None,
    attachments: list | None = None,
    blocks: list | None = None,
    as_user: bool | None = None,
    metadata: dict | None = None,
    reply_broadcast: bool | None = None,
    thread_ts: str | None = None,
    unfurl_links: bool | None = None,
    unfurl_media: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Schedule a message to be sent to a channel.

    Args:
        channel: ID of the channel to send the scheduled message to (e.g. ``C0123``).
        post_at: Unix epoch timestamp (seconds) at which to deliver the message (e.g. ``1700010000``).
        text: Message text or fallback text when ``blocks`` are provided. Supports Slack mrkdwn.
        attachments: Legacy attachment array. Prefer ``blocks`` for new messages.
        blocks: Block Kit block array defining the message layout.
        as_user: Schedule as the authenticated user rather than as the bot (legacy; ignored for workspace apps).
        metadata: Structured metadata object attached to the message (``event_type`` + ``event_payload``).
        reply_broadcast: Also post the threaded reply to the channel when ``thread_ts`` is set.
        thread_ts: Timestamp of the parent message to schedule a thread reply to (e.g. ``1700000000.000100``).
        unfurl_links: Automatically unfurl URL links when the message is delivered.
        unfurl_media: Automatically unfurl media URLs (images, video) when the message is delivered.
    """
    return await client.api_call(
        "chat.scheduleMessage",
        channel=channel,
        post_at=post_at,
        text=text,
        attachments=attachments,
        blocks=blocks,
        as_user=as_user,
        metadata=metadata,
        reply_broadcast=reply_broadcast,
        thread_ts=thread_ts,
        unfurl_links=unfurl_links,
        unfurl_media=unfurl_media,
    )


@mcp.tool
async def chat_scheduled_messages_list(
    channel: str | None = None,
    cursor: str | None = None,
    latest: str | None = None,
    limit: int | None = None,
    oldest: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List scheduled messages.

    Args:
        channel: Filter to scheduled messages for this channel ID (e.g. ``C0123``). Omit to list across all channels.
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        latest: Only include messages scheduled at or before this Unix epoch timestamp.
        limit: Maximum number of scheduled messages to return per page (default 100).
        oldest: Only include messages scheduled at or after this Unix epoch timestamp.
        team_id: Encoded team ID to scope the list to (for org-wide tokens).
    """
    return await client.api_call(
        "chat.scheduledMessages.list",
        channel=channel,
        cursor=cursor,
        latest=latest,
        limit=limit,
        oldest=oldest,
        team_id=team_id,
    )


@mcp.tool
async def chat_start_stream(
    channel: str,
    thread_ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Start an AI assistant streaming message.

    Args:
        channel: ID of the channel to start the stream in (e.g. ``C0123``).
        thread_ts: Timestamp of the parent thread to attach the stream to (e.g. ``1700000000.000100``).
    """
    return await client.api_call(
        "chat.startStream", channel=channel, thread_ts=thread_ts
    )


@mcp.tool
async def chat_stop_stream(
    channel: str,
    thread_ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Stop an AI assistant streaming message.

    Args:
        channel: ID of the channel containing the stream (e.g. ``C0123``).
        thread_ts: Timestamp of the parent thread whose stream should be stopped (e.g. ``1700000000.000100``).
    """
    return await client.api_call(
        "chat.stopStream", channel=channel, thread_ts=thread_ts
    )


@mcp.tool
async def chat_stream(
    channel: str,
    thread_ts: str,
    text: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Stream a message to an AI assistant thread.

    Args:
        channel: ID of the channel containing the stream (e.g. ``C0123``).
        thread_ts: Timestamp of the parent thread to stream text into (e.g. ``1700000000.000100``).
        text: Text chunk to stream into the message.
    """
    return await client.api_call(
        "chat.stream", channel=channel, thread_ts=thread_ts, text=text
    )


@mcp.tool
async def chat_unfurl(
    channel: str,
    ts: str,
    unfurls: dict,
    user_auth_blocks: list | None = None,
    user_auth_message: str | None = None,
    user_auth_required: bool | None = None,
    user_auth_url: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Provide custom unfurl behavior for URLs in messages.

    Args:
        channel: ID of the channel containing the message with URLs to unfurl (e.g. ``C0123``).
        ts: Timestamp of the message containing the URLs (e.g. ``1700000000.000100``).
        unfurls: Map of URLs to their unfurl attachment or Block Kit objects (e.g. ``{"https://example.com": {...}}``).
        user_auth_blocks: Block Kit blocks shown to the user in an auth prompt when ``user_auth_required`` is True.
        user_auth_message: Plain-text message shown to the user in an auth prompt when ``user_auth_required`` is True.
        user_auth_required: Prompt the user to authenticate before unfurling the URL.
        user_auth_url: URL to redirect the user to for authentication when ``user_auth_required`` is True.
    """
    return await client.api_call(
        "chat.unfurl",
        channel=channel,
        ts=ts,
        unfurls=unfurls,
        user_auth_blocks=user_auth_blocks,
        user_auth_message=user_auth_message,
        user_auth_required=user_auth_required,
        user_auth_url=user_auth_url,
    )


@mcp.tool
async def chat_update(
    channel: str,
    ts: str,
    text: str | None = None,
    attachments: list | None = None,
    blocks: list | None = None,
    as_user: bool | None = None,
    link_names: bool | None = None,
    metadata: dict | None = None,
    parse: str | None = None,
    reply_broadcast: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update a message.

    Args:
        channel: ID of the channel containing the message to update (e.g. ``C0123``).
        ts: Timestamp of the message to update (e.g. ``1700000000.000100``).
        text: New message text or fallback text when ``blocks`` are provided. Supports Slack mrkdwn.
        attachments: Updated legacy attachment array. Prefer ``blocks`` for new messages.
        blocks: Updated Block Kit block array replacing the existing layout.
        as_user: Update as the authenticated user rather than as the bot (legacy; ignored for workspace apps).
        link_names: Find and link channel names and usernames in the updated ``text``.
        metadata: Updated structured metadata object (``event_type`` + ``event_payload``).
        parse: How to handle message text: ``full`` (linkify everything) or ``none`` (pass text as-is).
        reply_broadcast: Broadcast the updated threaded reply to the channel.
    """
    return await client.api_call(
        "chat.update",
        channel=channel,
        ts=ts,
        text=text,
        attachments=attachments,
        blocks=blocks,
        as_user=as_user,
        link_names=link_names,
        metadata=metadata,
        parse=parse,
        reply_broadcast=reply_broadcast,
    )
