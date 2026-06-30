from typing import Any

from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def slack_lists_get_my_items(
    include_approvals: bool | None = None,
    include_subtasks: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List the Slack List records assigned to the current user (undocumented session endpoint).

    Surfaces the user's tasks and approvals across all their lists — answers
    "what's on my plate". Returns ``lists``, ``records``, and ``counts``.

    Args:
        include_approvals: When ``True``, include approval records assigned to the user.
        include_subtasks: When ``True``, include subtask records nested under parent items.
    """
    return await client.session_call(
        "lists.getMyItems",
        include_approvals=include_approvals,
        include_subtasks=include_subtasks,
    )


@mcp.tool
async def slack_lists_access_delete(
    list_id: str,
    channel_ids: list[str] | None = None,
    user_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove access to a list for specified entities.

    Args:
        list_id: ID of the list (a file ID) to remove access from (e.g. ``F0123``).
        channel_ids: Channel IDs to revoke access for (e.g. ``["C0123"]``).
        user_ids: User IDs to revoke access for (e.g. ``["U0123"]``).
    """
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
    """Set access level to a list for specified entities.

    Args:
        list_id: ID of the list (a file ID) to set access on (e.g. ``F0123``).
        access_level: Access level to grant; one of ``read``, ``write``, or ``owner``.
        channel_ids: Channel IDs to grant access to (e.g. ``["C0123"]``).
        user_ids: User IDs to grant access to (e.g. ``["U0123"]``).
    """
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
    description_blocks: list[dict[str, Any]] | None = None,
    schema: list[dict[str, Any]] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new list.

    Args:
        name: Name (title) of the list to create.
        description_blocks: Rich-text blocks describing the list.
        schema: Column definitions for the list, each describing a field's key, name, and type.
    """
    return await client.api_call_json(
        "slackLists.create",
        name=name,
        description_blocks=description_blocks,
        schema=schema,
    )


@mcp.tool
async def slack_lists_download_get(
    job_id: str,
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get a list download.

    Args:
        job_id: ID of the download job previously started for the list.
        list_id: ID of the list (a file ID) being downloaded (e.g. ``F0123``).
    """
    return await client.api_call_json(
        "slackLists.download.get", job_id=job_id, list_id=list_id
    )


@mcp.tool
async def slack_lists_download_start(
    list_id: str,
    include_archived: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Start a list download.

    Args:
        list_id: ID of the list (a file ID) to download (e.g. ``F0123``).
        include_archived: When ``True``, include archived items in the download.
    """
    return await client.api_call_json(
        "slackLists.download.start",
        list_id=list_id,
        include_archived=include_archived,
    )


@mcp.tool
async def slack_lists_items_create(
    list_id: str,
    initial_fields: list[dict[str, Any]] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a new list item.

    Args:
        list_id: ID of the list (a file ID) to add the item to (e.g. ``F0123``).
        initial_fields: Field values for the new item, each an object with a ``column_id`` and a typed value.
    """
    return await client.api_call_json(
        "slackLists.items.create", list_id=list_id, initial_fields=initial_fields
    )


@mcp.tool
async def slack_lists_items_delete(
    item_id: str,
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a list item.

    Args:
        item_id: ID of the list item (record) to delete.
        list_id: ID of the list (a file ID) containing the item (e.g. ``F0123``).
    """
    return await client.api_call_json(
        "slackLists.items.delete", id=item_id, list_id=list_id
    )


@mcp.tool
async def slack_lists_items_delete_multiple(
    item_ids: list[str],
    list_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete multiple list items.

    Args:
        item_ids: IDs of the list items (records) to delete.
        list_id: ID of the list (a file ID) containing the items (e.g. ``F0123``).
    """
    return await client.api_call_json(
        "slackLists.items.deleteMultiple", ids=item_ids, list_id=list_id
    )


@mcp.tool
async def slack_lists_items_info(
    item_id: str,
    list_id: str,
    include_is_subscribed: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get info about a list item.

    Args:
        item_id: ID of the list item (record) to fetch.
        list_id: ID of the list (a file ID) containing the item (e.g. ``F0123``).
        include_is_subscribed: When ``True``, include whether the caller is subscribed to the item.
    """
    return await client.api_call_json(
        "slackLists.items.info",
        id=item_id,
        list_id=list_id,
        include_is_subscribed=include_is_subscribed,
    )


@mcp.tool
async def slack_lists_items_list(
    list_id: str,
    cursor: str | None = None,
    limit: int | None = None,
    archived: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List items in a list.

    Args:
        list_id: ID of the list (a file ID) whose items to return (e.g. ``F0123``).
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Maximum number of items to return per page.
        archived: When ``True``, return archived items instead of active ones.
    """
    return await client.api_call_json(
        "slackLists.items.list",
        list_id=list_id,
        cursor=cursor,
        limit=limit,
        archived=archived,
    )


@mcp.tool
async def slack_lists_items_update(
    list_id: str,
    cells: list[dict[str, Any]],
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update cells in a list item.

    Args:
        list_id: ID of the list (a file ID) containing the item (e.g. ``F0123``).
        cells: Cells to update, each an object with ``row_id`` (the item/record), ``column_id``, and a typed value.
    """
    return await client.api_call_json(
        "slackLists.items.update", list_id=list_id, cells=cells
    )


@mcp.tool
async def slack_lists_update(
    list_id: str,
    name: str | None = None,
    description_blocks: list[dict[str, Any]] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update a list.

    Args:
        list_id: ID of the list (a file ID) to update (e.g. ``F0123``).
        name: New name (title) for the list.
        description_blocks: New rich-text blocks describing the list.
    """
    return await client.api_call_json(
        "slackLists.update",
        id=list_id,
        name=name,
        description_blocks=description_blocks,
    )
