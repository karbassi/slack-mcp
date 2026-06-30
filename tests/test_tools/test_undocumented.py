import json
from unittest.mock import AsyncMock, patch

import pytest

from slack_mcp.compact import (
    compact_items,
    compact_message_list,
    compact_messages_by_channel,
    get_compactor,
)
from slack_mcp.tools.undocumented import _draft_body
from tests.conftest import assert_api_call


async def test_client_boot(mcp_client, slack_stub):
    result = await mcp_client.call_tool("client_boot", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("client.boot")


async def test_client_counts(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "client_counts", {"thread_count_by_last_read": True}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call, "client.counts", thread_count_by_last_read=True
    )


async def test_client_user_boot(mcp_client, slack_stub):
    result = await mcp_client.call_tool("client_user_boot", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("client.userBoot")


async def test_subscriptions_thread_mark(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "subscriptions_thread_mark",
        {"channel": "C123", "thread_ts": "1234.5678", "ts": "1234.9999"},
    )
    assert result.is_error is False
    slack_stub.session_call_form.assert_called_once_with(
        "subscriptions.thread.mark",
        channel="C123",
        thread_ts="1234.5678",
        ts="1234.9999",
        read=True,
    )


async def test_threads_get_view(mcp_client, slack_stub):
    result = await mcp_client.call_tool("threads_get_view", {})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "threads.getView")


async def test_drafts_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("drafts_list", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("drafts.list")


async def test_drafts_list_with_params(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "drafts_list", {"is_active": True, "limit": 10}
    )
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "drafts.list", is_active="true", limit="10"
    )


class TestDraftBody:
    def test_wraps_text_in_rich_text(self):
        body = _draft_body("C123", "hello")
        blocks = json.loads(body["blocks"])
        assert blocks[0]["type"] == "rich_text"
        section = blocks[0]["elements"][0]
        assert section["elements"][0] == {"type": "text", "text": "hello"}

    def test_minimal_destination(self):
        body = _draft_body("C123", "hi")
        assert json.loads(body["destinations"]) == [{"channel_id": "C123"}]

    def test_thread_destination_includes_broadcast(self):
        body = _draft_body("C123", "hi", thread_ts="1234.5678", broadcast=True)
        assert json.loads(body["destinations"]) == [
            {"channel_id": "C123", "thread_ts": "1234.5678", "broadcast": True}
        ]

    def test_file_ids_default_empty(self):
        assert json.loads(_draft_body("C123", "hi")["file_ids"]) == []

    def test_file_ids_passed_through(self):
        body = _draft_body("C123", "hi", file_ids=["F1", "F2"])
        assert json.loads(body["file_ids"]) == ["F1", "F2"]

    def test_client_msg_id_is_unique(self):
        a = _draft_body("C123", "hi")["client_msg_id"]
        b = _draft_body("C123", "hi")["client_msg_id"]
        assert a != b

    def test_fields_are_json_strings(self):
        # Endpoint quirk: blocks/destinations/file_ids are double-encoded.
        body = _draft_body("C123", "hi")
        assert all(
            isinstance(body[k], str)
            for k in ("blocks", "destinations", "file_ids")
        )


async def test_drafts_create(mcp_client, slack_stub):
    slack_stub.session_call.return_value = {"ok": True, "draft": {"id": "D123"}}
    result = await mcp_client.call_tool(
        "drafts_create", {"channel_id": "C123", "text": "Hello world"}
    )
    assert result.is_error is False
    call_kwargs = slack_stub.session_call.call_args
    assert call_kwargs[0][0] == "drafts.create"
    assert '"channel_id": "C123"' in call_kwargs[1]["destinations"]
    assert "Hello world" in call_kwargs[1]["blocks"]
    assert call_kwargs[1]["file_ids"] == "[]"


async def test_drafts_create_thread(mcp_client, slack_stub):
    slack_stub.session_call.return_value = {"ok": True, "draft": {"id": "D123"}}
    result = await mcp_client.call_tool(
        "drafts_create",
        {
            "channel_id": "C123",
            "text": "Reply",
            "thread_ts": "1234.5678",
            "broadcast": True,
        },
    )
    assert result.is_error is False
    call_kwargs = slack_stub.session_call.call_args
    assert '"thread_ts": "1234.5678"' in call_kwargs[1]["destinations"]
    assert '"broadcast": true' in call_kwargs[1]["destinations"]


async def test_drafts_update(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "drafts_update",
        {
            "draft_id": "D123",
            "client_last_updated_ts": "1234.567",
            "channel_id": "C123",
            "text": "Updated",
        },
    )
    assert result.is_error is False
    call_kwargs = slack_stub.session_call.call_args
    assert call_kwargs[0][0] == "drafts.update"
    assert call_kwargs[1]["draft_id"] == "D123"
    assert call_kwargs[1]["client_last_updated_ts"] == "1234.5670000"
    assert "Updated" in call_kwargs[1]["blocks"]


async def test_drafts_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "drafts_delete",
        {"draft_id": "D123", "client_last_updated_ts": "1234.567"},
    )
    assert result.is_error is False
    slack_stub.session_call_form.assert_called_once_with(
        "drafts.delete", draft_id="D123", client_last_updated_ts="1234.5670000"
    )


async def test_drafts_delete_skips_malformed_list_entries(mcp_client, slack_stub):
    # Auto-fetch path: a malformed drafts.list entry must not raise KeyError.
    slack_stub.session_call.return_value = {
        "ok": True,
        "drafts": [{"no_id": True}, {"id": "D123", "last_updated_ts": "1234.567"}],
    }
    result = await mcp_client.call_tool("drafts_delete", {"draft_id": "D123"})
    assert result.is_error is False
    slack_stub.session_call_form.assert_called_once_with(
        "drafts.delete", draft_id="D123", client_last_updated_ts="1234.5670000"
    )


async def test_drafts_delete_keeps_searching_past_malformed_match(
    mcp_client, slack_stub
):
    # A matching-id entry that lacks last_updated_ts must not short-circuit;
    # keep searching for a usable timestamp.
    slack_stub.session_call.return_value = {
        "ok": True,
        "drafts": [
            {"id": "D123"},
            {"id": "D123", "last_updated_ts": "1234.567"},
        ],
    }
    result = await mcp_client.call_tool("drafts_delete", {"draft_id": "D123"})
    assert result.is_error is False
    slack_stub.session_call_form.assert_called_once_with(
        "drafts.delete", draft_id="D123", client_last_updated_ts="1234.5670000"
    )


async def test_saved_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("saved_list", {"limit": 10})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "saved.list", limit=10)


async def test_saved_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "saved_add",
        {"item_type": "message", "item_id": "C123", "ts": "1234.5678"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call,
        "saved.add",
        item_type="message",
        item_id="C123",
        ts="1234.5678",
    )


async def test_saved_add_with_due_date(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "saved_add",
        {
            "item_type": "message",
            "item_id": "C123",
            "ts": "1234.5678",
            "date_due": "1700000000",
        },
    )
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "saved.add",
        item_type="message",
        item_id="C123",
        ts="1234.5678",
        date_due="1700000000",
    )


async def test_saved_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "saved_delete",
        {"item_type": "message", "item_id": "C123", "ts": "1234.5678"},
    )
    assert result.is_error is False
    slack_stub.session_call_form.assert_called_once_with(
        "saved.delete", item_type="message", item_id="C123", ts="1234.5678"
    )


async def test_emoji_add(mcp_client, slack_stub):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.content = b"\x89PNG"
    mock_response.headers = {"content-type": "image/png"}
    mock_response.raise_for_status = lambda: None

    with patch("slack_mcp.tools.undocumented.httpx.AsyncClient") as mock_http:
        mock_http.return_value.__aenter__ = AsyncMock(
            return_value=mock_http.return_value
        )
        mock_http.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_http.return_value.get = AsyncMock(return_value=mock_response)

        result = await mcp_client.call_tool(
            "emoji_add",
            {"name": "test_emoji", "image_url": "https://example.com/emoji.png"},
        )

    assert result.is_error is False
    slack_stub.session_call_multipart.assert_called_once_with(
        "emoji.add",
        data={"name": "test_emoji", "mode": "data"},
        files={"image": ("test_emoji.png", b"\x89PNG", "image/png")},
    )


async def test_emoji_remove(mcp_client, slack_stub):
    result = await mcp_client.call_tool("emoji_remove", {"name": "test_emoji"})
    assert result.is_error is False
    slack_stub.session_call_form.assert_called_once_with(
        "emoji.remove", name="test_emoji"
    )


async def test_emoji_admin_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "emoji_admin_list", {"page": 1, "count": 50}
    )
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "emoji.adminList", page=1, count=50
    )


async def test_search_modules_messages(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "search_modules_messages", {"query": "hello", "count": 10}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.session_call, "search.modules.messages", query="hello", count=10
    )


async def test_search_modules_files(mcp_client, slack_stub):
    result = await mcp_client.call_tool("search_modules_files", {"query": "report"})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "search.modules.files", query="report")


async def test_search_modules_channels(mcp_client, slack_stub):
    result = await mcp_client.call_tool("search_modules_channels", {"query": "eng"})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "search.modules.channels", query="eng")


async def test_search_modules_people(mcp_client, slack_stub):
    result = await mcp_client.call_tool("search_modules_people", {"query": "alice"})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "search.modules.people", query="alice")


async def test_search_modules_dms(mcp_client, slack_stub):
    result = await mcp_client.call_tool("search_modules_dms", {"query": "project"})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "search.modules.dms", query="project")


async def test_messages_list(mcp_client, slack_stub):
    groups = [{"channel": "C123", "timestamps": ["1700000000.000100"]}]
    result = await mcp_client.call_tool("messages_list", {"message_ids": groups})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "messages.list", message_ids=groups)
    assert get_compactor("messages_list") is compact_messages_by_channel


async def test_conversations_view(mcp_client, slack_stub):
    result = await mcp_client.call_tool("conversations_view", {"channel": "C123"})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with(
        "conversations.view", channel="C123"
    )


async def test_conversations_list_prefs(mcp_client, slack_stub):
    result = await mcp_client.call_tool("conversations_list_prefs", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("conversations.listPrefs")


async def test_users_channel_sections_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_channel_sections_list", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("users.channelSections.list")


async def test_users_priority_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("users_priority_list", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("users.priority.list")


async def test_experiments_get_by_user(mcp_client, slack_stub):
    result = await mcp_client.call_tool("experiments_get_by_user", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("experiments.getByUser")


async def test_api_features(mcp_client, slack_stub):
    result = await mcp_client.call_tool("api_features", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("api.features")


async def test_ai_apps_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("ai_apps_list", {})
    assert result.is_error is False
    slack_stub.session_call.assert_called_once_with("aiApps.list")


async def test_session_test_unexpected_error_propagates(mcp_client, slack_stub):
    """Unexpected exceptions should not be silently caught."""
    slack_stub.xoxc_token = "xoxc-test"
    slack_stub.xoxd_token = "xoxd-test"
    slack_stub.session_call.side_effect = RuntimeError("unexpected")
    from fastmcp.exceptions import ToolError

    with pytest.raises(ToolError):
        await mcp_client.call_tool("session_test", {})


async def test_session_test_known_errors_return_structured(mcp_client, slack_stub):
    """Known network/API errors should return structured error dicts."""
    slack_stub.xoxc_token = "xoxc-test"
    slack_stub.xoxd_token = "xoxd-test"
    slack_stub.session_call.side_effect = ValueError("invalid token")
    result = await mcp_client.call_tool("session_test", {}, raise_on_error=False)
    assert result.is_error is True
    assert result.structured_content["error"] == "invalid_or_expired"
    assert "invalid token" in result.structured_content["message"]


def test_search_modules_messages_compactable():
    assert get_compactor("search_modules_messages") is compact_message_list


def test_conversations_view_compactable():
    assert get_compactor("conversations_view") is compact_message_list


def test_saved_list_compactable():
    assert get_compactor("saved_list") is compact_items
