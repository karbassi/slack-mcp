import pytest
from slack_mcp.tools.search import search_all, search_files, search_messages


@pytest.mark.asyncio
async def test_search_all(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await search_all(query="hello", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("search.all", query="hello")


@pytest.mark.asyncio
async def test_search_files(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await search_files(query="report", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("search.files", query="report")


@pytest.mark.asyncio
async def test_search_messages(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await search_messages(query="meeting", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("search.messages", query="meeting")
