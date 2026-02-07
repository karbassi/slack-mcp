import pytest

from slack_mcp.tools.emoji import (
    emoji_list,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_emoji_list_live(live_client):
    result = await emoji_list(client=live_client)
    assert result["ok"] is True
