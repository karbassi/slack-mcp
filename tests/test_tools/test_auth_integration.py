import pytest

from slack_mcp.tools.auth import auth_revoke, auth_teams_list, auth_test


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would revoke the token")
async def test_auth_revoke_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_auth_teams_list_live(live_client):
    result = await auth_teams_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_auth_test_live(live_client):
    result = await auth_test(client=live_client)
    assert result["ok"] is True
    assert "user_id" in result
