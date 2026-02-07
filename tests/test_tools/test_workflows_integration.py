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
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid workflow IDs")
async def test_workflows_featured_remove_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires valid workflow IDs")
async def test_workflows_featured_set_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid workflow_step_execute_id")
async def test_workflows_step_completed_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid workflow_step_execute_id")
async def test_workflows_step_failed_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid workflow_step_edit_id")
async def test_workflows_update_step_live(live_client):
    pass
