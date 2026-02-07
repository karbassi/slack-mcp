import pytest

from slack_mcp.tools.tooling import (
    tooling_tokens_rotate,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid refresh_token, client_id, and client_secret")
async def test_tooling_tokens_rotate_live(live_client):
    pass
