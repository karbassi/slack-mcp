from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def auth_revoke(
    test: Optional[bool] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Revoke a token."""
    kwargs = {}
    if test is not None:
        kwargs["test"] = test
    return await client.api_call("auth.revoke", **kwargs)


@mcp.tool
async def auth_teams_list(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    include_icon: Optional[bool] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List the workspaces a token can access."""
    kwargs = {}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    if include_icon is not None:
        kwargs["include_icon"] = include_icon
    return await client.api_call("auth.teams.list", **kwargs)


@mcp.tool
async def auth_test(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Check authentication and get identity."""
    return await client.api_call("auth.test")
