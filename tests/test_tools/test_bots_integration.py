import pytest

from slack_mcp.tools.bots import bots_info


@pytest.mark.integration
@pytest.mark.asyncio
async def test_bots_info_live(live_client):
    result = await bots_info(client=live_client)
    # May return ok:false if no bot specified, but the call should not error
    assert "ok" in result
