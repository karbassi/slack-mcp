from importlib.metadata import version

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import LONG_TTL, mcp, slack_client


@mcp.tool
async def auth_revoke(
    test: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Revoke a token."""
    return await client.api_call("auth.revoke", test=test)


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def auth_teams_list(
    cursor: str | None = None,
    limit: int | None = None,
    include_icon: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List the workspaces a token can access."""
    return await client.api_call(
        "auth.teams.list", cursor=cursor, limit=limit, include_icon=include_icon
    )


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def auth_test(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Check authentication and get identity."""
    result = await client.api_call("auth.test")
    result["_slack_mcp_version"] = version("slack-mcp")
    return result
