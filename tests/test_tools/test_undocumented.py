from unittest.mock import AsyncMock, patch

import pytest

from slack_mcp.tools.undocumented import (
    ai_apps_list,
    api_features,
    client_boot,
    client_counts,
    client_user_boot,
    conversations_list_prefs,
    conversations_view,
    drafts_create,
    drafts_delete,
    drafts_list,
    drafts_update,
    emoji_add,
    emoji_admin_list,
    emoji_remove,
    experiments_get_by_user,
    saved_add,
    saved_delete,
    saved_list,
    search_modules_channels,
    search_modules_dms,
    search_modules_files,
    search_modules_messages,
    search_modules_people,
    subscriptions_thread_mark,
    threads_get_view,
    users_channel_sections_list,
    users_priority_list,
)


@pytest.mark.asyncio
async def test_client_boot(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await client_boot(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("client.boot")


@pytest.mark.asyncio
async def test_client_counts(mock_client):
    mock_client.session_call.return_value = {"ok": True, "channels": []}
    result = await client_counts(thread_count_by_last_read=True, client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "client.counts", thread_count_by_last_read=True
    )


@pytest.mark.asyncio
async def test_client_user_boot(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await client_user_boot(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("client.userBoot")


@pytest.mark.asyncio
async def test_subscriptions_thread_mark(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await subscriptions_thread_mark(
        channel="C123", thread_ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "subscriptions.thread.mark",
        channel="C123",
        thread_ts="1234.5678",
        read=True,
    )


@pytest.mark.asyncio
async def test_threads_get_view(mock_client):
    mock_client.session_call.return_value = {"ok": True, "threads": []}
    result = await threads_get_view(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("threads.getView")


@pytest.mark.asyncio
async def test_drafts_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "drafts": []}
    result = await drafts_list(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("drafts.list")


@pytest.mark.asyncio
async def test_drafts_list_with_params(mock_client):
    mock_client.session_call.return_value = {"ok": True, "drafts": []}
    result = await drafts_list(is_active=True, limit=10, client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "drafts.list", is_active="true", limit="10"
    )


@pytest.mark.asyncio
async def test_drafts_create(mock_client):
    mock_client.session_call.return_value = {"ok": True, "draft": {"id": "D123"}}
    result = await drafts_create(
        channel_id="C123", text="Hello world", client=mock_client
    )
    assert result["ok"] is True
    call_kwargs = mock_client.session_call.call_args
    assert call_kwargs[0][0] == "drafts.create"
    assert '"channel_id": "C123"' in call_kwargs[1]["destinations"]
    assert "Hello world" in call_kwargs[1]["blocks"]
    assert call_kwargs[1]["file_ids"] == "[]"


@pytest.mark.asyncio
async def test_drafts_create_thread(mock_client):
    mock_client.session_call.return_value = {"ok": True, "draft": {"id": "D123"}}
    result = await drafts_create(
        channel_id="C123", text="Reply", thread_ts="1234.5678",
        broadcast=True, client=mock_client
    )
    assert result["ok"] is True
    call_kwargs = mock_client.session_call.call_args
    assert '"thread_ts": "1234.5678"' in call_kwargs[1]["destinations"]
    assert '"broadcast": true' in call_kwargs[1]["destinations"]


@pytest.mark.asyncio
async def test_drafts_update(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await drafts_update(
        draft_id="D123", client_last_updated_ts="1234.567",
        channel_id="C123", text="Updated", client=mock_client
    )
    assert result["ok"] is True
    call_kwargs = mock_client.session_call.call_args
    assert call_kwargs[0][0] == "drafts.update"
    assert call_kwargs[1]["draft_id"] == "D123"
    assert call_kwargs[1]["client_last_updated_ts"] == "1234.5670000"
    assert "Updated" in call_kwargs[1]["blocks"]


@pytest.mark.asyncio
async def test_drafts_delete(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await drafts_delete(
        draft_id="D123", client_last_updated_ts="1234.567", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "drafts.delete", draft_id="D123", client_last_updated_ts="1234.5670000"
    )


@pytest.mark.asyncio
async def test_saved_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "items": []}
    result = await saved_list(limit=10, client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("saved.list", limit=10)


@pytest.mark.asyncio
async def test_saved_add(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await saved_add(
        item_type="message", item_id="C123", ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "saved.add", item_type="message", item_id="C123", ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_saved_add_with_due_date(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await saved_add(
        item_type="message", item_id="C123", ts="1234.5678",
        date_due="1700000000", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "saved.add", item_type="message", item_id="C123",
        ts="1234.5678", date_due="1700000000"
    )


@pytest.mark.asyncio
async def test_saved_delete(mock_client):
    mock_client.session_call_form.return_value = {"ok": True}
    result = await saved_delete(
        item_type="message", item_id="C123", ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.session_call_form.assert_called_once_with(
        "saved.delete", item_type="message", item_id="C123", ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_emoji_add(mock_client):
    mock_client.session_call_multipart.return_value = {"ok": True}
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.content = b"\x89PNG"
    mock_response.headers = {"content-type": "image/png"}
    mock_response.raise_for_status = lambda: None

    with patch("slack_mcp.tools.undocumented.httpx.AsyncClient") as mock_http:
        mock_http.return_value.__aenter__ = AsyncMock(return_value=mock_http.return_value)
        mock_http.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_http.return_value.get = AsyncMock(return_value=mock_response)

        result = await emoji_add(
            name="test_emoji", image_url="https://example.com/emoji.png", client=mock_client
        )

    assert result["ok"] is True
    mock_client.session_call_multipart.assert_called_once_with(
        "emoji.add",
        data={"name": "test_emoji", "mode": "data"},
        files={"image": ("test_emoji.png", b"\x89PNG", "image/png")},
    )


@pytest.mark.asyncio
async def test_emoji_remove(mock_client):
    mock_client.session_call_form.return_value = {"ok": True}
    result = await emoji_remove(name="test_emoji", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call_form.assert_called_once_with("emoji.remove", name="test_emoji")


@pytest.mark.asyncio
async def test_emoji_admin_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "emoji": []}
    result = await emoji_admin_list(page=1, count=50, client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("emoji.adminList", page=1, count=50)


@pytest.mark.asyncio
async def test_search_modules_messages(mock_client):
    mock_client.session_call.return_value = {"ok": True, "items": []}
    result = await search_modules_messages(query="hello", count=10, client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "search.modules.messages", query="hello", count=10
    )


@pytest.mark.asyncio
async def test_search_modules_files(mock_client):
    mock_client.session_call.return_value = {"ok": True, "items": []}
    result = await search_modules_files(query="report", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("search.modules.files", query="report")


@pytest.mark.asyncio
async def test_search_modules_channels(mock_client):
    mock_client.session_call.return_value = {"ok": True, "items": []}
    result = await search_modules_channels(query="eng", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("search.modules.channels", query="eng")


@pytest.mark.asyncio
async def test_search_modules_people(mock_client):
    mock_client.session_call.return_value = {"ok": True, "items": []}
    result = await search_modules_people(query="alice", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("search.modules.people", query="alice")


@pytest.mark.asyncio
async def test_search_modules_dms(mock_client):
    mock_client.session_call.return_value = {"ok": True, "items": []}
    result = await search_modules_dms(query="project", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("search.modules.dms", query="project")


@pytest.mark.asyncio
async def test_conversations_view(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await conversations_view(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("conversations.view", channel="C123")


@pytest.mark.asyncio
async def test_conversations_list_prefs(mock_client):
    mock_client.session_call.return_value = {"ok": True, "prefs": []}
    result = await conversations_list_prefs(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("conversations.listPrefs")


@pytest.mark.asyncio
async def test_users_channel_sections_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "sections": []}
    result = await users_channel_sections_list(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("users.channelSections.list")


@pytest.mark.asyncio
async def test_users_priority_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "users": []}
    result = await users_priority_list(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("users.priority.list")


@pytest.mark.asyncio
async def test_experiments_get_by_user(mock_client):
    mock_client.session_call.return_value = {"ok": True, "experiments": []}
    result = await experiments_get_by_user(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("experiments.getByUser")


@pytest.mark.asyncio
async def test_api_features(mock_client):
    mock_client.session_call.return_value = {"ok": True, "features": {}}
    result = await api_features(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("api.features")


@pytest.mark.asyncio
async def test_ai_apps_list(mock_client):
    mock_client.session_call.return_value = {"ok": True, "apps": []}
    result = await ai_apps_list(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("aiApps.list")
