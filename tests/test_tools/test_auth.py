from tests.conftest import assert_api_call


async def test_auth_revoke(mcp_client, slack_stub):
    result = await mcp_client.call_tool("auth_revoke", {"test": True})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "auth.revoke", test=True)


async def test_auth_teams_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("auth_teams_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "auth.teams.list")


async def test_auth_test(mcp_client, slack_stub):
    result = await mcp_client.call_tool("auth_test", {})
    assert result.is_error is False
    slack_stub.api_call.assert_called_once_with("auth.test")
