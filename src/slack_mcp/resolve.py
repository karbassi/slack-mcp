import asyncio
import re

from slack_sdk.errors import SlackApiError

from slack_mcp.client import SlackClient

MAX_CONCURRENCY = 10

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



# Slack ID prefixes we can resolve:
#   U/W = user, C/G/D/Z = channel/DM, B = bot
# IDs are prefix + 8+ uppercase alphanumeric chars
_ID_RE = re.compile(r"\b([UW][A-Z0-9]{8,}|[CGDZ][A-Z0-9]{8,}|B[A-Z0-9]{8,})\b")

# Keys whose values look like IDs but aren't resolvable
_SKIP_KEYS = {
    "client_msg_id",
    "team_id",
    "team",
    "enterprise_id",
    "app_id",
    "api_app_id",
}


def extract_ids_from_json(data: object) -> tuple[set[str], set[str], set[str]]:
    """Scan any JSON structure for Slack IDs (users, channels, bots)."""
    user_ids: set[str] = set()
    channel_ids: set[str] = set()
    bot_ids: set[str] = set()

    def _scan(obj: object, key: str | None = None) -> None:
        if isinstance(obj, str):
            if key in _SKIP_KEYS:
                return
            for match in _ID_RE.findall(obj):
                c = match[0]
                if c in ("U", "W"):
                    user_ids.add(match)
                elif c in ("C", "G"):
                    channel_ids.add(match)
                elif c == "B":
                    bot_ids.add(match)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                _scan(v, k)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item, key)

    _scan(data)
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
