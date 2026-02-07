import pytest

from slack_mcp.tools.pins import pins_add, pins_list, pins_remove


@pytest.mark.asyncio
async def test_pins_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await pins_add(channel="C123", timestamp="1234.5678", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "pins.add", channel="C123", timestamp="1234.5678"
    )


@pytest.mark.asyncio
async def test_pins_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "items": []}
    result = await pins_list(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("pins.list", channel="C123")


@pytest.mark.asyncio
async def test_pins_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await pins_remove(
        channel="C123", timestamp="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "pins.remove", channel="C123", timestamp="1234.5678"
    )
