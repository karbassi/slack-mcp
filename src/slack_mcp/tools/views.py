from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def views_open(
    trigger_id: str,
    view: dict,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Open a view for a user."""
    return await client.api_call("views.open", trigger_id=trigger_id, view=view)


@mcp.tool
async def views_publish(
    user_id: str,
    view: dict,
    hash: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Publish a static view for a user."""
    kwargs = {"user_id": user_id, "view": view}
    if hash is not None:
        kwargs["hash"] = hash
    return await client.api_call("views.publish", **kwargs)


@mcp.tool
async def views_push(
    trigger_id: str,
    view: dict,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Push a view onto the stack of a root view."""
    return await client.api_call("views.push", trigger_id=trigger_id, view=view)


@mcp.tool
async def views_update(
    view: dict,
    external_id: str | None = None,
    hash: str | None = None,
    view_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an existing view."""
    kwargs = {"view": view}
    if external_id is not None:
        kwargs["external_id"] = external_id
    if hash is not None:
        kwargs["hash"] = hash
    if view_id is not None:
        kwargs["view_id"] = view_id
    return await client.api_call("views.update", **kwargs)
