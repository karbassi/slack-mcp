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
@pytest.mark.skip(
    reason="not_allowed_token_type: views.publish requires bot token with Home Tab enabled"
)
async def test_views_publish_live(live_client):
    """Publish a Home Tab view for a user."""
    view = {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Integration test home tab",
                },
            }
        ],
    }
    result = await views_publish(
        user_id="U0000000000",
        view=view,
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a trigger_id from an interactive event")
async def test_views_push_live(live_client):
    """Push a view onto the stack of a root view."""
    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Pushed View"},
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Pushed view content"},
            }
        ],
    }
    result = await views_push(
        trigger_id="0000000000.0000000000",
        view=view,
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a trigger_id and an existing view to update")
async def test_views_update_live(live_client):
    """Update an existing view."""
    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Updated View"},
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Updated view content"},
            }
        ],
    }
    result = await views_update(
        view=view,
        view_id="V0000000000",
        client=live_client,
    )
    assert "ok" in result
