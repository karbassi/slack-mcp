from __future__ import annotations

import time
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastmcp.server.middleware.middleware import MiddlewareContext
from fastmcp.tools.tool import ToolResult
from key_value.aio.stores.memory import MemoryStore
from mcp.types import CallToolRequestParams, TextContent

from slack_mcp.server import (
    LONG_TTL,
    SHORT_TTL,
    CachingMiddleware,
    ThreadCachingMiddleware,
    _make_cache_key,
    mcp,
)


def test_caching_middleware_attached():
    """CachingMiddleware is registered on the server."""
    assert any(isinstance(m, CachingMiddleware) for m in mcp.middleware)


@pytest.mark.asyncio
async def test_cache_ttl_meta_declared_at_tools():
    """Cache TTL is declared at the tool via meta={"cache_ttl": ...}. Spot-check
    a long- and short-cached tool, and assert every cache_ttl is a known value —
    catching a typo'd TTL or a tool that lost its meta in a rename.
    """
    users_info = await mcp.get_tool("users_info")
    assert (users_info.meta or {}).get("cache_ttl") == LONG_TTL

    permalink = await mcp.get_tool("chat_get_permalink")
    assert (permalink.meta or {}).get("cache_ttl") == SHORT_TTL

    for tool in await mcp.list_tools():
        ttl = (tool.meta or {}).get("cache_ttl")
        assert ttl in (None, LONG_TTL, SHORT_TTL), (
            f"{tool.name} has unexpected cache_ttl {ttl!r}"
        )


def _ctx_with_ttl(
    tool_name: str, cache_ttl: int | None, arguments: dict | None = None
) -> MiddlewareContext:
    """A context whose FastMCP resolves the tool to one carrying cache_ttl meta."""
    meta = {"cache_ttl": cache_ttl} if cache_ttl is not None else {}
    tool = SimpleNamespace(meta=meta, tags=set())
    fastmcp_context = SimpleNamespace(
        fastmcp=SimpleNamespace(get_tool=AsyncMock(return_value=tool))
    )
    return MiddlewareContext(
        message=CallToolRequestParams(name=tool_name, arguments=arguments),
        method="tools/call",
        fastmcp_context=fastmcp_context,
    )


@pytest.mark.asyncio
async def test_tool_with_cache_ttl_is_cached():
    """A tool whose meta declares a cache_ttl returns the cached result on the
    second call."""
    store = MemoryStore()
    middleware = CachingMiddleware(cache_storage=store)

    call_count = 0

    async def fake_call_next(context):  # noqa: ARG001
        nonlocal call_count
        call_count += 1
        return ToolResult(
            content=[TextContent(type="text", text='{"ok": true, "user": {}}')]
        )

    ctx = _ctx_with_ttl("users_info", SHORT_TTL, {"user": "U123"})

    result1 = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    result2 = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert result1.content[0].text == result2.content[0].text
    assert call_count == 1, "Second call should be served from cache"


@pytest.mark.asyncio
async def test_tool_without_cache_ttl_always_hits_api():
    """A tool whose meta has no cache_ttl always calls through."""
    store = MemoryStore()
    middleware = CachingMiddleware(cache_storage=store)

    call_count = 0

    async def fake_call_next(context):  # noqa: ARG001
        nonlocal call_count
        call_count += 1
        return ToolResult(content=[TextContent(type="text", text='{"ok": true}')])

    ctx = _ctx_with_ttl("chat_post_message", None, {"channel": "C123", "text": "hi"})

    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert call_count == 2, "Uncached tool should always call through"


def _make_context(tool_name: str, arguments: dict | None = None) -> MiddlewareContext:
    return MiddlewareContext(
        message=CallToolRequestParams(name=tool_name, arguments=arguments),
        method="tools/call",
    )


# --- ThreadCachingMiddleware tests ---

_FAKE_RESULT = ToolResult(
    content=[TextContent(type="text", text='{"ok": true, "messages": []}')]
)


@pytest.mark.asyncio
async def test_old_thread_is_cached():
    """conversations_replies with a ts older than 1 hour returns cached result."""
    store = MemoryStore()
    middleware = ThreadCachingMiddleware(cache_storage=store)

    call_count = 0
    old_ts = f"{time.time() - 7200:.6f}"  # 2 hours ago

    async def fake_call_next(context):  # noqa: ARG001
        nonlocal call_count
        call_count += 1
        return _FAKE_RESULT

    ctx = _make_context("conversations_replies", {"channel": "C123", "ts": old_ts})

    result1 = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    result2 = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert result1.content[0].text == result2.content[0].text
    assert call_count == 1, "Old thread should be cached after first call"


@pytest.mark.asyncio
async def test_recent_thread_is_not_cached():
    """conversations_replies with a recent ts always calls through."""
    store = MemoryStore()
    middleware = ThreadCachingMiddleware(cache_storage=store)

    call_count = 0
    recent_ts = f"{time.time() - 300:.6f}"  # 5 minutes ago

    async def fake_call_next(context):  # noqa: ARG001
        nonlocal call_count
        call_count += 1
        return _FAKE_RESULT

    ctx = _make_context("conversations_replies", {"channel": "C123", "ts": recent_ts})

    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert call_count == 2, "Recent thread should not be cached"


@pytest.mark.asyncio
async def test_old_history_range_is_cached():
    """conversations_history with old oldest+latest bounds is cached."""
    store = MemoryStore()
    middleware = ThreadCachingMiddleware(cache_storage=store)

    call_count = 0
    old_oldest = f"{time.time() - 14400:.6f}"  # 4 hours ago
    old_latest = f"{time.time() - 7200:.6f}"  # 2 hours ago

    async def fake_call_next(context):  # noqa: ARG001
        nonlocal call_count
        call_count += 1
        return _FAKE_RESULT

    ctx = _make_context(
        "conversations_history",
        {"channel": "C123", "oldest": old_oldest, "latest": old_latest},
    )

    result1 = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    result2 = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert result1.content[0].text == result2.content[0].text
    assert call_count == 1, "Old bounded history range should be cached"


@pytest.mark.asyncio
async def test_recent_history_is_not_cached():
    """conversations_history without bounds or with recent bounds is not cached."""
    store = MemoryStore()
    middleware = ThreadCachingMiddleware(cache_storage=store)

    call_count = 0

    async def fake_call_next(context):  # noqa: ARG001
        nonlocal call_count
        call_count += 1
        return _FAKE_RESULT

    # No oldest/latest — fetching latest messages
    ctx = _make_context("conversations_history", {"channel": "C123"})

    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert call_count == 2, "Unbounded history should not be cached"


@pytest.mark.asyncio
async def test_cache_clear_tool():
    """Clearing the store invalidates cached thread data."""
    store = MemoryStore()
    middleware = ThreadCachingMiddleware(cache_storage=store)

    call_count = 0
    old_ts = f"{time.time() - 7200:.6f}"

    async def fake_call_next(context):  # noqa: ARG001
        nonlocal call_count
        call_count += 1
        return _FAKE_RESULT

    ctx = _make_context("conversations_replies", {"channel": "C123", "ts": old_ts})

    # Populate cache
    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    assert call_count == 1

    # Clear the store (simulates what cache_clear does with DiskStore._cache.clear())
    # MemoryStore needs both _cache and setup tracking cleared
    store._cache.clear()
    store._setup_collection_complete.clear()

    # Next call should go through to the API again
    await middleware.on_call_tool(context=ctx, call_next=fake_call_next)
    assert call_count == 2, "Cache should be empty after clearing"


def test_detailed_true_produces_different_cache_key():
    """detailed=True must produce a different cache key since the cached
    response is post-compaction — detailed=True skips compaction and must
    not share a cache entry with the compacted default."""
    args_without = {"channel": "C123", "ts": "1234.5678"}
    args_with_false = {"channel": "C123", "ts": "1234.5678", "detailed": False}
    args_with_true = {"channel": "C123", "ts": "1234.5678", "detailed": True}

    key_base = _make_cache_key("conversations_replies", args_without)
    key_false = _make_cache_key("conversations_replies", args_with_false)
    key_true = _make_cache_key("conversations_replies", args_with_true)

    assert key_base == key_false, (
        f"detailed=False should match absent (both get compacted): "
        f"{key_base!r} != {key_false!r}"
    )
    assert key_base != key_true, (
        f"detailed=True must differ from default (different response): "
        f"{key_base!r} == {key_true!r}"
    )
