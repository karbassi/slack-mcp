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


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid workflow IDs")
async def test_workflows_featured_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid workflow IDs")
async def test_workflows_featured_list_live(live_client):
    """List featured workflows in the workspace."""
    result = await workflows_featured_list(client=live_client)
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid workflow IDs")
async def test_workflows_featured_remove_live(live_client):
    """Remove workflows from the featured list."""
    result = await workflows_featured_remove(
        workflow_ids=["Wf0000000000"],
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid workflow IDs")
async def test_workflows_featured_set_live(live_client):
    """Set the featured workflows list (replaces entire list)."""
    result = await workflows_featured_set(
        workflow_ids=["Wf0000000000"],
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="requires a valid workflow_step_execute_id from an active step"
)
async def test_workflows_step_completed_live(live_client):
    """Mark a workflow step execution as completed."""
    result = await workflows_step_completed(
        workflow_step_execute_id="0000000000",
        outputs={},
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="requires a valid workflow_step_execute_id from an active step"
)
async def test_workflows_step_failed_live(live_client):
    """Mark a workflow step execution as failed."""
    result = await workflows_step_failed(
        workflow_step_execute_id="0000000000",
        error={"message": "Integration test failure"},
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="requires a valid workflow_step_edit_id from a configuration event"
)
async def test_workflows_update_step_live(live_client):
    """Update the configuration for a workflow step."""
    result = await workflows_update_step(
        workflow_step_edit_id="0000000000",
        step_name="Integration Test Step",
        inputs={},
        outputs=[],
        client=live_client,
    )
    assert "ok" in result
