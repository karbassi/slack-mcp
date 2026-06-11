from tests.conftest import assert_api_call


async def test_emoji_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "emoji": {}}
    result = await mcp_client.call_tool("emoji_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "emoji.list")
