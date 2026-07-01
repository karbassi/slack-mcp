import uuid

import pytest

from slack_mcp.tools.chat import chat_delete, chat_post_message
from slack_mcp.tools.conversations import conversations_archive, conversations_create
from slack_mcp.tools.undocumented import (
    activity_feed,
    ai_apps_list,
    ai_digest_list,
    ai_summarize_unreads_snapshot,
    api_features,
    client_boot,
    client_counts,
    client_dms,
    client_user_boot,
    connect_invites_list,
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
    messages_list,
    saved_add,
    saved_delete,
    saved_get,
    saved_list,
    search_modules_channels,
    search_modules_dms,
    search_modules_files,
    search_modules_messages,
    search_modules_people,
    session_test,
    subscriptions_thread_get_view,
    subscriptions_thread_mark,
    threads_get_view,
    today_items_list,
    users_channel_sections_list,
    users_priority_list,
)

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@pytest.fixture
async def temp_channel(live_client):
    """Create a temp channel and archive it after the test."""
    name = f"test-undoc-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]
    yield channel_id
    await conversations_archive(channel=channel_id, client=live_client)


# --- Session test ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_session_test_live(live_client):
    result = await session_test(client=live_client)
    assert "ok" in result


# --- Client/Boot ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_client_boot_live(live_client):
    result = await client_boot(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_client_counts_live(live_client):
    result = await client_counts(client=live_client)
    assert result["ok"] is True


@pytest.mark.usefixtures("requires_session_tokens")
async def test_client_user_boot_live(live_client):
    result = await client_user_boot(client=live_client)
    assert result["ok"] is True


@pytest.mark.usefixtures("requires_session_tokens")
async def test_threads_get_view_live(live_client):
    result = await threads_get_view(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_subscriptions_thread_get_view_live(live_client):
    result = await subscriptions_thread_get_view(limit=10, client=live_client)
    assert result["ok"] is True


@pytest.mark.usefixtures("requires_session_tokens")
async def test_client_dms_live(live_client):
    result = await client_dms(count=10, client=live_client)
    assert result["ok"] is True


# --- Drafts lifecycle ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_drafts_lifecycle_live(live_client, temp_channel):
    """Create, list, update, delete a draft."""
    # Create
    result = await drafts_create(
        channel_id=temp_channel, text="Integration test draft", client=live_client
    )
    assert result["ok"] is True
    draft = result["draft"]
    draft_id = draft["id"]
    ts = draft["last_updated_ts"]

    # List and verify it exists
    result = await drafts_list(is_active=True, client=live_client)
    assert result["ok"] is True
    assert any(d["id"] == draft_id for d in result.get("drafts", []))

    # Update
    result = await drafts_update(
        draft_id=draft_id,
        client_last_updated_ts=ts,
        channel_id=temp_channel,
        text="Updated integration test draft",
        client=live_client,
    )
    assert result["ok"] is True
    ts = result["draft"]["last_updated_ts"]

    # Delete
    result = await drafts_delete(
        draft_id=draft_id, client_last_updated_ts=ts, client=live_client
    )
    assert result["ok"] is True


@pytest.mark.usefixtures("requires_session_tokens")
async def test_drafts_delete_auto_lookup_live(live_client, temp_channel):
    """Delete a draft without passing client_last_updated_ts."""
    result = await drafts_create(
        channel_id=temp_channel, text="Auto-delete test", client=live_client
    )
    assert result["ok"] is True
    draft_id = result["draft"]["id"]

    result = await drafts_delete(draft_id=draft_id, client=live_client)
    assert result["ok"] is True


# --- Saved Items ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_saved_lifecycle_live(live_client, temp_channel):
    """Save a message, list it, then unsave it."""
    from slack_mcp.tools.chat import chat_post_message

    # Post a message to save
    msg = await chat_post_message(
        channel=temp_channel, text="Message to save", client=live_client
    )
    assert msg["ok"] is True
    msg_ts = msg["ts"]

    # Save it
    result = await saved_add(
        item_type="message", item_id=temp_channel, ts=msg_ts, client=live_client
    )
    assert result["ok"] is True

    # List saved items
    result = await saved_list(client=live_client)
    assert result["ok"] is True

    # Fetch the specific saved item back by id (just saved above, so must succeed)
    result = await saved_get(
        items=[
            {
                "item_type": "message",
                "item_id": temp_channel,
                "ts": msg_ts,
                "item_detail": "",
            }
        ],
        client=live_client,
    )
    assert result["ok"] is True

    # Unsave it
    result = await saved_delete(
        item_type="message", item_id=temp_channel, ts=msg_ts, client=live_client
    )
    assert result["ok"] is True


# --- Emoji ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_emoji_admin_list_live(live_client):
    result = await emoji_admin_list(count=5, client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_emoji_add_tool_live(live_client):
    """Add a custom emoji via emoji_add (URL-based), then remove it."""
    name = f"test_{uuid.uuid4().hex[:8]}"
    image_url = (
        "https://www.google.com/images/branding/googlelogo"
        "/2x/googlelogo_color_272x92dp.png"
    )

    result = await emoji_add(name=name, image_url=image_url, client=live_client)
    assert "ok" in result

    if result.get("ok") is True:
        await emoji_remove(name=name, client=live_client)


@pytest.mark.usefixtures("requires_session_tokens")
async def test_emoji_add_remove_live(live_client):
    """Add a custom emoji from a local PNG then remove it."""
    from pathlib import Path

    name = f"test_{uuid.uuid4().hex[:8]}"
    png_path = Path(__file__).parent.parent / "fixtures" / "test_emoji.png"
    png_bytes = png_path.read_bytes()

    result = await live_client.session_call_multipart(
        "emoji.add",
        data={"name": name, "mode": "data"},
        files={"image": (f"{name}.png", png_bytes, "image/png")},
    )
    assert result.get("ok") is True

    result = await emoji_remove(name=name, client=live_client)
    # Some workspaces restrict emoji removal (enterprise_is_restricted)
    assert "ok" in result


# --- Threads ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_subscriptions_thread_mark_live(live_client, temp_channel):
    """Post a thread and mark it as read."""
    from slack_mcp.tools.chat import chat_post_message

    # Create a thread
    parent = await chat_post_message(
        channel=temp_channel, text="Thread parent", client=live_client
    )
    assert parent["ok"] is True
    thread_ts = parent["ts"]

    reply = await chat_post_message(
        channel=temp_channel,
        text="Thread reply",
        thread_ts=thread_ts,
        client=live_client,
    )
    assert reply["ok"] is True

    result = await subscriptions_thread_mark(
        channel=temp_channel,
        thread_ts=thread_ts,
        ts=reply["ts"],
        read=True,
        client=live_client,
    )
    assert "ok" in result


# --- Search modules ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_modules_messages_live(live_client):
    result = await search_modules_messages(query="test", count=5, client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_modules_files_live(live_client):
    result = await search_modules_files(query="test", count=5, client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_modules_channels_live(live_client):
    result = await search_modules_channels(query="test", count=5, client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_modules_people_live(live_client):
    result = await search_modules_people(query="test", count=5, client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_modules_dms_live(live_client):
    result = await search_modules_dms(query="test", count=5, client=live_client)
    assert "ok" in result


# --- Conversations (undocumented) ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_conversations_view_live(live_client, temp_channel):
    result = await conversations_view(channel=temp_channel, client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_conversations_list_prefs_live(live_client):
    result = await conversations_list_prefs(client=live_client)
    assert "ok" in result


# --- Users (undocumented) ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_users_channel_sections_list_live(live_client):
    result = await users_channel_sections_list(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_users_priority_list_live(live_client):
    result = await users_priority_list(client=live_client)
    assert "ok" in result


# --- Workspace introspection ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_experiments_get_by_user_live(live_client):
    result = await experiments_get_by_user(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_api_features_live(live_client):
    result = await api_features(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_ai_apps_list_live(live_client):
    result = await ai_apps_list(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_ai_summarize_unreads_snapshot_live(live_client):
    # ai.alpha.* may be gated by workspace AI features — tolerate ok: false.
    result = await ai_summarize_unreads_snapshot(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_ai_digest_list_live(live_client):
    # ai.alpha.* may be gated by workspace AI features — tolerate ok: false.
    # On the test workspace this returns ok: true with digests metadata.
    result = await ai_digest_list(client=live_client)
    assert "ok" in result


# --- Slack Connect ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_connect_invites_list_live(live_client):
    # The test workspace may have no Connect invites — an empty
    # connect_invites list is still a valid ok: true response.
    result = await connect_invites_list(client=live_client)
    assert result["ok"] is True
    assert "connect_invites" in result


# --- Activity inbox ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_activity_feed_live(live_client):
    result = await activity_feed(limit=10, client=live_client)
    assert result["ok"] is True


# --- Today view ---


@pytest.mark.usefixtures("requires_session_tokens")
async def test_today_items_list_live(live_client):
    # The Today view is feature-gated/rolled-out per workspace; the free test
    # workspace returns ok: false (unknown_method). Assert the tool round-trips
    # and yields a well-formed Slack envelope; tolerate ok: false where gated.
    result = await today_items_list(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_messages_list_live(live_client, temp_channel):
    """Post a message, then batch-fetch it back by channel + ts."""
    posted = await chat_post_message(
        channel=temp_channel, text="messages.list integration", client=live_client
    )
    ts = posted["ts"]
    result = await messages_list(
        message_ids=[{"channel": temp_channel, "timestamps": [ts]}],
        client=live_client,
    )
    assert result["ok"] is True
    fetched = result["messages"][temp_channel]
    assert any(m["ts"] == ts for m in fetched)
    await chat_delete(channel=temp_channel, ts=ts, client=live_client)
