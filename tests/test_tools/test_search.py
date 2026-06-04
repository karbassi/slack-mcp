import pytest

from slack_mcp.compact import (
    compact_search_all,
    compact_search_files,
    compact_search_messages,
    get_compactor,
)
from slack_mcp.tools.search import search_all, search_files, search_messages
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_search_all(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await search_all(query="hello", client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "search.all", query="hello")


@pytest.mark.asyncio
async def test_search_files(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await search_files(query="report", client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "search.files", query="report")


@pytest.mark.asyncio
async def test_search_messages(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await search_messages(query="meeting", client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "search.messages", query="meeting")


def test_search_all_compactable():
    assert get_compactor("search_all") is compact_search_all


def test_search_files_compactable():
    assert get_compactor("search_files") is compact_search_files


def test_search_messages_compactable():
    assert get_compactor("search_messages") is compact_search_messages
