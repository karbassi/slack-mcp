from __future__ import annotations

import pytest

from slack_mcp.tools.api import api_test


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_test_live(live_client):
    result = await api_test(client=live_client)
    assert result["ok"] is True
