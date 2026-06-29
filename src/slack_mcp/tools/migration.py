from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import LONG_TTL, mcp, slack_client


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def migration_exchange(
    users: str,
    team_id: str | None = None,
    to_old: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Exchange a legacy ID for a new ID, or vice versa.

    Args:
        users: Comma-separated list of user IDs (up to 400) to translate (e.g. ``U0123,U0456``).
        team_id: Specify a team ID to scope the lookup, required for Enterprise Grid org tokens.
        to_old: Set to ``True`` to map global IDs back to their local (legacy) workspace IDs.
    """
    return await client.api_call(
        "migration.exchange", users=users, team_id=team_id, to_old=to_old
    )
