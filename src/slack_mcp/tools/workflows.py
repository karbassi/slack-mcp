from typing import Any

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def workflows_featured_add(
    workflow_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add featured workflows.

    Args:
        workflow_ids: Workflow IDs forwarded as the ``workflow_ids`` param. Note: the live Slack API
            expects ``channel_id`` + ``trigger_ids`` instead (see #37).
    """
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
    """Remove featured workflows.

    Args:
        workflow_ids: Workflow IDs forwarded as the ``workflow_ids`` param. Note: the live Slack API
            expects ``channel_id`` + ``trigger_ids`` instead (see #37).
    """
    return await client.api_call("workflows.featured.remove", workflow_ids=workflow_ids)


@mcp.tool
async def workflows_featured_set(
    workflow_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set featured workflows.

    Args:
        workflow_ids: Workflow IDs forwarded as the ``workflow_ids`` param. Note: the live Slack API
            expects ``channel_id`` + ``trigger_ids`` instead (see #37).
    """
    return await client.api_call("workflows.featured.set", workflow_ids=workflow_ids)


@mcp.tool
async def workflows_step_completed(
    workflow_step_execute_id: str,
    outputs: dict[str, Any] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Indicate a workflow step has been completed successfully.

    Args:
        workflow_step_execute_id: Context identifier for the step execution, from the ``workflow_step_execute`` event.
        outputs: Key-value object mapping output names from the step's configuration to their values.
    """
    return await client.api_call(
        "workflows.stepCompleted",
        workflow_step_execute_id=workflow_step_execute_id,
        outputs=outputs,
    )


@mcp.tool
async def workflows_step_failed(
    error: dict[str, Any],
    workflow_step_execute_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Indicate a workflow step has failed.

    Args:
        error: A JSON-based object with a ``message`` property that should contain a human-readable error message.
        workflow_step_execute_id: Context identifier for the step execution, from the ``workflow_step_execute`` event.
    """
    return await client.api_call(
        "workflows.stepFailed",
        error=error,
        workflow_step_execute_id=workflow_step_execute_id,
    )


@mcp.tool
async def workflows_update_step(
    workflow_step_edit_id: str,
    inputs: dict[str, Any] | None = None,
    outputs: list[dict[str, Any]] | None = None,
    step_image_url: str | None = None,
    step_name: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update the configuration for a workflow step.

    Args:
        workflow_step_edit_id: A context identifier from the ``view_submission`` payload, mapping to editing a step.
        inputs: Key-value map of inputs from the user's step configuration; each value has a ``value`` property.
        outputs: A list of output objects (each with ``name``, ``type``, and ``label``) used during step execution.
        step_image_url: Optional override for the image shown to users in the Workflow Builder for this step.
        step_name: Optional override for the name shown to users in the Workflow Builder for this step.
    """
    return await client.api_call(
        "workflows.updateStep",
        workflow_step_edit_id=workflow_step_edit_id,
        inputs=inputs,
        outputs=outputs,
        step_image_url=step_image_url,
        step_name=step_name,
    )
