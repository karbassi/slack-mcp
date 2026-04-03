"""Tests for CompactResponseMiddleware."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from slack_mcp.compact import compactable


@pytest.fixture
def _clear_compactors():
    """Ensure test decorators don't leak into other tests."""
    from slack_mcp.compact import _COMPACTORS

    before = dict(_COMPACTORS)
    yield
    _COMPACTORS.clear()
    _COMPACTORS.update(before)


def _make_context(tool_name: str, arguments: dict | None = None):
    ctx = MagicMock()
    ctx.message.name = tool_name
    ctx.message.arguments = arguments or {}
    return ctx


def _make_result(structured_content: dict | None = None):
    result = MagicMock()
    result.structured_content = structured_content
    return result


class TestCompactResponseMiddleware:
    @pytest.mark.asyncio
    async def test_strips_compactable_tool(self, _clear_compactors):
        from slack_mcp.server import CompactResponseMiddleware

        spy = MagicMock()

        @compactable(spy)
        def my_tool():
            pass

        data = {"ok": True, "messages": []}
        result = _make_result(structured_content=data)
        call_next = AsyncMock(return_value=result)
        ctx = _make_context("my_tool")

        mw = CompactResponseMiddleware()
        out = await mw.on_call_tool(ctx, call_next)

        spy.assert_called_once_with(data)
        assert out is result

    @pytest.mark.asyncio
    async def test_passthrough_when_detailed_true(self, _clear_compactors):
        from slack_mcp.server import CompactResponseMiddleware

        spy = MagicMock()

        @compactable(spy)
        def my_tool2():
            pass

        result = _make_result(structured_content={"ok": True})
        call_next = AsyncMock(return_value=result)
        ctx = _make_context("my_tool2", {"detailed": True})

        mw = CompactResponseMiddleware()
        out = await mw.on_call_tool(ctx, call_next)

        spy.assert_not_called()
        assert out is result

    @pytest.mark.asyncio
    async def test_ignores_non_compactable_tool(self):
        from slack_mcp.server import CompactResponseMiddleware

        result = _make_result(structured_content={"ok": True})
        call_next = AsyncMock(return_value=result)
        ctx = _make_context("auth_test")

        mw = CompactResponseMiddleware()
        out = await mw.on_call_tool(ctx, call_next)

        assert out is result

    @pytest.mark.asyncio
    async def test_ignores_no_structured_content(self, _clear_compactors):
        from slack_mcp.server import CompactResponseMiddleware

        spy = MagicMock()

        @compactable(spy)
        def my_tool3():
            pass

        result = _make_result(structured_content=None)
        call_next = AsyncMock(return_value=result)
        ctx = _make_context("my_tool3")

        mw = CompactResponseMiddleware()
        out = await mw.on_call_tool(ctx, call_next)

        spy.assert_not_called()
        assert out is result

    @pytest.mark.asyncio
    async def test_strips_when_detailed_false(self, _clear_compactors):
        from slack_mcp.server import CompactResponseMiddleware

        spy = MagicMock()

        @compactable(spy)
        def my_tool4():
            pass

        data = {"ok": True}
        result = _make_result(structured_content=data)
        call_next = AsyncMock(return_value=result)
        ctx = _make_context("my_tool4", {"detailed": False})

        mw = CompactResponseMiddleware()
        await mw.on_call_tool(ctx, call_next)

        spy.assert_called_once_with(data)

    @pytest.mark.asyncio
    async def test_strips_when_detailed_absent(self, _clear_compactors):
        from slack_mcp.server import CompactResponseMiddleware

        spy = MagicMock()

        @compactable(spy)
        def my_tool5():
            pass

        data = {"ok": True}
        result = _make_result(structured_content=data)
        call_next = AsyncMock(return_value=result)
        ctx = _make_context("my_tool5", {"query": "test"})

        mw = CompactResponseMiddleware()
        await mw.on_call_tool(ctx, call_next)

        spy.assert_called_once_with(data)


def test_compact_middleware_before_name_resolution():
    """CompactResponseMiddleware must be registered before NameResolutionMiddleware.

    In FastMCP's onion model, earlier middleware is inner. On the return path
    (after call_next), inner middleware runs first. So registering Compact
    before NameResolution means: tool -> Compact (strips bloat) -> NameResolution
    (resolves fewer IDs).
    """
    from slack_mcp.server import (
        CompactResponseMiddleware,
        NameResolutionMiddleware,
        mcp,
    )

    compact_idx = None
    name_res_idx = None
    for i, m in enumerate(mcp.middleware):
        if isinstance(m, CompactResponseMiddleware):
            compact_idx = i
        if isinstance(m, NameResolutionMiddleware):
            name_res_idx = i

    assert compact_idx is not None, "CompactResponseMiddleware not registered"
    assert name_res_idx is not None, "NameResolutionMiddleware not registered"
    assert compact_idx < name_res_idx, (
        f"CompactResponseMiddleware (index {compact_idx}) must be registered "
        f"before NameResolutionMiddleware (index {name_res_idx}) "
        "so compaction runs first on the return path"
    )
