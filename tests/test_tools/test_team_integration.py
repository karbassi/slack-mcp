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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_team_info_live(live_client):
    result = await team_info(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_team_billing_info_live(live_client):
    result = await team_billing_info(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_team_preferences_list_live(live_client):
    result = await team_preferences_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_team_profile_get_live(live_client):
    result = await team_profile_get(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="missing_scope: requires legacy 'admin' scope")
async def test_team_access_logs_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="missing_scope: requires legacy 'admin' scope")
async def test_team_billable_info_live(live_client):
    """Get billable users information for the workspace."""
    result = await team_billable_info(client=live_client)
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="missing_scope: requires legacy 'admin' scope")
async def test_team_integration_logs_live(live_client):
    """Get integration activity logs for the workspace."""
    result = await team_integration_logs(client=live_client)
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="not_allowed_token_type: team.externalTeams.list requires org-level token"
)
async def test_team_external_teams_list_live(live_client):
    """List external teams and their connection statuses."""
    result = await team_external_teams_list(client=live_client)
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would disconnect an external team")
async def test_team_external_teams_disconnect_live(live_client):
    """Disconnect an external organization."""
    result = await team_external_teams_disconnect(
        target_team="T0000000000",
        client=live_client,
    )
    assert "ok" in result
