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
async def test_reminders_list_live(live_client):
    result = await reminders_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reminders_add_live(live_client):
    """Create a reminder."""
    added = await reminders_add(
        text="integration test reminder", time="in 1 hour", client=live_client
    )
    assert added["ok"] is True
