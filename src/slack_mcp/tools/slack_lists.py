from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def slack_lists_access_delete(
    list_id: str,
    channel_ids: list[str] | None = None,
    user_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove access to a list for specified entities."""
    return await client.api_call_json(
        "slackLists.access.delete",
        list_id=list_id,
        channel_ids=channel_ids,
        user_ids=user_ids,
    )


@mcp.tool
async def slack_lists_access_set(
    list_id: str,
    access_level: str,
    channel_ids: list[str] | None = None,
    user_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set access level to a list for specified entities."""
    return await client.api_call_json(
        "slackLists.access.set",
        list_id=list_id,
        access_level=access_level,
        channel_ids=channel_ids,
        user_ids=user_ids,
    )


@mcp.tool
async def slack_lists_create(
    name: str,
    description: str | None = None,
    columns: list[dict[str, str]] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new list."""
    return await client.api_call_json(
        "slackLists.create", name=name, description=description, columns=columns
    )


@mcp.tool
async def slack_lists_download_get(
    job_id: str,
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get a list download."""
    return await client.api_call_json(
        "slackLists.download.get", job_id=job_id, list_id=list_id
    )


@mcp.tool
async def slack_lists_download_start(
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Start a list download."""
    return await client.api_call_json("slackLists.download.start", list_id=list_id)


@mcp.tool
async def slack_lists_items_create(
    list_id: str,
    column_values: dict[str, str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new list item."""
    return await client.api_call_json(
        "slackLists.items.create", list_id=list_id, column_values=column_values
    )


@mcp.tool
async def slack_lists_items_delete(
    item_id: str,
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a list item."""
    return await client.api_call_json(
        "slackLists.items.delete", id=item_id, list_id=list_id
    )


@mcp.tool
async def slack_lists_items_delete_multiple(
    item_ids: list[str],
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete multiple list items."""
    return await client.api_call_json(
        "slackLists.items.deleteMultiple", ids=item_ids, list_id=list_id
    )


@mcp.tool
async def slack_lists_items_info(
    item_id: str,
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get info about a list item."""
    return await client.api_call_json(
        "slackLists.items.info", id=item_id, list_id=list_id
    )


@mcp.tool
async def slack_lists_items_list(
    list_id: str,
    cursor: str | None = None,
    limit: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List items in a list."""
    return await client.api_call_json(
        "slackLists.items.list", list_id=list_id, cursor=cursor, limit=limit
    )


@mcp.tool
async def slack_lists_items_update(
    item_id: str,
    list_id: str,
    column_values: dict[str, str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update a list item."""
    return await client.api_call_json(
        "slackLists.items.update",
        id=item_id,
        list_id=list_id,
        column_values=column_values,
    )


@mcp.tool
async def slack_lists_update(
    list_id: str,
    name: str | None = None,
    description: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update a list."""
    return await client.api_call_json(
        "slackLists.update", id=list_id, name=name, description=description
    )
