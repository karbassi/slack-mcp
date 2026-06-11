from tests.conftest import assert_api_call


async def test_dnd_end_dnd(mcp_client, slack_stub):
    result = await mcp_client.call_tool("dnd_end_dnd", {})
    assert result.is_error is False
    slack_stub.api_call.assert_called_once_with("dnd.endDnd")


async def test_dnd_end_snooze(mcp_client, slack_stub):
    result = await mcp_client.call_tool("dnd_end_snooze", {})
    assert result.is_error is False
    slack_stub.api_call.assert_called_once_with("dnd.endSnooze")


async def test_dnd_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("dnd_info", {"user": "U123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "dnd.info", user="U123")


async def test_dnd_set_snooze(mcp_client, slack_stub):
    result = await mcp_client.call_tool("dnd_set_snooze", {"num_minutes": 60})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "dnd.setSnooze", num_minutes=60)


async def test_dnd_team_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("dnd_team_info", {"users": "U123,U456"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "dnd.teamInfo", users="U123,U456")
