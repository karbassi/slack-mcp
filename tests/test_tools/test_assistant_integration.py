import pytest

from slack_mcp.tools.assistant import (
    assistant_threads_set_status,
    assistant_threads_set_suggested_prompts,
    assistant_threads_set_title,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires active assistant thread")
async def test_assistant_threads_set_status_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires active assistant thread")
async def test_assistant_threads_set_suggested_prompts_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires active assistant thread")
async def test_assistant_threads_set_title_live(live_client):
    pass
