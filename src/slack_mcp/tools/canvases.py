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
    """Remove access to a canvas for specified entities."""
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
    """Set access level to a canvas for specified entities."""
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
    """Create a canvas."""
    return await client.api_call_json(
        "canvases.create", title=title, document_content=document_content
    )


@mcp.tool
async def canvases_delete(
    canvas_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a canvas."""
    return await client.api_call("canvases.delete", canvas_id=canvas_id)


@mcp.tool
async def canvases_edit(
    canvas_id: str,
    changes: list[dict[str, Any]],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Edit a canvas."""
    return await client.api_call_json(
        "canvases.edit", canvas_id=canvas_id, changes=changes
    )


@mcp.tool
async def canvases_sections_lookup(
    canvas_id: str,
    criteria: dict[str, Any],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Find sections matching criteria in a canvas."""
    return await client.api_call_json(
        "canvases.sections.lookup", canvas_id=canvas_id, criteria=criteria
    )
