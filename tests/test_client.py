"""Tests for SlackClient — the None-dropping contract at the call seam.

Tools forward every Slack parameter by keyword, leaving absent optionals as
None. The client drops None before hitting the wire so tools don't need
per-call ``if x is not None`` guards. These tests pin that contract; tool
unit tests rely on it (via the ``assert_api_call`` helper) rather than
re-proving it per tool.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from slack_mcp.client import SlackClient, _drop_none


class TestDropNone:
    def test_drops_none_values(self):
        assert _drop_none({"a": 1, "b": None, "c": "x"}) == {"a": 1, "c": "x"}

    def test_keeps_falsy_but_meaningful_values(self):
        kept = _drop_none({"flag": False, "n": 0, "s": "", "items": []})
        assert kept == {"flag": False, "n": 0, "s": "", "items": []}

    def test_empty(self):
        assert _drop_none({}) == {}


def _client_with_mock_web() -> SlackClient:
    client = object.__new__(SlackClient)
    client.web_client = SimpleNamespace(
        api_call=AsyncMock(return_value=SimpleNamespace(data={"ok": True}))
    )
    return client


def _client_with_mock_session() -> SlackClient:
    client = object.__new__(SlackClient)
    client.xoxc_token = "xoxc-test"
    client.xoxd_token = "xoxd-test"
    resp = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {"ok": True},
    )
    client.session_client = SimpleNamespace(post=AsyncMock(return_value=resp))
    return client


class TestApiCallDropsNone:
    @pytest.mark.asyncio
    async def test_form_call_drops_none_keeps_falsy(self):
        client = _client_with_mock_web()
        await client.api_call(
            "users.list", cursor="C", limit=None, exclude_archived=False
        )
        client.web_client.api_call.assert_called_once_with(
            "users.list", data={"cursor": "C", "exclude_archived": False}
        )

    @pytest.mark.asyncio
    async def test_json_call_drops_none(self):
        client = _client_with_mock_web()
        await client.api_call_json("canvas.x", a=1, b=None)
        client.web_client.api_call.assert_called_once_with("canvas.x", json={"a": 1})


class TestSessionCallDropsNone:
    @pytest.mark.asyncio
    async def test_session_json_drops_none(self):
        client = _client_with_mock_session()
        await client.session_call("threads.getView", limit=10, cursor=None)
        client.session_client.post.assert_called_once_with(
            "threads.getView", json={"limit": 10}
        )

    @pytest.mark.asyncio
    async def test_session_form_drops_none(self):
        client = _client_with_mock_session()
        await client.session_call_form("conversations.mark", channel="C", ts=None)
        method, kwargs = client.session_client.post.call_args
        assert method == ("conversations.mark",)
        assert kwargs["data"] == {"channel": "C"}
