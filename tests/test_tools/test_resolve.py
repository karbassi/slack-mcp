import pytest

from slack_mcp.tools.resolve import resolve_names


@pytest.mark.asyncio
async def test_resolve_names_users(mock_client):
    mock_client.api_call.return_value = {
        "ok": True,
        "user": {
            "id": "U123",
            "name": "jdoe",
            "real_name": "Jane Doe",
            "profile": {"display_name": "Jane", "real_name": "Jane Doe"},
        },
    }
    result = await resolve_names(user_ids=["U123"], client=mock_client)
    assert result["ok"] is True
    assert result["names"]["U123"] == "Jane"
    mock_client.api_call.assert_called_once_with("users.info", user="U123")


@pytest.mark.asyncio
async def test_resolve_names_channels(mock_client):
    mock_client.api_call.return_value = {
        "ok": True,
        "channel": {"id": "C456", "name": "general"},
    }
    result = await resolve_names(channel_ids=["C456"], client=mock_client)
    assert result["ok"] is True
    assert result["names"]["C456"] == "general"
    mock_client.api_call.assert_called_once_with("conversations.info", channel="C456")


@pytest.mark.asyncio
async def test_resolve_names_mixed(mock_client):
    async def _side_effect(method, **kwargs):
        if method == "users.info":
            return {
                "ok": True,
                "user": {
                    "id": kwargs["user"],
                    "name": "alice",
                    "real_name": "Alice Smith",
                    "profile": {"display_name": "Alice", "real_name": "Alice Smith"},
                },
            }
        if method == "conversations.info":
            return {
                "ok": True,
                "channel": {"id": kwargs["channel"], "name": "random"},
            }
        return {"ok": False}

    mock_client.api_call.side_effect = _side_effect
    result = await resolve_names(
        user_ids=["U111"], channel_ids=["C222"], client=mock_client
    )
    assert result["ok"] is True
    assert result["names"]["U111"] == "Alice"
    assert result["names"]["C222"] == "random"


@pytest.mark.asyncio
async def test_resolve_names_fallback_real_name(mock_client):
    mock_client.api_call.return_value = {
        "ok": True,
        "user": {
            "id": "U789",
            "name": "bob",
            "real_name": "Bob Jones",
            "profile": {"display_name": "", "real_name": "Bob Jones"},
        },
    }
    result = await resolve_names(user_ids=["U789"], client=mock_client)
    assert result["names"]["U789"] == "Bob Jones"


@pytest.mark.asyncio
async def test_resolve_names_api_failure(mock_client):
    mock_client.api_call.return_value = {"ok": False, "error": "user_not_found"}
    result = await resolve_names(user_ids=["UBAD"], client=mock_client)
    assert result["ok"] is True
    assert result["names"]["UBAD"] is None


@pytest.mark.asyncio
async def test_resolve_names_empty(mock_client):
    result = await resolve_names(client=mock_client)
    assert result["ok"] is True
    assert result["names"] == {}
    mock_client.api_call.assert_not_called()
