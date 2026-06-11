from typing import Any

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def views_open(
    trigger_id: str,
    view: dict[str, Any],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Open a view for a user."""
    return await client.api_call("views.open", trigger_id=trigger_id, view=view)


@mcp.tool
async def views_publish(
    user_id: str,
    view: dict[str, Any],
    hash: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Publish a static view for a user."""
    return await client.api_call(
        "views.publish", user_id=user_id, view=view, hash=hash
    )


@mcp.tool
async def views_push(
    trigger_id: str,
    view: dict[str, Any],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Push a view onto the stack of a root view."""
    return await client.api_call("views.push", trigger_id=trigger_id, view=view)


@mcp.tool
async def views_update(
    view: dict[str, Any],
    external_id: str | None = None,
    hash: str | None = None,
    view_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an existing view."""
    return await client.api_call(
        "views.update",
        view=view,
        external_id=external_id,
        hash=hash,
        view_id=view_id,
    )
