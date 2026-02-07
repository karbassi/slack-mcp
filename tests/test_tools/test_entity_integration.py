import pytest

from slack_mcp.tools.entity import (
    entity_present_details,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific app_id, entity_id, and entity_type")
async def test_entity_present_details_live(live_client):
    pass
