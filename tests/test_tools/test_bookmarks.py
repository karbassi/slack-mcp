from tests.conftest import assert_api_call


async def test_bookmarks_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "bookmarks_add",
        {
            "channel_id": "C123",
            "title": "Test",
            "type": "link",
            "link": "https://example.com",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "bookmarks.add",
        channel_id="C123",
        title="Test",
        type="link",
        link="https://example.com",
    )


async def test_bookmarks_edit(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "bookmarks_edit",
        {"bookmark_id": "Bk123", "channel_id": "C123", "title": "Updated"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "bookmarks.edit",
        bookmark_id="Bk123",
        channel_id="C123",
        title="Updated",
    )


async def test_bookmarks_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "bookmarks": []}
    result = await mcp_client.call_tool("bookmarks_list", {"channel_id": "C123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "bookmarks.list", channel_id="C123")


async def test_bookmarks_remove(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "bookmarks_remove", {"bookmark_id": "Bk123", "channel_id": "C123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "bookmarks.remove",
        bookmark_id="Bk123",
        channel_id="C123",
    )
