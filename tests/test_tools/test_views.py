import pytest

from slack_mcp.tools.views import views_open, views_publish, views_push, views_update


@pytest.mark.asyncio
async def test_views_open(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    view = {"type": "modal", "title": {"type": "plain_text", "text": "Test"}}
    result = await views_open(trigger_id="T123", view=view, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "views.open", trigger_id="T123", view=view
    )


@pytest.mark.asyncio
async def test_views_publish(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    view = {"type": "home", "blocks": []}
    result = await views_publish(user_id="U123", view=view, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "views.publish", user_id="U123", view=view
    )


@pytest.mark.asyncio
async def test_views_push(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    view = {"type": "modal", "title": {"type": "plain_text", "text": "Pushed"}}
    result = await views_push(trigger_id="T123", view=view, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "views.push", trigger_id="T123", view=view
    )


@pytest.mark.asyncio
async def test_views_update(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    view = {"type": "modal", "title": {"type": "plain_text", "text": "Updated"}}
    result = await views_update(view=view, view_id="V123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "views.update", view=view, view_id="V123"
    )
