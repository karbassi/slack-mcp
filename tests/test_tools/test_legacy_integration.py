import pytest
from slack_mcp.tools.legacy import (
    bots_list,
    channels_delete,
    chat_command,
    commands_list,
    files_edit,
    files_share_legacy,
    team_prefs_get,
    users_admin_invite,
    users_admin_set_inactive,
    users_prefs_get,
    users_prefs_set,
)


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")
async def test_bots_list_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: destructive, would delete a channel")
async def test_channels_delete_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: would execute a slash command")
async def test_chat_command_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")
async def test_commands_list_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")
async def test_files_edit_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")
async def test_files_share_legacy_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")
async def test_team_prefs_get_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: destructive, would invite a user")
async def test_users_admin_invite_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: destructive, would deactivate a user")
async def test_users_admin_set_inactive_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")
async def test_users_prefs_get_live(live_client):
    pass


@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")
async def test_users_prefs_set_live(live_client):
    pass
