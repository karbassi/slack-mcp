import pytest
from slack_mcp.tools.tooling import tooling_tokens_rotate


@pytest.mark.asyncio
async def test_tooling_tokens_rotate(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await tooling_tokens_rotate(
        refresh_token="xoxe-1-...",
        client_id="C123",
        client_secret="S456",
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "tooling.tokens.rotate",
        refresh_token="xoxe-1-...",
        client_id="C123",
        client_secret="S456",
        grant_type="refresh_token",
    )
