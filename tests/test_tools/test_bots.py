import pytest

from slack_mcp.tools.bots import bots_info
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_bots_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "bot": {"id": "B123"}}
    result = await bots_info(bot="B123", client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "bots.info", bot="B123")


@pytest.mark.asyncio
async def test_bots_info_no_args(mock_client):
    mock_client.api_call.return_value = {"ok": True, "bot": {}}
    result = await bots_info(client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "bots.info")
