from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def blocks_validate(
    blocks: list[dict],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Validate an array of Block Kit blocks.

    Args:
        blocks: The Block Kit blocks to validate.
    """
    return await client.api_call("blocks.validate", blocks=blocks)
