from tests.conftest import assert_api_call


async def test_calendar_get_installed_calendars(mcp_client, slack_stub):
    slack_stub.session_call.return_value = {"ok": True, "gcal": {}, "ocal": {}}
    result = await mcp_client.call_tool("calendar_get_installed_calendars", {})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "calendar.getInstalledCalendars")


async def test_calendar_user_status(mcp_client, slack_stub):
    slack_stub.session_call.return_value = {"ok": True, "status": {}}
    result = await mcp_client.call_tool("calendar_user_status", {})
    assert result.is_error is False
    assert_api_call(slack_stub.session_call, "calendar.user.status")
