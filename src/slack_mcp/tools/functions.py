from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def functions_complete_error(
    error: str,
    function_execution_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Signal that a function failed to complete.

    Args:
        error: Human-readable error message describing why the function failed.
        function_execution_id: ID of the function execution to fail, from the ``function_executed`` event.
    """
    return await client.api_call(
        "functions.completeError",
        error=error,
        function_execution_id=function_execution_id,
    )


@mcp.tool
async def functions_complete_success(
    function_execution_id: str,
    outputs: dict,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Signal the successful completion of a function.

    Args:
        function_execution_id: ID of the function execution to complete, from the ``function_executed`` event.
        outputs: Mapping of output names to values, matching the output parameters declared in the function definition.
    """
    return await client.api_call(
        "functions.completeSuccess",
        function_execution_id=function_execution_id,
        outputs=outputs,
    )
