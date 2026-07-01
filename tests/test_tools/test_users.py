import base64

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


async def test_users_get_presence_self(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "presence": "active"}
    result = await mcp_client.call_tool("users_get_presence", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.getPresence")


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


async def test_users_profile_get_extras(mcp_client, slack_stub):
    slack_stub.session_call.return_value = {
        "ok": True,
        "channels": [],
        "shared_channels": [],
        "full_member_channels": [],
        "onboarding_complete": True,
    }
    result = await mcp_client.call_tool("users_profile_get_extras", {"user": "U123"})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "users.profile.getExtras", user="U123")


async def test_users_profile_get_extras_self(mcp_client, slack_stub):
    slack_stub.session_call.return_value = {"ok": True, "channels": []}
    result = await mcp_client.call_tool("users_profile_get_extras", {})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "users.profile.getExtras")


async def test_users_profile_get_sections(mcp_client, slack_stub):
    slack_stub.session_call_form.return_value = {"ok": True, "result": []}
    result = await mcp_client.call_tool(
        "users_profile_get_sections", {"user": "U123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call_form, "users.profile.getSections", user="U123"
    )


async def test_users_custom_status_list(mcp_client, slack_stub):
    slack_stub.session_call.return_value = {
        "ok": True,
        "statuses": [],
        "scheduled_statuses": [],
    }
    result = await mcp_client.call_tool(
        "users_custom_status_list", {"statuses_count_per_section": 5}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call,
        "users.customStatus.list",
        statuses_count_per_section=5,
    )


async def test_users_profile_set(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "users_profile_set", {"profile": {"status_text": "busy"}}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "users.profile.set", profile={"status_text": "busy"}
    )


async def test_users_set_photo(mcp_client, slack_stub):
    image_b64 = base64.b64encode(b"PNGDATA").decode()
    result = await mcp_client.call_tool(
        "users_set_photo", {"image_base64": image_b64}
    )
    assert result.is_error is False
    # Decodes base64 to bytes and uploads via slack_sdk's multipart helper.
    slack_stub.users_set_photo.assert_called_once()
    _, kwargs = slack_stub.users_set_photo.call_args
    assert kwargs["image"] == b"PNGDATA"


async def test_users_set_photo_rejects_invalid_base64(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "users_set_photo", {"image_base64": "@@@not base64@@@"}, raise_on_error=False
    )
    assert result.is_error is True
    assert "image_base64" in result.content[0].text
    slack_stub.users_set_photo.assert_not_called()


async def test_users_set_presence(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_set_presence", {"presence": "away"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.setPresence", presence="away")
