import pytest

from slack_mcp.tools.assistant import (
    assistant_threads_set_status,
    assistant_threads_set_suggested_prompts,
    assistant_threads_set_title,
)


@pytest.mark.asyncio
async def test_assistant_threads_set_status(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await assistant_threads_set_status(
        channel_id="C123", thread_ts="1234.5678", status="thinking", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "assistant.threads.setStatus",
        channel_id="C123",
        thread_ts="1234.5678",
        status="thinking",
    )


@pytest.mark.asyncio
async def test_assistant_threads_set_suggested_prompts(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await assistant_threads_set_suggested_prompts(
        channel_id="C123",
        thread_ts="1234.5678",
        prompts=[{"title": "Hi", "message": "Hello"}],
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "assistant.threads.setSuggestedPrompts",
        channel_id="C123",
        thread_ts="1234.5678",
        prompts=[{"title": "Hi", "message": "Hello"}],
    )


@pytest.mark.asyncio
async def test_assistant_threads_set_title(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await assistant_threads_set_title(
        channel_id="C123",
        thread_ts="1234.5678",
        title="My Thread",
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "assistant.threads.setTitle",
        channel_id="C123",
        thread_ts="1234.5678",
        title="My Thread",
    )
