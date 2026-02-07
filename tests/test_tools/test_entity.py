import pytest
from slack_mcp.tools.entity import entity_present_details


@pytest.mark.asyncio
async def test_entity_present_details(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await entity_present_details(
        app_id="A123", entity_id="E123", entity_type="channel", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "entity.presentDetails",
        app_id="A123",
        entity_id="E123",
        entity_type="channel",
    )
