from slack_mcp.compact import compact_items, get_compactor
from tests.conftest import assert_api_call


async def test_stars_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "stars_add", {"channel": "C123", "timestamp": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "stars.add", channel="C123", timestamp="1234.5678"
    )


async def test_stars_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "items": []}
    result = await mcp_client.call_tool("stars_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "stars.list")


async def test_stars_remove(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "stars_remove", {"channel": "C123", "timestamp": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "stars.remove", channel="C123", timestamp="1234.5678"
    )


def test_stars_list_compactable():
    assert get_compactor("stars_list") is compact_items
