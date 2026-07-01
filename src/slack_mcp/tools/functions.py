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


@mcp.tool
async def functions_workflows_list(
    limit: int | None = None,
    filter_options: dict | None = None,
    sort_options: dict | None = None,
    workflow_builder_only: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List workflows and their triggers (undocumented session endpoint).

    Args:
        limit: Maximum number of workflows to return.
        filter_options: Object narrowing which workflows are returned (e.g. by
            source or collaborator); omitted when unset.
        sort_options: Object controlling result ordering (e.g. sort key and
            direction); omitted when unset.
        workflow_builder_only: When True, restrict results to workflows created
            in Workflow Builder.

    Returns:
        A dict with ``ok`` plus ``workflows`` (the matching workflow objects) and
        ``workflow_triggers`` (the triggers associated with those workflows).
    """
    return await client.session_call(
        "functions.workflows.list",
        limit=limit,
        filter_options=filter_options,
        sort_options=sort_options,
        workflow_builder_only=workflow_builder_only,
    )
