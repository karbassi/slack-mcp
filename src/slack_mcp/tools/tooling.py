from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def tooling_tokens_rotate(
    refresh_token: str,
    client_id: str,
    client_secret: str,
    grant_type: str = "refresh_token",
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Rotate OAuth tokens."""
    return await client.api_call(
        "tooling.tokens.rotate",
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        grant_type=grant_type,
    )
