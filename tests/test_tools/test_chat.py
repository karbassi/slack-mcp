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


@pytest.mark.asyncio
async def test_chat_append_stream(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_append_stream(
        channel="C123", thread_ts="1234.5678", text="hello", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.appendStream", channel="C123", thread_ts="1234.5678", text="hello"
    )


@pytest.mark.asyncio
async def test_chat_delete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_delete(channel="C123", ts="1234.5678", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.delete", channel="C123", ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_chat_delete_scheduled_message(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_delete_scheduled_message(
        channel="C123", scheduled_message_id="Q123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.deleteScheduledMessage", channel="C123", scheduled_message_id="Q123"
    )


@pytest.mark.asyncio
async def test_chat_get_permalink(mock_client):
    mock_client.api_call.return_value = {"ok": True, "permalink": "https://..."}
    result = await chat_get_permalink(
        channel="C123", message_ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.getPermalink", channel="C123", message_ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_chat_me_message(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_me_message(channel="C123", text="test", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.meMessage", channel="C123", text="test"
    )


@pytest.mark.asyncio
async def test_chat_post_ephemeral(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_post_ephemeral(
        channel="C123", user="U123", text="secret", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.postEphemeral", channel="C123", user="U123", text="secret"
    )


@pytest.mark.asyncio
async def test_chat_post_message(mock_client):
    mock_client.api_call.return_value = {"ok": True, "ts": "1234.5678"}
    result = await chat_post_message(
        channel="C123", text="Hello world", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.postMessage", channel="C123", text="Hello world"
    )


@pytest.mark.asyncio
async def test_chat_schedule_message(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_schedule_message(
        channel="C123", post_at=1234567890, text="later", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.scheduleMessage", channel="C123", post_at=1234567890, text="later"
    )


@pytest.mark.asyncio
async def test_chat_scheduled_messages_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "scheduled_messages": []}
    result = await chat_scheduled_messages_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("chat.scheduledMessages.list")


@pytest.mark.asyncio
async def test_chat_start_stream(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_start_stream(
        channel="C123", thread_ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.startStream", channel="C123", thread_ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_chat_stop_stream(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_stop_stream(
        channel="C123", thread_ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.stopStream", channel="C123", thread_ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_chat_stream(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_stream(
        channel="C123", thread_ts="1234.5678", text="streaming", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.stream", channel="C123", thread_ts="1234.5678", text="streaming"
    )


@pytest.mark.asyncio
async def test_chat_unfurl(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    unfurls = {"https://example.com": {"text": "Example"}}
    result = await chat_unfurl(
        channel="C123", ts="1234.5678", unfurls=unfurls, client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.unfurl", channel="C123", ts="1234.5678", unfurls=unfurls
    )


@pytest.mark.asyncio
async def test_chat_update(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await chat_update(
        channel="C123", ts="1234.5678", text="updated", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "chat.update", channel="C123", ts="1234.5678", text="updated"
    )
