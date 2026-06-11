from slack_mcp.compact import compact_items, get_compactor
from tests.conftest import assert_api_call


async def test_pins_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "pins_add", {"channel": "C123", "timestamp": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "pins.add", channel="C123", timestamp="1234.5678"
    )


async def test_pins_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "items": []}
    result = await mcp_client.call_tool("pins_list", {"channel": "C123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "pins.list", channel="C123")


async def test_pins_remove(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "pins_remove", {"channel": "C123", "timestamp": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "pins.remove", channel="C123", timestamp="1234.5678"
    )


def test_pins_list_compactable():
    assert get_compactor("pins_list") is compact_items
