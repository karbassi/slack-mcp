from tests.conftest import assert_api_call


async def test_bots_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("bots_info", {"bot": "B123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "bots.info", bot="B123")


async def test_bots_info_no_args(mcp_client, slack_stub):
    result = await mcp_client.call_tool("bots_info", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "bots.info")
