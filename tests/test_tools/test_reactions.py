from slack_mcp.compact import compact_items, compact_single_item, get_compactor
from tests.conftest import assert_api_call


async def test_reactions_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "reactions_add",
        {"channel": "C123", "name": "thumbsup", "timestamp": "1234.5678"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "reactions.add",
        channel="C123",
        name="thumbsup",
        timestamp="1234.5678",
    )


async def test_reactions_get(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "message": {}}
    result = await mcp_client.call_tool(
        "reactions_get", {"channel": "C123", "timestamp": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "reactions.get", channel="C123", timestamp="1234.5678"
    )


async def test_reactions_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "items": []}
    result = await mcp_client.call_tool("reactions_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "reactions.list")


async def test_reactions_remove(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "reactions_remove",
        {"name": "thumbsup", "channel": "C123", "timestamp": "1234.5678"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "reactions.remove",
        name="thumbsup",
        channel="C123",
        timestamp="1234.5678",
    )


def test_reactions_get_compactable():
    assert get_compactor("reactions_get") is compact_single_item


def test_reactions_list_compactable():
    assert get_compactor("reactions_list") is compact_items
