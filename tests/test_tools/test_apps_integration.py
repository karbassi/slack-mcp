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


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires socket mode enabled on app")
async def test_apps_connections_open_live(live_client):
    result = await apps_connections_open(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid event_context from Events API")
async def test_apps_event_authorizations_list_live(live_client):
    result = await apps_event_authorizations_list(
        event_context="placeholder", client=live_client
    )
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would create a new app")
async def test_apps_manifest_create_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would delete an app")
async def test_apps_manifest_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires app configuration token")
async def test_apps_manifest_export_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would update app manifest")
async def test_apps_manifest_update_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires app configuration token")
async def test_apps_manifest_validate_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would uninstall the app")
async def test_apps_uninstall_live(live_client):
    pass
