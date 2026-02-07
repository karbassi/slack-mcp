import uuid

import pytest

from slack_mcp.tools.bookmarks import (
    bookmarks_add,
    bookmarks_edit,
    bookmarks_list,
    bookmarks_remove,
)
from slack_mcp.tools.conversations import conversations_archive, conversations_create


@pytest.mark.integration
@pytest.mark.asyncio
async def test_bookmarks_lifecycle_live(live_client):
    """Create a channel, add a bookmark, edit it, list, remove, then clean up."""
    name = f"test-bkmk-{uuid.uuid4().hex[:8]}"
    created = await conversations_create(name=name, client=live_client)
    assert created["ok"] is True
    channel_id = created["channel"]["id"]

    try:
        # Add bookmark
        added = await bookmarks_add(
            channel_id=channel_id,
            title="Test Bookmark",
            type="link",
            link="https://example.com",
            client=live_client,
        )
        assert added["ok"] is True
        bookmark_id = added["bookmark"]["id"]

        # Edit bookmark
        edited = await bookmarks_edit(
            bookmark_id=bookmark_id,
            channel_id=channel_id,
            title="Updated Bookmark",
            client=live_client,
        )
        assert edited["ok"] is True

        # List bookmarks
        listed = await bookmarks_list(channel_id=channel_id, client=live_client)
        assert listed["ok"] is True

        # Remove bookmark
        removed = await bookmarks_remove(
            bookmark_id=bookmark_id, channel_id=channel_id, client=live_client
        )
        assert removed["ok"] is True
    finally:
        await conversations_archive(channel=channel_id, client=live_client)
