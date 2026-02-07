import pytest

from slack_mcp.tools.calls import (
    calls_add,
    calls_end,
    calls_info,
    calls_participants_add,
    calls_participants_remove,
    calls_update,
)


@pytest.mark.asyncio
async def test_calls_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await calls_add(
        external_unique_id="ext123",
        join_url="https://example.com/join",
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "calls.add",
        external_unique_id="ext123",
        join_url="https://example.com/join",
    )


@pytest.mark.asyncio
async def test_calls_end(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await calls_end(id="R123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("calls.end", id="R123")


@pytest.mark.asyncio
async def test_calls_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "call": {}}
    result = await calls_info(id="R123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("calls.info", id="R123")


@pytest.mark.asyncio
async def test_calls_participants_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    users = [{"slack_id": "U123"}]
    result = await calls_participants_add(id="R123", users=users, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "calls.participants.add", id="R123", users=users
    )


@pytest.mark.asyncio
async def test_calls_participants_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    users = [{"slack_id": "U123"}]
    result = await calls_participants_remove(id="R123", users=users, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "calls.participants.remove", id="R123", users=users
    )


@pytest.mark.asyncio
async def test_calls_update(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await calls_update(id="R123", title="Updated", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "calls.update", id="R123", title="Updated"
    )
