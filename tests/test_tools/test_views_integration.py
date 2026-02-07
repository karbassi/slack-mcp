import pytest

from slack_mcp.tools.views import (
    views_open,
    views_publish,
    views_push,
    views_update,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a trigger_id from an interactive event")
async def test_views_open_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: views.publish requires bot token (xoxb)")
async def test_views_publish_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a trigger_id from an interactive event")
async def test_views_push_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a trigger_id and an existing view to update")
async def test_views_update_live(live_client):
    pass
