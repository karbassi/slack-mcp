from tests.conftest import assert_api_call


async def test_bots_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("bots_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "bots.list")


async def test_channels_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool("channels_delete", {"channel": "C123"})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("channels.delete", channel="C123")


async def test_chat_command(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "chat_command",
        {"channel": "C123", "command": "/test", "text": "hello"},
    )
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "chat.command", channel="C123", command="/test", text="hello"
    )


async def test_commands_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("commands_list", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("commands.list")


async def test_files_edit(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_edit", {"file": "F123", "title": "Updated"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call_form, "files.edit", file="F123", title="Updated"
    )


async def test_files_share_legacy(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_share_legacy", {"file": "F123", "channel": "C123"}
    )
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "files.share", file="F123", channel="C123"
    )


async def test_team_prefs_get(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_prefs_get", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("team.prefs.get")


async def test_users_admin_invite(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "users_admin_invite", {"email": "test@example.com"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call, "users.admin.invite", email="test@example.com"
    )


async def test_users_admin_set_inactive(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_admin_set_inactive", {"user": "U123"})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "users.admin.setInactive", user="U123"
    )


async def test_users_prefs_get(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_prefs_get", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("users.prefs.get")


async def test_users_prefs_set(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "users_prefs_set", {"name": "theme", "value": "dark"}
    )
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "users.prefs.set", name="theme", value="dark"
    )
