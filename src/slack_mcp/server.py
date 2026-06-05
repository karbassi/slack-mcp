from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import hashlib
import os
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import version
from typing import Any

import pydantic_core
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.server.middleware.caching import CachableToolResult
from fastmcp.server.middleware.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools.tool import ToolResult
from key_value.aio.stores.disk import DiskStore
from mcp.types import CallToolRequestParams
from slack_sdk.errors import SlackApiError

from slack_mcp.client import SlackClient, get_client


@asynccontextmanager
async def _lifespan(_server: FastMCP) -> AsyncIterator[dict]:
    yield {}
    client = get_client()
    await client.close()


mcp = FastMCP(name="Slack MCP", version=version("slack-mcp"), lifespan=_lifespan)

# Cache TTLs (seconds). Per-tool TTL is declared at the tool via
# meta={"cache_ttl": LONG_TTL} and read by CachingMiddleware at call time.
LONG_TTL = 3600  # stable identity data — rarely changes
SHORT_TTL = 300  # more dynamic data — can change within minutes

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

ONE_HOUR = 3600
THREAD_CACHE_COLLECTION = "thread_cache"
RESPONSE_CACHE_COLLECTION = "response_cache"


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
    key_parts.extend(
        f"{ts_field}={args[ts_field]}"
        for ts_field in ("ts", "oldest", "latest")
        if ts_field in args
    )
    filtered = {
        k: v
        for k, v in args.items()
        if k not in ("channel", "ts", "oldest", "latest")
    }
    # Strip detailed=False (same as absent — both get compacted)
    if not filtered.get("detailed"):
        filtered.pop("detailed", None)
    other = dict(sorted(filtered.items()))
    if other:
        key_parts.append(pydantic_core.to_json(other, fallback=str).decode())
    return ":".join(key_parts)


async def _lookup_tool(context: MiddlewareContext[CallToolRequestParams]) -> Any | None:
    """Resolve the registered tool for this call so middleware can read its
    meta/tags, or None when unavailable (outside a server request, or unknown
    tool). One home for the FastMCP introspection guard."""
    fastmcp_context = getattr(context, "fastmcp_context", None)
    if fastmcp_context is None:
        return None
    try:
        return await fastmcp_context.fastmcp.get_tool(context.message.name)
    except Exception:
        return None


async def _cache_ttl(
    context: MiddlewareContext[CallToolRequestParams],
) -> int | None:
    """Per-tool cache TTL, declared at the tool via meta={"cache_ttl": <seconds>}
    and read here at call time. None means the tool isn't cached."""
    tool = await _lookup_tool(context)
    if tool is None:
        return None
    ttl = (tool.meta or {}).get("cache_ttl")
    return ttl if isinstance(ttl, int) else None


class CachingMiddleware(Middleware):
    """Cache read-only tool responses keyed by args, with a per-tool TTL declared
    in the tool's meta. The cached value is the fully-processed response (after
    name resolution and compaction), since those middlewares run inside this one.
    Only SlackErrorMiddleware sits outside it, re-flagging is_error on each call
    (including cache hits) because the cache wrapper drops that flag."""

    def __init__(self, cache_storage: Any) -> None:
        self._store = cache_storage
        super().__init__()

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        ttl = await _cache_ttl(context)
        if ttl is None:
            return await call_next(context)

        args = context.message.arguments or {}
        cache_key = _make_cache_key(context.message.name, args)

        cached = await self._store.get(
            key=cache_key, collection=RESPONSE_CACHE_COLLECTION
        )
        if cached is not None:
            return CachableToolResult.model_validate(cached).unwrap()

        result: ToolResult = await call_next(context)
        cachable = CachableToolResult.wrap(result)
        await self._store.put(
            key=cache_key,
            value=cachable.model_dump(mode="json"),
            collection=RESPONSE_CACHE_COLLECTION,
            ttl=ttl,
        )
        return result


class SlackErrorMiddleware(Middleware):
    """Flag Slack ``ok: false`` responses as MCP tool errors.

    Slack's session/undocumented endpoints return ``{"ok": false, ...}`` with
    HTTP 200, so FastMCP would otherwise report them as successful calls. We set
    ``is_error = True`` for those responses on every call — registered outermost
    so the flag is re-applied on cache hits (the cache wrapper drops it)."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        result = await call_next(context)
        content = result.structured_content
        if isinstance(content, dict) and content.get("ok") is False:
            result.is_error = True
        return result


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


# SlackErrorMiddleware is outermost (registered first) so it re-flags
# ok:false errors after every call, including cache hits — the cache wrapper
# drops is_error on the round-trip, so we re-apply the flag here. Setting it is
# idempotent, so cache hits stay correct.
# CachingMiddleware is next so a hit short-circuits resolution and compaction;
# the thread cache handles the old-message special case.
mcp.add_middleware(SlackErrorMiddleware())
mcp.add_middleware(CachingMiddleware(cache_storage=cache_store))
mcp.add_middleware(ThreadCachingMiddleware(cache_storage=cache_store))


async def _skips_resolution(context: MiddlewareContext[CallToolRequestParams]) -> bool:
    """A tool opts out of name resolution with the "skip-resolution" tag —
    declared at the tool, read here at call time."""
    tool = await _lookup_tool(context)
    return tool is not None and "skip-resolution" in (tool.tags or set())


class NameResolutionMiddleware(Middleware):
    """Auto-resolve user/channel/bot IDs in any tool response."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        result = await call_next(context)

        if await _skips_resolution(context):
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


class CompactResponseMiddleware(Middleware):
    """Strip bloat from Slack API responses for tools marked with @compactable."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        result = await call_next(context)

        from slack_mcp.compact import get_compactor

        compactor = get_compactor(context.message.name)
        if compactor is None:
            return result

        args = context.message.arguments or {}
        if args.get("detailed") is True:
            return result

        content = result.structured_content
        if content is not None and isinstance(content, dict):
            compactor(content)

        return result


mcp.add_middleware(NameResolutionMiddleware())

mcp.add_middleware(CompactResponseMiddleware())


@mcp.tool(tags={"skip-resolution"})
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
