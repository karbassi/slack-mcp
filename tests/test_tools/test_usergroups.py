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


@pytest.mark.asyncio
async def test_usergroups_create(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await usergroups_create(name="TestGroup", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("usergroups.create", name="TestGroup")


@pytest.mark.asyncio
async def test_usergroups_disable(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await usergroups_disable(usergroup="S123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("usergroups.disable", usergroup="S123")


@pytest.mark.asyncio
async def test_usergroups_enable(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await usergroups_enable(usergroup="S123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("usergroups.enable", usergroup="S123")


@pytest.mark.asyncio
async def test_usergroups_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "usergroups": []}
    result = await usergroups_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("usergroups.list")


@pytest.mark.asyncio
async def test_usergroups_update(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await usergroups_update(
        usergroup="S123", name="Updated", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "usergroups.update", usergroup="S123", name="Updated"
    )


@pytest.mark.asyncio
async def test_usergroups_users_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "users": ["U123"]}
    result = await usergroups_users_list(usergroup="S123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "usergroups.users.list", usergroup="S123"
    )


@pytest.mark.asyncio
async def test_usergroups_users_update(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await usergroups_users_update(
        usergroup="S123", users="U123,U456", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "usergroups.users.update", usergroup="S123", users="U123,U456"
    )
