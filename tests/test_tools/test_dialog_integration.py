import pytest

from slack_mcp.tools.dialog import (
    dialog_open,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a trigger_id from an interactive event")
async def test_dialog_open_live(live_client):
    pass
