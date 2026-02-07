import pytest

from slack_mcp.tools.usergroups import (
    usergroups_create,
    usergroups_disable,
    usergroups_enable,
    usergroups_list,
    usergroups_update,
    usergroups_users_list,
    usergroups_users_update,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would create a user group")
async def test_usergroups_create_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would disable a user group")
async def test_usergroups_disable_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would enable a user group")
async def test_usergroups_enable_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_usergroups_list_live(live_client):
    result = await usergroups_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would update a user group")
async def test_usergroups_update_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific usergroup ID")
async def test_usergroups_users_list_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would update users in a user group")
async def test_usergroups_users_update_live(live_client):
    pass
