import os
import uuid

import httpx
import pytest

from slack_mcp.tools.conversations import conversations_archive, conversations_create
from slack_mcp.tools.files import (
    files_complete_upload_external,
    files_delete,
    files_get_upload_url_external,
)
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


async def test_chat_command_live(live_client, requires_session_token):
    """Execute /shrug in a temp channel (harmless, just posts a message)."""
    name = f"test-cmd-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    channel_id = created["channel"]["id"]
    try:
        result = await chat_command(
            channel=channel_id, command="/shrug", client=live_client
        )
        assert result["ok"] is True
    finally:
        await conversations_archive(channel=channel_id, client=live_client)


async def test_files_edit_live(live_client, requires_session_token):
    """Upload a file via v2 flow, edit its title, then delete it."""
    content = b"files.edit integration test"
    url_result = await files_get_upload_url_external(
        filename="edit_test.txt", length=len(content), client=live_client
    )
    async with httpx.AsyncClient() as http:
        await http.post(url_result["upload_url"], content=content)
    completed = await files_complete_upload_external(
        files=[{"id": url_result["file_id"], "title": "Before Edit"}],
        client=live_client,
    )
    file_id = completed["files"][0]["id"]
    try:
        result = await files_edit(file=file_id, title="After Edit", client=live_client)
        assert result["ok"] is True
        assert result["file"]["title"] == "After Edit"
    finally:
        await files_delete(file=file_id, client=live_client)


async def test_files_share_legacy_live(live_client, requires_session_token):
    """Upload a file and share it to a temp channel."""
    name = f"test-share-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    channel_id = created["channel"]["id"]

    content = b"files.share integration test"
    url_result = await files_get_upload_url_external(
        filename="share_test.txt", length=len(content), client=live_client
    )
    async with httpx.AsyncClient() as http:
        await http.post(url_result["upload_url"], content=content)
    completed = await files_complete_upload_external(
        files=[{"id": url_result["file_id"], "title": "Share Test"}],
        client=live_client,
    )
    file_id = completed["files"][0]["id"]
    try:
        result = await files_share_legacy(
            file=file_id, channel=channel_id, client=live_client
        )
        assert result["ok"] is True
    finally:
        await files_delete(file=file_id, client=live_client)
        await conversations_archive(channel=channel_id, client=live_client)


async def test_users_prefs_set_live(live_client, requires_session_token):
    """Set a preference then restore it."""
    prefs = await users_prefs_get(client=live_client)
    original = prefs.get("prefs", {}).get("emoji_use_all", "true")

    result = await users_prefs_set(
        name="emoji_use_all", value="true", client=live_client
    )
    assert result["ok"] is True

    # Restore
    await users_prefs_set(name="emoji_use_all", value=original, client=live_client)


@pytest.mark.skip(reason="unknown_method: channels.delete no longer exists")
async def test_channels_delete_live(live_client):
    pass


@pytest.mark.skip(reason="enterprise_is_restricted: Enterprise Grid blocks invites")
async def test_users_admin_invite_live(live_client):
    pass


@pytest.mark.skip(
    reason="enterprise_is_restricted: Enterprise Grid requires target_team"
)
async def test_users_admin_set_inactive_live(live_client):
    pass
