import pytest

from slack_mcp.tools.pins import (
    pins_add,
    pins_list,
    pins_remove,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would pin an item to a channel")
async def test_pins_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: requires a specific channel")
async def test_pins_list_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would unpin an item from a channel")
async def test_pins_remove_live(live_client):
    pass
