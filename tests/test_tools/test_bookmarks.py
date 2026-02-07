import pytest

from slack_mcp.tools.bookmarks import (
    bookmarks_add,
    bookmarks_edit,
    bookmarks_list,
    bookmarks_remove,
)


@pytest.mark.asyncio
async def test_bookmarks_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await bookmarks_add(
        channel_id="C123",
        title="Test",
        type="link",
        link="https://example.com",
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "bookmarks.add",
        channel_id="C123",
        title="Test",
        type="link",
        link="https://example.com",
    )


@pytest.mark.asyncio
async def test_bookmarks_edit(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await bookmarks_edit(
        bookmark_id="Bk123", channel_id="C123", title="Updated", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "bookmarks.edit", bookmark_id="Bk123", channel_id="C123", title="Updated"
    )


@pytest.mark.asyncio
async def test_bookmarks_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "bookmarks": []}
    result = await bookmarks_list(channel_id="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("bookmarks.list", channel_id="C123")


@pytest.mark.asyncio
async def test_bookmarks_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await bookmarks_remove(
        bookmark_id="Bk123", channel_id="C123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "bookmarks.remove", bookmark_id="Bk123", channel_id="C123"
    )
