import pytest

from slack_mcp.tools.calendar import (
    calendar_get_installed_calendars,
    calendar_user_status,
)

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@pytest.mark.usefixtures("requires_session_tokens")
async def test_calendar_get_installed_calendars_live(live_client):
    result = await calendar_get_installed_calendars(client=live_client)
    assert result["ok"] is True


@pytest.mark.usefixtures("requires_session_tokens")
async def test_calendar_user_status_live(live_client):
    result = await calendar_user_status(client=live_client)
    assert result["ok"] is True
