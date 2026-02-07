import os

import pytest
from slack_mcp.tools.undocumented import (
    client_boot,
    client_counts,
    client_user_boot,
    threads_get_view,
)


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@pytest.fixture
def requires_session_tokens():
    if not os.getenv("SLACK_XOXC_TOKEN"):
        pytest.skip("SLACK_XOXC_TOKEN not set")


@pytest.mark.usefixtures("requires_session_tokens")
async def test_client_boot_live(live_client):
    result = await client_boot(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_client_counts_live(live_client):
    result = await client_counts(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_client_user_boot_live(live_client):
    result = await client_user_boot(client=live_client)
    assert "ok" in result


@pytest.mark.usefixtures("requires_session_tokens")
async def test_threads_get_view_live(live_client):
    result = await threads_get_view(client=live_client)
    assert "ok" in result
