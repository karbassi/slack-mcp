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


@pytest.mark.asyncio
async def test_bots_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "bots": []}
    result = await bots_list(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("bots.list")


@pytest.mark.asyncio
async def test_channels_delete(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await channels_delete(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "channels.delete", channel="C123"
    )


@pytest.mark.asyncio
async def test_chat_command(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await chat_command(
        channel="C123", command="/test", text="hello", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "chat.command", channel="C123", command="/test", text="hello"
    )


@pytest.mark.asyncio
async def test_commands_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "commands": []}
    result = await commands_list(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("commands.list")


@pytest.mark.asyncio
async def test_files_edit(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await files_edit(file="F123", title="Updated", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "files.edit", file="F123", title="Updated"
    )


@pytest.mark.asyncio
async def test_files_share_legacy(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await files_share_legacy(
        file="F123", channel="C123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "files.share", file="F123", channel="C123"
    )


@pytest.mark.asyncio
async def test_team_prefs_get(mock_client):
    mock_client.session_call.return_value = {"ok": True, "prefs": {}}
    result = await team_prefs_get(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("team.prefs.get")


@pytest.mark.asyncio
async def test_users_admin_invite(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await users_admin_invite(
        email="test@example.com", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "users.admin.invite", email="test@example.com"
    )


@pytest.mark.asyncio
async def test_users_admin_set_inactive(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await users_admin_set_inactive(user="U123", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "users.admin.setInactive", user="U123"
    )


@pytest.mark.asyncio
async def test_users_prefs_get(mock_client):
    mock_client.session_call.return_value = {"ok": True, "prefs": {}}
    result = await users_prefs_get(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("users.prefs.get")


@pytest.mark.asyncio
async def test_users_prefs_set(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await users_prefs_set(
        name="theme", value="dark", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "users.prefs.set", name="theme", value="dark"
    )
