from tests.conftest import assert_api_call


async def test_tooling_tokens_rotate(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "tooling_tokens_rotate",
        {"refresh_token": "xoxe-1-..."},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "tooling.tokens.rotate",
        refresh_token="xoxe-1-...",
    )
