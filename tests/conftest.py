from __future__ import annotations

import os
from unittest.mock import AsyncMock

import pytest

from slack_mcp.client import SlackClient


@pytest.fixture
def mock_client() -> SlackClient:
    """Return a SlackClient with mocked api_call and session_call."""
    client = object.__new__(SlackClient)
    client.api_call = AsyncMock(return_value={"ok": True})
    client.api_call_json = AsyncMock(return_value={"ok": True})
    client.session_call = AsyncMock(return_value={"ok": True})
    client.session_call_form = AsyncMock(return_value={"ok": True})
    return client


@pytest.fixture
def live_client() -> SlackClient:
    """Return a real SlackClient from .env for integration tests.

    Skips the test if SLACK_XOXP_TOKEN is not set.
    """
    if not os.getenv("SLACK_XOXP_TOKEN"):
        pytest.skip("SLACK_XOXP_TOKEN not set")
    return SlackClient()
