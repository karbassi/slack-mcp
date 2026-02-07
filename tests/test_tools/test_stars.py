import pytest

from slack_mcp.tools.stars import stars_add, stars_list, stars_remove


@pytest.mark.asyncio
async def test_stars_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await stars_add(channel="C123", timestamp="1234.5678", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "stars.add", channel="C123", timestamp="1234.5678"
    )


@pytest.mark.asyncio
async def test_stars_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "items": []}
    result = await stars_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("stars.list")


@pytest.mark.asyncio
async def test_stars_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await stars_remove(
        channel="C123", timestamp="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "stars.remove", channel="C123", timestamp="1234.5678"
    )
