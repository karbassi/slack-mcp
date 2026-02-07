import pytest
from slack_mcp.tools.team import (
    team_access_logs,
    team_billable_info,
    team_billing_info,
    team_external_teams_disconnect,
    team_external_teams_list,
    team_info,
    team_integration_logs,
    team_preferences_list,
    team_profile_get,
)


@pytest.mark.asyncio
async def test_team_access_logs(mock_client):
    mock_client.api_call.return_value = {"ok": True, "logins": []}
    result = await team_access_logs(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.accessLogs")


@pytest.mark.asyncio
async def test_team_billable_info(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await team_billable_info(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.billableInfo")


@pytest.mark.asyncio
async def test_team_billing_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "plan": ""}
    result = await team_billing_info(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.billing.info")


@pytest.mark.asyncio
async def test_team_external_teams_disconnect(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await team_external_teams_disconnect(
        target_team="T123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "team.externalTeams.disconnect", target_team="T123"
    )


@pytest.mark.asyncio
async def test_team_external_teams_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "external_teams": []}
    result = await team_external_teams_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.externalTeams.list")


@pytest.mark.asyncio
async def test_team_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "team": {}}
    result = await team_info(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.info")


@pytest.mark.asyncio
async def test_team_integration_logs(mock_client):
    mock_client.api_call.return_value = {"ok": True, "logs": []}
    result = await team_integration_logs(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.integrationLogs")


@pytest.mark.asyncio
async def test_team_preferences_list(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await team_preferences_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.preferences.list")


@pytest.mark.asyncio
async def test_team_profile_get(mock_client):
    mock_client.api_call.return_value = {"ok": True, "profile": {}}
    result = await team_profile_get(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("team.profile.get")
