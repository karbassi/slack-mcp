from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def entity_present_details(
    app_id: str,
    entity_id: str,
    entity_type: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Present details about an entity."""
    return await client.api_call(
        "entity.presentDetails",
        app_id=app_id,
        entity_id=entity_id,
        entity_type=entity_type,
    )
