from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def openid_connect_token(
    client_id: str,
    client_secret: str,
    code: Optional[str] = None,
    grant_type: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    refresh_token: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a temporary OAuth verifier code for an access token for Sign in with Slack."""
    kwargs = {"client_id": client_id, "client_secret": client_secret}
    if code is not None:
        kwargs["code"] = code
    if grant_type is not None:
        kwargs["grant_type"] = grant_type
    if redirect_uri is not None:
        kwargs["redirect_uri"] = redirect_uri
    if refresh_token is not None:
        kwargs["refresh_token"] = refresh_token
    return await client.api_call("openid.connect.token", **kwargs)


@mcp.tool
async def openid_connect_user_info(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get the identity of a user who authorized Sign in with Slack."""
    return await client.api_call("openid.connect.userInfo")
