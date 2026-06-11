from tests.conftest import assert_api_call


def _modal(title: str) -> dict:
    """A realistic Slack modal view payload (nested Block Kit objects)."""
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": title},
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": "hello"}}
        ],
    }


async def test_views_open(mcp_client, slack_stub):
    view = _modal("Test")
    result = await mcp_client.call_tool(
        "views_open", {"trigger_id": "T123", "view": view}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "views.open", trigger_id="T123", view=view)


async def test_views_publish(mcp_client, slack_stub):
    view = {
        "type": "home",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": "home"}}
        ],
    }
    result = await mcp_client.call_tool(
        "views_publish", {"user_id": "U123", "view": view}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "views.publish", user_id="U123", view=view)


async def test_views_push(mcp_client, slack_stub):
    view = _modal("Pushed")
    result = await mcp_client.call_tool(
        "views_push", {"trigger_id": "T123", "view": view}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "views.push", trigger_id="T123", view=view)


async def test_views_update(mcp_client, slack_stub):
    view = _modal("Updated")
    result = await mcp_client.call_tool(
        "views_update", {"view": view, "view_id": "V123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "views.update", view=view, view_id="V123"
    )
