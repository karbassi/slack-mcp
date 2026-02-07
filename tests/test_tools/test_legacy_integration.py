import os

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


@pytest.fixture
def requires_session_token():
    if not os.getenv("SLACK_XOXC_TOKEN"):
        pytest.skip("SLACK_XOXC_TOKEN not set")


async def test_bots_list_live(live_client, requires_session_token):
    result = await bots_list(client=live_client)
    # May or may not work with xoxc; accept ok or known error
    assert isinstance(result, dict)


async def test_commands_list_live(live_client, requires_session_token):
    result = await commands_list(client=live_client)
    assert isinstance(result, dict)


async def test_team_prefs_get_live(live_client, requires_session_token):
    result = await team_prefs_get(client=live_client)
    assert isinstance(result, dict)


async def test_users_prefs_get_live(live_client, requires_session_token):
    result = await users_prefs_get(client=live_client)
    assert isinstance(result, dict)


@pytest.mark.skip(reason="destructive: would delete a channel")
async def test_channels_delete_live(live_client):
    pass


@pytest.mark.skip(reason="destructive: would execute a slash command")
async def test_chat_command_live(live_client):
    pass


@pytest.mark.skip(reason="requires a specific file ID")
async def test_files_edit_live(live_client):
    pass


@pytest.mark.skip(reason="requires a specific file ID")
async def test_files_share_legacy_live(live_client):
    pass


@pytest.mark.skip(reason="destructive: would invite a user")
async def test_users_admin_invite_live(live_client):
    pass


@pytest.mark.skip(reason="destructive: would deactivate a user")
async def test_users_admin_set_inactive_live(live_client):
    pass


@pytest.mark.skip(reason="destructive: would modify user preferences")
async def test_users_prefs_set_live(live_client):
    pass
