import pytest
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from slack_mcp.resolve import resolve_ids, set_cache_store
from tests.conftest import assert_api_call


async def test_resolve_names_users(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {
        "ok": True,
        "user": {
            "id": "U123",
            "name": "jdoe",
            "real_name": "Jane Doe",
            "profile": {"display_name": "Jane", "real_name": "Jane Doe"},
        },
    }
    result = await mcp_client.call_tool("resolve_names", {"user_ids": ["U123"]})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "users.info", user="U123")
    assert result.structured_content["names"]["U123"] == "Jane"


async def test_resolve_names_channels(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {
        "ok": True,
        "channel": {"id": "C456", "name": "general"},
    }
    result = await mcp_client.call_tool("resolve_names", {"channel_ids": ["C456"]})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.info", channel="C456")
    assert result.structured_content["names"]["C456"] == "general"


async def test_resolve_names_fallback_real_name(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {
        "ok": True,
        "user": {
            "id": "U789",
            "name": "bob",
            "real_name": "Bob Jones",
            "profile": {"display_name": "", "real_name": "Bob Jones"},
        },
    }
    result = await mcp_client.call_tool("resolve_names", {"user_ids": ["U789"]})
    assert result.is_error is False
    # Empty display_name falls back to real_name.
    assert result.structured_content["names"]["U789"] == "Bob Jones"


async def test_resolve_names_api_failure(mcp_client, slack_stub):
    slack_stub.api_call.side_effect = SlackApiError(
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
    result = await mcp_client.call_tool("resolve_names", {"user_ids": ["UBAD"]})
    assert result.is_error is False
    # A per-ID lookup failure is swallowed — the failed ID isn't in the map.
    assert result.structured_content["names"] == {}


async def test_resolve_names_auth_error_propagates(mcp_client, slack_stub):
    slack_stub.api_call.side_effect = SlackApiError(
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
    result = await mcp_client.call_tool(
        "resolve_names", {"user_ids": ["U123"]}, raise_on_error=False
    )
    assert result.is_error is True


async def test_resolve_names_deduplicates_ids(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {
        "ok": True,
        "user": {
            "id": "U123",
            "name": "jdoe",
            "real_name": "Jane Doe",
            "profile": {"display_name": "Jane", "real_name": "Jane Doe"},
        },
    }
    result = await mcp_client.call_tool(
        "resolve_names", {"user_ids": ["U123", "U123", "U123"]}
    )
    assert result.is_error is False
    slack_stub.api_call.assert_called_once_with("users.info", user="U123")
    assert result.structured_content["names"]["U123"] == "Jane"


async def test_resolve_names_empty(mcp_client, slack_stub):
    result = await mcp_client.call_tool("resolve_names", {})
    assert result.is_error is False
    slack_stub.api_call.assert_not_called()


@pytest.mark.asyncio
async def test_resolve_ids_caches_results(mock_client):
    """Second resolve for the same ID should hit cache, not the API."""
    from key_value.aio.stores.memory import MemoryStore

    store = MemoryStore()
    set_cache_store(store)

    mock_client.api_call.return_value = {
        "ok": True,
        "user": {
            "id": "U0TESTCACHE",
            "name": "cached",
            "profile": {"display_name": "Cached User", "real_name": "Cached User"},
        },
    }

    # First call — hits API
    result1 = await resolve_ids(mock_client, {"U0TESTCACHE"}, set(), set())
    assert result1["U0TESTCACHE"] == "Cached User"
    assert mock_client.api_call.call_count == 1

    # Second call — should hit cache, not API
    result2 = await resolve_ids(mock_client, {"U0TESTCACHE"}, set(), set())
    assert result2["U0TESTCACHE"] == "Cached User"
    assert mock_client.api_call.call_count == 1  # still 1, no new call

    set_cache_store(None)
