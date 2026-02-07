import pytest

from slack_mcp.tools.canvases import (
    canvases_access_delete,
    canvases_access_set,
    canvases_create,
    canvases_delete,
    canvases_edit,
    canvases_sections_lookup,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would modify canvas access")
async def test_canvases_access_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would modify canvas access")
async def test_canvases_access_set_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would create a canvas")
async def test_canvases_create_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would delete a canvas")
async def test_canvases_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would edit a canvas")
async def test_canvases_edit_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires existing canvas")
async def test_canvases_sections_lookup_live(live_client):
    pass
