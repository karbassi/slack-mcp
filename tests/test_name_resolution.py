from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest
from fastmcp.server.middleware.middleware import MiddlewareContext
from fastmcp.tools.tool import ToolResult
from mcp.types import CallToolRequestParams, TextContent

from slack_mcp.server import NameResolutionMiddleware


def _make_context(tool_name: str, arguments: dict | None = None) -> MiddlewareContext:
    return MiddlewareContext(
        message=CallToolRequestParams(name=tool_name, arguments=arguments),
        method="tools/call",
    )


def _make_result(data: dict) -> ToolResult:
    return ToolResult(content=[TextContent(type="text", text=json.dumps(data))])


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
            {"user": "U123", "text": "Hello <@U456> check <#C789>"},
            {"bot_id": "B111", "text": "Bot message"},
        ],
    }

    async def fake_call_next(ctx):
        return _make_result(data)

    client = _mock_client(_api_side_effect)
    ctx = _make_context("conversations_history", {"channel": "C000"})

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    enriched = json.loads(result.content[0].text)
    names = enriched["_resolved_names"]
    assert names["U123"] == "Alice"
    assert names["U456"] == "Alice"
    assert names["C789"] == "general"
    assert names["B111"] == "Testbot"


@pytest.mark.asyncio
async def test_enriches_conversations_replies():
    middleware = NameResolutionMiddleware()
    data = {
        "ok": True,
        "messages": [{"user": "U123", "text": "thread msg"}],
    }

    async def fake_call_next(ctx):
        return _make_result(data)

    client = _mock_client(_api_side_effect)
    ctx = _make_context("conversations_replies", {"channel": "C000", "ts": "123.456"})

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    enriched = json.loads(result.content[0].text)
    assert enriched["_resolved_names"]["U123"] == "Alice"


@pytest.mark.asyncio
async def test_enriches_search_messages():
    middleware = NameResolutionMiddleware()
    data = {
        "ok": True,
        "messages": {
            "matches": [{"user": "U123", "text": "found it"}],
        },
    }

    async def fake_call_next(ctx):
        return _make_result(data)

    client = _mock_client(_api_side_effect)
    ctx = _make_context("search_messages", {"query": "test"})

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    enriched = json.loads(result.content[0].text)
    assert enriched["_resolved_names"]["U123"] == "Alice"


@pytest.mark.asyncio
async def test_non_target_tool_passes_through():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "channels": []}

    async def fake_call_next(ctx):
        return _make_result(data)

    ctx = _make_context("conversations_list")
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    parsed = json.loads(result.content[0].text)
    assert "_resolved_names" not in parsed


@pytest.mark.asyncio
async def test_empty_messages_no_enrichment():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": []}

    async def fake_call_next(ctx):
        return _make_result(data)

    ctx = _make_context("conversations_history", {"channel": "C000"})
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    parsed = json.loads(result.content[0].text)
    assert "_resolved_names" not in parsed


@pytest.mark.asyncio
async def test_no_ids_in_messages_no_enrichment():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"text": "plain text, no IDs"}]}

    async def fake_call_next(ctx):
        return _make_result(data)

    ctx = _make_context("conversations_history", {"channel": "C000"})
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    parsed = json.loads(result.content[0].text)
    assert "_resolved_names" not in parsed


@pytest.mark.asyncio
async def test_failed_lookups_excluded():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"user": "UBAD", "text": "hi"}]}

    from slack_sdk.errors import SlackApiError
    from slack_sdk.web.async_slack_response import AsyncSlackResponse

    async def failing_api(method, **kwargs):
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

    async def fake_call_next(ctx):
        return _make_result(data)

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    parsed = json.loads(result.content[0].text)
    assert "_resolved_names" not in parsed


@pytest.mark.asyncio
async def test_middleware_registered():
    from slack_mcp.server import mcp

    assert any(isinstance(m, NameResolutionMiddleware) for m in mcp.middleware)
