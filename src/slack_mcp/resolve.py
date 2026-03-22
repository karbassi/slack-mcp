import asyncio
import re

from slack_sdk.errors import SlackApiError

from slack_mcp.client import SlackClient

MAX_CONCURRENCY = 10

_USER_MENTION_RE = re.compile(r"<@(U[A-Z0-9]+)")
_CHANNEL_MENTION_RE = re.compile(r"<#([CG][A-Z0-9]+)")

_NOT_FOUND_ERRORS = {
    "user_not_found",
    "user_not_visible",
    "channel_not_found",
    "bot_not_found",
}


async def _resolve_user(
    client: SlackClient, uid: str, sem: asyncio.Semaphore
) -> tuple[str, str | None]:
    async with sem:
        try:
            resp = await client.api_call("users.info", user=uid)
        except SlackApiError as e:
            if e.response.get("error") in _NOT_FOUND_ERRORS:
                return uid, None
            raise
        user = resp.get("user", {})
        profile = user.get("profile", {})
        name = (
            profile.get("display_name")
            or profile.get("real_name")
            or user.get("real_name")
            or user.get("name")
        )
        return uid, name


async def _resolve_channel(
    client: SlackClient, cid: str, sem: asyncio.Semaphore
) -> tuple[str, str | None]:
    async with sem:
        try:
            resp = await client.api_call("conversations.info", channel=cid)
        except SlackApiError as e:
            if e.response.get("error") in _NOT_FOUND_ERRORS:
                return cid, None
            raise
        return cid, resp.get("channel", {}).get("name")


async def _resolve_bot(
    client: SlackClient, bid: str, sem: asyncio.Semaphore
) -> tuple[str, str | None]:
    async with sem:
        try:
            resp = await client.api_call("bots.info", bot=bid)
        except SlackApiError as e:
            if e.response.get("error") in _NOT_FOUND_ERRORS:
                return bid, None
            raise
        return bid, resp.get("bot", {}).get("name")


def extract_ids_from_messages(
    messages: list[dict],
) -> tuple[set[str], set[str], set[str]]:
    """Extract unique user, channel, and bot IDs from a list of Slack messages."""
    user_ids: set[str] = set()
    channel_ids: set[str] = set()
    bot_ids: set[str] = set()

    for msg in messages:
        if (uid := msg.get("user")) and uid.startswith("U"):
            user_ids.add(uid)

        if (bid := msg.get("bot_id")) and bid.startswith("B"):
            bot_ids.add(bid)

        text = msg.get("text", "")
        user_ids.update(_USER_MENTION_RE.findall(text))
        channel_ids.update(_CHANNEL_MENTION_RE.findall(text))

    return user_ids, channel_ids, bot_ids


async def resolve_ids(
    client: SlackClient,
    user_ids: set[str],
    channel_ids: set[str],
    bot_ids: set[str],
) -> dict[str, str]:
    """Resolve all IDs concurrently. Returns {id: name} mapping, skipping failures."""
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    tasks = (
        [_resolve_user(client, uid, sem) for uid in user_ids]
        + [_resolve_channel(client, cid, sem) for cid in channel_ids]
        + [_resolve_bot(client, bid, sem) for bid in bot_ids]
    )
    if not tasks:
        return {}
    results = await asyncio.gather(*tasks)
    return {id_: name for id_, name in results if name is not None}
