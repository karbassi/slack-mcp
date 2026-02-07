import pytest

from slack_mcp.tools.calls import (
    calls_add,
    calls_end,
    calls_info,
    calls_participants_add,
    calls_participants_remove,
    calls_update,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would create a call")
async def test_calls_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would end a call")
async def test_calls_end_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires existing call ID")
async def test_calls_info_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would add participants")
async def test_calls_participants_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would remove participants")
async def test_calls_participants_remove_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would update a call")
async def test_calls_update_live(live_client):
    pass
