import pytest

from slack_mcp.tools.auth import auth_test
from slack_mcp.tools.dnd import (
    dnd_end_dnd,
    dnd_end_snooze,
    dnd_info,
    dnd_set_snooze,
    dnd_team_info,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dnd_info_live(live_client):
    result = await dnd_info(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dnd_snooze_lifecycle_live(live_client):
    """Set snooze, check info, then end snooze."""
    # Set snooze for 1 minute
    snoozed = await dnd_set_snooze(num_minutes=1, client=live_client)
    assert snoozed["ok"] is True

    # Check info shows snooze active
    info = await dnd_info(client=live_client)
    assert info["ok"] is True
    assert info.get("snooze_enabled") is True

    # End snooze
    ended = await dnd_end_snooze(client=live_client)
    assert ended["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dnd_team_info_live(live_client):
    """Get DND team info using our own user ID."""
    auth = await auth_test(client=live_client)
    user_id = auth["user_id"]

    result = await dnd_team_info(users=user_id, client=live_client)
    assert result["ok"] is True
