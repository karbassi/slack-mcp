from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def openid_connect_token(
    client_id: str,
    client_secret: str,
    code: str | None = None,
    grant_type: str | None = None,
    redirect_uri: str | None = None,
    refresh_token: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a temporary OAuth code for an access token for Sign in with Slack.

    Args:
        client_id: Issued client ID for your Slack app.
        client_secret: Issued client secret for your Slack app.
        code: The temporary authorization code returned via the OAuth redirect.
        grant_type: The grant type: ``authorization_code`` (default) or ``refresh_token``.
        redirect_uri: Redirect URI used in the initial authorization request; must match exactly.
        refresh_token: The refresh token, used when ``grant_type`` is ``refresh_token``.
    """
    return await client.api_call(
        "openid.connect.token",
        client_id=client_id,
        client_secret=client_secret,
        code=code,
        grant_type=grant_type,
        redirect_uri=redirect_uri,
        refresh_token=refresh_token,
    )


@mcp.tool
async def openid_connect_user_info(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get the identity of a user who authorized Sign in with Slack."""
    return await client.api_call("openid.connect.userInfo")
