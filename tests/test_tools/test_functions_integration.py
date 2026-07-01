import pytest

from slack_mcp.tools.functions import (
    functions_complete_error,
    functions_complete_success,
    functions_workflows_list,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid function_execution_id")
async def test_functions_complete_error_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid function_execution_id")
async def test_functions_complete_success_live(live_client):
    result = await functions_complete_success(
        function_execution_id="Fx0000000000", outputs={}, client=live_client
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_functions_workflows_list_live(live_client):
    """List workflows and their triggers (tolerates an empty workspace)."""
    result = await functions_workflows_list(limit=5, client=live_client)
    assert result["ok"] is True
    assert "workflows" in result
    assert "workflow_triggers" in result
