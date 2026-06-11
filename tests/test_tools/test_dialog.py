from tests.conftest import assert_api_call


async def test_dialog_open(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "dialog_open",
        {"dialog": {"title": "Test"}, "trigger_id": "T123"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "dialog.open",
        dialog={"title": "Test"},
        trigger_id="T123",
    )
