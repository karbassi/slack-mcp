import pytest

from slack_mcp.tools.reminders import (
    reminders_add,
    reminders_complete,
    reminders_delete,
    reminders_info,
    reminders_list,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would create a reminder")
async def test_reminders_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would mark a reminder as complete")
async def test_reminders_complete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would delete a reminder")
async def test_reminders_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific reminder ID")
async def test_reminders_info_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reminders_list_live(live_client):
    result = await reminders_list(client=live_client)
    assert result["ok"] is True
