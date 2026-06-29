from __future__ import annotations

import atexit
import os
import shutil
import tempfile
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest
from fastmcp.client import Client

from slack_mcp.client import SlackClient
from slack_mcp.resolve import set_cache_store

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

# Point the Response cache's DiskStore (wired at server import from
# XDG_CACHE_HOME) at a throwaway dir before slack_mcp.server is first imported —
# lazily, in fixtures / when test modules load, all after this conftest runs —
# so Client-driven tests never touch the real on-disk cache. Removed at exit.
_CACHE_DIR = tempfile.mkdtemp(prefix="slack-mcp-test-cache-")
os.environ["XDG_CACHE_HOME"] = _CACHE_DIR
atexit.register(shutil.rmtree, _CACHE_DIR, ignore_errors=True)

# Every SlackClient call method, mocked uniformly on the stub.
_CALL_METHODS = (
    "api_call",
    "api_call_json",
    "session_call",
    "session_call_form",
    "session_call_multipart",
    "files_upload_v2",
)


@pytest.fixture(autouse=True)
def _disable_resolve_cache():
    """Disable the resolver's disk cache during unit tests."""
    set_cache_store(None)
    yield
    set_cache_store(None)


@pytest.fixture(autouse=True)
def _clear_response_cache():
    """Clear the Response/Thread cache between tests so a cached result from one
    test can't satisfy another's call_tool."""
    try:
        from slack_mcp.server import cache_store
    except ImportError:
        # Server not importable in this context (e.g. pure-helper test runs).
        return
    # Any other failure (e.g. cache_store shape change) should fail loudly.
    cache_store._cache.clear()


def assert_api_call(mock, method: str, **expected) -> None:
    """Assert a mocked client call method was called once with ``method`` and
    exactly ``expected`` keyword args, ignoring any forwarded ``None`` values.

    Tools forward every Slack parameter by keyword, leaving absent optionals as
    None; the real client drops them (see test_client.py). Tool tests use this
    helper so they assert the args a tool genuinely supplies, not the
    language-level fact that an unpassed optional defaults to None.
    """
    mock.assert_called_once()
    args, kwargs = mock.call_args
    assert args[0] == method, f"expected method {method!r}, got {args[0]!r}"
    sent = {k: v for k, v in kwargs.items() if v is not None}
    assert sent == expected, f"expected {expected!r}, got {sent!r}"


@pytest.fixture
def slack_stub(monkeypatch) -> SlackClient:
    """A mock SlackClient wired in at the ``get_client()`` seam.

    Patching the singleton in both ``slack_mcp.server`` (where tools resolve it
    via ``Depends(slack_client)`` and the middleware call it) and
    ``slack_mcp.client`` makes every Tool call reach this stub. Each call method
    is an AsyncMock returning ``{"ok": True}``; override ``.return_value`` (or
    ``.side_effect``) per test to shape the Slack response.
    """
    import slack_mcp.client as client_mod
    import slack_mcp.server as server_mod

    stub = object.__new__(SlackClient)
    for name in _CALL_METHODS:
        setattr(stub, name, AsyncMock(return_value={"ok": True}))
    stub.close = AsyncMock()

    monkeypatch.setattr(server_mod, "get_client", lambda: stub)
    monkeypatch.setattr(client_mod, "get_client", lambda: stub)
    return stub


@pytest.fixture
async def mcp_client(slack_stub: SlackClient) -> AsyncIterator[Client]:  # noqa: ARG001
    """An in-memory FastMCP Client bound to the real server.

    Drives tools through their actual interface — schema validation, the full
    middleware stack, and serialization — with Slack stubbed via ``slack_stub``.
    ``slack_stub`` is a dependency (it installs the patch before the Client
    connects), not referenced directly in the body.
    """
    from slack_mcp.server import mcp

    async with Client(mcp) as client:
        yield client


@pytest.fixture
def mock_client() -> SlackClient:
    """Direct-call SlackClient stub for unit tests of non-tool helpers and
    middleware (e.g. ``resolve_ids``, the resolution middleware). Tool tests go
    through the MCP interface via ``mcp_client`` + ``slack_stub`` instead."""
    client = object.__new__(SlackClient)
    for name in _CALL_METHODS:
        setattr(client, name, AsyncMock(return_value={"ok": True}))
    return client


@pytest.fixture
def live_client() -> SlackClient:
    """Return a real SlackClient from .env for integration tests.

    Skips the test if SLACK_XOXP_TOKEN is not set.
    """
    if not os.getenv("SLACK_XOXP_TOKEN"):
        pytest.skip("SLACK_XOXP_TOKEN not set")
    return SlackClient()
