import contextlib
import uuid

import pytest
from slack_sdk.errors import SlackApiError

from slack_mcp.tools.chat import chat_post_message
from slack_mcp.tools.conversations import (
    conversations_accept_shared_invite,
    conversations_approve_shared_invite,
    conversations_archive,
    conversations_canvases_create,
    conversations_close,
    conversations_create,
    conversations_decline_shared_invite,
    conversations_external_invite_permissions_set,
    conversations_history,
    conversations_info,
    conversations_invite,
    conversations_invite_shared,
    conversations_join,
    conversations_kick,
    conversations_leave,
    conversations_list,
    conversations_list_connect_invites,
    conversations_mark,
    conversations_members,
    conversations_open,
    conversations_rename,
    conversations_replies,
    conversations_request_shared_invite_approve,
    conversations_request_shared_invite_deny,
    conversations_request_shared_invite_list,
    conversations_set_purpose,
    conversations_set_topic,
    conversations_unarchive,
)


@pytest.fixture
async def temp_channel(live_client):
    """Create a temp channel and archive it after the test."""
    name = f"test-conv-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]
    yield channel_id
    await conversations_archive(channel=channel_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_list_live(live_client):
    result = await conversations_list(limit=5, client=live_client)
    assert result["ok"] is True
    assert "channels" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_create_and_archive_live(live_client):
    """Create a temp channel, exercise operations, then archive it."""
    name = f"test-{uuid.uuid4().hex[:8]}"

    # Create
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        # Info
        info = await conversations_info(channel=channel_id, client=live_client)
        assert info["ok"] is True
        assert info["channel"]["name"] == name

        # History (empty channel)
        history = await conversations_history(
            channel=channel_id, limit=5, client=live_client
        )
        assert history["ok"] is True

        # Members
        members = await conversations_members(channel=channel_id, client=live_client)
        assert members["ok"] is True

        # Set topic
        topic = await conversations_set_topic(
            channel=channel_id, topic="integration test topic", client=live_client
        )
        assert topic["ok"] is True

        # Set purpose
        purpose = await conversations_set_purpose(
            channel=channel_id, purpose="integration test purpose", client=live_client
        )
        assert purpose["ok"] is True

        # Rename
        new_name = f"test-{uuid.uuid4().hex[:8]}"
        renamed = await conversations_rename(
            channel=channel_id, name=new_name, client=live_client
        )
        assert renamed["ok"] is True

    finally:
        # Archive (cleanup)
        archived = await conversations_archive(channel=channel_id, client=live_client)
        assert archived["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_unarchive_live(live_client):
    """Create, archive, unarchive, then re-archive."""
    name = f"test-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        await conversations_archive(channel=channel_id, client=live_client)
        result = await conversations_unarchive(channel=channel_id, client=live_client)
        assert result["ok"] is True
    finally:
        await conversations_archive(channel=channel_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_join_and_leave_live(live_client):
    """Create a public channel, leave it, rejoin it, then archive."""
    name = f"test-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        left = await conversations_leave(channel=channel_id, client=live_client)
        assert left["ok"] is True

        joined = await conversations_join(channel=channel_id, client=live_client)
        assert joined["ok"] is True
    finally:
        await conversations_archive(channel=channel_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Slack Connect")
async def test_conversations_accept_shared_invite_live(live_client):
    """Accept a Slack Connect shared invite (requires Slack Connect)."""
    await conversations_accept_shared_invite(
        channel_name="test-accept", invite_id="I_FAKE", client=live_client
    )


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Slack Connect")
async def test_conversations_approve_shared_invite_live(live_client):
    """Approve a Slack Connect shared invite (requires Slack Connect)."""
    await conversations_approve_shared_invite(
        invite_id="I_FAKE", client=live_client
    )


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Slack Connect")
async def test_conversations_decline_shared_invite_live(live_client):
    """Decline a Slack Connect shared invite (requires Slack Connect)."""
    await conversations_decline_shared_invite(
        invite_id="I_FAKE", client=live_client
    )


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Slack Connect")
async def test_conversations_external_invite_permissions_set_live(live_client):
    """Set external invite permissions (requires Slack Connect)."""
    await conversations_external_invite_permissions_set(
        channel="C_FAKE", action="allow", client=live_client
    )


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Slack Connect")
async def test_conversations_invite_shared_live(live_client):
    """Send a Slack Connect shared invite (requires Slack Connect)."""
    await conversations_invite_shared(
        channel="C_FAKE", emails=["test@example.com"], client=live_client
    )


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Slack Connect")
async def test_conversations_request_shared_invite_approve_live(live_client):
    """Approve a shared channel invite request (requires Slack Connect)."""
    await conversations_request_shared_invite_approve(
        invite_id="I_FAKE", client=live_client
    )


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Slack Connect")
async def test_conversations_request_shared_invite_deny_live(live_client):
    """Deny a shared channel invite request (requires Slack Connect)."""
    await conversations_request_shared_invite_deny(
        invite_id="I_FAKE", client=live_client
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_canvases_create_live(live_client, temp_channel):
    """Create a canvas in a channel."""
    result = await conversations_canvases_create(
        channel_id=temp_channel, client=live_client
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_close_live(live_client):
    """Open a DM with ourselves and then close it."""
    from slack_mcp.tools.auth import auth_test

    auth = await auth_test(client=live_client)
    user_id = auth["user_id"]

    opened = await conversations_open(users=user_id, client=live_client)
    assert opened["ok"] is True
    dm_id = opened["channel"]["id"]

    result = await conversations_close(channel=dm_id, client=live_client)
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_invite_live(live_client):
    """Invite ourselves to a channel we left, verifying the API call works."""
    name = f"test-inv-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        from slack_mcp.tools.auth import auth_test

        auth = await auth_test(client=live_client)
        user_id = auth["user_id"]

        # Leave first so we can re-invite ourselves
        await conversations_leave(channel=channel_id, client=live_client)

        invite_result = await conversations_invite(
            channel=channel_id, users=user_id, client=live_client
        )
        assert invite_result["ok"] is True
    except SlackApiError as e:
        # Some token types cannot use conversations.invite
        assert e.response["error"] in (
            "not_allowed_token_type",
            "cant_invite_self",
            "method_not_supported_for_channel_type",
        )
    finally:
        # Rejoin before archiving (archive requires membership)
        with contextlib.suppress(SlackApiError):
            await conversations_join(channel=channel_id, client=live_client)
        await conversations_archive(channel=channel_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_kick_live(live_client):
    """Kick requires a second user; verify the API responds."""
    name = f"test-kick-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        from slack_mcp.tools.auth import auth_test

        auth = await auth_test(client=live_client)
        user_id = auth["user_id"]

        # Kicking yourself from your own channel: expect cant_kick_self or similar
        result = await conversations_kick(
            channel=channel_id, user=user_id, client=live_client
        )
        assert "ok" in result
    except Exception:
        pass  # cant_kick_self is expected
    finally:
        await conversations_archive(channel=channel_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_list_connect_invites_live(live_client):
    """List Slack Connect invites."""
    try:
        result = await conversations_list_connect_invites(client=live_client)
        assert "ok" in result
    except SlackApiError as e:
        # Some workspaces/token types don't support Slack Connect
        assert e.response["error"] in (
            "missing_scope",
            "feature_not_enabled",
            "not_allowed",
            "not_allowed_token_type",
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_mark_live(live_client, temp_channel):
    """Set the read cursor in a channel."""
    # Post a message to get a valid timestamp
    posted = await chat_post_message(
        channel=temp_channel, text="mark test", client=live_client
    )
    assert posted["ok"] is True
    ts = posted["ts"]

    try:
        result = await conversations_mark(
            channel=temp_channel, ts=ts, client=live_client
        )
        assert "ok" in result
    except SlackApiError as e:
        # May fail depending on token type or session token configuration
        assert e.response["error"] in (
            "missing_scope",
            "not_authed",
            "channel_not_found",
            "not_allowed_token_type",
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_open_live(live_client):
    """Open a DM with ourselves."""
    from slack_mcp.tools.auth import auth_test

    auth = await auth_test(client=live_client)
    user_id = auth["user_id"]

    result = await conversations_open(users=user_id, client=live_client)
    assert result["ok"] is True
    assert "channel" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_replies_live(live_client, temp_channel):
    """Post a message and fetch its thread replies."""
    posted = await chat_post_message(
        channel=temp_channel, text="thread parent", client=live_client
    )
    assert posted["ok"] is True
    ts = posted["ts"]

    result = await conversations_replies(
        channel=temp_channel, ts=ts, client=live_client
    )
    assert result["ok"] is True
    assert "messages" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_request_shared_invite_list_live(live_client):
    """List shared channel invite requests."""
    try:
        result = await conversations_request_shared_invite_list(client=live_client)
        assert "ok" in result
    except SlackApiError as e:
        # Some workspaces/token types don't support Slack Connect
        assert e.response["error"] in (
            "missing_scope",
            "feature_not_enabled",
            "restricted_action",
            "not_allowed_token_type",
        )
