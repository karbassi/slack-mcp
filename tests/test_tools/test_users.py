import pytest

from slack_mcp.tools.users import (
    users_conversations,
    users_delete_photo,
    users_discoverable_contacts_lookup,
    users_get_presence,
    users_identity,
    users_info,
    users_list,
    users_lookup_by_email,
    users_profile_get,
    users_profile_set,
    users_set_photo,
    users_set_presence,
)


@pytest.mark.asyncio
async def test_users_conversations(mock_client):
    mock_client.api_call.return_value = {"ok": True, "channels": []}
    result = await users_conversations(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.conversations")


@pytest.mark.asyncio
async def test_users_delete_photo(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await users_delete_photo(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.deletePhoto")


@pytest.mark.asyncio
async def test_users_discoverable_contacts_lookup(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await users_discoverable_contacts_lookup(
        email="test@example.com", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "users.discoverableContacts.lookup", email="test@example.com"
    )


@pytest.mark.asyncio
async def test_users_get_presence(mock_client):
    mock_client.api_call.return_value = {"ok": True, "presence": "active"}
    result = await users_get_presence(user="U123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.getPresence", user="U123")


@pytest.mark.asyncio
async def test_users_identity(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await users_identity(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.identity")


@pytest.mark.asyncio
async def test_users_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "user": {"id": "U123"}}
    result = await users_info(user="U123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.info", user="U123")


@pytest.mark.asyncio
async def test_users_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "members": []}
    result = await users_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.list")


@pytest.mark.asyncio
async def test_users_lookup_by_email(mock_client):
    mock_client.api_call.return_value = {"ok": True, "user": {}}
    result = await users_lookup_by_email(email="test@example.com", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "users.lookupByEmail", email="test@example.com"
    )


@pytest.mark.asyncio
async def test_users_profile_get(mock_client):
    mock_client.api_call.return_value = {"ok": True, "profile": {}}
    result = await users_profile_get(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.profile.get")


@pytest.mark.asyncio
async def test_users_profile_set(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await users_profile_set(
        profile={"status_text": "busy"}, client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "users.profile.set", profile={"status_text": "busy"}
    )


@pytest.mark.asyncio
async def test_users_set_photo(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await users_set_photo(image="/path/to/img", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.setPhoto", image="/path/to/img")


@pytest.mark.asyncio
async def test_users_set_presence(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await users_set_presence(presence="away", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("users.setPresence", presence="away")
