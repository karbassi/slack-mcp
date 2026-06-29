from tests.conftest import assert_api_call


async def test_workflows_featured_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "workflows_featured_add", {"channel_id": "C123", "trigger_ids": ["Ft123"]}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "workflows.featured.add",
        channel_id="C123",
        trigger_ids=["Ft123"],
    )


async def test_workflows_featured_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("workflows_featured_list", {})
    assert result.is_error is False
    slack_stub.api_call.assert_called_once_with("workflows.featured.list")


async def test_workflows_featured_remove(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "workflows_featured_remove", {"channel_id": "C123", "trigger_ids": ["Ft123"]}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "workflows.featured.remove",
        channel_id="C123",
        trigger_ids=["Ft123"],
    )


async def test_workflows_featured_set(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "workflows_featured_set",
        {"channel_id": "C123", "trigger_ids": ["Ft123", "Ft456"]},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "workflows.featured.set",
        channel_id="C123",
        trigger_ids=["Ft123", "Ft456"],
    )


async def test_workflows_step_completed(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "workflows_step_completed",
        {"workflow_step_execute_id": "WS123"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "workflows.stepCompleted",
        workflow_step_execute_id="WS123",
    )


async def test_workflows_step_failed(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "workflows_step_failed",
        {
            "error": {"message": "oops"},
            "workflow_step_execute_id": "WS123",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "workflows.stepFailed",
        error={"message": "oops"},
        workflow_step_execute_id="WS123",
    )


async def test_workflows_update_step(mcp_client, slack_stub):
    inputs = {"name": {"value": "Ada", "skip_variable_replacement": False}}
    result = await mcp_client.call_tool(
        "workflows_update_step",
        {
            "workflow_step_edit_id": "WSE123",
            "inputs": inputs,
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "workflows.updateStep",
        workflow_step_edit_id="WSE123",
        inputs=inputs,
    )
