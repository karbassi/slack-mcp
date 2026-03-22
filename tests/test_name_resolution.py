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
            {"user": "U0ADCDDNVGT", "text": "Hello <@U0BXYZ12345> check <#C0AD56E4N6B>"},
            {"bot_id": "BA13894H00", "text": "Bot message"},
        ],
    }

    async def fake_call_next(ctx):
        return _make_result(data)

    client = _mock_client(_api_side_effect)
    ctx = _make_context("conversations_history", {"channel": "C000"})

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    enriched = json.loads(result.content[0].text)
    names = enriched["resolved_names"]
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

    async def fake_call_next(ctx):
        return _make_result(data)

    client = _mock_client(_api_side_effect)
    ctx = _make_context("search_messages", {"query": "test"})

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    enriched = json.loads(result.content[0].text)
    assert enriched["resolved_names"]["U0ADCDDNVGT"] == "Alice"


@pytest.mark.asyncio
async def test_non_target_tool_passes_through():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "channels": []}

    async def fake_call_next(ctx):
        return _make_result(data)

    ctx = _make_context("conversations_list")
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    parsed = json.loads(result.content[0].text)
    assert "resolved_names" not in parsed


@pytest.mark.asyncio
async def test_empty_messages_no_enrichment():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": []}

    async def fake_call_next(ctx):
        return _make_result(data)

    ctx = _make_context("conversations_history", {"channel": "C000"})
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    parsed = json.loads(result.content[0].text)
    assert "resolved_names" not in parsed


@pytest.mark.asyncio
async def test_no_ids_in_messages_no_enrichment():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"text": "plain text, no IDs"}]}

    async def fake_call_next(ctx):
        return _make_result(data)

    ctx = _make_context("conversations_history", {"channel": "C000"})
    result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    parsed = json.loads(result.content[0].text)
    assert "resolved_names" not in parsed


@pytest.mark.asyncio
async def test_failed_lookups_excluded():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"user": "UBAD00000X", "text": "hi"}]}

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
    assert "resolved_names" not in parsed


@pytest.mark.asyncio
async def test_resolution_error_returns_original_result():
    middleware = NameResolutionMiddleware()
    data = {"ok": True, "messages": [{"user": "U0ADCDDNVGT", "text": "hi"}]}
    original_json = json.dumps(data)

    from slack_sdk.errors import SlackApiError
    from slack_sdk.web.async_slack_response import AsyncSlackResponse

    async def auth_error(method, **kwargs):
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

    async def fake_call_next(ctx):
        return _make_result(data)

    with patch("slack_mcp.server.get_client", return_value=client):
        result = await middleware.on_call_tool(context=ctx, call_next=fake_call_next)

    assert result.content[0].text == original_json
    assert "resolved_names" not in json.loads(result.content[0].text)


@pytest.mark.asyncio
async def test_middleware_registered():
    from slack_mcp.server import mcp

    assert any(isinstance(m, NameResolutionMiddleware) for m in mcp.middleware)
