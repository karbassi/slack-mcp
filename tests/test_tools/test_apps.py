from tests.conftest import assert_api_call


async def test_apps_activities_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "apps_activities_list", {"app_id": "A123", "limit": 100}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "apps.activities.list", app_id="A123", limit=100
    )


async def test_apps_connections_open(mcp_client, slack_stub):
    result = await mcp_client.call_tool("apps_connections_open", {})
    assert result.is_error is False
    slack_stub.api_call.assert_called_once_with("apps.connections.open")


async def test_apps_event_authorizations_list(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "apps_event_authorizations_list", {"event_context": "test_ctx"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "apps.event.authorizations.list",
        event_context="test_ctx",
    )


async def test_apps_manifest_create(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "apps_manifest_create", {"manifest": '{"name":"test"}'}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "apps.manifest.create", manifest='{"name":"test"}'
    )


async def test_apps_manifest_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool("apps_manifest_delete", {"app_id": "A123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "apps.manifest.delete", app_id="A123")


async def test_apps_manifest_export(mcp_client, slack_stub):
    result = await mcp_client.call_tool("apps_manifest_export", {"app_id": "A123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "apps.manifest.export", app_id="A123")


async def test_apps_manifest_update(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "apps_manifest_update", {"app_id": "A123", "manifest": '{"name":"updated"}'}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "apps.manifest.update",
        app_id="A123",
        manifest='{"name":"updated"}',
    )


async def test_apps_manifest_validate(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "apps_manifest_validate", {"manifest": '{"name":"test"}'}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "apps.manifest.validate", manifest='{"name":"test"}'
    )


async def test_apps_uninstall(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "apps_uninstall", {"client_id": "C123", "client_secret": "S456"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "apps.uninstall",
        client_id="C123",
        client_secret="S456",
    )
