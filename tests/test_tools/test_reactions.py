import pytest

from slack_mcp.compact import compact_items, compact_single_item, get_compactor
from slack_mcp.tools.reactions import (
    reactions_add,
    reactions_get,
    reactions_list,
    reactions_remove,
)
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_reactions_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await reactions_add(
        channel="C123", name="thumbsup", timestamp="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "reactions.add", channel="C123", name="thumbsup", timestamp="1234.5678"
    )


@pytest.mark.asyncio
async def test_reactions_get(mock_client):
    mock_client.api_call.return_value = {"ok": True, "message": {}}
    result = await reactions_get(
        channel="C123", timestamp="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    assert_api_call(
        mock_client.api_call, "reactions.get", channel="C123", timestamp="1234.5678"
    )


@pytest.mark.asyncio
async def test_reactions_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "items": []}
    result = await reactions_list(client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "reactions.list")


@pytest.mark.asyncio
async def test_reactions_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await reactions_remove(
        name="thumbsup", channel="C123", timestamp="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    assert_api_call(
        mock_client.api_call,
        "reactions.remove",
        name="thumbsup",
        channel="C123",
        timestamp="1234.5678",
    )


def test_reactions_get_compactable():
    assert get_compactor("reactions_get") is compact_single_item


def test_reactions_list_compactable():
    assert get_compactor("reactions_list") is compact_items
