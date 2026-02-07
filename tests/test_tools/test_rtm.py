import pytest
from slack_mcp.tools.rtm import rtm_connect, rtm_start


@pytest.mark.asyncio
async def test_rtm_connect(mock_client):
    mock_client.api_call.return_value = {"ok": True, "url": "wss://..."}
    result = await rtm_connect(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("rtm.connect")


@pytest.mark.asyncio
async def test_rtm_start(mock_client):
    mock_client.api_call.return_value = {"ok": True, "url": "wss://..."}
    result = await rtm_start(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("rtm.start")
