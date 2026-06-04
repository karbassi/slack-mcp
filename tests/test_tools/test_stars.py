import pytest

from slack_mcp.compact import compact_items, get_compactor
from slack_mcp.tools.stars import stars_add, stars_list, stars_remove
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_stars_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await stars_add(channel="C123", timestamp="1234.5678", client=mock_client)
    assert result["ok"] is True
    assert_api_call(
        mock_client.api_call, "stars.add", channel="C123", timestamp="1234.5678"
    )


@pytest.mark.asyncio
async def test_stars_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "items": []}
    result = await stars_list(client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "stars.list")


@pytest.mark.asyncio
async def test_stars_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await stars_remove(
        channel="C123", timestamp="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    assert_api_call(
        mock_client.api_call, "stars.remove", channel="C123", timestamp="1234.5678"
    )


def test_stars_list_compactable():
    assert get_compactor("stars_list") is compact_items
