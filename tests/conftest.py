from __future__ import annotations

import atexit
import os
import shutil
import tempfile
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest
from dotenv import load_dotenv
from fastmcp.client import Client
from slack_sdk.errors import SlackApiError

from slack_mcp.client import SlackClient
from slack_mcp.resolve import set_cache_store

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

# Integration tests hit a live workspace as the token owner with no sandbox — an
# ambient SLACK_XOX* pointing at a real workspace is destructive (a prior run
# deleted a real profile photo). The runtime lets the environment win so an MCP
# host can pick the workspace; tests need the opposite, pinning to the test .env
# regardless of what's exported. The live_client team guard is the hard backstop.
load_dotenv(override=True)

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
    "users_set_photo",
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
async def live_client() -> AsyncIterator[SlackClient]:
    """Return a real SlackClient from .env for integration tests.

    Skips the test if SLACK_XOXP_TOKEN is not set, and HARD-FAILS if the token
    resolves to any workspace other than the throwaway test team. This is the
    real seatbelt against mutating a production workspace — it holds regardless
    of load_dotenv override behavior or a stray ambient token.
    """
    if not os.getenv("SLACK_XOXP_TOKEN"):
        pytest.skip("SLACK_XOXP_TOKEN not set")
    expected_team = os.getenv("SLACK_TEST_TEAM_ID")
    if not expected_team:
        pytest.skip(
            "SLACK_TEST_TEAM_ID not set — can't confirm .env points at the "
            "throwaway test workspace, so refusing to run integration tests. "
            "Set it in .env to the test team's ID (from auth.test)."
        )
    client = SlackClient()
    # yield inside try so the client's httpx session is closed even when the
    # team guard fails (pytest.fail raises) or a test errors mid-run.
    try:
        # Verify the workspace once per session, not per test — one auth.test
        # instead of one per fixture use. A session-scoped fixture can't hold the
        # httpx client (pytest-asyncio's function-scoped loop closes under it), so
        # memoize the check while the client stays function-scoped.
        await _verify_test_workspace(client, expected_team)
        yield client
    finally:
        await client.close()


_team_verified = False


async def _verify_test_workspace(client: SlackClient, expected_team: str) -> None:
    global _team_verified
    if _team_verified:
        return
    try:
        auth = await client.api_call("auth.test")
    except SlackApiError as e:
        # slack_sdk raises on ok:false, so a bad/expired token lands here rather
        # than as a team mismatch — say so, don't misreport it as wrong workspace.
        pytest.fail(f"auth.test failed ({e.response.get('error')!r}) — check the "
                    "SLACK_XOX* tokens in .env, they may be invalid or expired.")
    team_id = auth.get("team_id")
    if team_id != expected_team:
        pytest.fail(
            f"Refusing to run integration tests: auth.test resolved to team "
            f"{team_id!r} ({auth.get('team')!r}), not the expected test "
            f"workspace {expected_team!r}. Point .env at the test workspace."
        )
    _team_verified = True


@pytest.fixture
def requires_session_tokens():
    """Skip a test unless both session tokens are set.

    Undocumented session endpoints (``SlackClient.session_call*``) require both
    ``SLACK_XOXC_TOKEN`` and ``SLACK_XOXD_TOKEN`` — without both, the call raises
    ``ValueError``. Skip cleanly when either is missing instead of failing hard.
    """
    if not os.getenv("SLACK_XOXC_TOKEN") or not os.getenv("SLACK_XOXD_TOKEN"):
        pytest.skip("SLACK_XOXC_TOKEN/SLACK_XOXD_TOKEN not set")
