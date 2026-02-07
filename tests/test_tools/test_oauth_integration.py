import pytest

from slack_mcp.tools.oauth import (
    oauth_access,
    oauth_v2_access,
    oauth_v2_exchange,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid OAuth authorization code")
async def test_oauth_access_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid OAuth v2 authorization code")
async def test_oauth_v2_access_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid legacy token to exchange")
async def test_oauth_v2_exchange_live(live_client):
    pass
