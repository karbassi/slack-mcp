import uuid

import pytest

from slack_mcp.tools.conversations import (
    conversations_archive,
    conversations_create,
    conversations_history,
    conversations_info,
    conversations_join,
    conversations_leave,
    conversations_list,
    conversations_list_connect_invites,
    conversations_members,
    conversations_rename,
    conversations_replies,
    conversations_request_shared_invite_list,
    conversations_set_purpose,
    conversations_set_topic,
    conversations_unarchive,
)


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
        members = await conversations_members(
            channel=channel_id, client=live_client
        )
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
        archived = await conversations_archive(
            channel=channel_id, client=live_client
        )
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
        result = await conversations_unarchive(
            channel=channel_id, client=live_client
        )
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
