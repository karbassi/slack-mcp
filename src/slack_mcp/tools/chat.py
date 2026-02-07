from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def chat_append_stream(
    channel: str,
    thread_ts: str,
    text: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Append text to an AI assistant streaming message."""
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
    """Delete a message."""
    kwargs = {"channel": channel, "ts": ts}
    if as_user is not None:
        kwargs["as_user"] = as_user
    return await client.api_call("chat.delete", **kwargs)


@mcp.tool
async def chat_delete_scheduled_message(
    channel: str,
    scheduled_message_id: str,
    as_user: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a pending scheduled message from the queue."""
    kwargs = {"channel": channel, "scheduled_message_id": scheduled_message_id}
    if as_user is not None:
        kwargs["as_user"] = as_user
    return await client.api_call("chat.deleteScheduledMessage", **kwargs)


@mcp.tool
async def chat_get_permalink(
    channel: str,
    message_ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a permalink URL for a specific message."""
    return await client.api_call(
        "chat.getPermalink", channel=channel, message_ts=message_ts
    )


@mcp.tool
async def chat_me_message(
    channel: str,
    text: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Send a /me message to a channel."""
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
    """Send an ephemeral message to a user in a channel."""
    kwargs = {"channel": channel, "user": user}
    if text is not None:
        kwargs["text"] = text
    if attachments is not None:
        kwargs["attachments"] = attachments
    if blocks is not None:
        kwargs["blocks"] = blocks
    if as_user is not None:
        kwargs["as_user"] = as_user
    if thread_ts is not None:
        kwargs["thread_ts"] = thread_ts
    return await client.api_call("chat.postEphemeral", **kwargs)


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
    """Send a message to a channel."""
    kwargs = {"channel": channel}
    if text is not None:
        kwargs["text"] = text
    if attachments is not None:
        kwargs["attachments"] = attachments
    if blocks is not None:
        kwargs["blocks"] = blocks
    if as_user is not None:
        kwargs["as_user"] = as_user
    if icon_emoji is not None:
        kwargs["icon_emoji"] = icon_emoji
    if icon_url is not None:
        kwargs["icon_url"] = icon_url
    if link_names is not None:
        kwargs["link_names"] = link_names
    if metadata is not None:
        kwargs["metadata"] = metadata
    if mrkdwn is not None:
        kwargs["mrkdwn"] = mrkdwn
    if parse is not None:
        kwargs["parse"] = parse
    if reply_broadcast is not None:
        kwargs["reply_broadcast"] = reply_broadcast
    if thread_ts is not None:
        kwargs["thread_ts"] = thread_ts
    if unfurl_links is not None:
        kwargs["unfurl_links"] = unfurl_links
    if unfurl_media is not None:
        kwargs["unfurl_media"] = unfurl_media
    if username is not None:
        kwargs["username"] = username
    return await client.api_call("chat.postMessage", **kwargs)


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
    """Schedule a message to be sent to a channel."""
    kwargs = {"channel": channel, "post_at": post_at}
    if text is not None:
        kwargs["text"] = text
    if attachments is not None:
        kwargs["attachments"] = attachments
    if blocks is not None:
        kwargs["blocks"] = blocks
    if as_user is not None:
        kwargs["as_user"] = as_user
    if metadata is not None:
        kwargs["metadata"] = metadata
    if reply_broadcast is not None:
        kwargs["reply_broadcast"] = reply_broadcast
    if thread_ts is not None:
        kwargs["thread_ts"] = thread_ts
    if unfurl_links is not None:
        kwargs["unfurl_links"] = unfurl_links
    if unfurl_media is not None:
        kwargs["unfurl_media"] = unfurl_media
    return await client.api_call("chat.scheduleMessage", **kwargs)


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
    """List scheduled messages."""
    kwargs = {}
    if channel is not None:
        kwargs["channel"] = channel
    if cursor is not None:
        kwargs["cursor"] = cursor
    if latest is not None:
        kwargs["latest"] = latest
    if limit is not None:
        kwargs["limit"] = limit
    if oldest is not None:
        kwargs["oldest"] = oldest
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("chat.scheduledMessages.list", **kwargs)


@mcp.tool
async def chat_start_stream(
    channel: str,
    thread_ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Start an AI assistant streaming message."""
    return await client.api_call(
        "chat.startStream", channel=channel, thread_ts=thread_ts
    )


@mcp.tool
async def chat_stop_stream(
    channel: str,
    thread_ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Stop an AI assistant streaming message."""
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
    """Stream a message to an AI assistant thread."""
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
    """Provide custom unfurl behavior for URLs in messages."""
    kwargs = {"channel": channel, "ts": ts, "unfurls": unfurls}
    if user_auth_blocks is not None:
        kwargs["user_auth_blocks"] = user_auth_blocks
    if user_auth_message is not None:
        kwargs["user_auth_message"] = user_auth_message
    if user_auth_required is not None:
        kwargs["user_auth_required"] = user_auth_required
    if user_auth_url is not None:
        kwargs["user_auth_url"] = user_auth_url
    return await client.api_call("chat.unfurl", **kwargs)


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
    """Update a message."""
    kwargs = {"channel": channel, "ts": ts}
    if text is not None:
        kwargs["text"] = text
    if attachments is not None:
        kwargs["attachments"] = attachments
    if blocks is not None:
        kwargs["blocks"] = blocks
    if as_user is not None:
        kwargs["as_user"] = as_user
    if link_names is not None:
        kwargs["link_names"] = link_names
    if metadata is not None:
        kwargs["metadata"] = metadata
    if parse is not None:
        kwargs["parse"] = parse
    if reply_broadcast is not None:
        kwargs["reply_broadcast"] = reply_broadcast
    return await client.api_call("chat.update", **kwargs)
