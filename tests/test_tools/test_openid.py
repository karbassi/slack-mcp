import pytest

from slack_mcp.tools.openid import openid_connect_token, openid_connect_user_info
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_openid_connect_token(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await openid_connect_token(
        client_id="C123", client_secret="S456", code="code789", client=mock_client
    )
    assert result["ok"] is True
    assert_api_call(
        mock_client.api_call,
        "openid.connect.token",
        client_id="C123",
        client_secret="S456",
        code="code789",
    )


@pytest.mark.asyncio
async def test_openid_connect_user_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "sub": "U123"}
    result = await openid_connect_user_info(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("openid.connect.userInfo")
