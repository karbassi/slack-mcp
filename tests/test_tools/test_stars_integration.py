import uuid

import pytest

from slack_mcp.tools.chat import chat_delete, chat_post_message
from slack_mcp.tools.conversations import conversations_archive, conversations_create
from slack_mcp.tools.stars import stars_add, stars_list, stars_remove


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stars_list_live(live_client):
    result = await stars_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stars_lifecycle_live(live_client):
    """Post a message, star it, list stars, unstar it, clean up."""
    name = f"test-stars-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        # Post a message
        posted = await chat_post_message(
            channel=channel_id, text="star me", client=live_client
        )
        assert posted["ok"] is True
        ts = posted["ts"]

        # Star it
        starred = await stars_add(
            channel=channel_id, timestamp=ts, client=live_client
        )
        assert starred["ok"] is True

        # Remove star
        unstarred = await stars_remove(
            channel=channel_id, timestamp=ts, client=live_client
        )
        assert unstarred["ok"] is True

        # Clean up message
        await chat_delete(channel=channel_id, ts=ts, client=live_client)
    finally:
        await conversations_archive(channel=channel_id, client=live_client)
