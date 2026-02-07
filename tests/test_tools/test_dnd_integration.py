import pytest

from slack_mcp.tools.dnd import (
    dnd_end_dnd,
    dnd_end_snooze,
    dnd_info,
    dnd_set_snooze,
    dnd_team_info,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would end DND session")
async def test_dnd_end_dnd_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would end snooze mode")
async def test_dnd_end_snooze_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dnd_info_live(live_client):
    result = await dnd_info(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would enable snooze mode")
async def test_dnd_set_snooze_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid user IDs")
async def test_dnd_team_info_live(live_client):
    pass
