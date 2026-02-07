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


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires active AI assistant stream")
async def test_chat_append_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would delete a message")
async def test_chat_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would delete a scheduled message")
async def test_chat_delete_scheduled_message_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires existing message ts and channel")
async def test_chat_get_permalink_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would post a /me message")
async def test_chat_me_message_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would post ephemeral message")
async def test_chat_post_ephemeral_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would post a message")
async def test_chat_post_message_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would schedule a message")
async def test_chat_schedule_message_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chat_scheduled_messages_list_live(live_client):
    result = await chat_scheduled_messages_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires active AI assistant stream")
async def test_chat_start_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires active AI assistant stream")
async def test_chat_stop_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires active AI assistant stream")
async def test_chat_stream_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would unfurl URLs")
async def test_chat_unfurl_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would update a message")
async def test_chat_update_live(live_client):
    pass
