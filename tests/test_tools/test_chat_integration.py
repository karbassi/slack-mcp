import time
import uuid

import pytest

from slack_mcp.tools.chat import (
    chat_append_stream,
    chat_delete,
    chat_delete_scheduled_message,
    chat_get_permalink,
    chat_me_message,
    chat_post_ephemeral,
    chat_post_message,
    chat_schedule_message,
    chat_scheduled_messages_list,
    chat_start_stream,
    chat_stop_stream,
    chat_stream,
    chat_unfurl,
    chat_update,
)
from slack_mcp.tools.conversations import (
    conversations_archive,
    conversations_create,
)


@pytest.fixture
async def temp_channel(live_client):
    """Create a temp channel and archive it after the test."""
    name = f"test-chat-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]
    yield channel_id
    await conversations_archive(channel=channel_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chat_post_message_and_delete_live(live_client, temp_channel):
    """Post a message, get permalink, update it, then delete it."""
    # Post
    posted = await chat_post_message(
        channel=temp_channel, text="integration test message", client=live_client
    )
    assert posted["ok"] is True
    ts = posted["ts"]

    # Get permalink
    permalink = await chat_get_permalink(
        channel=temp_channel, message_ts=ts, client=live_client
    )
    assert permalink["ok"] is True
    assert "permalink" in permalink

    # Update
    updated = await chat_update(
        channel=temp_channel, ts=ts, text="updated message", client=live_client
    )
    assert updated["ok"] is True

    # Delete
    deleted = await chat_delete(channel=temp_channel, ts=ts, client=live_client)
    assert deleted["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chat_me_message_live(live_client, temp_channel):
    """Post a /me message and clean up the channel."""
    result = await chat_me_message(
        channel=temp_channel, text="is testing", client=live_client
    )
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chat_schedule_and_delete_live(live_client, temp_channel):
    """Schedule a message, list it, then delete it before it sends."""
    post_at = int(time.time()) + 3600  # 1 hour from now

    scheduled = await chat_schedule_message(
        channel=temp_channel,
        post_at=post_at,
        text="scheduled integration test",
        client=live_client,
    )
    assert scheduled["ok"] is True
    scheduled_id = scheduled["scheduled_message_id"]

    # List scheduled messages
    listed = await chat_scheduled_messages_list(
        channel=temp_channel, client=live_client
    )
    assert listed["ok"] is True

    # Delete the scheduled message
    deleted = await chat_delete_scheduled_message(
        channel=temp_channel,
        scheduled_message_id=scheduled_id,
        client=live_client,
    )
    assert deleted["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chat_scheduled_messages_list_live(live_client):
    result = await chat_scheduled_messages_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_chat_append_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_chat_start_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_chat_stop_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_chat_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="missing_scope: requires links:write")
async def test_chat_unfurl_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chat_post_ephemeral_live(live_client, temp_channel):
    """Post an ephemeral message to ourselves."""
    from slack_mcp.tools.auth import auth_test

    auth = await auth_test(client=live_client)
    user_id = auth["user_id"]

    result = await chat_post_ephemeral(
        channel=temp_channel, user=user_id, text="ephemeral test", client=live_client
    )
    assert result["ok"] is True
