from tests.conftest import assert_api_call


async def test_chat_append_stream(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_append_stream",
        {"channel": "C123", "thread_ts": "1234.5678", "text": "hello"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.appendStream",
        channel="C123",
        thread_ts="1234.5678",
        text="hello",
    )


async def test_chat_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_delete", {"channel": "C123", "ts": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "chat.delete", channel="C123", ts="1234.5678"
    )


async def test_chat_delete_scheduled_message(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_delete_scheduled_message",
        {"channel": "C123", "scheduled_message_id": "Q123"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.deleteScheduledMessage",
        channel="C123",
        scheduled_message_id="Q123",
    )


async def test_chat_get_permalink(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "permalink": "https://..."}
    result = await mcp_client.call_tool(
        "chat_get_permalink", {"channel": "C123", "message_ts": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.getPermalink",
        channel="C123",
        message_ts="1234.5678",
    )


async def test_chat_me_message(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_me_message", {"channel": "C123", "text": "test"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "chat.meMessage", channel="C123", text="test"
    )


async def test_chat_post_ephemeral(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_post_ephemeral",
        {"channel": "C123", "user": "U123", "text": "secret"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.postEphemeral",
        channel="C123",
        user="U123",
        text="secret",
    )


async def test_chat_post_message(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "ts": "1234.5678"}
    result = await mcp_client.call_tool(
        "chat_post_message", {"channel": "C123", "text": "Hello world"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.postMessage",
        channel="C123",
        text="Hello world",
    )


async def test_chat_schedule_message(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_schedule_message",
        {"channel": "C123", "post_at": 1234567890, "text": "later"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.scheduleMessage",
        channel="C123",
        post_at=1234567890,
        text="later",
    )


async def test_chat_scheduled_messages_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "scheduled_messages": []}
    result = await mcp_client.call_tool("chat_scheduled_messages_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "chat.scheduledMessages.list")


async def test_chat_start_stream(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_start_stream", {"channel": "C123", "thread_ts": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.startStream",
        channel="C123",
        thread_ts="1234.5678",
    )


async def test_chat_stop_stream(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_stop_stream", {"channel": "C123", "thread_ts": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.stopStream",
        channel="C123",
        thread_ts="1234.5678",
    )


async def test_chat_stream(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_stream",
        {"channel": "C123", "thread_ts": "1234.5678", "text": "streaming"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.stream",
        channel="C123",
        thread_ts="1234.5678",
        text="streaming",
    )


async def test_chat_unfurl(mcp_client, slack_stub):
    unfurls = {"https://example.com": {"text": "Example"}}
    result = await mcp_client.call_tool(
        "chat_unfurl",
        {"channel": "C123", "ts": "1234.5678", "unfurls": unfurls},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.unfurl",
        channel="C123",
        ts="1234.5678",
        unfurls=unfurls,
    )


async def test_chat_update(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_update",
        {"channel": "C123", "ts": "1234.5678", "text": "updated"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "chat.update",
        channel="C123",
        ts="1234.5678",
        text="updated",
    )
