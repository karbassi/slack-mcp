from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import hashlib
import os
import time
from importlib.metadata import version
from typing import Any

import pydantic_core
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.server.middleware.caching import (
    CachableToolResult,
    CallToolSettings,
    ResponseCachingMiddleware,
)
from fastmcp.server.middleware.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools.tool import ToolResult
from key_value.aio.stores.disk import DiskStore
from mcp.types import CallToolRequestParams
from slack_sdk.errors import SlackApiError

from slack_mcp.client import SlackClient, get_client

mcp = FastMCP(name="Slack MCP", version=version("slack-mcp"))

# Stable identity data — rarely changes (1 hour)
LONG_CACHED_TOOLS = [
    # Identity / Team
    "auth_test",
    "auth_teams_list",
    "team_info",
    "team_profile_get",
    "team_preferences_list",
    "team_prefs_get",
    "users_prefs_get",
    "emoji_list",
    "commands_list",
    "migration_exchange",
    # Bulk resolution (names are stable identity data)
    "resolve_names",
    # Users
    "users_info",
    "users_list",
    "users_lookup_by_email",
    "users_profile_get",
    "users_identity",
    # Bots
    "bots_info",
    "bots_list",
]

# More dynamic data — can change within minutes (5 minutes)
SHORT_CACHED_TOOLS = [
    "users_conversations",
    # Channels / Groups
    "conversations_info",
    "conversations_list",
    "conversations_members",
    "usergroups_list",
    "usergroups_users_list",
    # Other reads
    "bookmarks_list",
    "files_info",
    "team_external_teams_list",
    "chat_get_permalink",
]

CACHED_TOOLS = LONG_CACHED_TOOLS + SHORT_CACHED_TOOLS

from platformdirs import user_cache_dir

# Namespace cache by token so multiple workspaces don't collide
_xdg = os.environ.get("XDG_CACHE_HOME")
_base = Path(_xdg) / "slack-mcp" if _xdg else Path(user_cache_dir("slack-mcp"))
_token = os.environ.get("SLACK_XOXP_TOKEN", "")
_ns = hashlib.sha256(_token.encode()).hexdigest()[:12]
cache_dir = _base / _ns
cache_store = DiskStore(directory=cache_dir)

from slack_mcp.resolve import set_cache_store

set_cache_store(cache_store)

mcp.add_middleware(
    ResponseCachingMiddleware(
        cache_storage=cache_store,
        call_tool_settings=CallToolSettings(
            ttl=3600,
            included_tools=LONG_CACHED_TOOLS,
        ),
    )
)
mcp.add_middleware(
    ResponseCachingMiddleware(
        cache_storage=cache_store,
        call_tool_settings=CallToolSettings(
            ttl=300,
            included_tools=SHORT_CACHED_TOOLS,
        ),
    )
)

ONE_HOUR = 3600
THREAD_CACHE_COLLECTION = "thread_cache"


def _is_old_timestamp(ts: str) -> bool:
    """Check if a Slack timestamp is older than 1 hour."""
    try:
        epoch = float(ts.split(".")[0])
        return (time.time() - epoch) > ONE_HOUR
    except (ValueError, IndexError):
        return False


def _make_cache_key(tool_name: str, args: dict[str, Any]) -> str:
    """Build a deterministic cache key from tool name and arguments."""
    channel = args.get("channel", "")
    key_parts = [tool_name, channel]
    for ts_field in ("ts", "oldest", "latest"):
        if ts_field in args:
            key_parts.append(f"{ts_field}={args[ts_field]}")
    other = {
        k: v
        for k, v in sorted(args.items())
        if k not in ("channel", "ts", "oldest", "latest")
    }
    if other:
        key_parts.append(pydantic_core.to_json(other, fallback=str).decode())
    return ":".join(key_parts)


class ThreadCachingMiddleware(Middleware):
    """Cache conversations_replies and bounded conversations_history for old threads."""

    def __init__(self, cache_storage: Any) -> None:
        self._store = cache_storage
        super().__init__()

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        tool_name = context.message.name
        args = context.message.arguments or {}

        if tool_name == "conversations_replies":
            ts = args.get("ts")
            if ts and _is_old_timestamp(ts):
                return await self._cached_call(tool_name, args, context, call_next)

        elif tool_name == "conversations_history":
            oldest = args.get("oldest")
            latest = args.get("latest")
            if oldest and latest and _is_old_timestamp(latest):
                return await self._cached_call(tool_name, args, context, call_next)

        return await call_next(context)

    async def _cached_call(
        self,
        tool_name: str,
        args: dict[str, Any],
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        cache_key = _make_cache_key(tool_name, args)

        cached = await self._store.get(
            key=cache_key, collection=THREAD_CACHE_COLLECTION
        )
        if cached is not None:
            return CachableToolResult.model_validate(cached).unwrap()

        result: ToolResult = await call_next(context)
        cachable = CachableToolResult.wrap(result)
        await self._store.put(
            key=cache_key,
            value=cachable.model_dump(mode="json"),
            collection=THREAD_CACHE_COLLECTION,
            ttl=ONE_HOUR,
        )
        return result


mcp.add_middleware(ThreadCachingMiddleware(cache_storage=cache_store))

# Tools that never return IDs — skip resolution to avoid overhead
_SKIP_RESOLUTION = {
    "api_test",
    "cache_clear",
    "resolve_names",
}


class NameResolutionMiddleware(Middleware):
    """Auto-resolve user/channel/bot IDs in any tool response."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        result = await call_next(context)

        if context.message.name in _SKIP_RESOLUTION:
            return result

        if not result.structured_content:
            return result

        from slack_mcp.resolve import extract_ids_from_json, resolve_ids

        user_ids, channel_ids, bot_ids = extract_ids_from_json(
            result.structured_content
        )
        if not user_ids and not channel_ids and not bot_ids:
            return result

        try:
            client = get_client()
            names = await resolve_ids(client, user_ids, channel_ids, bot_ids)
        except (SlackApiError, OSError, TimeoutError):
            return result

        if names:
            result.structured_content["resolved_names"] = names

        return result


mcp.add_middleware(NameResolutionMiddleware())


@mcp.tool
def cache_clear() -> str:
    """Clear the Slack MCP cache so subsequent calls fetch fresh data from the API."""
    count = cache_store._cache.clear()
    return f"Cache cleared ({count} entries removed)."


def slack_client() -> SlackClient:
    return get_client()


# Import all tool modules so @mcp.tool decorators register the tools
import slack_mcp.tools.api
import slack_mcp.tools.apps
import slack_mcp.tools.assistant
import slack_mcp.tools.auth
import slack_mcp.tools.bookmarks
import slack_mcp.tools.bots
import slack_mcp.tools.calls
import slack_mcp.tools.canvases
import slack_mcp.tools.chat
import slack_mcp.tools.conversations
import slack_mcp.tools.dialog
import slack_mcp.tools.dnd
import slack_mcp.tools.emoji
import slack_mcp.tools.entity
import slack_mcp.tools.files
import slack_mcp.tools.functions
import slack_mcp.tools.legacy
import slack_mcp.tools.migration
import slack_mcp.tools.oauth
import slack_mcp.tools.openid
import slack_mcp.tools.pins
import slack_mcp.tools.reactions
import slack_mcp.tools.reminders
import slack_mcp.tools.resolve
import slack_mcp.tools.rtm
import slack_mcp.tools.search
import slack_mcp.tools.slack_lists
import slack_mcp.tools.stars
import slack_mcp.tools.team
import slack_mcp.tools.tooling
import slack_mcp.tools.undocumented
import slack_mcp.tools.usergroups
import slack_mcp.tools.users
import slack_mcp.tools.views
import slack_mcp.tools.workflows

if __name__ == "__main__":
    mcp.run()
