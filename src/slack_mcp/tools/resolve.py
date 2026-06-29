from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.resolve import resolve_ids
from slack_mcp.server import LONG_TTL, mcp, slack_client


@mcp.tool(meta={"cache_ttl": LONG_TTL}, tags={"skip-resolution"})
async def resolve_names(
    user_ids: list[str] | None = None,
    channel_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Resolve user and channel IDs to display names in a single call.

    Accepts lists of user IDs (e.g. U12345) and/or channel IDs (e.g. C12345)
    and returns a mapping of each ID to its display name. Lookups run
    concurrently for performance.

    Args:
        user_ids: User IDs to resolve to display names (e.g. ``["U0123"]``).
        channel_ids: Channel IDs to resolve to display names (e.g. ``["C0123"]``).
    """
    names = await resolve_ids(
        client,
        user_ids=set(user_ids or []),
        channel_ids=set(channel_ids or []),
        bot_ids=set(),
    )
    return {"ok": True, "names": names}
