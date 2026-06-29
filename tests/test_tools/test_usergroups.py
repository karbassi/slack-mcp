from tests.conftest import assert_api_call


async def test_usergroups_create(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "usergroups_create",
        {"name": "TestGroup", "additional_channels": "C789", "enable_section": True},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "usergroups.create",
        name="TestGroup",
        additional_channels="C789",
        enable_section=True,
    )


async def test_usergroups_disable(mcp_client, slack_stub):
    result = await mcp_client.call_tool("usergroups_disable", {"usergroup": "S123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "usergroups.disable", usergroup="S123")


async def test_usergroups_enable(mcp_client, slack_stub):
    result = await mcp_client.call_tool("usergroups_enable", {"usergroup": "S123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "usergroups.enable", usergroup="S123")


async def test_usergroups_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "usergroups": []}
    result = await mcp_client.call_tool("usergroups_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "usergroups.list")


async def test_usergroups_update(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "usergroups_update",
        {
            "usergroup": "S123",
            "name": "Updated",
            "additional_channels": "C789",
            "enable_section": True,
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "usergroups.update",
        usergroup="S123",
        name="Updated",
        additional_channels="C789",
        enable_section=True,
    )


async def test_usergroups_users_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "users": ["U123"]}
    result = await mcp_client.call_tool(
        "usergroups_users_list", {"usergroup": "S123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "usergroups.users.list", usergroup="S123"
    )


async def test_usergroups_users_update(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "usergroups_users_update",
        {"usergroup": "S123", "users": "U123,U456", "is_shared": True},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "usergroups.users.update",
        usergroup="S123",
        users="U123,U456",
        is_shared=True,
    )
