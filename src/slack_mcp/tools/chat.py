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
    """Delete a pending scheduled message from the queue."""
    return await client.api_call(
        "chat.deleteScheduledMessage",
        channel=channel,
        scheduled_message_id=scheduled_message_id,
        as_user=as_user,
    )


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
    """Send a message to a channel."""
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
    """Schedule a message to be sent to a channel."""
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
    """List scheduled messages."""
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
    """Update a message."""
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
