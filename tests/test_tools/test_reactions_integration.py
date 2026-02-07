import uuid

import pytest

from slack_mcp.tools.chat import chat_delete, chat_post_message
from slack_mcp.tools.conversations import conversations_archive, conversations_create
from slack_mcp.tools.reactions import (
    reactions_add,
    reactions_get,
    reactions_list,
    reactions_remove,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reactions_list_live(live_client):
    result = await reactions_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reactions_lifecycle_live(live_client):
    """Post a message, add reaction, get reactions, remove reaction, clean up."""
    name = f"test-react-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        # Post a message
        posted = await chat_post_message(
            channel=channel_id, text="react to me", client=live_client
        )
        assert posted["ok"] is True
        ts = posted["ts"]

        # Add reaction
        added = await reactions_add(
            channel=channel_id, name="thumbsup", timestamp=ts, client=live_client
        )
        assert added["ok"] is True

        # Get reactions
        got = await reactions_get(
            channel=channel_id, timestamp=ts, client=live_client
        )
        assert got["ok"] is True

        # Remove reaction
        removed = await reactions_remove(
            name="thumbsup", channel=channel_id, timestamp=ts, client=live_client
        )
        assert removed["ok"] is True

        # Clean up message
        await chat_delete(channel=channel_id, ts=ts, client=live_client)
    finally:
        await conversations_archive(channel=channel_id, client=live_client)
