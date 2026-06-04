import pytest

from slack_mcp.tools.oauth import oauth_access, oauth_v2_access, oauth_v2_exchange
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_oauth_access(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await oauth_access(
        client_id="C123", client_secret="S456", code="code789", client=mock_client
    )
    assert result["ok"] is True
    assert_api_call(
        mock_client.api_call,
        "oauth.access",
        client_id="C123",
        client_secret="S456",
        code="code789",
    )


@pytest.mark.asyncio
async def test_oauth_v2_access(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await oauth_v2_access(
        client_id="C123", client_secret="S456", code="code789", client=mock_client
    )
    assert result["ok"] is True
    assert_api_call(
        mock_client.api_call,
        "oauth.v2.access",
        client_id="C123",
        client_secret="S456",
        code="code789",
    )


@pytest.mark.asyncio
async def test_oauth_v2_exchange(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await oauth_v2_exchange(
        client_id="C123", client_secret="S456", token="xoxp-token", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "oauth.v2.exchange",
        client_id="C123",
        client_secret="S456",
        token="xoxp-token",
    )
