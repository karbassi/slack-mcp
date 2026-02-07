from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def oauth_access(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: Optional[str] = None,
    single_channel: Optional[bool] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a temporary OAuth verifier code for an access token (V1)."""
    kwargs = {"client_id": client_id, "client_secret": client_secret, "code": code}
    if redirect_uri is not None:
        kwargs["redirect_uri"] = redirect_uri
    if single_channel is not None:
        kwargs["single_channel"] = single_channel
    return await client.api_call("oauth.access", **kwargs)


@mcp.tool
async def oauth_v2_access(
    client_id: str,
    client_secret: str,
    code: str,
    grant_type: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    refresh_token: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a temporary OAuth verifier code for an access token (V2)."""
    kwargs = {"client_id": client_id, "client_secret": client_secret, "code": code}
    if grant_type is not None:
        kwargs["grant_type"] = grant_type
    if redirect_uri is not None:
        kwargs["redirect_uri"] = redirect_uri
    if refresh_token is not None:
        kwargs["refresh_token"] = refresh_token
    return await client.api_call("oauth.v2.access", **kwargs)


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
