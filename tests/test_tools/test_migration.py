import pytest
from slack_mcp.tools.migration import migration_exchange


@pytest.mark.asyncio
async def test_migration_exchange(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await migration_exchange(users="U123,U456", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "migration.exchange", users="U123,U456"
    )
