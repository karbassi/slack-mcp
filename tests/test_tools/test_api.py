from __future__ import annotations

import pytest

from tests.conftest import assert_api_call


async def test_api_test(mcp_client, slack_stub):
    result = await mcp_client.call_tool("api_test", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "api.test")


async def test_api_test_with_error(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": False, "error": "my_error"}
    result = await mcp_client.call_tool("api_test", {"error": "my_error"}, raise_on_error=False)
    assert result.is_error is True
    assert_api_call(slack_stub.api_call, "api.test", error="my_error")


async def test_api_test_with_foo(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "args": {"foo": "bar"}}
    result = await mcp_client.call_tool("api_test", {"foo": "bar"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "api.test", foo="bar")
