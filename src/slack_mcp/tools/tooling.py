from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def tooling_tokens_rotate(
    refresh_token: str,
    client_id: str,
    client_secret: str,
    grant_type: str = "refresh_token",
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Rotate OAuth tokens.

    Args:
        refresh_token: The refresh token issued alongside the rotating access token to be exchanged for a new pair.
        client_id: Issued client ID for the app whose tokens are being rotated.
        client_secret: Issued client secret for the app whose tokens are being rotated.
        grant_type: OAuth grant type for the exchange; should be ``refresh_token``.
    """
    return await client.api_call(
        "tooling.tokens.rotate",
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        grant_type=grant_type,
    )
