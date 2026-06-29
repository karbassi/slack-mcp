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
    """Open a view for a user.

    Args:
        trigger_id: Exchange a trigger to post to the user (e.g. ``12345.98765.abcd2358fdea``).
        view: A view payload object (of type ``modal``).
    """
    return await client.api_call("views.open", trigger_id=trigger_id, view=view)


@mcp.tool
async def views_publish(
    user_id: str,
    view: dict[str, Any],
    hash: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Publish a static view for a user.

    Args:
        user_id: ID of the user you want to publish a view to (e.g. ``U0123``).
        view: A view payload object (of type ``home``).
        hash: A string representing view state, used to protect against race conditions when updating an existing view.
    """
    return await client.api_call(
        "views.publish", user_id=user_id, view=view, hash=hash
    )


@mcp.tool
async def views_push(
    trigger_id: str,
    view: dict[str, Any],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Push a view onto the stack of a root view.

    Args:
        trigger_id: Exchange a trigger to post to the user (e.g. ``12345.98765.abcd2358fdea``).
        view: A view payload object (of type ``modal``) to push onto the existing view stack.
    """
    return await client.api_call("views.push", trigger_id=trigger_id, view=view)


@mcp.tool
async def views_update(
    view: dict[str, Any],
    external_id: str | None = None,
    hash: str | None = None,
    view_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an existing view.

    Args:
        view: A view payload object (of type ``modal``) with the updated contents.
        external_id: A unique identifier set by the developer when opening the view, identifying which view to update.
        hash: A string that represents view state to protect against possible race conditions when updating the view.
        view_id: A unique identifier of the view to be updated, returned when the view was opened (e.g. ``VMHU10V25``).
    """
    return await client.api_call(
        "views.update",
        view=view,
        external_id=external_id,
        hash=hash,
        view_id=view_id,
    )
