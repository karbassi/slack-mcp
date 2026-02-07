from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def migration_exchange(
    users: str,
    team_id: str | None = None,
    to_old: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a legacy ID for a new ID, or vice versa."""
    kwargs = {"users": users}
    if team_id is not None:
        kwargs["team_id"] = team_id
    if to_old is not None:
        kwargs["to_old"] = to_old
    return await client.api_call("migration.exchange", **kwargs)
