from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def apps_connections_open(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Generate a temporary Socket Mode WebSocket URL."""
    return await client.api_call("apps.connections.open")


@mcp.tool
async def apps_event_authorizations_list(
    event_context: str,
    cursor: str | None = None,
    limit: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get a list of authorizations for the given event context."""
    return await client.api_call(
        "apps.event.authorizations.list",
        event_context=event_context,
        cursor=cursor,
        limit=limit,
    )


@mcp.tool
async def apps_manifest_create(
    manifest: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create an app from an app manifest."""
    return await client.api_call("apps.manifest.create", manifest=manifest)


@mcp.tool
async def apps_manifest_delete(
    app_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Permanently deletes an app created through app manifests."""
    return await client.api_call("apps.manifest.delete", app_id=app_id)


@mcp.tool
async def apps_manifest_export(
    app_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Export an app manifest from an existing app."""
    return await client.api_call("apps.manifest.export", app_id=app_id)


@mcp.tool
async def apps_manifest_update(
    app_id: str,
    manifest: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an app from an app manifest."""
    return await client.api_call(
        "apps.manifest.update", app_id=app_id, manifest=manifest
    )


@mcp.tool
async def apps_manifest_validate(
    manifest: str,
    app_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Validate an app manifest."""
    return await client.api_call(
        "apps.manifest.validate", manifest=manifest, app_id=app_id
    )


@mcp.tool
async def apps_uninstall(
    client_id: str,
    client_secret: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Uninstall your app from a workspace."""
    return await client.api_call(
        "apps.uninstall", client_id=client_id, client_secret=client_secret
    )
