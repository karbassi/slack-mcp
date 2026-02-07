from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def slack_lists_access_delete(
    list_id: str,
    channel_ids: Optional[list] = None,
    user_ids: Optional[list] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove access to a list for specified entities."""
    kwargs = {"list_id": list_id}
    if channel_ids is not None:
        kwargs["channel_ids"] = channel_ids
    if user_ids is not None:
        kwargs["user_ids"] = user_ids
    return await client.api_call_json("slackLists.access.delete", **kwargs)


@mcp.tool
async def slack_lists_access_set(
    list_id: str,
    access_level: str,
    channel_ids: Optional[list] = None,
    user_ids: Optional[list] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set access level to a list for specified entities."""
    kwargs = {"list_id": list_id, "access_level": access_level}
    if channel_ids is not None:
        kwargs["channel_ids"] = channel_ids
    if user_ids is not None:
        kwargs["user_ids"] = user_ids
    return await client.api_call_json("slackLists.access.set", **kwargs)


@mcp.tool
async def slack_lists_create(
    name: str,
    description: Optional[str] = None,
    columns: Optional[list] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new list."""
    kwargs = {"name": name}
    if description is not None:
        kwargs["description"] = description
    if columns is not None:
        kwargs["columns"] = columns
    return await client.api_call_json("slackLists.create", **kwargs)


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
    column_values: Optional[dict] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new list item."""
    kwargs = {"list_id": list_id}
    if column_values is not None:
        kwargs["column_values"] = column_values
    return await client.api_call_json("slackLists.items.create", **kwargs)


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
    item_ids: list,
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
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List items in a list."""
    kwargs = {"list_id": list_id}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    return await client.api_call_json("slackLists.items.list", **kwargs)


@mcp.tool
async def slack_lists_items_update(
    item_id: str,
    list_id: str,
    column_values: Optional[dict] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update a list item."""
    kwargs = {"id": item_id, "list_id": list_id}
    if column_values is not None:
        kwargs["column_values"] = column_values
    return await client.api_call_json("slackLists.items.update", **kwargs)


@mcp.tool
async def slack_lists_update(
    list_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update a list."""
    kwargs = {"id": list_id}
    if name is not None:
        kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    return await client.api_call_json("slackLists.update", **kwargs)
