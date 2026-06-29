from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def tooling_tokens_rotate(
    refresh_token: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Rotate app configuration tokens.

    Args:
        refresh_token: The ``xoxe`` refresh token issued alongside the old app configuration token.
    """
    return await client.api_call(
        "tooling.tokens.rotate", refresh_token=refresh_token
    )
