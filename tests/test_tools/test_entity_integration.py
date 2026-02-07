import pytest

from slack_mcp.tools.entity import (
    entity_present_details,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: requires bot token (xoxb)")
async def test_entity_present_details_live(live_client):
    pass
