import pytest

from slack_mcp.tools.auth import auth_revoke, auth_teams_list, auth_test


@pytest.mark.asyncio
async def test_auth_revoke(mock_client):
    mock_client.api_call.return_value = {"ok": True, "revoked": True}
    result = await auth_revoke(test=True, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("auth.revoke", test=True)


@pytest.mark.asyncio
async def test_auth_teams_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "teams": []}
    result = await auth_teams_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("auth.teams.list")


@pytest.mark.asyncio
async def test_auth_test(mock_client):
    mock_client.api_call.return_value = {"ok": True, "user_id": "U123"}
    result = await auth_test(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("auth.test")
