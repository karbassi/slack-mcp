import uuid

import pytest

from slack_mcp.tools.chat import chat_delete, chat_post_message
from slack_mcp.tools.conversations import conversations_archive, conversations_create
from slack_mcp.tools.pins import pins_add, pins_list, pins_remove


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pins_lifecycle_live(live_client):
    """Post a message, pin it, list pins, unpin it, then clean up."""
    name = f"test-pins-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        # Post a message to pin
        posted = await chat_post_message(
            channel=channel_id, text="pin me", client=live_client
        )
        assert posted["ok"] is True
        ts = posted["ts"]

        # Pin it
        pinned = await pins_add(
            channel=channel_id, timestamp=ts, client=live_client
        )
        assert pinned["ok"] is True

        # List pins
        listed = await pins_list(channel=channel_id, client=live_client)
        assert listed["ok"] is True

        # Unpin it
        unpinned = await pins_remove(
            channel=channel_id, timestamp=ts, client=live_client
        )
        assert unpinned["ok"] is True

        # Clean up message
        await chat_delete(channel=channel_id, ts=ts, client=live_client)
    finally:
        await conversations_archive(channel=channel_id, client=live_client)
