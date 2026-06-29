from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def entity_present_details(
    app_id: str,
    entity_id: str,
    entity_type: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Present details about an entity.

    Args:
        app_id: ID of the app presenting the entity (e.g. ``A0123``).
        entity_id: Identifier of the entity to present, as understood by the app.
        entity_type: Type of the entity being presented (e.g. ``slack#/entities/file``).
    """
    return await client.api_call(
        "entity.presentDetails",
        app_id=app_id,
        entity_id=entity_id,
        entity_type=entity_type,
    )
