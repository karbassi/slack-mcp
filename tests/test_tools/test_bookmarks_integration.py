import pytest

from slack_mcp.tools.bookmarks import (
    bookmarks_add,
    bookmarks_edit,
    bookmarks_list,
    bookmarks_remove,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would add a bookmark")
async def test_bookmarks_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would edit a bookmark")
async def test_bookmarks_edit_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a channel with bookmarks")
async def test_bookmarks_list_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would remove a bookmark")
async def test_bookmarks_remove_live(live_client):
    pass
