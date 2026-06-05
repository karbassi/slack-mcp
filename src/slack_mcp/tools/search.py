from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import (
    compact_search_all,
    compact_search_files,
    compact_search_messages,
    compactable,
)
from slack_mcp.server import SLOW_CALL_TIMEOUT, mcp, slack_client


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
@compactable(compact_search_all)
async def search_all(
    query: str,
    count: int | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for messages and files. Set detailed=True for full response."""
    return await client.api_call(
        "search.all",
        query=query,
        count=count,
        highlight=highlight,
        page=page,
        sort=sort,
        sort_dir=sort_dir,
        team_id=team_id,
    )


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
@compactable(compact_search_files)
async def search_files(
    query: str,
    count: int | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for files matching a query. Set detailed=True for full response."""
    return await client.api_call(
        "search.files",
        query=query,
        count=count,
        highlight=highlight,
        page=page,
        sort=sort,
        sort_dir=sort_dir,
        team_id=team_id,
    )


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
@compactable(compact_search_messages)
async def search_messages(
    query: str,
    count: int | None = None,
    cursor: str | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for messages matching a query. Set detailed=True for full response."""
    return await client.api_call(
        "search.messages",
        query=query,
        count=count,
        cursor=cursor,
        highlight=highlight,
        page=page,
        sort=sort,
        sort_dir=sort_dir,
        team_id=team_id,
    )
