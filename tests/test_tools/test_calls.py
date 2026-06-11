from tests.conftest import assert_api_call


async def test_calls_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "calls_add",
        {
            "external_unique_id": "ext123",
            "join_url": "https://example.com/join",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "calls.add",
        external_unique_id="ext123",
        join_url="https://example.com/join",
    )


async def test_calls_end(mcp_client, slack_stub):
    result = await mcp_client.call_tool("calls_end", {"id": "R123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "calls.end", id="R123")


async def test_calls_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("calls_info", {"id": "R123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "calls.info", id="R123")


async def test_calls_participants_add(mcp_client, slack_stub):
    users = [{"slack_id": "U123"}]
    result = await mcp_client.call_tool(
        "calls_participants_add", {"id": "R123", "users": users}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "calls.participants.add", id="R123", users=users
    )


async def test_calls_participants_remove(mcp_client, slack_stub):
    users = [{"slack_id": "U123"}]
    result = await mcp_client.call_tool(
        "calls_participants_remove", {"id": "R123", "users": users}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "calls.participants.remove", id="R123", users=users
    )


async def test_calls_update(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "calls_update", {"id": "R123", "title": "Updated"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "calls.update", id="R123", title="Updated")
