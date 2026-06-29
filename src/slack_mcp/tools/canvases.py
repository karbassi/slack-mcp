from typing import Any

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def canvases_access_delete(
    canvas_id: str,
    channel_ids: list[str] | None = None,
    user_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove access to a canvas for specified entities.

    Args:
        canvas_id: Encoded ID of the canvas to remove access from (e.g. ``F0123ABC456``).
        channel_ids: Channel IDs whose access to the canvas should be removed (e.g. ``["C0123"]``).
        user_ids: User IDs whose access to the canvas should be removed (e.g. ``["U0123"]``).
    """
    return await client.api_call_json(
        "canvases.access.delete",
        canvas_id=canvas_id,
        channel_ids=channel_ids,
        user_ids=user_ids,
    )


@mcp.tool
async def canvases_access_set(
    canvas_id: str,
    access_level: str,
    channel_ids: list[str] | None = None,
    user_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set access level to a canvas for specified entities.

    Args:
        canvas_id: Encoded ID of the canvas to set access on (e.g. ``F0123ABC456``).
        access_level: Access level granted to the entities, either ``read`` or ``write``.
        channel_ids: Channel IDs to grant the access level to (e.g. ``["C0123"]``).
        user_ids: User IDs to grant the access level to (e.g. ``["U0123"]``).
    """
    return await client.api_call_json(
        "canvases.access.set",
        canvas_id=canvas_id,
        access_level=access_level,
        channel_ids=channel_ids,
        user_ids=user_ids,
    )


@mcp.tool
async def canvases_create(
    title: str | None = None,
    document_content: dict[str, Any] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a canvas.

    Args:
        title: Title of the newly created canvas.
        document_content: Structured content; an object with ``type`` of ``markdown`` and a ``markdown`` body field.
    """
    return await client.api_call_json(
        "canvases.create", title=title, document_content=document_content
    )


@mcp.tool
async def canvases_delete(
    canvas_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a canvas.

    Args:
        canvas_id: Encoded ID of the canvas to delete (e.g. ``F0123ABC456``).
    """
    return await client.api_call("canvases.delete", canvas_id=canvas_id)


@mcp.tool
async def canvases_edit(
    canvas_id: str,
    changes: list[dict[str, Any]],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Edit a canvas.

    Args:
        canvas_id: Encoded ID of the canvas to edit (e.g. ``F0123ABC456``).
        changes: Ordered edit operations, each with an operation (insert/replace/delete), document_content, section_id.
    """
    return await client.api_call_json(
        "canvases.edit", canvas_id=canvas_id, changes=changes
    )


@mcp.tool
async def canvases_sections_lookup(
    canvas_id: str,
    criteria: dict[str, Any],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Find sections matching criteria in a canvas.

    Args:
        canvas_id: Encoded ID of the canvas to search within (e.g. ``F0123ABC456``).
        criteria: Filter for which sections to return, e.g. a ``contains_text`` substring and/or ``section_types``.
    """
    return await client.api_call_json(
        "canvases.sections.lookup", canvas_id=canvas_id, criteria=criteria
    )
