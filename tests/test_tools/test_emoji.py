import pytest
from slack_mcp.tools.emoji import emoji_list


@pytest.mark.asyncio
async def test_emoji_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "emoji": {}}
    result = await emoji_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("emoji.list")
