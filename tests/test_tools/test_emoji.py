import pytest

from slack_mcp.tools.emoji import emoji_list
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_emoji_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "emoji": {}}
    result = await emoji_list(client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "emoji.list")
