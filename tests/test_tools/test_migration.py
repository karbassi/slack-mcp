import pytest

from slack_mcp.tools.migration import migration_exchange
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_migration_exchange(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await migration_exchange(users="U123,U456", client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "migration.exchange", users="U123,U456")
