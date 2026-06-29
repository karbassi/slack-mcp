from tests.conftest import assert_api_call


async def test_functions_complete_error(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "functions_complete_error",
        {"error": "something broke", "function_execution_id": "Fn123"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "functions.completeError",
        error="something broke",
        function_execution_id="Fn123",
    )


async def test_functions_complete_success(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "functions_complete_success",
        {"function_execution_id": "Fn123", "outputs": {"result": "done"}},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "functions.completeSuccess",
        function_execution_id="Fn123",
        outputs={"result": "done"},
    )


async def test_functions_complete_success_requires_outputs(mcp_client):
    # outputs is required by functions.completeSuccess.
    result = await mcp_client.call_tool(
        "functions_complete_success",
        {"function_execution_id": "Fn123"},
        raise_on_error=False,
    )
    assert result.is_error is True
