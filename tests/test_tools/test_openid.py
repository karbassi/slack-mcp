from tests.conftest import assert_api_call


async def test_openid_connect_token(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "openid_connect_token",
        {"client_id": "C123", "client_secret": "S456", "code": "code789"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "openid.connect.token",
        client_id="C123",
        client_secret="S456",
        code="code789",
    )


async def test_openid_connect_user_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("openid_connect_user_info", {})
    assert result.is_error is False
    slack_stub.api_call.assert_called_once_with("openid.connect.userInfo")
