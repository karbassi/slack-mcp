from tests.conftest import assert_api_call


async def test_oauth_access(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "oauth_access",
        {"client_id": "C123", "client_secret": "S456", "code": "code789"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "oauth.access",
        client_id="C123",
        client_secret="S456",
        code="code789",
    )


async def test_oauth_v2_access(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "oauth_v2_access",
        {
            "client_id": "C123",
            "client_secret": "S456",
            "code": "code789",
            "code_verifier": "pkce-verifier",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "oauth.v2.access",
        client_id="C123",
        client_secret="S456",
        code="code789",
        code_verifier="pkce-verifier",
    )


async def test_oauth_v2_user_access(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "oauth_v2_user_access",
        {"client_id": "C123", "client_secret": "S456", "code": "code789"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "oauth.v2.user.access",
        client_id="C123",
        client_secret="S456",
        code="code789",
    )


async def test_oauth_v2_user_access_pkce(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "oauth_v2_user_access",
        {
            "client_id": "C123",
            "client_secret": "S456",
            "code": "code789",
            "code_verifier": "pkce-verifier",
            "redirect_uri": "https://example.com/cb",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "oauth.v2.user.access",
        client_id="C123",
        client_secret="S456",
        code="code789",
        code_verifier="pkce-verifier",
        redirect_uri="https://example.com/cb",
    )


async def test_oauth_v2_user_access_pkce_omits_secret(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "oauth_v2_user_access",
        {
            "client_id": "C123",
            "code": "code789",
            "code_verifier": "pkce-verifier",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "oauth.v2.user.access",
        client_id="C123",
        code="code789",
        code_verifier="pkce-verifier",
    )


async def test_oauth_v2_user_access_refresh_omits_code(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "oauth_v2_user_access",
        {
            "client_id": "C123",
            "client_secret": "S456",
            "grant_type": "refresh_token",
            "refresh_token": "xoxe-refresh",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "oauth.v2.user.access",
        client_id="C123",
        client_secret="S456",
        grant_type="refresh_token",
        refresh_token="xoxe-refresh",
    )


async def test_oauth_v2_user_access_refresh_without_token_errors(
    mcp_client, slack_stub
):
    result = await mcp_client.call_tool(
        "oauth_v2_user_access",
        {
            "client_id": "C123",
            "client_secret": "S456",
            "grant_type": "refresh_token",
        },
        raise_on_error=False,
    )
    assert result.is_error is True
    slack_stub.api_call.assert_not_called()


async def test_oauth_v2_user_access_without_code_or_refresh_errors(
    mcp_client, slack_stub
):
    result = await mcp_client.call_tool(
        "oauth_v2_user_access",
        {"client_id": "C123", "client_secret": "S456"},
        raise_on_error=False,
    )
    assert result.is_error is True
    slack_stub.api_call.assert_not_called()


async def test_oauth_v2_exchange(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "oauth_v2_exchange",
        {"client_id": "C123", "client_secret": "S456", "token": "xoxp-token"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "oauth.v2.exchange",
        client_id="C123",
        client_secret="S456",
        token="xoxp-token",
    )
