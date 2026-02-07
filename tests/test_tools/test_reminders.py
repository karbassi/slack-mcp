import pytest
from slack_mcp.tools.reminders import (
    reminders_add,
    reminders_complete,
    reminders_delete,
    reminders_info,
    reminders_list,
)


@pytest.mark.asyncio
async def test_reminders_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await reminders_add(
        text="Do thing", time="in 5 minutes", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "reminders.add", text="Do thing", time="in 5 minutes"
    )


@pytest.mark.asyncio
async def test_reminders_complete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await reminders_complete(reminder="Rm123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "reminders.complete", reminder="Rm123"
    )


@pytest.mark.asyncio
async def test_reminders_delete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await reminders_delete(reminder="Rm123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "reminders.delete", reminder="Rm123"
    )


@pytest.mark.asyncio
async def test_reminders_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "reminder": {}}
    result = await reminders_info(reminder="Rm123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("reminders.info", reminder="Rm123")


@pytest.mark.asyncio
async def test_reminders_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "reminders": []}
    result = await reminders_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("reminders.list")
