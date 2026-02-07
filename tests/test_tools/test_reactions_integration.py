import pytest

from slack_mcp.tools.reactions import (
    reactions_add,
    reactions_get,
    reactions_list,
    reactions_remove,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would add a reaction to a message")
async def test_reactions_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific message or file to get reactions for")
async def test_reactions_get_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reactions_list_live(live_client):
    result = await reactions_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would remove a reaction from a message")
async def test_reactions_remove_live(live_client):
    pass
