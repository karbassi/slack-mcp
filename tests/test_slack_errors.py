from __future__ import annotations

import json

import pytest
from fastmcp.server.middleware.middleware import MiddlewareContext
from fastmcp.tools.tool import ToolResult
from mcp.types import CallToolRequestParams, TextContent

from slack_mcp.server import CachingMiddleware, SlackErrorMiddleware, mcp


def _make_context(tool_name: str) -> MiddlewareContext:
    return MiddlewareContext(
        message=CallToolRequestParams(name=tool_name, arguments={}),
        method="tools/call",
    )


def _make_result(data: dict) -> ToolResult:
    return ToolResult(
        content=[TextContent(type="text", text=json.dumps(data))],
        structured_content=data,
    )


def test_slack_error_middleware_attached():
    """SlackErrorMiddleware is registered on the server."""
    assert any(isinstance(m, SlackErrorMiddleware) for m in mcp.middleware)


def test_slack_error_middleware_outermost():
    """SlackErrorMiddleware must precede CachingMiddleware so it re-flags
    is_error on cache hits (the cache wrapper drops the flag)."""
    error_idx = next(
        i for i, m in enumerate(mcp.middleware)
        if isinstance(m, SlackErrorMiddleware)
    )
    caching_idx = next(
        i for i, m in enumerate(mcp.middleware)
        if isinstance(m, CachingMiddleware)
    )
    assert error_idx < caching_idx


@pytest.mark.asyncio
async def test_ok_false_sets_is_error():
    """A tool result with ok:false gets is_error=True."""
    middleware = SlackErrorMiddleware()
    data = {"ok": False, "error": "channel_not_found"}

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context("conversations_info")
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert result.is_error is True


@pytest.mark.asyncio
async def test_ok_true_leaves_is_error_false():
    """A tool result with ok:true leaves is_error unset (falsy)."""
    middleware = SlackErrorMiddleware()
    data = {"ok": True, "channel": {"id": "C123", "name": "general"}}

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context("conversations_info")
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert not result.is_error


@pytest.mark.asyncio
async def test_non_dict_content_leaves_is_error_false():
    """A result whose structured_content is not a dict is left unchanged."""
    middleware = SlackErrorMiddleware()

    async def fake_call_next(_ctx):
        return ToolResult(
            content=[TextContent(type="text", text="plain string")],
            structured_content=None,
        )

    ctx = _make_context("cache_clear")
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert not result.is_error


@pytest.mark.asyncio
async def test_dict_without_ok_key_leaves_is_error_false():
    """A dict response with no 'ok' key is left unchanged."""
    middleware = SlackErrorMiddleware()
    data = {"some_key": "some_value"}

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context("any_tool")
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert not result.is_error
