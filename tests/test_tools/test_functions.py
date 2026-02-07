import pytest
from slack_mcp.tools.functions import functions_complete_error, functions_complete_success


@pytest.mark.asyncio
async def test_functions_complete_error(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await functions_complete_error(
        error="something broke", function_execution_id="Fn123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "functions.completeError",
        error="something broke",
        function_execution_id="Fn123",
    )


@pytest.mark.asyncio
async def test_functions_complete_success(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await functions_complete_success(
        function_execution_id="Fn123", outputs={"result": "done"}, client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "functions.completeSuccess",
        function_execution_id="Fn123",
        outputs={"result": "done"},
    )
