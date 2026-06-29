from tests.conftest import assert_api_call


async def test_entity_present_details(mcp_client, slack_stub):
    metadata = {"E123": {"entity_type": "slack#/entities/file"}}
    result = await mcp_client.call_tool(
        "entity_present_details",
        {"trigger_id": "T123", "metadata": metadata},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "entity.presentDetails",
        trigger_id="T123",
        metadata=metadata,
    )
