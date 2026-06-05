from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastmcp.server.middleware.middleware import MiddlewareContext
from fastmcp.tools.tool import ToolResult
from mcp.types import CallToolRequestParams, TextContent

from slack_mcp.server import NameResolutionMiddleware, _lookup_tool


def _make_context(tool_name: str, arguments: dict | None = None) -> MiddlewareContext:
    return MiddlewareContext(
        message=CallToolRequestParams(name=tool_name, arguments=arguments),
        method="tools/call",
    )


def _make_context_with_tags(tool_name: str, tags: set[str]) -> MiddlewareContext:
    """A context whose FastMCP can resolve the tool to one carrying ``tags``."""
    tool = SimpleNamespace(tags=tags)
    fastmcp_context = SimpleNamespace(
        fastmcp=SimpleNamespace(get_tool=AsyncMock(return_value=tool))
    )
    return MiddlewareContext(
        message=CallToolRequestParams(name=tool_name, arguments={}),
        method="tools/call",
        fastmcp_context=fastmcp_context,
    )


def _make_result(data: dict) -> ToolResult:
    return ToolResult(
        content=[TextContent(type="text", text=json.dumps(data))],
        structured_content=data,
    )


def _mock_client(side_effect):
    client = AsyncMock()
    client.api_call.side_effect = side_effect
    return client


def _api_side_effect(method, **kwargs):
    if method == "users.info":
        uid = kwargs["user"]
        return {
            "ok": True,
            "user": {
                "id": uid,
                "name": "alice",
                "profile": {"display_name": "Alice", "real_name": "Alice Smith"},
            },
        }
    if method == "conversations.info":
        cid = kwargs["channel"]
        return {"ok": True, "channel": {"id": cid, "name": "general"}}
    if method == "bots.info":
        bid = kwargs["bot"]
        return {"ok": True, "bot": {"id": bid, "name": "Testbot"}}
    return {"ok": False}


@pytest.mark.asyncio
async def test_enriches_conversations_history():
    middleware = NameResolutionMiddleware()
    data = {
        "ok": True,
        "messages": [
            {
                "user": "U0ADCDDNVGT",
                "text": "Hello <@U0BXYZ12345> check <#C0AD56E4N6B>",
            },
            {"bot_id": "BA13894H00", "text": "Bot message"},
        ],
    }

    async def fake_call_next(_ctx):
        return _make_result(data)

    client = _mock_client(_api_side_effect)
    ctx = _make_context("conversations_history", {"channel": "C000"})

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    names = result.structured_content["resolved_names"]
    assert names["U0ADCDDNVGT"] == "Alice"
    assert names["U0BXYZ12345"] == "Alice"
    assert names["C0AD56E4N6B"] == "general"
    assert names["BA13894H00"] == "Testbot"


@pytest.mark.asyncio
async def test_enriches_search_messages():
    middleware = NameResolutionMiddleware()
    data = {
        "ok": True,
        "messages": {
            "matches": [{"user": "U0ADCDDNVGT", "text": "found it"}],
        },
    }

    async def fake_call_next(_ctx):
        return _make_result(data)

    client = _mock_client(_api_side_effect)
    ctx = _make_context("search_messages", {"query": "test"})

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert result.structured_content["resolved_names"]["U0ADCDDNVGT"] == "Alice"


@pytest.mark.asyncio
async def test_non_target_tool_passes_through():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "channels": []}

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context("conversations_list")
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert "resolved_names" not in result.structured_content


@pytest.mark.asyncio
async def test_empty_messages_no_enrichment():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": []}

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context("conversations_history", {"channel": "C000"})
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert "resolved_names" not in result.structured_content


@pytest.mark.asyncio
async def test_no_ids_in_messages_no_enrichment():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"text": "plain text, no IDs"}]}

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context("conversations_history", {"channel": "C000"})
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert "resolved_names" not in result.structured_content


@pytest.mark.asyncio
async def test_failed_lookups_excluded():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"user": "UBAD00000X", "text": "hi"}]}

    from slack_sdk.errors import SlackApiError
    from slack_sdk.web.async_slack_response import AsyncSlackResponse

    async def failing_api(_method, **_kwargs):
        raise SlackApiError(
            message="user_not_found",
            response=AsyncSlackResponse(
                client=None,
                http_verb="POST",
                api_url="https://slack.com/api/users.info",
                req_args={},
                data={"ok": False, "error": "user_not_found"},
                headers={},
                status_code=200,
            ),
        )

    client = _mock_client(failing_api)
    ctx = _make_context("conversations_history", {"channel": "C000"})

    async def fake_call_next(_ctx):
        return _make_result(data)

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert "resolved_names" not in result.structured_content


@pytest.mark.asyncio
async def test_resolution_error_returns_original_result():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"user": "U0ADCDDNVGT", "text": "hi"}]}

    from slack_sdk.errors import SlackApiError
    from slack_sdk.web.async_slack_response import AsyncSlackResponse

    async def auth_error(_method, **_kwargs):
        raise SlackApiError(
            message="invalid_auth",
            response=AsyncSlackResponse(
                client=None,
                http_verb="POST",
                api_url="https://slack.com/api/users.info",
                req_args={},
                data={"ok": False, "error": "invalid_auth"},
                headers={},
                status_code=200,
            ),
        )

    client = _mock_client(auth_error)
    ctx = _make_context("conversations_history", {"channel": "C000"})

    async def fake_call_next(_ctx):
        return _make_result(data)

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert "resolved_names" not in result.structured_content


@pytest.mark.asyncio
async def test_skip_resolution_tag_bypasses_enrichment():
    """A tool tagged 'skip-resolution' returns unmodified even if its response
    contains IDs (e.g. resolve_names, whose output is already resolved)."""
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "U0ADCDDNVGT": "Alice"}  # ids present in the payload

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context_with_tags("resolve_names", {"skip-resolution"})

    # get_client is not patched: if resolution ran it would error out, but the
    # tag must short-circuit before any client call.
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert "resolved_names" not in result.structured_content


@pytest.mark.asyncio
async def test_untagged_tool_still_resolves():
    """A tool without the tag (via the tag-aware context) still enriches."""
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"user": "U0ADCDDNVGT", "text": "hi"}]}

    async def fake_call_next(_ctx):
        return _make_result(data)

    ctx = _make_context_with_tags("conversations_history", set())
    client = _mock_client(_api_side_effect)

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert result.structured_content["resolved_names"]["U0ADCDDNVGT"] == "Alice"


@pytest.mark.asyncio
async def test_lookup_tool_none_without_fastmcp_context():
    ctx = _make_context("users_info")
    assert await _lookup_tool(ctx) is None


@pytest.mark.asyncio
async def test_lookup_tool_none_when_get_tool_raises():
    fastmcp_context = SimpleNamespace(
        fastmcp=SimpleNamespace(get_tool=AsyncMock(side_effect=KeyError("nope")))
    )
    ctx = MiddlewareContext(
        message=CallToolRequestParams(name="ghost", arguments={}),
        method="tools/call",
        fastmcp_context=fastmcp_context,
    )
    assert await _lookup_tool(ctx) is None


@pytest.mark.asyncio
async def test_lookup_tool_returns_tool():
    ctx = _make_context_with_tags("users_info", {"x"})
    tool = await _lookup_tool(ctx)
    assert tool is not None
    assert tool.tags == {"x"}


@pytest.mark.asyncio
async def test_middleware_registered():
    from slack_mcp.server import mcp

    assert any(isinstance(m, NameResolutionMiddleware) for m in mcp.middleware)
