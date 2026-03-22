import pytest

from slack_mcp.tools.assistant import (
    assistant_threads_set_status,
    assistant_threads_set_suggested_prompts,
    assistant_threads_set_title,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_assistant_threads_set_status_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_assistant_threads_set_suggested_prompts_live(live_client):
    result = await assistant_threads_set_suggested_prompts(
        channel_id="C0000000000",
        thread_ts="1234567890.123456",
        prompts=[{"title": "Help", "message": "How can I help?"}],
        title="Suggestions",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_assistant_threads_set_title_live(live_client):
    result = await assistant_threads_set_title(
        channel_id="C0000000000",
        thread_ts="1234567890.123456",
        title="Test Thread Title",
        client=live_client,
    )
    assert "ok" in result
