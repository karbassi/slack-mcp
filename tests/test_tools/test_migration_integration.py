import pytest

from slack_mcp.tools.auth import auth_test
from slack_mcp.tools.migration import (
    migration_exchange,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_migration_exchange_live(live_client):
    """Exchange our own user ID (maps to itself on Enterprise Grid)."""
    auth = await auth_test(client=live_client)
    user_id = auth["user_id"]

    result = await migration_exchange(users=user_id, client=live_client)
    assert result["ok"] is True
    assert user_id in result.get("user_id_map", {})
