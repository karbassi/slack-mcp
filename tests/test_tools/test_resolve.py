import pytest
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_slack_response import AsyncSlackResponse

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
    mock_client.api_call.side_effect = SlackApiError(
        message="user_not_found",
        response=AsyncSlackResponse(
            client=None,
            http_verb="POST",
            api_url="https://slack.com/api/users.info",
            req_args={},
            data={"ok": False, "error": "user_not_found"},
            headers={},
            status_code=200,
        ),
    )
    result = await resolve_names(user_ids=["UBAD"], client=mock_client)
    assert result["ok"] is True
    assert "UBAD" not in result["names"]


@pytest.mark.asyncio
async def test_resolve_names_auth_error_propagates(mock_client):
    mock_client.api_call.side_effect = SlackApiError(
        message="not_authed",
        response=AsyncSlackResponse(
            client=None,
            http_verb="POST",
            api_url="https://slack.com/api/users.info",
            req_args={},
            data={"ok": False, "error": "not_authed"},
            headers={},
            status_code=200,
        ),
    )
    with pytest.raises(SlackApiError):
        await resolve_names(user_ids=["U123"], client=mock_client)


@pytest.mark.asyncio
async def test_resolve_names_deduplicates_ids(mock_client):
    mock_client.api_call.return_value = {
        "ok": True,
        "user": {
            "id": "U123",
            "name": "jdoe",
            "real_name": "Jane Doe",
            "profile": {"display_name": "Jane", "real_name": "Jane Doe"},
        },
    }
    result = await resolve_names(user_ids=["U123", "U123", "U123"], client=mock_client)
    assert result["names"]["U123"] == "Jane"
    mock_client.api_call.assert_called_once_with("users.info", user="U123")


@pytest.mark.asyncio
async def test_resolve_names_empty(mock_client):
    result = await resolve_names(client=mock_client)
    assert result["ok"] is True
    assert result["names"] == {}
    mock_client.api_call.assert_not_called()
