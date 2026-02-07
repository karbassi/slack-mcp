import pytest

from slack_mcp.tools.stars import (
    stars_add,
    stars_list,
    stars_remove,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would star an item")
async def test_stars_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stars_list_live(live_client):
    result = await stars_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would remove a star from an item")
async def test_stars_remove_live(live_client):
    pass
