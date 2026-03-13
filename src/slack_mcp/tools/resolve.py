import asyncio

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def resolve_names(
    user_ids: list[str] | None = None,
    channel_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Resolve user and channel IDs to display names in a single call.

    Accepts lists of user IDs (e.g. U12345) and/or channel IDs (e.g. C12345)
    and returns a mapping of each ID to its display name. Lookups run
    concurrently for performance.
    """
    user_ids = user_ids or []
    channel_ids = channel_ids or []

    async def _resolve_user(uid: str) -> tuple[str, str | None]:
        resp = await client.api_call("users.info", user=uid)
        if resp.get("ok"):
            user = resp.get("user", {})
            profile = user.get("profile", {})
            name = (
                profile.get("display_name")
                or profile.get("real_name")
                or user.get("real_name")
                or user.get("name")
            )
            return uid, name
        return uid, None

    async def _resolve_channel(cid: str) -> tuple[str, str | None]:
        resp = await client.api_call("conversations.info", channel=cid)
        if resp.get("ok"):
            channel_obj = resp.get("channel", {})
            name = channel_obj.get("name")
            return cid, name
        return cid, None

    tasks = [_resolve_user(uid) for uid in user_ids] + [
        _resolve_channel(cid) for cid in channel_ids
    ]
    results = await asyncio.gather(*tasks)
    return {"ok": True, "names": dict(results)}
