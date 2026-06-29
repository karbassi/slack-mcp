from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def oauth_access(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str | None = None,
    single_channel: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a temporary OAuth verifier code for an access token (V1)."""
    return await client.api_call(
        "oauth.access",
        client_id=client_id,
        client_secret=client_secret,
        code=code,
        redirect_uri=redirect_uri,
        single_channel=single_channel,
    )


@mcp.tool
async def oauth_v2_access(
    client_id: str,
    client_secret: str,
    code: str,
    grant_type: str | None = None,
    redirect_uri: str | None = None,
    refresh_token: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a temporary OAuth verifier code for an access token (V2)."""
    return await client.api_call(
        "oauth.v2.access",
        client_id=client_id,
        client_secret=client_secret,
        code=code,
        grant_type=grant_type,
        redirect_uri=redirect_uri,
        refresh_token=refresh_token,
    )


@mcp.tool
async def oauth_v2_user_access(
    client_id: str,
    client_secret: str,
    code: str,
    code_verifier: str | None = None,
    grant_type: str | None = None,
    redirect_uri: str | None = None,
    refresh_token: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a temporary OAuth verifier code for a user access token (V2).

    Args:
        client_id: Your app's client ID.
        client_secret: Your app's client secret.
        code: The OAuth callback code (omit when refreshing).
        code_verifier: PKCE verifier matching the original challenge.
        grant_type: ``authorization_code`` (default) or ``refresh_token``.
        redirect_uri: Must match the value used to request the code.
        refresh_token: The refresh token, when ``grant_type=refresh_token``.
    """
    return await client.api_call(
        "oauth.v2.user.access",
        client_id=client_id,
        client_secret=client_secret,
        code=code,
        code_verifier=code_verifier,
        grant_type=grant_type,
        redirect_uri=redirect_uri,
        refresh_token=refresh_token,
    )


@mcp.tool
async def oauth_v2_exchange(
    client_id: str,
    client_secret: str,
    token: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a legacy access token for a new expiring access token."""
    return await client.api_call(
        "oauth.v2.exchange",
        client_id=client_id,
        client_secret=client_secret,
        token=token,
    )
