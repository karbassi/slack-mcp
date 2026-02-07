from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


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
    outputs: Optional[dict] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Signal the successful completion of a function."""
    kwargs = {"function_execution_id": function_execution_id}
    if outputs is not None:
        kwargs["outputs"] = outputs
    return await client.api_call("functions.completeSuccess", **kwargs)
