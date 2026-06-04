from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def workflows_featured_add(
    workflow_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add featured workflows."""
    return await client.api_call("workflows.featured.add", workflow_ids=workflow_ids)


@mcp.tool
async def workflows_featured_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List featured workflows."""
    return await client.api_call("workflows.featured.list")


@mcp.tool
async def workflows_featured_remove(
    workflow_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove featured workflows."""
    return await client.api_call("workflows.featured.remove", workflow_ids=workflow_ids)


@mcp.tool
async def workflows_featured_set(
    workflow_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set featured workflows."""
    return await client.api_call("workflows.featured.set", workflow_ids=workflow_ids)


@mcp.tool
async def workflows_step_completed(
    workflow_step_execute_id: str,
    outputs: dict[str, str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Indicate a workflow step has been completed successfully."""
    return await client.api_call(
        "workflows.stepCompleted",
        workflow_step_execute_id=workflow_step_execute_id,
        outputs=outputs,
    )


@mcp.tool
async def workflows_step_failed(
    error: dict[str, str],
    workflow_step_execute_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Indicate a workflow step has failed."""
    return await client.api_call(
        "workflows.stepFailed",
        error=error,
        workflow_step_execute_id=workflow_step_execute_id,
    )


@mcp.tool
async def workflows_update_step(
    workflow_step_edit_id: str,
    inputs: dict[str, str] | None = None,
    outputs: list[dict[str, str]] | None = None,
    step_image_url: str | None = None,
    step_name: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update the configuration for a workflow step."""
    return await client.api_call(
        "workflows.updateStep",
        workflow_step_edit_id=workflow_step_edit_id,
        inputs=inputs,
        outputs=outputs,
        step_image_url=step_image_url,
        step_name=step_name,
    )
