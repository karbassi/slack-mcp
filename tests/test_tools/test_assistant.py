from tests.conftest import assert_api_call


async def test_assistant_search_context(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "assistant_search_context",
        {"query": "what is project gizmo", "limit": 5},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "assistant.search.context",
        query="what is project gizmo",
        limit=5,
    )


async def test_assistant_threads_set_status(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "assistant_threads_set_status",
        {
            "channel_id": "C123",
            "thread_ts": "1234.5678",
            "status": "thinking",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "assistant.threads.setStatus",
        channel_id="C123",
        thread_ts="1234.5678",
        status="thinking",
    )


async def test_assistant_threads_set_suggested_prompts(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "assistant_threads_set_suggested_prompts",
        {
            "channel_id": "C123",
            "thread_ts": "1234.5678",
            "prompts": [{"title": "Hi", "message": "Hello"}],
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "assistant.threads.setSuggestedPrompts",
        channel_id="C123",
        thread_ts="1234.5678",
        prompts=[{"title": "Hi", "message": "Hello"}],
    )


async def test_assistant_threads_set_title(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "assistant_threads_set_title",
        {
            "channel_id": "C123",
            "thread_ts": "1234.5678",
            "title": "My Thread",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "assistant.threads.setTitle",
        channel_id="C123",
        thread_ts="1234.5678",
        title="My Thread",
    )
