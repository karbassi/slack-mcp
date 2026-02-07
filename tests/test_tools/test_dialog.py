import pytest

from slack_mcp.tools.dialog import dialog_open


@pytest.mark.asyncio
async def test_dialog_open(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await dialog_open(
        dialog={"title": "Test"}, trigger_id="T123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "dialog.open", dialog={"title": "Test"}, trigger_id="T123"
    )
