from __future__ import annotations

import pytest

from slack_mcp.tools.api import api_test
from tests.conftest import assert_api_call


@pytest.mark.asyncio
async def test_api_test(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await api_test(client=mock_client)
    assert result == {"ok": True}
    assert_api_call(mock_client.api_call, "api.test")


@pytest.mark.asyncio
async def test_api_test_with_error(mock_client):
    mock_client.api_call.return_value = {"ok": False, "error": "my_error"}
    result = await api_test(error="my_error", client=mock_client)
    assert result == {"ok": False, "error": "my_error"}
    assert_api_call(mock_client.api_call, "api.test", error="my_error")


@pytest.mark.asyncio
async def test_api_test_with_foo(mock_client):
    mock_client.api_call.return_value = {"ok": True, "args": {"foo": "bar"}}
    result = await api_test(foo="bar", client=mock_client)
    assert result["ok"] is True
    assert_api_call(mock_client.api_call, "api.test", foo="bar")
