import pytest

from slack_mcp.tools.migration import (
    migration_exchange,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid legacy user IDs to exchange")
async def test_migration_exchange_live(live_client):
    pass
