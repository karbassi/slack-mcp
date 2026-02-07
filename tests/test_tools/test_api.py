from __future__ import annotations

import pytest

from slack_mcp.tools.api import api_test


@pytest.mark.asyncio
async def test_api_test(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await api_test(client=mock_client)
    assert result == {"ok": True}
    mock_client.api_call.assert_called_once_with("api.test")


@pytest.mark.asyncio
async def test_api_test_with_error(mock_client):
    mock_client.api_call.return_value = {"ok": False, "error": "my_error"}
    result = await api_test(error="my_error", client=mock_client)
    assert result == {"ok": False, "error": "my_error"}
    mock_client.api_call.assert_called_once_with("api.test", error="my_error")


@pytest.mark.asyncio
async def test_api_test_with_foo(mock_client):
    mock_client.api_call.return_value = {"ok": True, "args": {"foo": "bar"}}
    result = await api_test(foo="bar", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("api.test", foo="bar")
