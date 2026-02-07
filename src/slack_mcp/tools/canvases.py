from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def canvases_access_delete(
    canvas_id: str,
    channel_ids: Optional[list] = None,
    user_ids: Optional[list] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove access to a canvas for specified entities."""
    kwargs = {"canvas_id": canvas_id}
    if channel_ids is not None:
        kwargs["channel_ids"] = channel_ids
    if user_ids is not None:
        kwargs["user_ids"] = user_ids
    return await client.api_call("canvases.access.delete", **kwargs)


@mcp.tool
async def canvases_access_set(
    canvas_id: str,
    access_level: str,
    channel_ids: Optional[list] = None,
    user_ids: Optional[list] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set access level to a canvas for specified entities."""
    kwargs = {"canvas_id": canvas_id, "access_level": access_level}
    if channel_ids is not None:
        kwargs["channel_ids"] = channel_ids
    if user_ids is not None:
        kwargs["user_ids"] = user_ids
    return await client.api_call("canvases.access.set", **kwargs)


@mcp.tool
async def canvases_create(
    title: Optional[str] = None,
    document_content: Optional[dict] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a canvas."""
    kwargs = {}
    if title is not None:
        kwargs["title"] = title
    if document_content is not None:
        kwargs["document_content"] = document_content
    return await client.api_call("canvases.create", **kwargs)


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
    changes: list,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Edit a canvas."""
    return await client.api_call("canvases.edit", canvas_id=canvas_id, changes=changes)


@mcp.tool
async def canvases_sections_lookup(
    canvas_id: str,
    criteria: dict,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Find sections matching criteria in a canvas."""
    return await client.api_call(
        "canvases.sections.lookup", canvas_id=canvas_id, criteria=criteria
    )
