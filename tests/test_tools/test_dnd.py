import pytest
from slack_mcp.tools.dnd import (
    dnd_end_dnd,
    dnd_end_snooze,
    dnd_info,
    dnd_set_snooze,
    dnd_team_info,
)


@pytest.mark.asyncio
async def test_dnd_end_dnd(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await dnd_end_dnd(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("dnd.endDnd")


@pytest.mark.asyncio
async def test_dnd_end_snooze(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await dnd_end_snooze(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("dnd.endSnooze")


@pytest.mark.asyncio
async def test_dnd_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "dnd_enabled": True}
    result = await dnd_info(user="U123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("dnd.info", user="U123")


@pytest.mark.asyncio
async def test_dnd_set_snooze(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await dnd_set_snooze(num_minutes=60, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("dnd.setSnooze", num_minutes=60)


@pytest.mark.asyncio
async def test_dnd_team_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "users": {}}
    result = await dnd_team_info(users="U123,U456", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("dnd.teamInfo", users="U123,U456")
