import pytest

from slack_mcp.tools.search import (
    search_all,
    search_files,
    search_messages,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_all_live(live_client):
    result = await search_all(query="test", client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_files_live(live_client):
    result = await search_files(query="test", client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_messages_live(live_client):
    result = await search_messages(query="test", client=live_client)
    assert result["ok"] is True
