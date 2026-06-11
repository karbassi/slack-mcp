from tests.conftest import assert_api_call


async def test_users_conversations(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "channels": []}
    result = await mcp_client.call_tool("users_conversations", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.conversations")


async def test_users_delete_photo(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_delete_photo", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.deletePhoto")


async def test_users_discoverable_contacts_lookup(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "users_discoverable_contacts_lookup", {"email": "test@example.com"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "users.discoverableContacts.lookup",
        email="test@example.com",
    )


async def test_users_get_presence(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "presence": "active"}
    result = await mcp_client.call_tool("users_get_presence", {"user": "U123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.getPresence", user="U123")


async def test_users_identity(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_identity", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.identity")


async def test_users_info(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "user": {"id": "U123"}}
    result = await mcp_client.call_tool("users_info", {"user": "U123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.info", user="U123")


async def test_users_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "members": []}
    result = await mcp_client.call_tool("users_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.list")


async def test_users_lookup_by_email(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "user": {}}
    result = await mcp_client.call_tool(
        "users_lookup_by_email", {"email": "test@example.com"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "users.lookupByEmail", email="test@example.com"
    )


async def test_users_profile_get(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "profile": {}}
    result = await mcp_client.call_tool("users_profile_get", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.profile.get")


async def test_users_profile_set(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "users_profile_set", {"profile": {"status_text": "busy"}}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "users.profile.set", profile={"status_text": "busy"}
    )


async def test_users_set_photo(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_set_photo", {"image": "/path/to/img"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.setPhoto", image="/path/to/img")


async def test_users_set_presence(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_set_presence", {"presence": "away"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.setPresence", presence="away")
