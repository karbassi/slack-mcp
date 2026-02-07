import pytest

from slack_mcp.tools.apps import (
    apps_connections_open,
    apps_event_authorizations_list,
    apps_manifest_create,
    apps_manifest_delete,
    apps_manifest_export,
    apps_manifest_update,
    apps_manifest_validate,
    apps_uninstall,
)


@pytest.mark.asyncio
async def test_apps_connections_open(mock_client):
    mock_client.api_call.return_value = {"ok": True, "url": "wss://example.com"}
    result = await apps_connections_open(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("apps.connections.open")


@pytest.mark.asyncio
async def test_apps_event_authorizations_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "authorizations": []}
    result = await apps_event_authorizations_list(
        event_context="test_ctx", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "apps.event.authorizations.list", event_context="test_ctx"
    )


@pytest.mark.asyncio
async def test_apps_manifest_create(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await apps_manifest_create(manifest='{"name":"test"}', client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "apps.manifest.create", manifest='{"name":"test"}'
    )


@pytest.mark.asyncio
async def test_apps_manifest_delete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await apps_manifest_delete(app_id="A123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("apps.manifest.delete", app_id="A123")


@pytest.mark.asyncio
async def test_apps_manifest_export(mock_client):
    mock_client.api_call.return_value = {"ok": True, "manifest": {}}
    result = await apps_manifest_export(app_id="A123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("apps.manifest.export", app_id="A123")


@pytest.mark.asyncio
async def test_apps_manifest_update(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await apps_manifest_update(
        app_id="A123", manifest='{"name":"updated"}', client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "apps.manifest.update", app_id="A123", manifest='{"name":"updated"}'
    )


@pytest.mark.asyncio
async def test_apps_manifest_validate(mock_client):
    mock_client.api_call.return_value = {"ok": True, "errors": []}
    result = await apps_manifest_validate(
        manifest='{"name":"test"}', client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "apps.manifest.validate", manifest='{"name":"test"}'
    )


@pytest.mark.asyncio
async def test_apps_uninstall(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await apps_uninstall(
        client_id="C123", client_secret="S456", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "apps.uninstall", client_id="C123", client_secret="S456"
    )
