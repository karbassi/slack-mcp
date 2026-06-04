from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def functions_complete_error(
    error: str,
    function_execution_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Signal that a function failed to complete."""
    return await client.api_call(
        "functions.completeError",
        error=error,
        function_execution_id=function_execution_id,
    )


@mcp.tool
async def functions_complete_success(
    function_execution_id: str,
    outputs: dict | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Signal the successful completion of a function."""
    return await client.api_call(
        "functions.completeSuccess",
        function_execution_id=function_execution_id,
        outputs=outputs,
    )
