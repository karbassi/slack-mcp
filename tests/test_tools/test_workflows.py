import pytest
from slack_mcp.tools.workflows import (
    workflows_featured_add,
    workflows_featured_list,
    workflows_featured_remove,
    workflows_featured_set,
    workflows_step_completed,
    workflows_step_failed,
    workflows_update_step,
)


@pytest.mark.asyncio
async def test_workflows_featured_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await workflows_featured_add(
        workflow_ids=["W123"], client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "workflows.featured.add", workflow_ids=["W123"]
    )


@pytest.mark.asyncio
async def test_workflows_featured_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "workflows": []}
    result = await workflows_featured_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("workflows.featured.list")


@pytest.mark.asyncio
async def test_workflows_featured_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await workflows_featured_remove(
        workflow_ids=["W123"], client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "workflows.featured.remove", workflow_ids=["W123"]
    )


@pytest.mark.asyncio
async def test_workflows_featured_set(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await workflows_featured_set(
        workflow_ids=["W123", "W456"], client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "workflows.featured.set", workflow_ids=["W123", "W456"]
    )


@pytest.mark.asyncio
async def test_workflows_step_completed(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await workflows_step_completed(
        workflow_step_execute_id="WS123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "workflows.stepCompleted", workflow_step_execute_id="WS123"
    )


@pytest.mark.asyncio
async def test_workflows_step_failed(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await workflows_step_failed(
        error={"message": "oops"},
        workflow_step_execute_id="WS123",
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "workflows.stepFailed",
        error={"message": "oops"},
        workflow_step_execute_id="WS123",
    )


@pytest.mark.asyncio
async def test_workflows_update_step(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await workflows_update_step(
        workflow_step_edit_id="WSE123",
        inputs={"key": {"value": "val"}},
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "workflows.updateStep",
        workflow_step_edit_id="WSE123",
        inputs={"key": {"value": "val"}},
    )
