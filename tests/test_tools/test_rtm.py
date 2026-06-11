from tests.conftest import assert_api_call


async def test_rtm_connect(mcp_client, slack_stub):
    result = await mcp_client.call_tool("rtm_connect", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "rtm.connect")


async def test_rtm_start(mcp_client, slack_stub):
    result = await mcp_client.call_tool("rtm_start", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "rtm.start")
