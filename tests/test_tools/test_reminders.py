from tests.conftest import assert_api_call


async def test_reminders_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "reminders_add", {"text": "Do thing", "time": "in 5 minutes"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "reminders.add", text="Do thing", time="in 5 minutes"
    )


async def test_reminders_complete(mcp_client, slack_stub):
    result = await mcp_client.call_tool("reminders_complete", {"reminder": "Rm123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "reminders.complete", reminder="Rm123")


async def test_reminders_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool("reminders_delete", {"reminder": "Rm123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "reminders.delete", reminder="Rm123")


async def test_reminders_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("reminders_info", {"reminder": "Rm123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "reminders.info", reminder="Rm123")


async def test_reminders_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("reminders_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "reminders.list")
