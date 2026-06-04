import pytest

from slack_mcp.tools.rtm import rtm_connect, rtm_start
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_rtm_connect(mock_client):
    mock_client.api_call.return_value = {"ok": True, "url": "wss://..."}
    result = await rtm_connect(client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "rtm.connect")


@pytest.mark.asyncio
async def test_rtm_start(mock_client):
    mock_client.api_call.return_value = {"ok": True, "url": "wss://..."}
    result = await rtm_start(client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "rtm.start")
