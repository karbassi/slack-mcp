import pytest

from slack_mcp.tools.rtm import (
    rtm_connect,
    rtm_start,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="missing_scope: requires rtm:stream")
async def test_rtm_connect_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="missing_scope: requires rtm:stream")
async def test_rtm_start_live(live_client):
    pass
