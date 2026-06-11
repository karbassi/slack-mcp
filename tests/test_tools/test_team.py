from tests.conftest import assert_api_call


async def test_team_access_logs(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_access_logs", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.accessLogs")


async def test_team_billable_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_billable_info", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.billableInfo")


async def test_team_billing_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_billing_info", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.billing.info")


async def test_team_external_teams_disconnect(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "team_external_teams_disconnect", {"target_team": "T123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "team.externalTeams.disconnect", target_team="T123"
    )


async def test_team_external_teams_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_external_teams_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.externalTeams.list")


async def test_team_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_info", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.info")


async def test_team_integration_logs(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_integration_logs", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.integrationLogs")


async def test_team_preferences_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_preferences_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.preferences.list")


async def test_team_profile_get(mcp_client, slack_stub):
    result = await mcp_client.call_tool("team_profile_get", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "team.profile.get")
