from tests.conftest import assert_api_call


async def test_entity_present_details(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "entity_present_details",
        {"app_id": "A123", "entity_id": "E123", "entity_type": "channel"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "entity.presentDetails",
        app_id="A123",
        entity_id="E123",
        entity_type="channel",
    )
