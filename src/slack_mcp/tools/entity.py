from typing import Any

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def entity_present_details(
    trigger_id: str,
    metadata: dict[str, Any] | None = None,
    user_auth_required: bool | None = None,
    user_auth_url: str | None = None,
    error: dict[str, Any] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Present details about an entity in a flexpane.

    Args:
        trigger_id: Reference to the user action that initiated the request.
        metadata: Flexpane metadata keyed by entity ID, each describing the entity to present.
        user_auth_required: Whether the user must authenticate before details can be shown.
        user_auth_url: Custom URL where the user can authenticate.
        error: Error object with status and messaging details, if the entity can't be presented.
    """
    return await client.api_call(
        "entity.presentDetails",
        trigger_id=trigger_id,
        metadata=metadata,
        user_auth_required=user_auth_required,
        user_auth_url=user_auth_url,
        error=error,
    )
