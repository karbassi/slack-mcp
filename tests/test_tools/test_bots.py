import pytest

from slack_mcp.tools.bots import bots_info


@pytest.mark.asyncio
async def test_bots_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "bot": {"id": "B123"}}
    result = await bots_info(bot="B123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("bots.info", bot="B123")


@pytest.mark.asyncio
async def test_bots_info_no_args(mock_client):
    mock_client.api_call.return_value = {"ok": True, "bot": {}}
    result = await bots_info(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("bots.info")
