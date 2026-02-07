import pytest

from slack_mcp.tools.functions import (
    functions_complete_error,
    functions_complete_success,
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
    pass
