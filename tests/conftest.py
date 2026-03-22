from __future__ import annotations

import os
from unittest.mock import AsyncMock

import pytest

from slack_mcp.client import SlackClient
from slack_mcp.resolve import set_cache_store


@pytest.fixture(autouse=True)
def _disable_resolve_cache():
    """Disable the resolver's disk cache during unit tests."""
    set_cache_store(None)
    yield
    set_cache_store(None)


@pytest.fixture
def mock_client() -> SlackClient:
    """Return a SlackClient with mocked api_call and session_call."""
    client = object.__new__(SlackClient)
    client.api_call = AsyncMock(return_value={"ok": True})
    client.api_call_json = AsyncMock(return_value={"ok": True})
    client.session_call = AsyncMock(return_value={"ok": True})
    client.session_call_form = AsyncMock(return_value={"ok": True})
    client.session_call_multipart = AsyncMock(return_value={"ok": True})
    return client


@pytest.fixture
def live_client() -> SlackClient:
    """Return a real SlackClient from .env for integration tests.

    Skips the test if SLACK_XOXP_TOKEN is not set.
    """
    if not os.getenv("SLACK_XOXP_TOKEN"):
        pytest.skip("SLACK_XOXP_TOKEN not set")
    return SlackClient()
