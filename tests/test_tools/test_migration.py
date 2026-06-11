from tests.conftest import assert_api_call


async def test_migration_exchange(mcp_client, slack_stub):
    result = await mcp_client.call_tool("migration_exchange", {"users": "U123,U456"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "migration.exchange", users="U123,U456")
