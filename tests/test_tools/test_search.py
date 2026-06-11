from slack_mcp.compact import (
    compact_search_all,
    compact_search_files,
    compact_search_messages,
    get_compactor,
)
from tests.conftest import assert_api_call


async def test_search_all(mcp_client, slack_stub):
    result = await mcp_client.call_tool("search_all", {"query": "hello"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "search.all", query="hello")


async def test_search_files(mcp_client, slack_stub):
    result = await mcp_client.call_tool("search_files", {"query": "report"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "search.files", query="report")


async def test_search_messages(mcp_client, slack_stub):
    result = await mcp_client.call_tool("search_messages", {"query": "meeting"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "search.messages", query="meeting")


def test_search_all_compactable():
    assert get_compactor("search_all") is compact_search_all


def test_search_files_compactable():
    assert get_compactor("search_files") is compact_search_files


def test_search_messages_compactable():
    assert get_compactor("search_messages") is compact_search_messages
