from typing import Any

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def workflows_featured_add(
    channel_id: str,
    trigger_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add featured workflows to a channel.

    Args:
        channel_id: ID of the channel to feature the workflows in (e.g. ``C0123``).
        trigger_ids: Workflow trigger IDs to feature, max 15 (e.g. ``["Ft0123", "Ft0456"]``).
    """
    return await client.api_call(
        "workflows.featured.add", channel_id=channel_id, trigger_ids=trigger_ids
    )


@mcp.tool
async def workflows_featured_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List featured workflows."""
    return await client.api_call("workflows.featured.list")


@mcp.tool
async def workflows_featured_remove(
    channel_id: str,
    trigger_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove featured workflows from a channel.

    Args:
        channel_id: ID of the channel to remove the featured workflows from (e.g. ``C0123``).
        trigger_ids: Workflow trigger IDs to remove, max 15 (e.g. ``["Ft0123"]``).
    """
    return await client.api_call(
        "workflows.featured.remove", channel_id=channel_id, trigger_ids=trigger_ids
    )


@mcp.tool
async def workflows_featured_set(
    channel_id: str,
    trigger_ids: list[str],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Replace the featured workflows in a channel.

    Args:
        channel_id: ID of the channel to set featured workflows in (e.g. ``C0123``).
        trigger_ids: Workflow trigger IDs that replace the channel's featured set, max 15;
            an empty list clears all featured workflows (e.g. ``["Ft0123"]``).
    """
    return await client.api_call(
        "workflows.featured.set", channel_id=channel_id, trigger_ids=trigger_ids
    )


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


@mcp.tool
async def workflows_triggers_list(
    app_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List workflow triggers in the workspace (undocumented session endpoint).

    Args:
        app_ids: Restrict results to triggers owned by these app IDs
            (e.g. ``["A0123"]``); omitted when unset to return all triggers.

    Returns:
        A dict with ``ok`` plus ``triggers`` (the accessible trigger objects) and
        ``rejected_triggers`` (triggers that could not be returned, e.g. due to
        permissions).
    """
    return await client.session_call("workflows.triggers.list", app_ids=app_ids)
