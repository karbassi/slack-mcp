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


async def test_search_inline_channel(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "search_inline", {"query": "hello", "count": 5, "channel": "C0123ABC"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call_form,
        "search.inline",
        query="hello",
        count=5,
        channel="C0123ABC",
    )


async def test_search_inline_user(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "search_inline", {"query": "hello", "user": "U0123ABC"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call_form,
        "search.inline",
        query="hello",
        user="U0123ABC",
    )


async def test_search_inline_requires_exactly_one_scope(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "search_inline", {"query": "hello"}, raise_on_error=False
    )
    assert result.is_error is True
    slack_stub.session_call_form.assert_not_called()


async def test_search_inline_rejects_both_scopes(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "search_inline",
        {"query": "hello", "channel": "C0123ABC", "user": "U0123ABC"},
        raise_on_error=False,
    )
    assert result.is_error is True
    slack_stub.session_call_form.assert_not_called()


async def test_search_save(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "search_save", {"terms": "deploy", "type": "message"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call_form,
        "search.save",
        terms="deploy",
        type="message",
    )


async def test_enterprise_search_get_connectors(mcp_client, slack_stub):
    result = await mcp_client.call_tool("enterprise_search_get_connectors", {})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "enterpriseSearch.getConnectors")


def test_search_all_compactable():
    assert get_compactor("search_all") is compact_search_all


def test_search_files_compactable():
    assert get_compactor("search_files") is compact_search_files


def test_search_messages_compactable():
    assert get_compactor("search_messages") is compact_search_messages
